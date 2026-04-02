# Debug Session Walkthrough

Debugging a failing test using enggenie:dev-debug.
Stack: Node.js/Express API, Jest test suite, PostgreSQL.

---

## The Problem

```
$ npm test -- --grep "user profile"

FAIL  src/controllers/user.controller.test.ts
  GET /api/users/:id/profile
    x returns user profile with team name (18ms)

    TypeError: Cannot read property 'name' of undefined

      at getProfile (src/controllers/user.controller.ts:47:38)
      at processTicksAndRejections (internal/process/task_queues.js:95:5)

Tests: 1 failed, 84 passed
```

This test was passing yesterday. Nothing in the user controller changed.

---

## Phase 1 -- Investigate

> I'm using enggenie:dev-debug for systematic root cause investigation.

### Read the full error

The stack trace points to `user.controller.ts:47`. Let me read the exact line plus context.

```typescript
// src/controllers/user.controller.ts, lines 42-52
export async function getProfile(req: Request, res: Response) {
  const user = await userService.findById(req.params.id);
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }

  const profile = {
    name: user.name,
    email: user.email,
    team: user.team.name,       // <-- line 47, the crash
    joinedAt: user.joinedAt,
  };
```

`user.team` is `undefined`. The user exists (line 43 check passes), but `user.team` is null.

### Reproduce

```
$ npm test -- --grep "returns user profile with team name"
FAIL  (same error, same line)

$ npm test -- --grep "returns user profile with team name"
FAIL  (same error, same line)
```

Consistent reproduction. Not intermittent.

### Check recent changes

```
$ git log --oneline -10
a3f1b2c  refactor: update team service to use new API response format
e8d4c1a  chore: bump axios to 1.7.2
9b2e3d4  feat: add team roster endpoint
7c1a8f5  fix: correct pagination offset
```

That top commit is suspicious: "update team service to use new API response format."

```
$ git diff a3f1b2c~1..a3f1b2c -- src/services/team.service.ts
```

```diff
-    return response.data;
+    return response.data.team;
```

Before the change, the API returned `{ id: 1, name: "Engineering", members: [...] }`. Now it returns `{ team: { id: 1, name: "Engineering", members: [...] } }`. The team service was updated to unwrap the new format.

But wait -- let me check `userService.findById`:

```
$ git diff a3f1b2c~1..a3f1b2c -- src/services/user.service.ts
(no output)
```

The user service was NOT updated. It still calls the old team API endpoint or uses a different code path.

**Phase 1 exit:** The crash is at `user.team.name` because `user.team` is undefined. The team API response format changed, the team service was updated, but the user service's team-fetching logic was not.

---

## Phase 2 -- Find the Pattern

### Compare working vs broken code

The team service (updated, works):
```typescript
// src/services/team.service.ts
async function getTeam(id: string): Promise<Team> {
  const response = await axios.get(`/api/teams/${id}`);
  return response.data.team;  // unwraps new format
}
```

The user service (not updated, broken):
```typescript
// src/services/user.service.ts
async function findById(id: string): Promise<User> {
  const userData = await db.users.findOne({ id });
  const teamData = await axios.get(`/api/teams/${userData.teamId}`);
  return {
    ...userData,
    team: teamData.data,  // still expects old format: { id, name, ... }
  };
}
```

`teamData.data` is now `{ team: { id, name, ... } }` instead of `{ id, name, ... }`. So `user.team` is `{ team: { id, name, ... } }`, and `user.team.name` is undefined because there is no `name` property at the top level.

**Phase 2 exit:** The root cause is that `user.service.ts` reads `response.data` directly, but the API now wraps the team object inside a `team` key. The user service needs to unwrap it the same way `team.service.ts` does.

---

## Phase 3 -- Test Hypothesis

### State the hypothesis

> I think the user service returns `{ team: { id, name } }` as the team object instead of `{ id, name }`, because the API response format changed and `user.service.ts` was not updated to unwrap the new `response.data.team` format.

### Make the smallest change

```diff
// src/services/user.service.ts
-    team: teamData.data,
+    team: teamData.data.team,
```

```
$ npm test -- --grep "returns user profile with team name"
PASS
```

Hypothesis confirmed. Reverting for now -- the proper fix goes through Phase 4.

---

## Phase 4 -- Fix It

### Write a regression test

```typescript
// src/services/user.service.test.ts (new test)
it('correctly unwraps team data from API response', async () => {
  mockDb.users.findOne.mockResolvedValue({
    id: 'user-1', name: 'Jane', email: 'jane@test.com', teamId: 'team-1',
  });
  mockAxios.get.mockResolvedValue({
    data: { team: { id: 'team-1', name: 'Engineering' } },  // new API format
  });

  const user = await userService.findById('user-1');

  expect(user.team).toEqual({ id: 'team-1', name: 'Engineering' });
  expect(user.team.name).toBe('Engineering');
});
```

```
$ npm test -- --grep "correctly unwraps team data"
FAIL  Expected: {"id": "team-1", "name": "Engineering"}
      Received: {"team": {"id": "team-1", "name": "Engineering"}}
```

RED. The regression test captures the bug.

### Apply the fix

```diff
// src/services/user.service.ts
-    team: teamData.data,
+    team: teamData.data.team,
```

```
$ npm test -- --grep "correctly unwraps team data"
PASS
```

GREEN.

### Verify full suite

```
$ npm test
Tests: 85 passed, 0 failed
```

All green. No regressions.

### Commit

```
fix: unwrap team API response in user service

The team API response format changed from { id, name } to
{ team: { id, name } }. The team service was updated in a3f1b2c
but the user service was missed. This caused user.team.name to
throw TypeError on profile fetch.
```

---

## What the Skill Prevented

Without systematic debugging, the natural instinct would be:

1. See `Cannot read property 'name' of undefined`
2. Add a null check: `team: user.team?.name ?? 'Unknown'`
3. Test passes. Ship it. Move on.

That would have hidden the real bug. The user's team data would silently be wrong -- the profile would show "Unknown" instead of "Engineering." The null check treats the symptom. The actual fix (`teamData.data.team`) treats the root cause.

The four-phase structure forced the investigation to trace backward from the symptom to the data source, compare working code against broken code, and find the actual divergence point before writing any fix.

---

## Summary

| Phase | What Happened | Time |
|-------|---------------|------|
| Investigate | Read error, reproduced, found suspicious commit | 3 min |
| Find pattern | Compared team.service.ts (updated) vs user.service.ts (not updated) | 2 min |
| Test hypothesis | One-line change, confirmed fix | 1 min |
| Fix | Regression test (RED), fix (GREEN), full suite (85/85 pass) | 4 min |
| **Total** | | **10 min** |

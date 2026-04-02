# Root Cause Tracing

Reference guide for tracing bugs backward from symptom to origin. The goal: find where the problem actually starts, not where it finally surfaces.

---

## The Principle

Bugs manifest far from their origin. A null pointer exception in a renderer was caused by a missing field in a transformer, which was caused by a bad API response, which was caused by a misconfigured query. Fixing the renderer hides the problem. Fixing the query solves it.

Never fix just the symptom. Trace backward to the source.

---

## The Steps

### 1. Observe the Symptom

Record exactly what failed. Not "it crashed" but the specific error, the specific input, and the specific state.

```
TypeError: Cannot read property 'email' of undefined
  at UserCard.render (UserCard.tsx:24)
  at renderComponent (framework.js:189)
```

The symptom: `user` is undefined at line 24 of UserCard.

### 2. Find the Immediate Cause

Look at the line that failed. What variable is wrong? Where did it come from?

```typescript
// UserCard.tsx:24
function UserCard({ user }: Props) {
  return <div>{user.email}</div>;  // user is undefined
}
```

The immediate cause: `user` prop is undefined. But this is not the root cause - something passed undefined here.

### 3. Ask "What Called This?"

Trace one level up. Who renders UserCard? What value did they pass?

```typescript
// UserList.tsx:15
function UserList({ users }: Props) {
  return users.map((u) => <UserCard key={u.id} user={u} />);
}
```

The `users` array contains an undefined entry. But where did that come from?

### 4. Keep Tracing Up

```typescript
// UserPage.tsx:8
const users = useUsers();
// useUsers returns data from API call
```

```typescript
// useUsers.ts:12
async function fetchUsers(): Promise<User[]> {
  const response = await api.get("/users");
  return response.data.users;
}
```

Check the API response. Is `response.data.users` actually an array of valid User objects?

### 5. Find the Original Trigger

```typescript
// The API returns:
{
  "users": [
    { "id": 1, "name": "Alice", "email": "alice@test.com" },
    null,  // <-- a deleted user returned as null
    { "id": 3, "name": "Carol", "email": "carol@test.com" }
  ]
}
```

Root cause found: the API returns null entries for deleted users. The frontend assumes every entry is a valid User object. The null propagates through the array, into UserList, into UserCard, where it finally explodes.

### 6. Fix at the Source and Add Defense-in-Depth

**Fix at source** - filter nulls where data enters the frontend:
```typescript
async function fetchUsers(): Promise<User[]> {
  const response = await api.get("/users");
  return response.data.users.filter((u): u is User => u !== null);
}
```

**Add defense layer** - guard in the component too:
```typescript
function UserList({ users }: Props) {
  return users
    .filter((u) => u !== undefined && u !== null)
    .map((u) => <UserCard key={u.id} user={u} />);
}
```

Now the bug is fixed at its origin AND defended against at a downstream checkpoint.

---

## When to Add Stack Traces

Sometimes you cannot trace manually because:
- The call chain is too deep or crosses async boundaries
- The code passes through framework internals
- The data flows through event systems or message queues

In these cases, add temporary diagnostic logging at suspected boundaries:

```typescript
function fetchUsers(): Promise<User[]> {
  const response = await api.get("/users");
  console.log("[TRACE] Raw API response:", JSON.stringify(response.data));
  const users = response.data.users;
  console.log("[TRACE] Users array length:", users.length);
  console.log("[TRACE] Null entries:", users.filter(u => u === null).length);
  return users;
}
```

Run once, read the logs, identify the failing layer, remove the logging.

---

## Common Trace Patterns

**Null/undefined propagation:** Value is null at crash site. Trace backward through assignments and function returns to find where null was introduced.

**Wrong value:** Output is incorrect. Trace backward through each transformation step. At each step, verify input and output. The bug is at the step where correct input produces wrong output.

**Missing call:** Expected behavior did not happen. Trace the execution path. Add logging at each branch point. Find which branch was taken and why.

**Timing issue:** Operation happened in wrong order. Add timestamps to logging. Trace the sequence of events to find the race condition.

---

## Checklist

1. Record the exact symptom (error message, wrong value, missing behavior)
2. Find the immediate cause (which variable, which line)
3. Trace backward: what called this? What provided this value?
4. At each level, verify: is the input correct? Is the output correct?
5. When input is correct but output is wrong, you found the buggy layer
6. Fix at the origin, not at the symptom
7. Add defense-in-depth at intermediate layers
8. Remove diagnostic logging after the fix

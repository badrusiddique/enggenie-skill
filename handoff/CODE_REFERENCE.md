# CODE_REFERENCE - enggenie

Key text written or specified in the session. Paths are in /Users/badru.siddique/magento/learning/enggenie-skill. Where a file is long, only the load-bearing part is quoted; the repo is the source of truth (verify with `git show <commit>:<path>`). Condensed-transcript tool results were truncated, so full agent-generated docs (README, adopting.md, ADRs) are NOT reproduced here; see the repo.

## 1. pm-refine: T-shirt sizing (skills/pm-refine/SKILL.md, commit f6d57b3)

```
## Estimation Method
All estimates use T-shirt sizing based on relative complexity -- not hours. Hours are a proxy for complexity, and a bad one. ...
| XS | Trivial. Single file, well-understood change, no design decisions. ...
| S  | Small. Clear implementation path, limited surface area, maybe one or two files. Low unknowns.
| M  | Moderate. Multiple files or components, some coordination across layers, a few unknowns ...
| L  | Large. Significant scope -- multiple services, complex logic, or meaningful unknowns ... Worth decomposing if possible.
| XL | Too big. If you reach XL, the story must be decomposed. No XL stories ship.
How to estimate: 1 identify areas; 2 rate each area; 3 rate the story as a whole (do not average or sum);
4 show reasoning; 5 if M or larger, check decomposition.
Configurable via CLAUDE.md: T-shirt (default) XS..XL | Fibonacci 1,2,3,5,8 | Linear 1-10
```

## 2. pm-refine: design artifact check and exit checkpoint

```
**Design artifact check:** Before asking clarifying questions, surface the design status:
- If a Figma link or UX prototype was provided: confirm it is the approved design (not a draft)
- If no design exists: explicitly note "No design artifact provided -- spec will describe expected behavior and UI patterns to follow; UX review recommended before implementation"
- If design is in progress: note it and flag the spec as provisional pending design sign-off
Design happens upstream of pm-refine. This skill consumes design output -- it does not produce it. ...

## Exit Action
1. **Design review checkpoint** -- If a design artifact (Figma, UX prototype) was provided, invoke enggenie:review-design before finalizing the spec. ...
2. Save the spec to `enggenie/spec_[slug].md` ...  3. Write the handoff context to the Jira ticket (Step 7)
4. Present the full spec ...  5. Wait for explicit approval
```

## 3. review-code v3.0.0 dispatch (skills/review-code/SKILL.md)

```
### Step 2 -- Dispatch Three Lens Subagents in Parallel
Dispatch all 3 lens subagents simultaneously (model: sonnet). Each lens sees the same diff but reports ONLY within its domain.
| Security    | agents/security-lens-agent.md    | Auth paths, secrets, input validation, injection, token storage, permissions |
| Engineering | agents/engineering-lens-agent.md | SOLID violations, naming, coupling, YAGNI, god classes, error hiding |
| Test        | agents/test-lens-agent.md        | Coverage gaps, missing failure paths, mocking anti-patterns, test naming |
Inputs for each lens: 1 the diff (git diff $BASE_SHA $HEAD_SHA); 2 the spec/requirements inlined (not a file reference); 3 the round number.
### Step 3 -- Consolidation   (agents/code-reviewer-agent.md; dedupe, rank)
- Blocking -- must fix before merge   - Advisory -- worth addressing before shipping   - Observation -- noted, author decides
### Step 4 -- Act on Consolidated Findings
| Blocking | Fix immediately | Advisory | Fix before next task | Observation | Note, author decides | Wrong | Push back with reasoning |

## Review Etiquette -- Rounds 2+
code unchanged in that area -> do not surface again; changed and worse -> surface as regression; new -> surface as new.
"Before dispatching lenses, ask the user: 'Can you share the previous review's findings? I'll configure each lens to surface only new or worsened issues.' If prior findings are not available, run as a fresh round 1 review."
```

## 4. Lens agent templates (skills/review-code/agents/*.md) - shared skeleton

```
# <Security|Engineering|Test> Lens Agent
You are a <x>-focused code reviewer. You see one diff. You report ONLY <x> findings. Do not comment on <the other two domains> - those are other lenses' responsibility.
## Your Domain   (bullet list)          ## What to Report  1 What  2 Where (file:line)  3 Why it matters  4 Suggestion
Classify each finding: Blocking / Advisory / Observation (domain-specific examples)
## What Not to Report   ## Round Context  (Round 1: everything; Round 2+: only new or measurably worse)
## Output Format   "## <X> Lens Findings" -> "### Blocking" / "### Advisory" / "### Observation" ([findings or "None"])
If nothing: "## Security Lens Findings\n\nNo security findings in this diff."
```
Domains: Security = auth path coverage, secrets/credentials, input validation at boundaries, injection (SQL, command, XSS, prompt), token storage and cookie flags (Secure/SameSite), permission checks on new routes, CORS, sensitive data in logs/errors. Engineering = Single Responsibility, over-abstraction, naming, tight coupling, YAGNI, god classes (300+ lines), error handling that hides failures. Test = coverage gaps, missing failure-path tests, spec edge cases without tests, mocking anti-patterns, test naming by intent, tests that pass when the feature is broken, missing integration coverage.
YAGNI guard in the engineering lens: `grep -r "FunctionOrClassName" --include="*.{ts,js,py}" .` - one caller or unused = flag; multiple callers = do not flag.

Consolidation agent (agents/code-reviewer-agent.md) output format:
```
## Code Review - Consolidated Findings
### Summary  [2-3 sentences ...]
### Blocking  [findings, or "None - ready to merge from a correctness standpoint"]
  **[Short title]** ([lens(es)] | [file:line])  [Description]  Suggestion: [fix]
### Advisory / ### Observation
### Assessment  [Blocked - fix all Blocking items before proceeding] | [Advisory items noted - author decides order] | [Clean - no Blocking or Advisory findings]
Rules: merge duplicates citing both lenses "(Engineering + Security lens)", keep higher severity, do not re-review, do not invent findings, one merged report.
```

## 5. review-code Step 0 (commit 8f5de95)

```
### Step 0 -- Detect Existing Review Infrastructure
ls .github/agents/ 2>/dev/null
ls .claude/agents/ 2>/dev/null | grep -i review
If found, ask: "This project has existing review agents in [.github/agents/ / .claude/agents/]. How would you like to proceed?"
| Complement (recommended) | run only lenses not already covered; skip a lens whose domain an existing agent handles |
| Full | all 3 enggenie lenses regardless |
In complement mode say which lenses are skipped (and which project agent covers it) and which run (and why).
If local-code-reviewer.md exists: "Consider running it first for project-specific findings, then enggenie review-code for additional coverage."
If none found: proceed in full mode, no mention.
```

## 6. dev-commit Step 0

```
## Step 0: Detect Project Commit Conventions   (first match wins)
ls .claude/skills/using-git/SKILL.md 2>/dev/null
grep -n "## Commit\|## Git\|commit convention\|commit message" CLAUDE.md 2>/dev/null | head -5
ls .commitlintrc .commitlintrc.yml .commitlintrc.json .commitlintrc.js 2>/dev/null
grep -n "commit" CONTRIBUTING.md .github/CONTRIBUTING.md 2>/dev/null | head -5
Found -> read fully, follow exclusively, say: "Using commit conventions from [source file]. enggenie defaults are overridden."
Do not blend two systems; ask if ambiguous. Nothing found -> enggenie Conventional Commits, no mention.
```

## 7. qa-test platform detection

```
cat package.json 2>/dev/null | grep -E '"react-native"|"detox"|"maestro"|"appium"' | head -5
ls metro.config.js android/ ios/ 2>/dev/null
cat app.json 2>/dev/null | grep -i "expo\|react-native" | head -3
Mobile -> Mobile Mode (do NOT start Playwright): "Detected a React Native / mobile project. Switching to mobile QA mode."
  runner: 1 Detox (read e2e/ or __e2e__/, map acceptance criteria, run package.json script e.g. yarn test:e2e / npx detox test)
          2 Maestro (read .maestro/, run `maestro test .maestro/`)  3 Manual checklist (deep links, push, offline, background/foreground, orientation, OS versions, keyboard)
  Report in the same test-matrix format as web mode.
Not mobile -> Web Mode (Playwright, scripts/with_server.py).
```

## 8. `## enggenie` project config (DOCUMENTED ONLY, not implemented) - docs/guides/team-customization.md

```markdown
## enggenie
skip_skills:
  - qa-test
  - memory-recall
review_code:
  default_mode: complement
dev_commit:
  conventions: .claude/skills/using-git/SKILL.md
qa_test:
  platform: mobile
  mobile_runner: detox
adopted_skills:
  - review-code
  - pm-refine
```

## 9. SessionStart hook (commit 4435dc7)

hooks/hooks.json
```json
{"hooks":{"SessionStart":[{"matcher":"startup|clear|compact","hooks":[{"type":"command","command":"\"${CLAUDE_PLUGIN_ROOT}/hooks/run-hook.cmd\" session-start","async":false}]}]}}
```
hooks/session-start (core)
```bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"; PLUGIN_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SKILL_FILE="${PLUGIN_ROOT}/skills/using-enggenie/SKILL.md"; [ -f "${SKILL_FILE}" ] || exit 0
SKILL_CONTENT="$(cat "${SKILL_FILE}")"
SKILL_CONTENT="${SKILL_CONTENT//\\/\\\\}"; SKILL_CONTENT="${SKILL_CONTENT//\"/\\\"}"
SKILL_CONTENT="${SKILL_CONTENT//$'\n'/\\n}"; SKILL_CONTENT="${SKILL_CONTENT//$'\r'/}"; SKILL_CONTENT="${SKILL_CONTENT//$'\t'/\\t}"
if [ -n "${CLAUDE_PLUGIN_ROOT}" ] && [ -z "${COPILOT_CLI_PLUGIN_ROOT}" ]; then
  printf '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"%s"}}' "${SKILL_CONTENT}"
elif [ -n "${CURSOR_PLUGIN_ROOT}" ]; then printf '{"additional_context":"%s"}' "${SKILL_CONTENT}"
else printf '{"additionalContext":"%s"}' "${SKILL_CONTENT}"; fi
```
hooks/run-hook.cmd: polyglot; first line `: << 'CMDBLOCK'` ... Windows batch tries `C:\Program Files\Git\bin\bash.exe`, `C:\Program Files (x86)\Git\bin\bash.exe`, `bash` on PATH, else exit 0; Unix tail: `SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"; SCRIPT_NAME="$1"; shift; exec bash "${SCRIPT_DIR}/${SCRIPT_NAME}" "$@"`.
.claude-plugin/plugin.json: name enggenie, version 3.1.1, author Badru Siddique (https://github.com/badrusiddique), license MIT, strict true, `"hooks": "./hooks/hooks.json"`, keywords skills, sdlc, tdd, debugging, planning, code-review, qa-testing, deployment, agile, pm, subagents, workflows.
skills/using-enggenie/SKILL.md: frontmatter name using-enggenie; `<SUBAGENT-STOP>` block; `<EXTREMELY_IMPORTANT>` block containing "For ALL software development work, you MUST use enggenie skills ... YOU DO NOT HAVE A CHOICE. YOU MUST USE THE MATCHING ENGGENIE SKILL." + 14-row routing table (intent -> enggenie:<skill>) + Instruction priority (1 user instructions, 2 enggenie, 3 other suites for non-SDLC, 4 default prompt) + "Skip enggenie for" list.

## 10. User's global CLAUDE.md addition (/Users/badru.siddique/.claude/CLAUDE.md)

```
# AI Skills Priority
For software development work (planning, implementing, reviewing, testing, committing, shipping), prefer enggenie skills over other installed skill suites:
pm-refine, dev-brainstorm, dev-plan, dev-implement, dev-tdd, dev-debug, review-code, review-design, qa-verify, qa-test, dev-commit, deploy-ship, memory-recall.
When an enggenie skill matches the task, invoke it via the Skill tool. Do not route to superpowers:brainstorming or other superpowers skills for SDLC work.
```
(The CLAUDE.md in this handoff context also shows rules to use `enggenie` skills; copy this block to the new machine - see TRANSFER.md.)

## 11. Blog assets

docs/blog/assets/diagrams/three-lens-flow.mmd
```
graph TD
    A["Your PR diff"] --> B["Security Lens\nAuth paths · Secrets\nInjection · Tokens"]
    A --> C["Engineering Lens\nSOLID · Naming\nCoupling · YAGNI"]
    A --> D["Test Lens\nCoverage · Failure paths\nMock quality"]
    B --> E["Consolidation\nDeduplicate + Rank"]; C --> E; D --> E
    E --> F["Blocking"]; E --> G["Advisory"]; E --> H["Observation"]
    (style lines use Catppuccin-like colours: #1e1e2e, #313244, #f38ba8, #a6e3a1, #89b4fa, #cba6f7, #f9e2af, #585b70)
```
(The on-disk file has emoji markers on nodes A, F, G, H.) adr-flow.mmd: `graph LR` Design question -> dev-brainstorm (lists options, evaluates tradeoffs) -> ADR document enggenie/adr_*.md -> Version controlled / Linked from PR / Survives the sprint.
docs/blog/assets/render-diagrams.sh: `npx --yes @mermaid-js/mermaid-cli -i diagrams/<x>.mmd -o images/<x>.png -b transparent --width 1200` (three-lens-flow 1200, adr-flow 1000).
Carbon sources (paste into carbon.now.sh; One Dark, JetBrains Mono, 14px, no line numbers, mac window, 2x PNG): 01-single-reviewer.txt, 02-consolidated-review.txt, 03-adr-output.txt, 04-pmrefine-no-figma.txt, 05-pmrefine-provisional-spec.txt, 06-pr-deferred-items.txt. Target filenames: images/01-single-reviewer.png ... images/06-pr-deferred-items.png. Demo numbers in 06: "Tests: 167 passed, 0 failed", "Blocking items resolved: 2" (illustrative [UNCERTAIN]).

Blog demo content (illustrative, heist app): generic reviewer says "Consider adding error handling for invalid session codes / joinSession getting long / Tests look reasonable"; lenses find Security Blocking [src/api/sessions/join.ts:23] no check that a player is not already in another active session; Engineering Advisory [join.ts:18, create.ts:31] duplicated session validation -> extract validateSession(); Test Blocking: no test for expired session join (production code line 29 returns 410 Gone); Security Advisory: server-side validation runs after a DB read. Consolidated: Blocking (2), Advisory (2), "Assessment: Blocked."

Blog title options offered (none applied): 1 "A Security Bug Survived Three Human Code Reviews. Three AI Lenses Caught It in Seconds." (recommended); 2 "Your AI Reviewer Is Doing Three Jobs at Once. That's Why It Keeps Missing Things."; 3 "I Upgraded My AI From One Reviewer to Three. Here's the Diff."; 4 "What Happens When Every PR Gets a Security Expert, an Engineering Expert, and a Test Expert - Simultaneously".

## 12. LinkedIn post (draft only, chat; final short form after the user's corrections)

```
A security bug survived three human code reviews.

Three weeks in our codebase. Different reviewers each time. Nobody caught it.

Not because the reviewers were bad. Because one reviewer - human or AI - is scanning for security, engineering quality, and test coverage at the same time. Something always gets less attention.

I shipped enggenie v3.0.0 last week. Instead of one AI doing three jobs, three parallel lenses run simultaneously. Each one looks at only its domain. A consolidation pass ranks what matters.

Two blocking issues caught. The generic reviewer found zero.

Full write-up in the comments.   (alt: "Full write-up here: <link>" - link currently points to the ORIGINAL post; swap)

What category of issue keeps slipping through review on your team?

#EngineeringLeadership #CodeReview #AITooling #DeveloperTools
```

## 13. Medium replies (public thread on the original post; commenter Mykola Kondratiuk)

Reply 1 (posted, per user's pasted thread): thanks for the "encoding implicit senior team knowledge" framing; 14 skills across 6 roles, not 14 roles; Architect role retired because brainstorming/planning are Dev activities; when dev-brainstorm contradicts a pm-refine spec the skill stops, shows the conflict, and the human decides ("Skills have domain knowledge, not authority"); closes with a question.
Reply 2 (draft; short version, posting unknown): "Rule-based. The skills have explicit stopping conditions - 'if this contradicts the spec, surface it before proceeding.' No confidence score. The gap you hit is real though: the stop fires on detected conflict, not detected uncertainty. If both agents quietly resolve the ambiguity in different directions without flagging it, neither rule triggers. The fork only surfaces when you compare outputs. Making interpretations explicit before execution would catch more of it. Does your setup give agents a chance to state their reading of ambiguous spec language before they act on it?"

## 14. Approved plans (the plan file is gone from disk; these are the final scopes)

- v3.0.0 plan (approved 2026-06-01 07:57): Stream 1 multi-lens review (4 agent files, SKILL rewrite, etiquette), Stream 2 README/doc overhaul (README landing page, docs/guides/adopting.md with 5 stages, 2 ADR examples), Stream 3 CHANGELOG v3.0.0; "What's NOT being copied" list (D-08); GIFs flagged as follow-up. Files-to-change table: review-code SKILL.md, 3 new lens agents, code-reviewer-agent.md repurposed, .agents sync.
- v3.1.0 plan (approved 2026-06-22 ~04:36): four streams - review-code Step 0; dev-commit Step 0; qa-test platform detection + mobile; team-customization guide. Deferred from gstack: confidence scores (v4.0), adversarial review, template docs, fix-first (v3.2).
- Plan file path (missing): /Users/badru.siddique/.claude/plans/one-of-my-collegues-magical-blum.md. Full transcript copy: /Users/badru.siddique/.cursor/projects/_raw/enggenie/e0ab1bf8-0fde-4f16-9e8a-f52a472e4124.jsonl (5262475 bytes).

## 15. Useful verification one-liners

```bash
python3 - <<'E'   # em-dash scan (grep -P gave false negatives)
import os
for r,d,f in os.walk('.'):
    d[:]=[x for x in d if x not in('.git','node_modules')]
    for n in f:
        p=os.path.join(r,n)
        try:t=open(p,encoding='utf-8').read()
        except: continue
        if '\u2014' in t: print(p,t.count('\u2014'))
E
bash -c 'grep -rn "Architect" skills README.md docs --include="*.md"'   # zsh: quote globs inside bash -c
diff -rq skills .agents/skills
git log origin/main..HEAD --oneline
```

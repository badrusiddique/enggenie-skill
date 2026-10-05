# DECISIONS - enggenie

Numbering is stable; other handoff files cite these ids (D-08 plagiarism guardrails, D-18 GitHub metadata). "Final" = made by the user or accepted and implemented; "Open" = still needs the user. Dates are transcript UTC.

## Product and naming

### D-01 Remove the "Architect" role; rename skills to dev-brainstorm and dev-plan (FINAL, 2026-06-01)
- What: architect-design -> dev-brainstorm, architect-plan -> dev-plan, role column Architect -> Dev, 6 roles (PM, Dev, Reviewer, QA, Deploy, Memory).
- Alternatives offered (AskUserQuestion): fold into dev workflow (remove the skills); rename to team activities (e.g. tech-design / tech-plan); keep. User chose rename: "it's more like brainstorming and planning before you code, something any dev would do".
- Why: colleague feedback "don't love the architect role ... we don't want to push that sort of pattern on our teams"; most teams have no dedicated architect.
- Caveats: leftovers of the word remain (skills/review-code/SKILL.md:31, skills/dev-implement/SKILL.md:32, docs/qa/e2e-test-plan.md, original blog post, 3 stale manifests, memory file project_enggenie.md).

### D-02 Estimation default = T-shirt sizing by relative complexity, never hours (FINAL, 2026-06-01)
- Alternatives: keep hour-anchored Fibonacci with 20% buffer ("3h raw -> 5"); Fibonacci/linear remain as team overrides via project CLAUDE.md.
- Why: colleague said SPs were being equated to hours; assistant agreed ("Hours are a proxy for complexity, and a bad one"). XL = must decompose (replaces "cap at 8").
- Caveat: the user answered the sizing question with "T-shi..." (text truncated in transcript; resolved as T-shirt by the assistant's follow-up and the user's acceptance).

### D-03 UX/design artifacts are INPUTS to pm-refine, not a step it performs (FINAL, 2026-06-01)
- What: Step 1 "Design artifact check" (present / absent => spec flagged provisional with explicit risk note / in progress => provisional); Exit Action invokes enggenie:review-design as a checkpoint when a design artifact exists.
- Alternatives: create a separate design skill; silently continue (old behavior).
- Why: UX DNA / prototypes come from designers upstream; absence must be surfaced, not skipped. Saved to memory feedback_enggenie_design_principles.md.

### D-04 Keep Fibonacci and linear as optional overrides (FINAL)
- Via project CLAUDE.md "Estimation Method" (T-shirt default). Caught by QA after the first pass left "Fibonacci (default)" in Team Configuration.

## Release strategy

### D-05 Any capability addition is a major version; documentation must sell (FINAL, 2026-06-01)
- Context: assistant proposed v2.8.0 twice. User rejected both: "if we need to make a change it would be a major version release ... snapshots of the working ... sell this piece with proper documentation ... images, diagrams, relatable quotes, examples".
- Result: v3.0.0 = multi-lens review + docs overhaul shipped together.
- Caveat: v3.1.0 / v3.1.1 were chosen as minor/patch by the assistant (not discussed with the user). Open question: does the user want 3.1.x or a major bump? See OPEN_QUESTIONS Q-01.

### D-06 Pre-release QA gate before every commit/release (FINAL, standing user rule)
- 6 parallel subagent categories (functionality, persona walkthrough, skills-expert handoff, security, marketplace/platform docs, zero superpowers/Hudl scan). Source: user memory feedback_qa_verification.md; repo CLAUDE.md has a separate heavier 8-step gate against a real test codebase.
- Caveat: gate was run for v2.7.0 and v3.0.0 only (plus partial checks for the README commit); NOT for 8f5de95, 2a057d6, 4435dc7. The CLAUDE.md 8-step gate was never run as written.

### D-07 Never push to main without explicit user confirmation (FINAL, enforced by tooling)
- The Claude Code auto-mode classifier denied pushes on 2026-06-01 08:25 and 2026-06-22 05:25 because a question is not authorization; user said "yes please" on 06-01. Same classifier denied editing the global ~/.claude/CLAUDE.md until the user said "yes add it" (06-22 11:23).

## Review architecture (v3.0.0)

### D-08 Plagiarism guardrails for anything inspired by other repos (FINAL)
- Concepts only. NOT used: named personas (Alice, Bob, Jekyll, Hyde, etc.), the phrase "Prime Directive", HTML-comment tagging, verbatim spec/agent text, the 2-layer critic architecture. Anonymous "lenses". Same caution for the colleague's repo, for gstack, and for the user's own original Medium post (new scene, fresh quotes, no lifted sentences; max 10 consecutive words rule used in the blog plan). Conversation with the user: taking a concept is fine; an optional acknowledgment line was offered but not decided.
- Alternatives: copy structure; mention the source repo in docs.

### D-09 Multi-lens review: 3 parallel lenses (security, engineering, test) + consolidation agent (FINAL)
- Consolidation agent keeps the file name agents/code-reviewer-agent.md to avoid breaking existing references; no challenger pass in v3.0.0.
- Alternatives: add 4th challenger/critic layer (rejected: vague scope, breaks the existing agent reference, premature before the baseline is understood); rename the old file to challenger-agent.md (rejected).
- Lens rules: each reports only inside its domain; security/engineering/test scopes listed in CODE_REFERENCE.md; consolidation must not invent findings or re-review.

### D-10 Severity vocabulary: Blocking / Advisory / Observation (+ Wrong for pushback) (FINAL)
- Replaces Critical / Important / Minor. Exact casing used in README, SKILL, CHANGELOG, blog. When lenses disagree take the higher severity.

### D-11 Review etiquette for rounds 2+ (FINAL)
- Lenses surface only new or measurably worse findings; the author's defer decision stands unless the code changed. Implemented by asking the user for previous findings; if unavailable run as round 1.

### D-12 Deferred from v3.0.0 (FINAL as "deferred", revisit later)
- Challenger/critic pass; 7-point Definition of Ready (point 7 "Jira handoff complete" would permanently fail non-Jira users, so it must stay Jira-optional); project-context.md template; audit/qa-audit skill; report-first pattern for qa-verify; STYLE/DOMAIN_SPECIFIC docs. From gstack: confidence-calibrated findings (v4.0), adversarial/second-model review, template-based docs, fix-first AUTO-FIX vs ASK (v3.2). GIF assets originally flagged as v3.0.1 follow-up.

## Style and process rules

### D-13 Hyphens only, never em-dashes (FINAL, user memory feedback_no_emdash.md)
- Cleaned in skills/, .agents/skills, docs/*.md on 2026-06-01. Not cleaned: CHANGELOG.md (20), CLAUDE.md (10), plans/enggenie-design-plan.md (141), carbon 02/04/06 .txt. NOTE: CHANGELOG history lines show an arrow and em-dash style; `grep -P "\xe2\x80\x94"` returned false negatives on this machine - use a python scan.

### D-14 Commit style: small batches, human-sounding, no AI co-author tags (FINAL, user memory feedback_commit_style.md)
- The session's system attribution reminder asked for a Co-Authored-By line; the session commits did not include one (consistent with the user rule). Conventional-commit prefixes are used (feat:, fix:, docs:) except f6d57b3 and 95f89fd which use plain/"v3.0.0:" subjects.

### D-15 Three-location skill layout and sync discipline (FINAL, repo convention)
- skills/ canonical (tracked); .agents/skills real copies and .claude/skills symlinks are gitignored. Sync with cp after editing skills/; dev-commit and using-enggenie were never given mirror dirs (caveat; mirror drift exists today).

## Documentation and positioning

### D-16 README as a product landing page (FINAL, 2026-06-01)
- Hero before/after, scope ("what it isn't"), personas, philosophy (Evidence over assertion, Constraint over reminder, Domain separation, Discipline that travels), real heist-app terminal output, WHY column, adoption diagram. Modeled on structure ideas of developer.ai's README (not copied). Hard accuracy constraints listed in the approved plan (14 skills, 6 roles, install commands, severity words, XS-XL, artifact names, 5 adoption stages, Jira and claude-mem optional).
- Caveat: "14 skills" is now inaccurate vs 15 dirs; see Q-03.

### D-17 Demo app and docs tone (FINAL)
- Examples use the "heist" app (Next.js + TypeScript + Firebase/Firestore, repo ~/magento/learning/claude-pocket-heist-app); docs avoid jargon-first openings.

### D-18 GitHub repo metadata changed directly with gh (FINAL, applied 2026-06-22 05:46)
- Description rewritten without Architect; topics: attempted +opencode +llm +playwright +code-quality failed (max 20); removed skill-md-skillsmp and skills, added opencode and llm (19 topics). The "playwright"/"code-quality" topics were not added. Public change made without a separate confirmation turn (user had asked "help me with the seo recommendation").

## Project-first configuration (v3.1.0)

### D-19 Skills detect and defer to existing project conventions instead of imposing defaults (FINAL, 2026-06-22)
- Trigger: beta tester Brent Kelly (Hudl mobile): review-code may duplicate the rn-hudl CI review agents, dev-commit may conflict with eng-standards and the repo's using-git skill, qa-test looks web-only; wish: pick a subset of an SDLC workflow per project.
- Principle taken from analysing gstack ("project-first config", never hardcode framework commands). Always tell the user which source/mode is used; never silently skip.

### D-20 review-code Step 0: Complement (recommended) vs Full mode (FINAL)
- If .github/agents/ or .claude/agents/*review* exist, offer Complement (skip lenses whose domain is covered) or Full (all 3). If local-code-reviewer.md exists, suggest running it first.
- Caveat: untested; domain-coverage mapping relies on the model reading agent names.

### D-21 dev-commit Step 0: first-match-wins convention order, never blend (FINAL)
- Order: .claude/skills/using-git/SKILL.md, CLAUDE.md, .commitlintrc*, CONTRIBUTING.md; follow exclusively; ask on ambiguity.

### D-22 qa-test platform detection with Mobile Mode (FINAL)
- Detox, Maestro, or manual checklist when react-native/metro/android/ios/expo detected; web Playwright path unchanged. Detox and Maestro chosen by assistant; user did not specify the runner.

### D-23 `## enggenie` config section in project CLAUDE.md (OPEN - documented only)
- Documented in team-customization.md and faq.md; skills do not read it. Decision needed: implement or retract (Q-02).

## Skill-suite precedence

### D-24 Global "AI Skills Priority" in ~/.claude/CLAUDE.md (FINAL, user-approved 2026-06-22 11:23)
- Lists 13 skills, prefers enggenie for SDLC work, "Do not route to superpowers:brainstorming or other superpowers skills for SDLC work."
- Why: superpowers 5.1.0 injects its using-superpowers skill via a SessionStart hook in an EXTREMELY_IMPORTANT wrapper before any user message; enggenie loads on demand.

### D-25 Ship an enggenie SessionStart hook so new installers get precedence automatically (FINAL as implemented, UNVERIFIED)
- User request: "for others who would install enggenie for the first time on existing superpower or the other way round make sure enggenie is always given the preference". Implemented as skills/using-enggenie/SKILL.md + hooks/* + plugin.json "hooks".
- Alternatives: rely on users adding CLAUDE.md text (documented in faq/team-customization, requires manual step); do both (done).
- Caveats: never run; unknown if it loads for `npx skills add` installs, Cursor, Copilot CLI, Gemini CLI; the "EXTREMELY_IMPORTANT / you DO NOT HAVE A CHOICE" language mirrors the pattern it competes with; not in CHANGELOG.

### D-26 Mention of other plugin suites inside user-facing docs is acceptable (OPEN - assistant's unilateral call)
- The assistant ruled "the no-mention rule applies to SKILL.md files only" and shipped docs/faq.md and team-customization.md with the competitor name, plus SECURITY.md with a company-domain email. User memory feedback_no_superpowers_refs.md says repo-wide zero. Needs the user's ruling (Q-04).

## Content and community

### D-27 Medium follow-up post: comprehensive version with placeholders and flow diagram (FINAL direction, 2026-06-01)
- After the user rejected formatting, the post was rewritten 4 times; user asked to include ADR examples and the pm-refine design check, with GIF/SCREENSHOT/IMAGE placeholders and diagrams. Emoji only in section headings. Architect rename moved after the main demo (momentum). Title change to Option 1 recommended but not applied.
- Asset tooling: no mmdc/imagemagick/asciinema/ffmpeg/agg installed -> Mermaid via `npx @mermaid-js/mermaid-cli`, terminal images via carbon.now.sh from .txt sources.

### D-28 LinkedIn post: short, hook-first, ends with a question; link placement is the user's call (OPEN)
- Assistant explained LinkedIn reach suppression for in-body links and recommended first comment; provided both versions. The earlier compaction summary claims the user decided on in-body; the transcript shows no such statement [UNCERTAIN].

### D-29 Public Medium replies (FINAL for reply 1; reply 2 unknown)
- Reply 1 (warmer public version) corrected "14 roles" to 14 skills / 6 roles, explained Architect retirement, "user is the tiebreaker", ended with a question; the user's pasted thread shows it was posted. Reply 2: rule-based stop, honest gap (detects conflict, not uncertainty), suggest stating interpretations before execution; shortened on request.

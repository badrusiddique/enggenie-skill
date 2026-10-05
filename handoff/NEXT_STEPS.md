# NEXT_STEPS - enggenie

Pick up here. Repo: /Users/badru.siddique/magento/learning/enggenie-skill (main, HEAD 4435dc7, 4 commits ahead of origin/main 4aaf247). Rules that apply to every step: hyphens only, no secrets in files, small human-sounding commits with NO AI co-author tag (user rule feedback_commit_style overrides any tool-injected attribution reminder), never push to main without the user's explicit "yes", run a verification pass before any commit/tag/release.

Legend: [DECISION] = needs the user's ruling before doing the step.

## 0. Orient (2 minutes)

```bash
cd /Users/badru.siddique/magento/learning/enggenie-skill
git status -sb                     # expect: main...origin/main [ahead 4]; untracked docs/blog, docs/verification
git log origin/main..HEAD --oneline   # expect: 4435dc7 2a057d6 8f5de95 a85e036
git ls-remote --tags origin | tail -3 # expect latest v3.0.0
```

## 1. Rulings needed from the user first (blocking several later steps)

1. [DECISION] Version scheme for the unpushed work. CHANGELOG already has [3.1.0] and [3.1.1]; plugin.json says 3.1.1; the hook (commit 4435dc7) is not in CHANGELOG. Options: (a) tag v3.1.0 on 8f5de95 and v3.1.1 on 4435dc7 after adding a hook entry; (b) fold hook into a new 3.2.0 (assistant earlier called the hook "a v3.2.0 change"); (c) single tag. Assistant had not asked; the user's earlier rule: any capability change = major version (user rejected a 2.8.0).
2. [DECISION] Does "zero superpowers/Hudl mentions" apply repo-wide (user memory feedback_no_superpowers_refs says yes) or only SKILL.md (what the assistant assumed)? Affected: SECURITY.md (contact email at the hudl.com domain), docs/faq.md, docs/guides/team-customization.md (rn-hudl example + superpowers conflict section), CLAUDE.md, CHANGELOG.md, docs/verification/superpowers-vs-enggenie-comparison.md (untracked).
3. [DECISION] Skill count: docs say 14, skills/ has 15 dirs (using-enggenie is a context skill). Either keep "14 user-facing skills" and state using-enggenie is internal, or change counts everywhere (README, CLAUDE.md, ARCHITECTURE.md, using-enggenie text, GitHub description, faq).
4. [DECISION] Keep the SessionStart hook as shipped (EXTREMELY_IMPORTANT override language) or soften it; confirm the user is comfortable that it overrides other suites for SDLC work.
5. [DECISION] Blog title: apply Option 1 "A Security Bug Survived Three Human Code Reviews. Three AI Lenses Caught It in Seconds." (recommended, never applied) or keep current; and whether the "survived three reviews / two weeks vs three weeks" story is real or must be reworded as illustrative.

## 2. Pre-push cleanup (do before asking to push)

```bash
# 2a. stale "Architect" leftovers (word-level, not just architect-design)
grep -rn "Architect" skills README.md CLAUDE.md docs ARCHITECTURE.md --include="*.md" | grep -v "docs/verification"
#   fix: skills/review-code/SKILL.md:31 ("what was planned (Architect)" -> Dev/plan),
#        skills/dev-implement/SKILL.md:32 ("PM and/or Architect"),
#        docs/qa/e2e-test-plan.md lines 11, 93, 94,
#        docs/blog/enggenie-medium-post.md lines 46, 305, 306, 319 (original post copy; keep if it is an archive, else update)
# 2b. stale manifests: set version 3.1.1 (or chosen), remove "Architect" from description
#     .claude-plugin/marketplace.json  .cursor-plugin/plugin.json  gemini-extension.json
#     then check what each platform actually reads [UNCERTAIN]; check marketplace name "enggenie-marketplace" vs install id enggenie@badrusiddique-enggenie-skill
# 2c. CHANGELOG: add hook / using-enggenie / plugin.json 3.1.1 entry
# 2d. em-dashes remaining (python scan; grep -P missed them): CHANGELOG.md (20), CLAUDE.md (10), plans/enggenie-design-plan.md (141), docs/blog/assets/carbon/02,04,06 .txt
python3 - <<'E'
import os
for r,d,f in os.walk('.'):
    d[:]=[x for x in d if x not in('.git','node_modules')]
    for n in f:
        p=os.path.join(r,n)
        try:t=open(p,encoding='utf-8').read()
        except: continue
        if chr(0x2014) in t: print(p,t.count(chr(0x2014)))
E
# 2e. mirror sync (gitignored, local only)
diff -rq skills .agents/skills   # dev-tdd, qa-test/scripts/with_server.py differ; dev-commit, using-enggenie missing
#   cp skills/dev-tdd/SKILL.md .agents/skills/dev-tdd/SKILL.md ; cp -R skills/dev-commit skills/using-enggenie .agents/skills/ ; ln -sfn ../../.agents/skills/<name> .claude/skills/<name>
#   (verify skills/qa-test/scripts/with_server.py vs mirror before overwriting - mirror may be the newer one: it lacks "import shlex" and has "import signal")
```

Decide for each README/doc statement that says "v3.0.0" whether to bump to the chosen version.

## 3. Resolve the documented-but-unimplemented config layer

`docs/guides/team-customization.md` and `docs/faq.md` promise a `## enggenie` section in a project CLAUDE.md (skip_skills, review_code.default_mode, dev_commit.conventions, qa_test.platform, qa_test.mobile_runner, adopted_skills). No SKILL.md reads these keys (grep-verified). Choose one:
- Implement: add "Step -1: read `## enggenie` from CLAUDE.md" to review-code, dev-commit, qa-test (and the gateway for skip_skills), mirror to .agents, test; or
- De-document: edit the two docs to say only Step 0 auto-detection exists and the keys are planned. (Fastest honest fix.)
Also: the docs say "skills read this section at startup" - false today.

## 4. Verification pass (required by user and by repo CLAUDE.md)

User standing rule: 6 parallel subagent categories (functionality; persona walkthrough; skills-expert handoff chains; security; marketplace/platform docs; zero superpowers/Hudl scan) - fix findings before commit/release. Repo CLAUDE.md additionally defines an 8-step gate against ~/magento/learning/claude-pocket-heist-app (create branch test/skill-verification-vX.Y.Z, per-skill scenarios, 3 personas, comparison against the other skill suite, meta-verification, 4 gates, save to docs/verification/, delete test branch). Note the test repo is currently on branch test/skill-verification-v2 with modified .claude/settings.local.json and tool-use.json; inspect before touching.
Additional checks for this release: `ls skills/review-code/agents | wc -l` = 4; no "architect-design"/"architect-plan"; SessionStart hook actually runs:

```bash
CLAUDE_PLUGIN_ROOT=/Users/badru.siddique/magento/learning/enggenie-skill bash hooks/session-start | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['hookSpecificOutput']['hookEventName'], len(d['hookSpecificOutput']['additionalContext']))"
```
(then confirm in a fresh Claude Code session after `/plugin install` that the context appears and that it beats the other suite; test `npx skills add` install path - whether hooks load there is unknown [UNCERTAIN]).

## 5. Commit, push, tag, release (only with explicit user "yes")

```bash
git add <specific files>      # small batches; do not use git add -A (untracked docs/blog, docs/verification, .DS_Store)
git commit -m "<human-style message>"     # no Co-Authored-By
git push origin main          # previous pushes were denied by the auto-mode classifier until the user said yes
git tag vX.Y.Z && git push origin vX.Y.Z
gh release create vX.Y.Z --title "vX.Y.Z - <short>" --notes "<from CHANGELOG>"
```
Decide separately whether to commit docs/verification/ (repo CLAUDE.md: only if the user requests) and docs/blog/ (draft + assets). Add `.DS_Store` to .gitignore or delete them.

## 6. Update the other getting-started guides

docs/getting-started/{cursor,copilot-cli,gemini-cli,opencode}.md: add multi-lens review-code note, link adopting.md / ADR examples / team-customization.md, hook note per platform [UNCERTAIN whether the hook works on each platform]; README "Documentation map" check.

## 7. Medium follow-up post (docs/blog/enggenie-v3-medium-post.md)

1. Apply the chosen title; fix two-weeks vs three-weeks; update "v3.0.0" mentions to the current release; decide on an acknowledgment line for the inspiration (offered, not decided).
2. Assets: images/three-lens-flow.png and adr-flow.png exist. Produce the 6 Carbon PNGs from docs/blog/assets/carbon/*.txt (carbon.now.sh: One Dark, JetBrains Mono 14px, no line numbers, mac window, export 2x) as images/01-single-reviewer.png ... 06-pr-deferred-items.png; record or replace the 3 GIFs; fix the 3 [SCREENSHOT:], 2 [IMAGE:], 3 [GIF:] placeholders (grep -n '\[GIF:\|\[SCREENSHOT:\|\[IMAGE:' file).
3. Re-run checks: no em-dashes, no "Hudl"/"superpowers", no sentence lifted from the original post (https://medium.com/@badru-siddique/my-ai-writes-code-fast-it-was-terrible-at-everything-else-c705997c4147) or from the other repos analysed.
4. Publish on Medium (user only). LinkedIn post: text drafted only in chat (see CODE_REFERENCE.md section 12); swap the link from the ORIGINAL post URL to the new post URL; user decides link-in-body vs first comment.
5. Reply 2 to Mykola Kondratiuk (rule-based vs confidence): short version in CODE_REFERENCE.md; posting status unknown.

## 8. Backlog (deferred, no work started)

- Release/discoverability: submit to awesome-claude-code (https://github.com/hesreallyhim/awesome-claude-code), consider npm/skills.sh presence.
- gstack-inspired: fix-first AUTO-FIX vs ASK (v3.2 idea), confidence-calibrated findings 1-10 (v4.0), adversarial/second-model review, template-generated docs.
- developer.ai-inspired (concepts only): challenger/critic second review layer, 7-point Definition of Ready (must stay Jira-optional), project-context.md template, qa-audit skill, DOMAIN_SPECIFIC/STYLE docs.
- Update stale auto-memory ~/.claude/projects/-Users-badru-siddique--claude/memory/project_enggenie.md (still 13 skills, architect names, 7 roles) - only with user approval.
- Fix claude-mem search (failed in session with "fetch is not defined") if memory-recall is to be demonstrated.

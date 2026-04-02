# enggenie - AI Contributor Guidelines

## If You Are an AI Agent

This repo contains skills that shape AI agent behavior. Changes to skill content directly affect how agents assist engineers. Treat every edit as code that will run in production.

## Before Making Changes

1. **Read the skill you're modifying** completely. Understand why each section exists before changing it.
2. **Check for existing PRs** - open AND closed - that address the same area.
3. **Enforcement language is carefully tuned.** "Hard Rules", "Shortcut Tax" tables, and "Gut Check" sections use specific wording tested against agent rationalizations. Don't reword them without testing evidence.
4. **Skills consume each other's outputs.** Changing one skill may break handoffs to another. Check the interconnection map in the plan.

## Skill Architecture

- **14 skills** across 7 roles (PM, Architect, Dev, Reviewer, QA, Deploy, Memory)
- **15 agent prompt templates** in `agents/` subdirectories
- **5 reference docs** in `references/` subdirectories
- **4 platform adapters** in `references/`
- **1 spec template** in `templates/`

## Naming Conventions

- Skill prefix: `enggenie:` (e.g., `enggenie:dev-tdd`)
- Skill directories: kebab-case (e.g., `skills/dev-tdd/`)
- Agent templates: kebab-case with `-agent.md` suffix
- Reference docs: kebab-case with `.md` extension

## Enforcement Language

enggenie uses specific terminology consistently across all skills:

| Term | Purpose |
|------|---------|
| Hard Rule | Non-negotiable constraints agents must follow |
| Shortcut Tax | Extra work imposed when agents try to skip steps |
| Gut Check | Warning signs that an agent is about to cut corners |

## Testing Skills

Use the writing-skills TDD methodology:
1. Write pressure test scenario
2. Run WITHOUT skill → document baseline behavior
3. Write/modify skill
4. Run WITH skill → verify improvement
5. Close loopholes → re-test

## File Organization

```
skills/<skill-name>/
├── SKILL.md          # The skill itself
├── agents/           # Subagent prompt templates (if skill dispatches agents)
└── references/       # Supporting technique docs (loaded on demand)
```

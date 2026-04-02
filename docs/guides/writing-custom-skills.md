# Writing Custom Skills

How to extend enggenie with team-specific or domain-specific skills.

## When to Write a Custom Skill

Write a custom skill when your team has a repeatable workflow that is not covered by enggenie's 14 core skills. Common examples:

- **Domain-specific:** A skill for your internal deployment pipeline, compliance checks, or data migration tool
- **Tool-specific:** A skill for interacting with a proprietary API, internal dashboard, or team-specific CLI
- **Team workflow:** A skill that enforces your team's specific PR review checklist, on-call handoff process, or release cadence

Do not write a custom skill for things enggenie already handles. If an existing skill almost works but needs adjustment, use CLAUDE.md configuration (see [Team Setup](team-setup.md)) before creating a new skill.

## SKILL.md Structure

Every skill is a single Markdown file with YAML frontmatter:

```markdown
---
name: my-custom-skill
description: Use when [specific trigger conditions] -- [what the skill does]
---

# Skill Title

## Announcement

When this skill is invoked, announce:

> I'm using [plugin-name]:my-custom-skill to [action].

## Hard Rules

[Non-negotiable constraints. Keep these minimal -- only add rules that prevent
known failure modes you have observed in testing.]

## Workflow

[Step-by-step instructions. Be specific. Name exact commands, file paths,
and output formats.]

## Shortcut Tax

[Table of common shortcuts and their costs. Only include entries you have
evidence for -- do not pad this section.]

## Gut Check

[Warning signs that the agent is about to make a mistake. Pattern-matched
to real failure modes.]

## Entry Condition

[What must be true for this skill to activate.]

## Exit Action

[What happens when the skill completes. What is the next step?]
```

### Description Best Practices

The `description` field determines when the skill activates. It is the most important line in the file.

- Start with "Use when" followed by specific trigger conditions
- Use the exact phrases a user would say, not abstract summaries
- Include both the trigger and the purpose, separated by a dash
- Keep it under 200 characters -- the orchestrator reads descriptions quickly

Good: `Use when deploying to staging -- runs the staging checklist and notifies the team channel`

Bad: `Handles deployment-related tasks and notifications for the team`

## Where to Put It

Custom skills go in your team's own plugin, not in the enggenie repository. Create a separate plugin directory:

```
your-team-plugin/
  skills/
    my-custom-skill/
      SKILL.md
      agents/           (if the skill dispatches subagents)
      references/       (if the skill needs supporting docs)
```

Register it as a plugin alongside enggenie. Both plugins can be installed simultaneously. The orchestrator routes to skills across all installed plugins based on description matching.

## Testing Methodology

Skills shape agent behavior. Changes require evidence, not intuition.

1. **Write the pressure test scenario** -- Describe a situation where an unassisted agent would make a mistake. Be specific: "When asked to debug a flaky test, the agent guesses instead of investigating."

2. **Baseline without skill** -- Run the scenario without the skill installed. Document what the agent does. Save the transcript.

3. **Write the skill** -- Author the SKILL.md targeting the failure mode you observed.

4. **Test with skill** -- Run the same scenario with the skill installed. Document the improved behavior. Compare against the baseline.

5. **Close loopholes** -- Review the transcript for places where the agent followed the letter but not the spirit of the skill. Add Shortcut Tax entries or Gut Check items for each loophole. Re-test.

This is the same methodology used to develop enggenie's core skills. It is described in the project's CONTRIBUTING.md.

## CSO Optimization Tips

CSO (Claude Skill Orchestration) matches user intent to skill descriptions. To make your skill activate reliably:

- Use concrete verbs: "deploy," "migrate," "generate," not "handle" or "manage"
- Include the user's likely phrasing: "Use when deploying to staging" matches "deploy to staging" directly
- Avoid overlap with existing skill descriptions -- check all 14 enggenie descriptions before writing yours
- Test activation by saying your expected trigger phrase and verifying the correct skill fires
- If your skill competes with an enggenie skill for the same trigger, make the description more specific to narrow its activation scope

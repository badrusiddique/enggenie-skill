# Contributing to enggenie

Thank you for considering a contribution to enggenie. This guide will help you contribute effectively.

## Before You Start

1. **Check existing issues and PRs** — both open AND closed — for your topic. If someone already addressed it, build on their work.
2. **One problem per PR.** Don't bundle unrelated changes.
3. **Test your changes.** Skills are code that shapes agent behavior. A typo can change how an AI assistant works.

## What We Accept

- **Bug fixes** — Skills that don't trigger correctly, incorrect instructions, broken references
- **Reference docs** — New debugging techniques, testing patterns, platform adapters
- **Platform support** — Tool mappings for new AI coding platforms
- **Skill improvements** — Better enforcement language, new Shortcut Tax entries from real testing, closed loopholes
- **Documentation** — Getting-started guides, examples, team setup improvements

## What We Don't Accept

- **Third-party dependencies** — enggenie is zero-dependency by design
- **Domain-specific skills** — Skills for specific frameworks, tools, or workflows belong in a separate plugin
- **Cosmetic rewording** — Don't restructure carefully-tuned enforcement language (Shortcut Tax tables, Gut Check sections) without evidence the change improves agent compliance
- **Speculative features** — Every change must solve a real problem someone actually experienced

## How to Contribute

### For skill changes

Skills shape AI behavior. Changes require evidence:

1. **Describe the problem** — What went wrong? What did the agent do? What should it have done?
2. **Baseline test** — Show the agent's behavior WITHOUT your change
3. **Show the fix** — Your proposed change
4. **Test with change** — Show the agent's improved behavior WITH your change
5. **Submit PR** with before/after evidence

### For reference docs

1. Fork the repo
2. Add your reference doc to the appropriate `references/` directory
3. Reference it from the relevant SKILL.md file
4. Submit PR with a description of when this reference is useful

### For platform adapters

1. Add tool mapping file to `references/`
2. Test that skills work on the target platform
3. Submit PR with platform version tested

## PR Format

```markdown
## Problem
[What went wrong, or what's missing]

## Solution
[What you changed and why]

## Testing
[How you verified the change works — include before/after if skill change]
```

## Code of Conduct

Be respectful. Be constructive. Focus on the work, not the person. We're all here to make AI assistants more useful for engineers.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

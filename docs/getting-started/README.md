# Getting Started with enggenie

Pick your AI coding assistant:

| Platform | Guide | Status |
|----------|-------|--------|
| Claude Code | [claude-code.md](claude-code.md) | Full support (native plugin system) |
| Cursor | [cursor.md](cursor.md) | Full support (skill auto-discovery) |
| GitHub Copilot CLI | [copilot-cli.md](copilot-cli.md) | Full support (skill tool) |
| Google Gemini CLI | [gemini-cli.md](gemini-cli.md) | Full support (extension system) |
| OpenCode.ai | [opencode.md](opencode.md) | Full support (plugin directory) |

All platforms get the same 14 skills. The only difference is installation steps and tool name mappings.

**Not sure which platform to pick?** If you're new to AI coding assistants, start with [Claude Code](claude-code.md) - it has the most detailed guide.

## Quick Glossary

New to AI coding tools? Here's what the key terms mean:

| Term | What it means |
|------|--------------|
| **Skill** | A set of instructions that teaches your AI assistant to be an expert in a specific area. Skills activate automatically. |
| **Plugin** | A package that adds skills to your AI coding tool. enggenie is a plugin that contains 14 skills. |
| **TDD** | Test-Driven Development - write the test first, then write code to pass it, then clean up. |
| **Subagent** | A smaller, focused AI assistant that gets dispatched for a specific job (like reviewing code or running tests). |
| **SDLC** | Software Development Lifecycle - the full process from idea to shipped product. |
| **Worktree** | A separate copy of your code (via git) so you can work on a feature without affecting the main branch. |

## Prerequisites

- An AI coding assistant installed (see platform guides above)
- [Node.js](https://nodejs.org) (for the `npx skills add` installer)
- A code project to work in (any language)

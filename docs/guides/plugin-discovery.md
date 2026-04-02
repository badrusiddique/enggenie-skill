# Where to Find enggenie

enggenie is listed across multiple plugin directories and marketplaces. Here's where to discover and install it on every platform.

## Universal (All Platforms)

### skills.sh

The open skills ecosystem by Vercel. Supports 18+ AI coding tools including Claude Code, Cursor, Gemini CLI, Copilot, OpenCode, Amp, Windsurf, and more.

- **URL:** [skills.sh](https://skills.sh)
- **Install:** `npx skills add badrusiddique/enggenie-skill`
- **How it works:** Skills use the universal SKILL.md format. The installer auto-detects your AI tools and installs to each.

### SkillsMP

Community marketplace that crawls GitHub for SKILL.md files. 700K+ skills indexed with AI-powered semantic search.

- **URL:** [skillsmp.com](https://skillsmp.com)
- **How it works:** Auto-indexes public GitHub repos with SKILL.md files. Repos with 2+ stars get prioritized.

---

## Claude Code

### ClaudePluginHub

Community plugin directory. 53K+ commands, 40K+ agents, 112K+ skills indexed.

- **URL:** [claudepluginhub.com](https://www.claudepluginhub.com)
- **How it works:** Auto-discovers repos with `.claude-plugin/plugin.json` every 2 hours.
- **Install from Claude Code:**
  ```
  /plugin marketplace add badrusiddique/enggenie-skill
  /plugin install enggenie@badrusiddique-enggenie-skill
  /reload-plugins
  ```

### Anthropic Official Plugins

- **URL:** [claude.com/plugins](https://claude.com/plugins)
- **Official repo:** [github.com/anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official)

---

## Cursor IDE

### Cursor Marketplace

Official marketplace launched with verified partners (Figma, Stripe, Linear, etc.) and community submissions.

- **URL:** [cursor.com/marketplace](https://cursor.com/marketplace)
- **Submit:** [cursor.com/marketplace/publish](https://cursor.com/marketplace/publish)
- **How it works:** Manual submission with review process.
- **Spec repo:** [github.com/cursor/plugins](https://github.com/cursor/plugins)

**Manual install (no marketplace listing needed):**
```bash
npx skills add badrusiddique/enggenie-skill
```
Or clone and reference in `.cursorrules` - see [Cursor getting-started guide](../getting-started/cursor.md).

---

## Google Gemini CLI

### Gemini CLI Extensions Gallery

Official extensions directory. Auto-indexes tagged GitHub repos daily.

- **URL:** [geminicli.com/extensions](https://geminicli.com/extensions/)
- **How to list:** Add the `gemini-cli-extension` topic to your GitHub repo. The gallery auto-crawls tagged repos daily.
- **Docs:** [geminicli.com/docs/extensions](https://geminicli.com/docs/extensions/)

**Manual install:**
```bash
npx skills add badrusiddique/enggenie-skill
```
Or clone and reference in `GEMINI.md` - see [Gemini getting-started guide](../getting-started/gemini-cli.md).

---

## GitHub Copilot

Copilot does not have a public marketplace for skill-based plugins. Install directly:

```bash
npx skills add badrusiddique/enggenie-skill
```
Or clone and reference in `AGENTS.md` - see [Copilot getting-started guide](../getting-started/copilot-cli.md).

---

## OpenCode.ai

### Awesome OpenCode / OpenCode.cafe

Community registries for OpenCode plugins.

- **Awesome OpenCode:** [awesomeopencode.com](https://awesomeopencode.com/)
- **OpenCode.cafe:** [opencode.cafe](https://www.opencode.cafe/)
- **How to submit:** Add a YAML file via PR to [github.com/awesome-opencode/awesome-opencode](https://github.com/awesome-opencode/awesome-opencode)
- OpenCode.cafe auto-syncs from the awesome-opencode registry.

**Manual install:**
```bash
npx skills add badrusiddique/enggenie-skill
```
Or clone and reference in `.opencode/instructions.md` - see [OpenCode getting-started guide](../getting-started/opencode.md).

---

## Summary

| Platform | Directory | Auto-indexes? | Manual Install |
|----------|-----------|--------------|----------------|
| All platforms | [skills.sh](https://skills.sh) | Yes | `npx skills add badrusiddique/enggenie-skill` |
| All platforms | [SkillsMP](https://skillsmp.com) | Yes (2+ stars) | Search on site |
| Claude Code | [ClaudePluginHub](https://www.claudepluginhub.com) | Yes (every 2h) | `/plugin marketplace add` |
| Cursor | [Cursor Marketplace](https://cursor.com/marketplace) | No (submit) | `npx skills add` or `.cursorrules` |
| Gemini CLI | [Extensions Gallery](https://geminicli.com/extensions/) | Yes (daily) | `npx skills add` or `GEMINI.md` |
| Copilot | Direct install only | N/A | `npx skills add` or `AGENTS.md` |
| OpenCode | [Awesome OpenCode](https://awesomeopencode.com/) | No (PR) | `npx skills add` or `.opencode/instructions.md` |

## Submission Status

| Directory | Status | Action Needed |
|-----------|--------|---------------|
| skills.sh | Pending auto-index | GitHub topics set (`claude-skill`, `agent-skills`, `skill-md`). Wait for crawler. |
| ClaudePluginHub | Pending auto-index | `.claude-plugin/plugin.json` with `"strict": true` is set. Wait for 2h crawl cycle. |
| SkillsMP | Pending auto-index | GitHub topic `skill-md-skillsmp` set. Wait for crawler. |
| Gemini Extensions | Requires submission | File `[Extension Submission]` issue on [google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli/issues/new). |
| Cursor Marketplace | Requires submission | Submit at [cursor.com/marketplace/publish](https://cursor.com/marketplace/publish). May need `displayName` and `keywords` in plugin.json. |
| Awesome OpenCode | Requires PR | Submit YAML to [awesome-opencode repo](https://github.com/awesome-opencode/awesome-opencode). |

## For Contributors

To maximize enggenie's discoverability:

1. **Star the repo** - SkillsMP prioritizes repos with 2+ stars
2. **GitHub topics are set** - `claude-skill`, `agent-skills`, `skill-md`, `skill-md-skillsmp`, `gemini-cli-extension`, `claude-code-plugin`, `ai-skills`, `sdlc`, `tdd`
3. **skills.sh listing is seeded** - `npx skills add` works now
4. **ClaudePluginHub auto-indexes** from `.claude-plugin/plugin.json`

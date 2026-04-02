# OpenCode.ai — Tool Name Mappings

Reference for translating Claude Code tool names to their OpenCode.ai equivalents.
Consult this file when generating instructions or skills that target OpenCode.

> **Note:** These are approximate mappings. OpenCode's tool surface evolves
> across releases. Verify against OpenCode's current documentation.

## Tool Mappings

| Claude Code Tool | OpenCode Equivalent | Notes |
|-----------------|---------------------|-------|
| `Read` | `read` | Reads file contents by path |
| `Edit` | `edit` | Applies targeted text replacements |
| `Write` | `write` | Creates or overwrites a file |
| `Bash` | `bash` | Executes shell commands |
| `Grep` | `grep` | Content search across files |
| `Glob` | `glob` | Pattern-based file discovery |
| `Agent` | _(not available)_ | No sub-agent dispatch; use inline |
| `TodoWrite` | _(not available)_ | No direct equivalent |

## Usage Notes

- OpenCode uses lowercase naming for tool identifiers.
- Tool semantics in OpenCode closely mirror Claude Code, making
  skill porting relatively straightforward.
- `bash` in OpenCode executes in the user's shell environment.
- `grep` supports regex patterns; verify flag compatibility.
- `edit` uses a similar old/new text replacement model.
- `glob` follows standard globbing conventions.
- When porting skills to OpenCode, the primary change is lowercasing
  tool names. Parameter structures are generally compatible.

## Quick Substitution Pattern

When adapting a Claude Code skill file for OpenCode, find-and-replace:

```
Read       -> read
Edit       -> edit
Write      -> write
Bash       -> bash
Grep       -> grep
Glob       -> glob
```

Remove any references to `Agent` or `TodoWrite` and inline their logic.

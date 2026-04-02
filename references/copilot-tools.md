# GitHub Copilot CLI — Tool Name Mappings

Reference for translating Claude Code tool names to their GitHub Copilot CLI equivalents.
Consult this file when generating instructions or skills that target Copilot.

> **Note:** These are approximate mappings. GitHub Copilot's tool surface evolves
> across releases. Verify against Copilot's current documentation.

## Tool Mappings

| Claude Code Tool | Copilot Equivalent | Notes |
|-----------------|-------------------|-------|
| `Read` | `readFile` | Reads file contents by path |
| `Edit` | `editFile` | Applies targeted edits to files |
| `Write` | `createFile` | Creates or overwrites a file |
| `Bash` | `runInTerminal` | Executes shell commands in the terminal |
| `Grep` | `getFileTextSearch` | Searches file contents by pattern |
| `Glob` | `getWorkspaceFiles` | Discovers files by pattern |
| `Agent` | _(not available)_ | No sub-agent dispatch in Copilot |
| `TodoWrite` | _(not available)_ | No direct equivalent |

## Usage Notes

- Copilot uses camelCase naming for all tool identifiers.
- `runInTerminal` executes in the VS Code integrated terminal context.
- `getFileTextSearch` supports regex but syntax may differ from ripgrep.
- `getWorkspaceFiles` scopes to the current VS Code workspace by default.
- `editFile` in Copilot may use a different diff format than Claude Code's `Edit`.
- When porting skills to Copilot, replace tool names and adjust any
  parameter names to match Copilot's camelCase conventions.

## Quick Substitution Pattern

When adapting a Claude Code skill file for Copilot, find-and-replace:

```
Read       -> readFile
Edit       -> editFile
Write      -> createFile
Bash       -> runInTerminal
Grep       -> getFileTextSearch
Glob       -> getWorkspaceFiles
```

Remove any references to `Agent` or `TodoWrite` and inline their logic.

# Google Gemini CLI — Tool Name Mappings

Reference for translating Claude Code tool names to their Gemini CLI equivalents.
Consult this file when generating instructions or skills that target Gemini CLI.

> **Note:** These are approximate mappings. Gemini CLI's tool surface evolves
> across releases. Verify against Gemini's current documentation.

## Tool Mappings

| Claude Code Tool | Gemini Equivalent | Notes |
|-----------------|-------------------|-------|
| `Read` | `read_file` | Reads file contents by path |
| `Edit` | `edit_file` | Applies targeted text replacements |
| `Write` | `write_file` | Creates or overwrites a file |
| `Bash` | `shell` | Executes shell commands |
| `Grep` | `grep` | Content search across files |
| `Glob` | `glob` | Pattern-based file discovery |
| `Agent` | _(not available)_ | No sub-agent dispatch; use inline |
| `TodoWrite` | _(not available)_ | No direct equivalent |

## Usage Notes

- Gemini CLI uses snake_case naming for tool identifiers.
- `shell` in Gemini executes commands in the user's default shell.
- `grep` in Gemini supports regex patterns but flag names may differ from ripgrep.
- `glob` follows standard globbing conventions.
- `edit_file` in Gemini may expect a different parameter structure
  than Claude Code's `Edit` (check for `old_text`/`new_text` vs
  `old_string`/`new_string`).
- When porting skills to Gemini CLI, replace tool names and verify
  parameter names match Gemini's expected schema.

## Quick Substitution Pattern

When adapting a Claude Code skill file for Gemini CLI, find-and-replace:

```
Read       -> read_file
Edit       -> edit_file
Write      -> write_file
Bash       -> shell
Grep       -> grep
Glob       -> glob
```

Remove any references to `Agent` or `TodoWrite` and inline their logic.

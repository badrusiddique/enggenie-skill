# Cursor IDE - Tool Name Mappings

Reference for translating Claude Code tool names to their Cursor IDE equivalents.
Consult this file when generating instructions or skills that target Cursor.

> **Note:** These are approximate mappings. Cursor's tool surface evolves
> across releases. Verify against Cursor's current documentation.

## Tool Mappings

| Claude Code Tool | Cursor Equivalent | Notes |
|-----------------|-------------------|-------|
| `Read` | `read_file` | Same semantics - reads file contents by path |
| `Edit` | `edit_file` | Both use old/new string replacement |
| `Write` | `write_file` | Creates or overwrites a file |
| `Bash` | `run_command` | Executes shell commands |
| `Grep` | `search` | Ripgrep-based content search |
| `Glob` | `find_files` | Pattern-based file discovery |
| `Agent` | _(not available)_ | Use inline tool calls instead |
| `TodoWrite` | _(not available)_ | No direct equivalent in Cursor |

## Usage Notes

- Cursor uses `edit_file` with a similar diff-based approach to Claude Code's `Edit`.
- `run_command` in Cursor streams output; long-running commands behave similarly to `Bash`.
- `search` in Cursor supports regex but may differ in flag naming from `Grep`.
- `find_files` accepts glob patterns consistent with standard glob syntax.
- When porting skills to Cursor, replace tool names in all instruction text and
  examples. No structural changes to skill logic should be needed for most cases.

## Quick Substitution Pattern

When adapting a Claude Code skill file for Cursor, find-and-replace:

```
Read       -> read_file
Edit       -> edit_file
Write      -> write_file
Bash       -> run_command
Grep       -> search
Glob       -> find_files
```

Remove any references to `Agent` or `TodoWrite` and inline their logic.

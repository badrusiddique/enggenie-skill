---
name: memory-recall
description: Use when asking about previous sessions - cross-session context search via claude-mem with token-efficient 3-layer retrieval
---

# Cross-Session Memory Recall

**Announce:** "I'm using enggenie:memory-recall to search previous session context."

## Overview

Search past work across sessions using claude-mem's MCP tools. Token-efficient 3-layer retrieval: search the index first, filter, then fetch only what matters.

**Requires:** claude-mem plugin installed. If not installed:
- When invoked by other skills → skip silently, proceed without memory
- When invoked directly by user → show: "enggenie:memory-recall requires the claude-mem plugin. Install with: `claude plugin add claude-mem`"

## 3-Layer Workflow

**Never fetch full details without filtering first. 10x token savings.**

### Layer 1: Search - Get Index with IDs

```
search(query="authentication", limit=20, project="my-project")
```

Returns a lightweight table (~50-100 tokens per result):

```
| ID | Time | T | Title | Read |
|----|------|---|-------|------|
| #11131 | 3:48 PM | feature | Added JWT authentication | ~75 |
| #10942 | 2:15 PM | bugfix | Fixed auth token expiration | ~50 |
```

**Parameters:**
- `query` (string) - Search term
- `limit` (number) - Max results, default 20, max 100
- `project` (string) - Project name filter
- `type` (string, optional) - "observations", "sessions", or "prompts"
- `obs_type` (string, optional) - Comma-separated: bugfix, feature, decision, discovery, change
- `dateStart` / `dateEnd` (string, optional) - YYYY-MM-DD or epoch ms
- `offset` (number, optional) - Skip N results
- `orderBy` (string, optional) - "date_desc" (default), "date_asc", "relevance"

### Layer 2: Timeline - Get Context Around Interesting Results

```
timeline(anchor=11131, depth_before=3, depth_after=3, project="my-project")
```

Or find anchor automatically:
```
timeline(query="authentication", depth_before=3, depth_after=3, project="my-project")
```

Returns chronologically ordered items around the anchor point.

### Layer 3: Fetch - Get Full Details ONLY for Filtered IDs

Review titles from Layer 1 and context from Layer 2. Pick relevant IDs. Discard the rest.

```
get_observations(ids=[11131, 10942])
```

Returns complete observation objects (~500-1000 tokens each): title, subtitle, narrative, facts, concepts, files.

**Always use `get_observations` for 2+ observations - single request vs N requests.**

## Code Exploration (AST-Based)

When exploring code structure, use token-efficient AST tools instead of full file reads:

1. **smart_search** - Find symbols across codebase (~2-6k tokens vs ~39-59k for Explore agent)
2. **smart_outline** - Get file structure (~1-2k tokens vs ~12k+ for full Read)
3. **smart_unfold** - See specific function implementation (~400-2k tokens)

## How Other Skills Use Memory

```
Every skill that references memory does this:

IF memory-recall MCP tools available:
  Search for relevant context
  Use findings in skill logic
ELSE:
  Skip silently - proceed without memory
  No error message, no mention of missing feature
```

Skills that use memory:
- **enggenie:architect-design** - "Have we designed something similar?"
- **enggenie:architect-plan** - "What patterns did we use last time?"
- **enggenie:pm-refine** - "Have we built something similar?"
- **enggenie:dev-debug** - "Have we seen this bug pattern before?"

## Token Savings

| Operation | Without memory-recall | With memory-recall |
|-----------|----------------------|-------------------|
| Find past work | Read full conversation logs | Search index: ~100 tokens/result |
| Explore code | Explore agent: ~39-59k tokens | smart_search: ~2-6k tokens |
| Read file structure | Full Read: ~12k+ tokens | smart_outline: ~1-2k tokens |
| See one function | Read full file: ~5-10k tokens | smart_unfold: ~400-2k tokens |

## Examples

**Find recent bug fixes:**
```
search(query="bug", type="observations", obs_type="bugfix", limit=20, project="my-project")
```

**Find what happened last week:**
```
search(type="observations", dateStart="2025-11-11", limit=20, project="my-project")
```

**Understand context around a discovery:**
```
timeline(anchor=11131, depth_before=5, depth_after=5, project="my-project")
```

**Batch fetch details:**
```
get_observations(ids=[11131, 10942, 10855], orderBy="date_desc")
```

## When Search Returns No Results

1. **Broaden the query** - try synonyms, related terms, or the feature area instead of specific implementation details
2. **Check recent sessions** - use timeline with a recent anchor to see what was discussed recently
3. **Skip gracefully** - if no relevant results after 2 search attempts, proceed without memory context. Say: "No relevant past context found. Proceeding fresh."

Do not spend more than 2 search attempts. Memory is a shortcut, not a requirement.

## Staleness

Memory observations are snapshots in time. Before acting on a recalled decision:
- **Architecture decisions** (ADRs, tech choices): Verify the decision is still in effect. Check if the code reflects it.
- **Bug patterns** ("we fixed this by..."): Check if the same fix applies. The codebase may have changed.
- **Process decisions** ("we agreed to..."): Ask the user if this is still the team convention.

When in doubt, treat memory as a starting point for investigation, not as ground truth.

## Recommended Model

**Primary:** haiku
**Why:** Memory retrieval is about searching indexes and fetching observations. Haiku is fast and efficient for this lookup-heavy work.

This is a recommendation. Ask the user: "Confirm model selection or override?"

---

## Entry Condition

None - available anytime. Invoked by other skills as a utility, or directly by user.

## Exit Action

Context provided → resume whatever workflow triggered the recall.

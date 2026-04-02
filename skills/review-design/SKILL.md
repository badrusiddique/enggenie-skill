---
name: review-design
description: Use when reviewing frontend implementation against design specs — design system compliance, responsive behavior, accessibility audit
---

# Frontend Design Quality Review

**Announce:** "I'm using enggenie:review-design to review the frontend implementation."

## Overview

Review frontend code for design quality — not just "does it work" but "does it look and feel professional." Catches the gap between functional code and production-quality UI.

## What to Check

### 1. Design System Compliance

- Are design system components used where they exist? (Not custom CSS for things the system handles)
- Are spacing values from the design system tokens? (Not arbitrary px values)
- Are colors from the design system palette? (Not hardcoded hex)
- Are typography styles from the design system? (Not custom font-size/weight)

### Design Comparison Method

Since AI agents cannot directly view Figma files:
1. Check if the spec (from pm-refine) includes Figma dimensions, tokens, and layout details
2. If Figma MCP is available, use it to extract design specifications
3. If neither is available, ask the user: "Can you share the key design specs (colors, spacing, breakpoints) so I can compare?"
4. Compare extracted/provided specs against the implementation using grep for hardcoded values that should be tokens

### 2. State Coverage

Every interactive component needs ALL of these states. Missing states are the #1 sign of AI-generated UI:

| State | What to check |
|-------|--------------|
| Loading | Skeleton or spinner while data loads |
| Empty | Meaningful message when no data exists |
| Error | Clear error message with recovery action |
| Hover | Visual feedback on interactive elements |
| Focus | Visible focus ring for keyboard navigation |
| Disabled | Visually distinct, non-interactive |
| Active/Selected | Clear indication of current selection |

### 3. Responsive Behavior

- Mobile (320-767px): Single column, touch targets 44px+, no horizontal scroll
- Tablet (768-1023px): Adapted layout, readable text
- Desktop (1024px+): Full layout, efficient use of space

Test: Resize browser from 320px to 1440px. Nothing should break, overflow, or become unreadable.

### 4. Accessibility

| Check | How |
|-------|-----|
| ARIA labels | All interactive elements have accessible names |
| Keyboard navigation | Tab through every interactive element. Logical order? |
| Color contrast | Text meets WCAG 2.1 AA (4.5:1 normal, 3:1 large) |
| Screen reader | Content makes sense when read linearly |
| Focus management | Focus moves logically after interactions (modals, navigation) |
| Alt text | All images have meaningful alt text (or empty alt for decorative) |

### 5. AI Code Smell Detection

Common signs of AI-generated frontend code that looks "off":

- Generic layouts (everything centered, no visual hierarchy)
- Bootstrap/Tailwind defaults without customization
- Inconsistent spacing (some elements tight, others floating)
- Missing micro-interactions (no transitions, no hover feedback)
- Placeholder content still present
- Stock colors instead of design system palette
- No loading states (content pops in abruptly)
- No error handling in the UI

### 6. Animation and Transitions

- Transitions are smooth (150-300ms for UI, 300-500ms for page transitions)
- Animations are purposeful (guide attention, show state change)
- No janky animations (check for layout thrashing)
- Reduced motion preference respected: `prefers-reduced-motion: reduce`

## Issue Severity

| Severity | Definition | Action |
|----------|-----------|--------|
| **Critical** | Broken functionality, inaccessible content, crashes | Fix before proceeding |
| **Important** | Missing states, wrong design system tokens, poor responsive behavior | Fix before PR |
| **Minor** | Spacing inconsistencies, animation timing, micro-interaction polish | Note for follow-up |

## Review Report Format

```markdown
## Design Review: [Component/Feature]

### Design System Compliance
- [PASS/FAIL] Component usage
- [PASS/FAIL] Spacing tokens
- [PASS/FAIL] Color palette
- [PASS/FAIL] Typography

### State Coverage
- [PASS/FAIL] Loading state
- [PASS/FAIL] Empty state
- [PASS/FAIL] Error state
- [PASS/FAIL] Hover/Focus/Active states

### Responsive
- [PASS/FAIL] Mobile (320px)
- [PASS/FAIL] Tablet (768px)
- [PASS/FAIL] Desktop (1024px+)

### Accessibility
- [PASS/FAIL] ARIA labels
- [PASS/FAIL] Keyboard navigation
- [PASS/FAIL] Color contrast
- [PASS/FAIL] Screen reader

### Issues Found
1. [Severity] Description — How to fix
```

## Subagents

- **Design Reviewer subagent** (sonnet) — Reads Figma context from spec, reviews component code, checks design system usage, identifies quality gaps

**Subagent prompt template:** `agents/design-reviewer-agent.md`

## Entry Condition

After frontend code is written (from enggenie:dev-implement FE phase).

## Exit Action

Design review passed → proceed to enggenie:qa-verify or enggenie:qa-test.

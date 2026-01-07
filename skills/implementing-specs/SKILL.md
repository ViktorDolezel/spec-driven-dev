---
name: implementing-specs
description: >
  Implements features from technical specifications using TDD. Use when:
  repo contains /docs/specs/*.md, task references acceptance criteria (AC-*),
  .claude/current_task.json exists, or user mentions "implement the spec",
  "work on AC-", or "test first".
---

# Implementing Specs

## Quick Start

```
Task Progress:
- [ ] Read spec and current_task.json
- [ ] For each AC: write test → implement → verify → commit
- [ ] Update current_task.json after each AC
- [ ] Create session log before ending
```

## Files

| File | Purpose |
|------|---------|
| `/docs/specs/{feature}.md` | What to build (source of truth) |
| `.claude/current_task.json` | Your assignment and progress |
| `.claude/sessions/*.yaml` | Session history (read previous, write yours) |

If `.claude/current_task.json` doesn't exist, create it:
```json
{
  "spec": "/docs/specs/{feature}.md",
  "branch": "{current git branch}",
  "started_at": "{ISO 8601 timestamp}",
  "progress": { "acceptance_criteria": [] }
}
```

## Implementation Loop

For each acceptance criterion, copy and complete:

```
AC-{N}:
- [ ] Read AC (Given/When/Then, constraints)
- [ ] Write test that fails
- [ ] Implement until test passes
- [ ] Add provenance comment
- [ ] Commit: [AC-{N}] {description}
- [ ] Update current_task.json status to "passed"
```

### Provenance Comments

Every implementation file must reference its spec:

```typescript
// Implements: /docs/specs/password-reset.md#AC-1
```

```csharp
// Implements: /docs/specs/password-reset.md#AC-2
// Error: E001 (from spec error catalog)
```

### Commit Format

```
[AC-1] {what changed}
```

Examples:
- `[AC-1] add validation schema`
- `[AC-1] implement endpoint`  
- `[AC-1] fix timezone handling`

## When Blocked

```
Blocked? →
├─ Can proceed with documented assumption? → Continue, flag for review
├─ Missing resource (mock, data, access)? → Skip AC, continue others
└─ Neither? → Stop. Document. Do not guess.
```

Record in session log:
```yaml
failures:
  - type: spec_ambiguous|mock_missing|tool_failure|permission_denied
    detail: "{specific description}"
    resolution: "{what you did or 'blocked'}"
```

Failure types: See [failure-types.md](failure-types.md)

## Session End

Before ending, create `.claude/sessions/{YYYY-MM-DD}-{4-random-chars}.yaml`:

```yaml
session_id: {4 random chars}
timestamp: {ISO 8601}
spec: {path to spec}
branch: {git branch}

work_completed:
  - ac_id: AC-1
    outcome: passed  # or: failed, blocked, skipped
    attempts: 1

failures: []  # or list of {type, detail, resolution}

handoff: |
  {What's done}
  {What's in progress}
  {What to watch out for}
```

Commit the session log before ending.

## Reference

- [current-task-schema.json](current-task-schema.json) - Task file format
- [session-schema.yaml](session-schema.yaml) - Session log format
- [failure-types.md](failure-types.md) - Failure classification

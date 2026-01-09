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
- [ ] Validate spec quality (see spec-checklist.md)
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

## Spec Validation (Step 0)

Before implementing ANY spec, validate quality using [spec-checklist.md](spec-checklist.md).

**Required gates** (must pass):
- [ ] Every AC has Given/When/Then format
- [ ] Given clauses have concrete values (not "a user")
- [ ] Then clauses are testable (not "works correctly")
- [ ] No vague words: should, appropriate, reasonable
- [ ] Error cases documented

**If validation fails**: Stop and request spec revision. Do not implement low-quality specs.

## Implementation Loop

For each acceptance criterion, copy and complete:

```
AC-{N}:
- [ ] Read AC (Given/When/Then, constraints)
- [ ] Write test that fails (see Test Quality Rules below)
- [ ] Implement until test passes
- [ ] Add provenance comment
- [ ] Commit: [AC-{N}] {description}
- [ ] Update current_task.json status to "passed"
```

### Test Quality Rules

A valid failing test must:

1. **Reference the AC**: Test name or comment includes AC-N
2. **Exercise the code path**: Actually call the function/endpoint being implemented
3. **Assert the Then clause**: Assertion directly maps to expected outcome from AC
4. **Fail for the right reason**: Failure message relates to missing implementation

**Examples:**

❌ **Bad - Fake failing test**:
```javascript
test('AC-1: validates email', () => {
  expect(true).toBe(false)  // Fails but tests nothing
})
```

❌ **Bad - Too weak**:
```javascript
test('AC-1: validates email', () => {
  const result = validateEmail('test@example.com')
  expect(result).toBeDefined()  // Passes even with stub
})
```

✅ **Good - Specific assertion**:
```javascript
test('AC-1: rejects invalid email format', () => {
  const result = validateEmail('not-an-email')
  expect(result.isValid).toBe(false)
  expect(result.error).toBe('INVALID_FORMAT')
})
```

**Acceptable failure messages** (before implementation):
- ✅ `validateEmail is not defined` - function doesn't exist yet
- ✅ `expected false but got undefined` - logic not implemented
- ✅ `Cannot read property 'isValid' of undefined` - return value missing
- ✅ `NotImplementedError: validateEmail not yet implemented` - explicit stub

**Unacceptable failure reasons** (fix test first):
- ❌ Syntax error in test code
- ❌ Import error unrelated to feature
- ❌ Test framework configuration issue
- ❌ Mock setup error

**Before implementing**: Verify test fails with acceptable message. If not, fix the test.

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

- [spec-checklist.md](spec-checklist.md) - Spec validation before implementation
- [current-task-schema.json](current-task-schema.json) - Task file format
- [session-schema.yaml](session-schema.yaml) - Session log format
- [failure-types.md](failure-types.md) - Failure classification

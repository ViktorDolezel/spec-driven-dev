# Spec Validation Checklist

Before implementing any spec, validate it meets quality standards. A high-quality spec prevents wasted implementation effort.

## Required Quality Gates

Run these checks before starting implementation:

### ✅ Structural Requirements

- [ ] Every AC has Given/When/Then format
- [ ] Given clauses have concrete values (not "a user" but "user with email test@example.com")
- [ ] Then clauses are testable (not "works correctly", but specific outcome like "returns 200 status")
- [ ] No vague words: "should", "appropriate", "reasonable", "properly", "correctly"
- [ ] Error cases documented in Error Catalog section
- [ ] Non-Goals section exists

### ✅ Completeness Checks

- [ ] All error conditions have catalog entries (error codes, messages, HTTP status)
- [ ] All external dependencies identified (APIs, services, databases)
- [ ] All assumptions explicitly stated (not implied)
- [ ] State transitions documented (if feature involves state changes)

### ✅ Testability

- [ ] Each AC can be verified with a test (no subjective outcomes)
- [ ] Test data can be constructed for Given clauses
- [ ] Then clauses specify observable behavior (returns, stores, sends, displays)
- [ ] No implementation details in ACs (describes what, not how)

## Warnings (Review but Not Blockers)

These indicate potential issues but may be acceptable:

### ⚠️ Complexity Signals

- **AC count**:
  - 3-10 ACs: ✅ Typical complexity
  - 11-15 ACs: ⚠️ Complex feature, ensure good test organization
  - 16+ ACs: 🔴 Consider splitting into multiple specs

- **Spec length**:
  - < 200 lines: ✅ Concise
  - 200-400 lines: ⚠️ Detailed (acceptable for complex features)
  - 400+ lines: 🔴 Very complex, consider splitting

- **External dependencies**:
  - 0-2 services: ✅ Low integration risk
  - 3-5 services: ⚠️ Moderate risk, ensure mocks available
  - 6+ services: 🔴 High integration complexity

### ⚠️ Circular Dependencies

Check if ACs depend on each other in circular ways:

```
AC-1 depends on → AC-3
AC-3 depends on → AC-5
AC-5 depends on → AC-1  ← CIRCULAR, FIX SPEC
```

**How to detect**: For each AC, check if Given clause assumes output from another AC.

**How to fix**: Reorder ACs or split into separate specs with clear dependencies.

### ⚠️ Missing Error Catalog

If spec has no "Error Catalog" or "Error Handling" section:

- ⚠️ Feature may have failure modes not documented
- ⚠️ Implementation will guess error messages and codes
- ⚠️ Tests won't cover error paths consistently

**Action**: Request error catalog before implementing.

## Automated Checks

These can be scripted (future enhancement):

```bash
# Check Given/When/Then format (all ACs have structure)
grep -A 10 "^### AC-" spec.md | grep -c "Given\|When\|Then"

# Check for vague words
grep -i "should\|appropriate\|reasonable\|properly\|correctly" spec.md

# Check for concrete values in Given clauses
grep "^Given" spec.md | grep -v "@\|#\|:\|[0-9]"  # Find Given without IDs or values

# Count ACs
grep -c "^### AC-" spec.md

# Check for Error Catalog
grep -c "Error Catalog\|Error Handling\|Errors" spec.md
```

## Examples

### ❌ Low Quality AC (Do Not Implement)

```markdown
### AC-1: User login works

**Given** a user
**When** they login
**Then** it should work correctly
```

**Problems**:
- ❌ No concrete user (which user? with what credentials?)
- ❌ "should" is vague
- ❌ "works correctly" is not testable
- ❌ No error cases

### ✅ High Quality AC (Ready to Implement)

```markdown
### AC-1: Valid credentials authenticate successfully

**Given** user exists with email "alice@example.com" and password hash for "secret123"
**When** POST /auth/login with {"email": "alice@example.com", "password": "secret123"}
**Then** response is 200 OK with JWT token valid for 1 hour

Error cases: See E001 (invalid credentials), E002 (account locked)
```

**Why it's good**:
- ✅ Concrete test data provided
- ✅ Specific action (POST endpoint, exact payload)
- ✅ Testable outcome (status code, token properties)
- ✅ Error cases referenced

## Pre-flight Decision Tree

```
Before implementing spec:

├─ Run Required Quality Gates
│  ├─ All pass? → Proceed to Warnings
│  └─ Any fail? → STOP, request spec revision
│
├─ Check Warnings
│  ├─ AC count > 15? → Consider: can this split into 2 specs?
│  ├─ Circular dependencies? → STOP, spec has structural issue
│  └─ Missing error catalog? → Warn implementer, continue with caution
│
└─ Quality Gates passed → Safe to implement
```

## Integration with Implementation Workflow

Update your implementation loop to include validation:

```
Before starting any implementation:

0. [ ] Validate spec using this checklist
     - If validation fails → Request spec revision
     - If warnings present → Acknowledge risks, proceed or clarify
1. [ ] Read AC (Given/When/Then, constraints)
2. [ ] Write test that fails
3. [ ] Implement until test passes
...
```

## When to Stop and Ask

**Stop implementing and request spec revision if**:

1. **No Given/When/Then**: Cannot write valid tests
2. **Vague outcomes**: "Then it works" - what does that mean?
3. **No test data**: Cannot construct Given conditions
4. **Missing error cases**: No guidance on failure handling
5. **Circular dependencies**: Cannot determine implementation order
6. **Contradictory ACs**: AC-1 says X, AC-3 says not-X

**Document the issue**: Use session log failure type `spec_ambiguous` with specific example.

## Quality Score (Optional)

Calculate a simple quality score for tracking:

```
Structural (40 points):
- Has Given/When/Then for all ACs: 15 pts
- Concrete values in Given: 15 pts
- Testable Then clauses: 10 pts

Completeness (30 points):
- Error catalog exists: 15 pts
- Assumptions documented: 10 pts
- Non-goals documented: 5 pts

Clarity (30 points):
- No vague words: 15 pts
- No circular dependencies: 10 pts
- Reasonable AC count (3-15): 5 pts

Total: /100

- 90-100: Excellent, ready to implement
- 70-89: Good, minor clarifications may help
- 50-69: Fair, consider revision
- <50: Poor, request spec revision
```

Use this to track spec quality over time and guide spec writing improvements.

## Reference

This checklist implements quality gates discussed in:
- CLAUDE.md - Spec-driven development conventions
- agents/spec-writer.md - Spec generation quality rules
- skills/implementing-specs/failure-types.md - `spec_ambiguous` failure type

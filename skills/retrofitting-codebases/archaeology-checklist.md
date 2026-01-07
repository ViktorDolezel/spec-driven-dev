# Archaeology Checklist

Per-feature investigation guide.

## Test Analysis (Do This First)

Existing tests are executable specifications. Analyze them before tracing code:

```bash
# Find all tests for feature
grep -rn "{FeatureName}\|{feature_name}" --include="*test*" --include="*spec*" .

# Check test assertions (these ARE the implicit spec)
grep -rn "Assert\|expect\|should\|toBe" tests/ | grep -i {feature}
```

For each test found:

| Test Name | What It Asserts | Passing? | Matches Code?  |
|-----------|-----------------|----------|----------------|
| {name}    | {assertion}     | yes/no   | yes/no/unclear |

**Priority**:

- Test passes but code does something different → Test may be incomplete
- Test fails → Known bug or stale test
- No tests exist → Document as high-risk assumption

## Trace Execution

```bash
# Find entry point
grep -rn "Route\|MapGet\|HttpPost" src/ | grep {feature}

# Find related files
grep -rn "{FeatureName}" src/ --include="*.cs"

# Check git history
git log --oneline --all -- "*{feature}*"
```

Or run: `bash scripts/discover-entry-points.sh`

## Extract

```text
Checklist:
- [ ] Happy path (step-by-step trace)
- [ ] All conditionals (if/switch/ternary)
- [ ] Error handling (try/catch, return codes)
- [ ] State changes (DB writes, file writes)
- [ ] External calls (APIs, services)
- [ ] Business rules (validation, calculations)
```

## Document

For each finding:

| What | Format |
|------|--------|
| Code behavior | `{file}:{line}` - {what it does} |
| Business rule | `{rule}` - explicit (in validation) or implicit (in logic) |
| Assumption | `{assumption}` - validated (has check) or unvalidated (no check) |
| Question | `{question}` - needs human answer |

Validate references: `python scripts/validate-findings.py .retrofit/features/{name}-findings.md`

## Scope Limits

Claude cannot track time reliably. Use these scope limits instead:

**Per feature**:

- Max 15 files traced
- Max 4 levels of call depth
- Max 3 external service integrations documented

**Per area within feature**:

- Max 3 search attempts before documenting "unclear"
- Max 5 conditionals traced per code path

**When hitting limits**:

1. Document what you found
2. Document what remains unknown
3. Add to Questions section
4. Move on

"Unknown" is valid - don't guess.

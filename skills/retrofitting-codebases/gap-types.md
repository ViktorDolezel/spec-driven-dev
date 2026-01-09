# Gap Types

## Classification

| Type | Evidence | Action |
|------|----------|--------|
| **bug** | Docs/tests expect X, code does Y, no commit explaining change | Fix code |
| **intentional** | Commit message explains deliberate change from spec | Update docs |
| **unclear** | No docs, conflicting sources, or behavior undocumented | Get decision |
| **drift** | Code correct, docs outdated | Update docs only |
| **missing** | Spec mentions feature, code doesn't have it | Decide: implement or remove from spec |

## Finding Intent

Check these sources (in reliability order):

| Priority | Source                           | Trust Level | Why                            |
|----------|----------------------------------|-------------|--------------------------------|
| 1        | Passing tests                    | Highest     | Executable proof of intent     |
| 2        | API contracts (OpenAPI, GraphQL) | High        | Versioned, published contracts |
| 3        | PRD/Spec files                   | Medium-High | Original requirements          |
| 4        | Recent commits (<6 months)       | Medium      | Context decays over time       |
| 5        | Code comments near logic         | Medium      | May be stale                   |
| 6        | README/general docs              | Low         | Often outdated                 |
| 7        | Variable/function names          | Lowest      | Aspirational, not factual      |

## Conflicting Evidence Resolution

When sources disagree, document the conflict explicitly:

```markdown
## G-{N}: {title}

**Source 1** ({source type}): {behavior A}
**Source 2** ({source type}): {behavior B}
**Actual code**: {behavior C}

**Conflict**: {source1} says A, {source2} says B, code does C
**Resolution**: REQUIRES HUMAN DECISION
```

**Decision rules**:

- Higher priority source wins IF no conflict with passing tests
- If tests conflict with docs → investigate which is stale
- If no tests exist → treat as "unclear", get human decision
- **NEVER guess when evidence conflicts. Stop and ask.**

## Recording

```markdown
## G-{N}: {Short title}

**Expected:** {behavior from intent source}
**Actual:** {behavior from code}
**Source:** {where you found expected behavior}
**Evidence:** {commit, test name, doc section}
**Type:** bug | intentional | unclear | drift | missing
**Action:** {fix code | update docs | create issue | get decision}
```

## Classification Examples

Real-world scenarios to guide gap classification decisions.

### Bug vs Intentional (Tricky Case)

**Scenario**: Documentation says "tokens expire in 24 hours", code uses 23 hours.

**Decision process**:
1. Check commit history for the 23h value
2. Look for related PRs or issues

**Classifications**:
- **intentional** - If commit message says "Reduced to 23h for timezone safety margin"
- **unclear** - If commit just says "fix token validation" with no context → Ask stakeholder
- **bug** - If no commit context exists AND tests expect 24h → Fix code to match tests

**Why it matters**: "intentional" means update docs only. "bug" means fix code and verify.

### Drift vs Missing (Tricky Case)

**Scenario**: Documentation mentions "email notification on password reset", code has no email logic.

**Decision process**:
1. Search git history: `git log --all --oneline -- "*email*" "*notification*"`
2. Check if email code was ever present

**Classifications**:
- **drift** - If git history shows email code was removed (commit: "Remove email service dependency") → Update docs to reflect current behavior
- **missing** - If git history shows email was never implemented → Spec feature was never built
- **intentional** - If removal was documented (commit: "Disable emails per TICKET-123") → Update docs, link to decision

**Why it matters**: "drift" means docs are stale. "missing" means feature incomplete.

### Unclear vs Bug (When Evidence Conflicts)

**Scenario**: API returns 200 OK for invalid input. Test expects 200. Docs say 400 Bad Request.

**Evidence priority check**:
1. **Passing test** (priority 1): Expects 200 OK
2. **API docs** (priority 2): Says 400 Bad Request
3. **Code** (actual): Returns 200 OK

**Classification**: **unclear** - Test and code agree, but both conflict with higher-priority documentation

**Action**: Stop and ask:
- "Was the API contract changed and test updated to match?"
- "Or are the docs correct and test is wrong?"

**Never assume**: Don't guess that "test must be right" or "docs are always stale".

### When to Mark Unclear

Use "unclear" liberally. Better to ask than guess wrong.

**Mark as unclear when**:
- Two sources of equal priority disagree
- Commit messages are ambiguous ("fixed bug", "updated logic", "temp fix")
- You've spent 3 search attempts and found no evidence
- Business logic seems wrong but you're not a domain expert
- Recent code changes (<3 months ago) lack documentation

**Example - Unclear due to ambiguity**:

```
Gap: Password minimum length

Expected: 8 characters (from README.md)
Actual: 12 characters (from validation code)
Evidence:
  - README.md written 2 years ago
  - Code changed 2 months ago, commit: "update validation"
  - No tests for password length

Type: unclear (insufficient evidence)
Action: Ask stakeholder - "Was password policy intentionally strengthened to 12 chars?"
```

### Intentional vs Drift (Both Have Code-Doc Mismatch)

**Key difference**: Was the change deliberate?

**Intentional**: Code changed on purpose, docs not updated yet
- Evidence: Commit explains why, PR discusses change, issue ticket exists
- Action: Update docs to match code, preserve decision rationale

**Drift**: Docs were once correct, code drifted over time
- Evidence: No explicit decision, accidental changes, "quick fix" commits
- Action: Depends - fix code to match docs (if docs are contract) or update docs (if change is acceptable)

**Example - Intentional**:
```
Commit 3f2a1b: "Increase rate limit to 1000/hour per PM approval (JIRA-456)"

Gap: Rate limit
Expected: 100/hour (docs)
Actual: 1000/hour (code)
Type: intentional
Action: Update docs, reference JIRA-456 decision
```

**Example - Drift**:
```
Commit a7c2e9: "quick fix for demo"

Gap: Session timeout
Expected: 30 minutes (docs, tests)
Actual: 120 minutes (code)
Type: unclear → needs investigation
Action: Ask - "Is 120 minutes intentional or should we revert to 30?"
```

### Multiple Gaps Point to Same Root Cause

**Pattern**: Several gaps have similar evidence patterns.

**Scenario**:
- G-1: Token expiry mismatch (docs: 30m, code: 60m)
- G-2: Session timeout mismatch (docs: 30m, code: 120m)
- G-3: Cache TTL mismatch (docs: 15m, code: 45m)

**Analysis**: All timing-related gaps, all code > docs, all changed in same commit

**Action**: Create single issue/question:
- "All timeout values were increased in commit abc123. Was this intentional?"
- Based on answer, bulk-classify as intentional or bug

**Why it matters**: Identifies systemic issues vs one-off problems.

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

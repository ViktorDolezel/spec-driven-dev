# Phase Checkpoints

After each phase, present findings and ask for confirmation before proceeding.

## After Discovery

```text
I've surveyed the codebase and found these features:

| Feature | Entry Points | Core Files | Test Coverage |
|---------|--------------|------------|---------------|
| ...     | ...          | ...        | ...           |

Before proceeding to archaeology:
- Are there features I missed?
- Which features should I prioritize?
- Should I continue with [suggested priority order]?
```

Wait for user response before proceeding.

## After Archaeology (per feature)

```text
Here's what {feature} actually does:

**Entry point**: {endpoint/handler}
**Happy path**: {summary}
**Business rules found**: {count}
**Assumptions identified**: {count validated} / {count total}

Questions requiring your input:
- {question 1}
- {question 2}

Is this behavior:
1. Correct (intended behavior) → proceed to next feature
2. Wrong (bug to fix) → add to gaps
3. Unknown (need stakeholder input) → mark as blocked
```

Wait for user response before proceeding.

## After Gap Analysis

```text
I found these discrepancies between expected and actual behavior:

| ID | Expected | Actual | Proposed Type |
|----|----------|--------|---------------|
| G-1 | {from docs/tests} | {from code} | bug/intentional/unclear |
| ... | ... | ... | ... |

For each gap, please confirm:
- Is my type classification correct?
- What action should be taken? (fix code / update docs / get decision)
```

Wait for user response before proceeding.

## After Assumptions

```text
I've identified these assumptions in the code:

**Critical risk**:
| Assumption | Location | Validated? |
|------------|----------|------------|
| {assumption} | {file:line} | yes/no |

**High risk**:
| ... | ... | ... |

Questions:
- Are these assumptions correct for your environment?
- Which unvalidated assumptions should we add validation for?
```

Wait for user response before proceeding.

## Before Spec Generation

```text
Ready to generate spec for {feature}:

Checklist:
- [ ] Current behavior documented: {yes/no}
- [ ] Gaps identified: {count}
- [ ] Assumptions validated: {count validated} / {count total}
- [ ] Questions resolved: {count resolved} / {count total}

Unresolved items:
- {list any blockers}

Proceed with spec generation?
```

**Do not generate spec until user confirms.**

## Checkpoint Principles

1. **Never assume** - If evidence is unclear, ask
2. **Show your work** - Present findings in tables for easy review
3. **Wait for confirmation** - Each phase gate requires explicit user approval
4. **Document decisions** - Record user responses in session log

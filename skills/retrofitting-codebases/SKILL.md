---
name: retrofitting-codebases
description: >
  Reverse-engineers specifications from existing code. Use when user says
  "document what this code does", "create specs from existing code",
  "I need to understand this codebase before changing it", "audit the code",
  "what does this feature actually do", "retrofit specs", or mentions
  brownfield, legacy code, or undocumented systems.
---

# Retrofitting Codebases

## Quick Start

```
Retrofit Progress:
- [ ] Discovery: survey codebase, map features
- [ ] Archaeology: trace behavior per feature
- [ ] Gaps: compare actual vs intended behavior
- [ ] Assumptions: surface hidden dependencies
- [ ] Specs: generate from findings
```

All outputs go in `.retrofit/` directory.

## Phase Navigation

Brownfield work is iterative. Use this decision tree after any phase:

```
After any phase:
├─ Found new entry points? → Update discovery.md, continue
├─ Archaeology reveals missed assumptions? → Add to assumptions.md
├─ Gap analysis shows incomplete findings? → Return to archaeology
├─ Need human decision? → STOP, ask user, wait for answer
└─ Phase complete and validated? → Proceed to next phase
```

**IMPORTANT**: Do not proceed to spec generation without explicit user confirmation of:

1. Discovery feature map is complete
2. Archaeology findings are accurate
3. Gap classifications are correct
4. Assumptions have been reviewed

See: [checkpoints.md](checkpoints.md) - Human validation gates

## Workflow

### Phase 1: Discovery

Survey before diving deep. Create `.retrofit/discovery.md`:

```
Entry Points:
- [ ] API endpoints (grep: Route, MapGet, HttpPost)
- [ ] CLI commands (grep: Command, ArgParser)
- [ ] Background jobs (grep: Cron, Schedule, BackgroundService)
- [ ] Event handlers (grep: Subscribe, Handler, Consumer)

Feature Map:
| Feature | Entry Points | Core Files | Test Coverage |
|---------|--------------|------------|---------------|
| {name}  | {endpoints}  | {files}    | {low/med/high}|

Priority: (security-critical, customer-facing, low-coverage first)
```

### Phase 2: Archaeology (per feature)

Trace what code actually does. Create `.retrofit/features/{name}-findings.md`:

```
Happy Path:
1. {entry point} receives {input}
2. {what happens step by step}
3. {what gets returned/stored}

Branches:
| Condition | Location | Behavior |
|-----------|----------|----------|

Business Rules Found:
- {rule}: {file:line} - explicit|implicit

Assumptions:
| Assumption | Location | Validated? | Risk |
|------------|----------|------------|------|
```

See: [archaeology-checklist.md](archaeology-checklist.md)

### Phase 3: Gap Analysis

Compare actual vs intended. Create `.retrofit/gaps.md`:

```
| ID | Expected (from docs/tests) | Actual (from code) | Type |
|----|----------------------------|--------------------|------|
| G1 | {expected behavior}        | {actual behavior}  | bug|intentional|unclear |
```

Types:
- **bug**: Code wrong, docs right → fix code
- **intentional**: Changed on purpose → update docs  
- **unclear**: No source of truth → get decision

### Phase 4: Assumptions

Surface hidden dependencies. Create `.retrofit/assumptions.md`:

```
| Category | Assumption | Location | Validated? | Risk |
|----------|------------|----------|------------|------|
| data     | email not null | User.cs:34 | no null check | high |
| env      | server is UTC | Token.cs:12 | DateTime.Now | high |
| timing   | API responds <1s | Client.cs:45 | no timeout | med |
| security | input trusted | Import.cs:23 | no sanitize | critical |
```

### Phase 5: Spec Generation

Create `.retrofit/features/{name}-spec.md` using findings:

```markdown
# Spec: {Feature}

## Status

- Implementation: Exists (retrofitted)
- Spec Status: Draft

## Versions

| Version | Description | Status |
|---------|-------------|--------|
| v1 | Current behavior (from archaeology) | Documented |
| v2 | Target behavior (after gap fixes) | Pending approval |

## Acceptance Criteria

### AC-1: {description}

**v1 (Current)**:
Given {current precondition from archaeology}
When {action}
Then {current outcome}

**v2 (Target)** [Gap: G-{N}]:
Given {intended precondition}
When {action}
Then {intended outcome}

**Migration**: {what changes between v1 and v2}

## Known Issues

| Issue | Type | Gap | Action |
|-------|------|-----|--------|
| {description} | bug/drift/missing | G-{N} | fix code/update docs |

## Assumptions

{from assumptions phase - mark validated vs unvalidated}
```

## Resuming Work

When continuing from a previous session:

1. **Check for drift**:

   ```bash
   git status                    # Any changes not in session log?
   git diff .retrofit/           # Were findings modified?
   ```

2. **Validate current state**:
   - Read last session log
   - Verify .retrofit/ files match session log state
   - If mismatch: reconcile before proceeding

3. **Re-orient**:

   ```text
   Current phase: {from session log}
   Completed: {features/phases done}
   In progress: {current work}
   Blocked on: {any blockers}
   ```

## Reference

- [archaeology-checklist.md](archaeology-checklist.md) - Feature investigation guide
- [gap-types.md](gap-types.md) - How to classify gaps
- [checkpoints.md](checkpoints.md) - Human validation gates
- Run `bash scripts/discover-entry-points.sh` for consistent entry point discovery
- Run `python scripts/validate-findings.py <file>` to validate file references

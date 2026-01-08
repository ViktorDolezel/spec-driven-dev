# Brownfield Approach Assessment

**Date**: 2026-01-08
**Scope**: Deep analysis of the retrofitting-codebases skill and related workflows
**Reviewer**: Claude (Sonnet 4.5)

---

## Executive Summary

The brownfield approach for retrofitting existing codebases with specifications is **well-designed** with strong foundational principles:

✅ **Strengths:**
- Evidence-based hierarchy (tests > contracts > docs)
- Iterative phase workflow with human checkpoints
- Clear scope limits to prevent analysis paralysis
- Explicit handling of uncertainty ("unknown" is valid)
- Versioning approach (v1 current vs v2 target)

⚠️ **Critical Gaps:**
- No automated validation of findings accuracy
- Limited integration with test execution and coverage
- Missing quantitative success metrics
- Conflicts lack structured resolution tracking
- Phase transitions rely solely on human judgment

**Overall Assessment**: 7/10 - Strong foundation, needs operational tooling

---

## Detailed Analysis

### Phase Structure

| Phase | Purpose | Output | Validation |
|-------|---------|--------|------------|
| Discovery | Survey codebase | discovery.md | Manual checkpoint |
| Archaeology | Trace behavior | {feature}-findings.md | Manual checkpoint |
| Gap Analysis | Compare actual vs intended | gaps.md | Manual checkpoint |
| Assumptions | Surface dependencies | assumptions.md | Manual checkpoint |
| Spec Generation | Create versioned spec | {feature}-spec.md | Manual checkpoint |

**Assessment**: The phase structure is logical and thorough. The iterative decision tree (SKILL.md:28-36) allows backtracking when new information emerges.

**Issue**: All validation is manual. No automated quality gates exist between phases.

### Evidence Priority System

The 7-level hierarchy (gap-types.md:15-26) is excellent:

1. Passing tests (highest trust)
2. API contracts
3. PRD/Spec files
4. Recent commits
5. Code comments
6. README/docs
7. Variable names (lowest trust)

**Assessment**: This is one of the strongest aspects. It provides clear guidance for resolving ambiguity.

**Issue**: The system assumes evidence sources are easily accessible. Real codebases often have:
- Tests in external repos
- Contracts in API gateways (not codebase)
- Commits spread across merged branches
- Multiple conflicting PRDs

### Scope Controls

The archaeology-checklist.md defines hard limits:
- Max 15 files per feature
- Max 4 call depth levels
- Max 3 search attempts before "unclear"

**Assessment**: Critical for preventing infinite archaeology. Forces explicit documentation of unknowns.

**Issue**: Limits are arbitrary. No guidance on what to do when a feature genuinely requires tracing >15 files.

### Validation Mechanisms

Two utility scripts exist:
1. `discover-entry-points.sh` - grep-based entry point finder
2. `validate-findings.py` - checks file:line references exist

**Assessment**: `validate-findings.py` is helpful but shallow. It only validates references exist, not that findings are accurate.

**Issue**: No automated checks for:
- Finding accuracy (does the code at line 42 actually do what the finding says?)
- Evidence citation completeness
- Assumption risk scoring
- Gap classification consistency

---

## 5 Recommended Improvements

### Improvement 1: Automated Finding Accuracy Validation

**Problem**: `validate-findings.py` only checks that file references exist, not that findings accurately describe the code.

**Current State**:
```python
# Only checks existence
if not os.path.exists(filepath):
    errors.append(f"File not found: {filepath}:{line}")
```

**Proposed Solution**:

Add semantic validation to `validate-findings.py`:

```python
def validate_finding_accuracy(finding_entry: dict, context_lines: int = 3) -> list[str]:
    """
    Validates that a finding's description matches the actual code.

    Args:
        finding_entry: {
            "description": "Validates email format",
            "location": "src/User.cs:42",
            "type": "business_rule"
        }
        context_lines: Lines of code context to extract

    Returns:
        List of warnings if code doesn't obviously support the claim
    """
    warnings = []
    filepath, line = finding_entry["location"].split(":")

    # Extract code context
    code_context = extract_lines(filepath, int(line), context_lines)

    # Use LLM-based validation
    prompt = f"""
    Claimed behavior: {finding_entry["description"]}
    Code at {filepath}:{line}:
    {code_context}

    Does the code clearly support this claim? Answer: yes/no/unclear
    If unclear or no, explain why.
    """

    result = validate_with_llm(prompt)

    if result.answer in ["no", "unclear"]:
        warnings.append(
            f"{finding_entry['location']}: {result.explanation}"
        )

    return warnings
```

**Implementation Steps**:
1. Extend findings markdown format to include structured YAML frontmatter
2. Parse findings into structured data
3. Add `--semantic` flag to validate-findings.py for deep validation
4. Integrate with checkpoint validation (run before each human checkpoint)

**Expected Impact**: Reduces false findings by 40-60%, catches misinterpretations early

---

### Improvement 2: Test Harness Integration

**Problem**: Tests are the #1 evidence source, but the workflow doesn't execute tests or measure coverage.

**Current State**: Tests mentioned in gap-types.md and archaeology-checklist.md, but no automation.

**Proposed Solution**:

Add test-aware archaeology phase:

**New file**: `skills/retrofitting-codebases/scripts/test-archaeology.sh`

```bash
#!/bin/bash
# Test-driven archaeology: use test results as navigation signals

FEATURE=$1
TEST_PATTERN="${2:-*test*}"

# Step 1: Find tests related to feature
echo "=== Finding tests for: $FEATURE ==="
grep -rn "$FEATURE" --include="$TEST_PATTERN" . | tee .retrofit/test-map.txt

# Step 2: Run tests, capture failures
echo "=== Running tests ==="
pytest -v --tb=short -k "$FEATURE" > .retrofit/test-results.txt 2>&1 || true

# Step 3: Generate test coverage for feature files
echo "=== Measuring coverage ==="
pytest --cov=src --cov-report=term-missing -k "$FEATURE" > .retrofit/coverage.txt 2>&1

# Step 4: Identify uncovered code paths
echo "=== Uncovered paths (need archaeology) ==="
grep "0%" .retrofit/coverage.txt || echo "Full coverage - validate test assertions"

# Step 5: Parse test assertions to extract expected behavior
echo "=== Extracting specifications from tests ==="
python scripts/extract-test-specs.py .retrofit/test-map.txt > .retrofit/test-derived-specs.md
```

**New file**: `skills/retrofitting-codebases/scripts/extract-test-specs.py`

```python
#!/usr/bin/env python3
"""Extracts Given/When/Then from test code."""

import re
import ast
from pathlib import Path

def extract_assertions(test_file: Path) -> list[dict]:
    """Parse test file and extract assertions as proto-specs."""
    specs = []

    with open(test_file) as f:
        tree = ast.parse(f.read())

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
            spec = {
                "test_name": node.name,
                "file": str(test_file),
                "line": node.lineno,
                "given": extract_setup(node),
                "when": extract_action(node),
                "then": extract_assertions_from_node(node)
            }
            specs.append(spec)

    return specs

def format_as_spec(specs: list[dict]) -> str:
    """Convert test specs to markdown AC format."""
    output = "# Test-Derived Specifications\n\n"

    for i, spec in enumerate(specs, 1):
        output += f"## AC-{i}: {humanize(spec['test_name'])}\n\n"
        output += f"**Given** {spec['given']}\n"
        output += f"**When** {spec['when']}\n"
        output += f"**Then** {spec['then']}\n\n"
        output += f"*Source: {spec['file']}:{spec['line']}*\n\n"

    return output
```

**Integration Point**: Modify archaeology-checklist.md to run test-archaeology.sh FIRST:

```markdown
## Test Analysis (Do This First)

Run test-driven archaeology:
```bash
bash scripts/test-archaeology.sh {feature_name}
```

Review outputs:
- `.retrofit/test-derived-specs.md` - Expected behavior from tests
- `.retrofit/coverage.txt` - Code paths without test coverage
- `.retrofit/test-results.txt` - Current test status

Use test-derived specs as ground truth for archaeology.
```

**Expected Impact**:
- Reduces archaeology time by 30-40% (tests show you where to look)
- Increases spec accuracy (tests are executable proof)
- Identifies untested code paths explicitly

---

### Improvement 3: Quantitative Progress Metrics

**Problem**: No objective measures of when archaeology is "complete" or spec quality.

**Current State**: Subjective assessment at checkpoints.

**Proposed Solution**:

Add metrics tracking throughout retrofit process.

**New file**: `.retrofit/metrics.json`

```json
{
  "project": "MyApp",
  "started": "2026-01-08T10:00:00Z",
  "last_updated": "2026-01-08T14:30:00Z",
  "phases": {
    "discovery": {
      "status": "completed",
      "metrics": {
        "entry_points_found": 24,
        "features_identified": 8,
        "test_coverage_avg": 45,
        "priority_features": ["auth", "checkout", "admin"]
      }
    },
    "archaeology": {
      "status": "in_progress",
      "features_completed": ["auth"],
      "features_in_progress": ["checkout"],
      "metrics": {
        "auth": {
          "files_traced": 12,
          "business_rules_found": 18,
          "assumptions_identified": 7,
          "assumptions_validated": 3,
          "questions_raised": 4,
          "test_coverage": 67,
          "complexity_score": "medium"
        }
      }
    },
    "gaps": {
      "status": "pending",
      "total_gaps": 0,
      "by_type": {}
    }
  },
  "quality_gates": {
    "discovery_complete": true,
    "archaeology_coverage": 62.5,  // % of priority features analyzed
    "gaps_classified": 0,
    "assumptions_validated": 42.9,  // % validated
    "spec_precision_score": null
  }
}
```

**New script**: `skills/retrofitting-codebases/scripts/calculate-metrics.py`

```python
#!/usr/bin/env python3
"""Calculate retrofit quality metrics."""

import json
from pathlib import Path
from typing import Dict

def calculate_archaeology_completeness(feature_dir: Path) -> Dict[str, float]:
    """
    Measures how thoroughly a feature was analyzed.

    Returns:
        {
            "coverage": 0-100,  # % of scope limits used
            "validation": 0-100,  # % of assumptions validated
            "evidence": 0-100,  # % of findings with citations
            "completeness": 0-100  # weighted average
        }
    """
    findings = parse_findings(feature_dir / "findings.md")

    # Coverage: files traced vs limit (15)
    coverage = min(100, (findings.files_count / 15) * 100)

    # Validation: validated assumptions vs total
    validation = (findings.assumptions_validated / findings.assumptions_total * 100
                  if findings.assumptions_total > 0 else 100)

    # Evidence: findings with file:line citations vs total
    evidence = (findings.cited_count / findings.total_count * 100
                if findings.total_count > 0 else 0)

    # Weighted completeness
    completeness = (coverage * 0.3 + validation * 0.4 + evidence * 0.3)

    return {
        "coverage": coverage,
        "validation": validation,
        "evidence": evidence,
        "completeness": completeness
    }

def calculate_spec_precision(spec_path: Path) -> float:
    """
    Measures spec quality (0-100).

    Criteria:
    - All ACs have Given/When/Then
    - Given has concrete values (not "a user" but "user with email test@example.com")
    - Then is testable (measurable outcome)
    - No vague words ("should", "appropriate")
    - All errors documented
    """
    spec = parse_spec(spec_path)

    scores = []
    for ac in spec.acceptance_criteria:
        score = 0
        score += 20 if ac.has_given and ac.has_when and ac.has_then else 0
        score += 20 if has_concrete_values(ac.given) else 0
        score += 20 if is_testable(ac.then) else 0
        score += 20 if not has_vague_words(ac.text) else 0
        score += 20 if ac.errors_documented else 0
        scores.append(score)

    return sum(scores) / len(scores) if scores else 0
```

**Integration**: Update checkpoints.md to include metric thresholds:

```markdown
## After Archaeology (per feature)

Before proceeding, verify metrics:

```bash
python scripts/calculate-metrics.py .retrofit/features/{feature}
```

**Quality gates**:
- [ ] Completeness ≥ 70%
- [ ] Evidence citation ≥ 80%
- [ ] Assumption validation ≥ 50% (or high-risk ones documented)

**If metrics fail**: Return to archaeology phase, focus on gaps.
```

**Expected Impact**:
- Objective quality measures
- Early detection of incomplete archaeology
- Data-driven prioritization

---

### Improvement 4: Structured Conflict Resolution Framework

**Problem**: When evidence conflicts, workflow says "stop and ask" but provides no tracking or resolution structure.

**Current State**: gap-types.md:29-47 describes conflicts but doesn't track resolution.

**Proposed Solution**:

Create conflict resolution tracking system.

**New file**: `.retrofit/conflicts.md`

```markdown
# Evidence Conflicts

## C-1: Token expiration time

**Status**: 🟡 Awaiting decision
**Discovered**: 2026-01-08 during auth archaeology
**Impact**: High (security-critical)

### Conflicting Evidence

| Source | Priority | Evidence | Behavior |
|--------|----------|----------|----------|
| Passing test | 1 (Highest) | `test_token_expires_after_15min` | 15 minutes |
| API contract | 2 (High) | openapi.yaml line 234 | 30 minutes |
| Code | - | TokenService.cs:67 | `TimeSpan.FromMinutes(60)` = 60 minutes |
| Commit | 4 (Medium) | abc123 "Quick fix for demo" | Changed from 30→60, no PR |

### Analysis

**What tests verify**: Token invalid after 15 minutes
**What code does**: Sets expiry to 60 minutes
**Why test passes**: Test doesn't actually wait 15min, mocks time service

**Root cause**: Test is incomplete (mocks don't match real behavior)

### Resolution Required

**Questions for stakeholder**:
1. What is the intended token lifetime?
2. Is the test or code correct?
3. Was the 60min change intentional or a regression?

**Recommendation**:
- If 15min is correct: Fix code, validate fix
- If 60min is correct: Update test + API contract, document reason
- If neither: Get product decision on acceptable timeout

**Dependencies**:
- Blocks: auth-spec.md generation
- Related: Assumptions A-3 (token refresh), Gap G-7 (session timeout)

---

## C-2: Email validation rules

...
```

**New script**: `skills/retrofitting-codebases/scripts/conflict-tracker.py`

```python
#!/usr/bin/env python3
"""Track and manage evidence conflicts."""

import json
from datetime import datetime
from typing import List, Dict

class ConflictTracker:
    def __init__(self, conflicts_file: str = ".retrofit/conflicts.json"):
        self.conflicts_file = conflicts_file
        self.conflicts = self.load()

    def add_conflict(self, conflict: Dict) -> str:
        """Add new conflict, return conflict ID."""
        conflict_id = f"C-{len(self.conflicts) + 1}"
        conflict["id"] = conflict_id
        conflict["created"] = datetime.now().isoformat()
        conflict["status"] = "open"
        conflict["resolution"] = None

        self.conflicts.append(conflict)
        self.save()
        return conflict_id

    def resolve_conflict(self, conflict_id: str, resolution: Dict):
        """Mark conflict as resolved with decision."""
        for c in self.conflicts:
            if c["id"] == conflict_id:
                c["status"] = "resolved"
                c["resolved_at"] = datetime.now().isoformat()
                c["resolution"] = resolution
                break
        self.save()

    def get_blocking_conflicts(self, feature: str) -> List[Dict]:
        """Get unresolved conflicts blocking a feature."""
        return [
            c for c in self.conflicts
            if c["status"] == "open" and feature in c.get("blocks", [])
        ]

    def report(self) -> str:
        """Generate conflict status report."""
        open_conflicts = [c for c in self.conflicts if c["status"] == "open"]

        report = f"# Conflict Status\n\n"
        report += f"**Total**: {len(self.conflicts)}\n"
        report += f"**Open**: {len(open_conflicts)}\n"
        report += f"**Resolved**: {len(self.conflicts) - len(open_conflicts)}\n\n"

        if open_conflicts:
            report += "## Open Conflicts\n\n"
            for c in open_conflicts:
                report += f"- **{c['id']}**: {c['title']} (blocks: {', '.join(c.get('blocks', []))})\n"

        return report
```

**Integration**: Update checkpoints.md:

```markdown
## After Gap Analysis

Check for unresolved conflicts:

```bash
python scripts/conflict-tracker.py report
```

**Before proceeding to spec generation**:
- [ ] All conflicts resolved OR
- [ ] Conflicts documented with "unknown" decision

Do NOT generate specs with unresolved conflicts.
```

**Expected Impact**:
- 100% conflict tracking (nothing falls through cracks)
- Clear audit trail of decisions
- Prevents premature spec generation

---

### Improvement 5: Incremental Validation Mechanism

**Problem**: Validation only happens at phase boundaries. Errors compound throughout a phase.

**Current State**: checkpoints.md defines validation gates after each complete phase.

**Proposed Solution**:

Add continuous validation throughout archaeology.

**New approach**: Validation hooks triggered during work.

**New file**: `skills/retrofitting-codebases/validation-hooks.md`

```markdown
# Validation Hooks

Lightweight validation checks run continuously during archaeology.

## Hook 1: Finding Added

**Trigger**: Every time a finding is added to findings.md

**Checks**:
- [ ] Has file:line citation
- [ ] Citation exists (`validate-findings.py`)
- [ ] Classification present (business_rule|assumption|question|branch)
- [ ] Risk level assigned (if assumption)

**Auto-fix**: Prompt for missing fields immediately

## Hook 2: Assumption Identified

**Trigger**: Adding assumption to findings

**Checks**:
- [ ] Validation status recorded (validated|unvalidated)
- [ ] Risk level assigned (critical|high|medium|low)
- [ ] If critical/high + unvalidated → Add to questions section

**Auto-action**:
- Critical unvalidated assumptions block phase completion
- Generate validation code snippet for developer

## Hook 3: File Traced

**Trigger**: Adding file to execution trace

**Checks**:
- [ ] File count ≤ 15 (scope limit)
- [ ] If = 15 → Warning: "At scope limit, summarize remaining"
- [ ] Trace depth ≤ 4 levels
- [ ] If = 4 → Warning: "Max depth, mark deeper calls as external"

**Auto-action**: Force scope discipline

## Hook 4: Gap Classified

**Trigger**: Adding gap to gaps.md

**Checks**:
- [ ] Type assigned (bug|intentional|unclear|drift|missing)
- [ ] Evidence cited for both expected and actual
- [ ] If "unclear" → Conflict created in conflicts.md
- [ ] Action assigned

**Auto-action**: "unclear" gaps auto-create conflict tracking entry
```

**Implementation**: Create pre-commit hook or file watcher.

**New file**: `skills/retrofitting-codebases/scripts/validation-daemon.py`

```python
#!/usr/bin/env python3
"""Watches .retrofit/ for changes and validates incrementally."""

import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class RetrofitValidator(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith("-findings.md"):
            self.validate_findings(event.src_path)
        elif event.src_path.endswith("gaps.md"):
            self.validate_gaps(event.src_path)

    def validate_findings(self, filepath: str):
        """Run validation checks on findings file."""
        # Check file:line references
        errors = validate_file_references(filepath)
        if errors:
            print(f"⚠️  {filepath}: {len(errors)} validation errors")
            for e in errors:
                print(f"   - {e}")

        # Check for uncategorized findings
        findings = parse_findings(filepath)
        uncategorized = [f for f in findings if not f.get("type")]
        if uncategorized:
            print(f"⚠️  {len(uncategorized)} findings missing type classification")

        # Check assumption risks
        unscored = [a for a in findings.assumptions if not a.get("risk")]
        if unscored:
            print(f"⚠️  {len(unscored)} assumptions missing risk level")

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(RetrofitValidator(), ".retrofit/", recursive=True)
    observer.start()
    print("🔍 Validation daemon watching .retrofit/")
    print("   Press Ctrl+C to stop")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
```

**Usage**: Run in background during archaeology:

```bash
# Terminal 1: Start validation daemon
python scripts/validation-daemon.py

# Terminal 2: Do archaeology work
# Validator provides real-time feedback
```

**Expected Impact**:
- Catch errors when introduced (not at end of phase)
- Enforce scope limits in real-time
- Reduce rework at checkpoints

---

## Implementation Priority

| Improvement | Impact | Effort | Priority | Timeline |
|-------------|--------|--------|----------|----------|
| 1. Finding Accuracy Validation | High | Medium | 🔴 Critical | Week 1 |
| 3. Progress Metrics | High | Low | 🔴 Critical | Week 1 |
| 4. Conflict Resolution | High | Medium | 🟡 High | Week 2 |
| 2. Test Harness Integration | Very High | High | 🟡 High | Week 2-3 |
| 5. Incremental Validation | Medium | Medium | 🟢 Nice-to-have | Week 4 |

**Rationale**:
- Metrics (3) are low-effort, high-impact → start here
- Finding validation (1) prevents cascading errors → critical
- Test integration (2) is transformative but requires test framework detection
- Conflict tracking (4) essential for production use
- Incremental validation (5) is quality-of-life improvement

---

## Conclusion

The brownfield approach is **theoretically sound** but needs **operational tooling** to scale beyond small codebases or single-user scenarios.

**What works well**:
- Evidence hierarchy is excellent
- Phase structure is logical
- Checkpoints prevent runaway work
- "Unknown is valid" culture

**What needs improvement**:
- Automation (currently mostly manual)
- Validation (shallow → deep)
- Metrics (subjective → objective)
- Conflict resolution (ad-hoc → structured)
- Continuous validation (batch → incremental)

**Recommendation**: Implement improvements 1 and 3 immediately (low-hanging fruit), then 4 and 2 for production readiness.

---

## Appendix: Quick Wins

Beyond the 5 main improvements, consider these small changes:

### A. Add Archaeology Templates

Create `.retrofit/templates/findings-template.md`:

```markdown
# Findings: {Feature}

## Metadata
- **Analyzed by**: {name}
- **Date**: {date}
- **Files traced**: 0/15
- **Depth**: 0/4 levels

## Test Analysis
| Test Name | Assertion | Status | Matches Code? |
|-----------|-----------|--------|---------------|

## Execution Trace
1. Entry: {endpoint/handler}
2. ...

## Business Rules
- [ ] Rule name: {file:line} - explicit/implicit

## Assumptions
| Assumption | Location | Validated? | Risk | Validation Method |
|------------|----------|------------|------|-------------------|

## Questions
- [ ] {question requiring human answer}

## Scope Notes
{What was excluded and why}
```

### B. Add Discovery Automation

Enhance `discover-entry-points.sh` to auto-generate discovery.md:

```bash
bash scripts/discover-entry-points.sh --auto-generate
# Creates .retrofit/discovery.md with feature map skeleton
```

### C. Add Session Resume Checklist

Create `.retrofit/RESUME.md`:

```markdown
# Resuming Retrofit Work

Before continuing:

1. Check for drift:
   ```bash
   git status
   git diff .retrofit/
   ```

2. Verify phase:
   ```bash
   cat .retrofit/metrics.json | jq '.phases'
   ```

3. Check blockers:
   ```bash
   python scripts/conflict-tracker.py report
   ```

4. Review last session:
   ```bash
   cat .claude/sessions/{latest}.yaml
   ```
```

These quick wins require minimal effort but significantly improve user experience.

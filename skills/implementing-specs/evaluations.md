# Evaluations

Test scenarios to verify skill effectiveness.

## Evaluation 1: Basic AC Implementation

```json
{
  "skills": ["implementing-specs"],
  "query": "Implement AC-1 from the password reset spec",
  "files": [
    "docs/specs/password-reset.md",
    ".claude/current_task.json"
  ],
  "expected_behavior": [
    "Reads docs/specs/password-reset.md to understand AC-1",
    "Writes or updates acceptance test before implementing",
    "Adds provenance comment: // Implements: /docs/specs/password-reset.md#AC-1",
    "Commits with format: [AC-1] {description}",
    "Updates .claude/current_task.json with status"
  ]
}
```

## Evaluation 2: Session Startup

```json
{
  "skills": ["implementing-specs"],
  "query": "Continue working on the auth feature",
  "files": [
    "docs/specs/auth.md",
    ".claude/current_task.json",
    ".claude/sessions/2026-01-03-x7k2.yaml"
  ],
  "expected_behavior": [
    "Reads current_task.json to find assignment",
    "Reads previous session log for context",
    "Identifies next pending AC from progress",
    "Continues from where previous session left off"
  ]
}
```

## Evaluation 3: Handling Blockers

```json
{
  "skills": ["implementing-specs"],
  "query": "Implement AC-3 which requires calling the payment API",
  "files": [
    "docs/specs/checkout.md",
    ".claude/current_task.json"
  ],
  "setup": "Payment API mock does not exist",
  "expected_behavior": [
    "Attempts to implement AC-3",
    "Recognizes mock is missing",
    "Records failure with type: mock_missing",
    "Skips AC-3 and continues to AC-4 (or documents blocker)",
    "Does not fabricate mock behavior"
  ]
}
```

## Evaluation 4: Session End

```json
{
  "skills": ["implementing-specs"],
  "query": "I need to stop for today",
  "files": [
    ".claude/current_task.json"
  ],
  "expected_behavior": [
    "Commits any uncommitted work (or reverts broken state)",
    "Creates session log in .claude/sessions/",
    "Session log includes work_completed, failures, handoff",
    "Handoff describes current state for next session"
  ]
}
```

## Should NOT Trigger

These queries should NOT activate this skill:

- "Write a spec for password reset" → use spec-writing skill/agent
- "What is TDD?" → answer directly, no skill needed
- "Review the password reset code" → use review skill/agent
- "Explain acceptance criteria" → answer directly

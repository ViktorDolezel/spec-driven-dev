# Evaluations

## Evaluation 1: Discovery Phase

```json
{
  "skills": ["retrofitting-codebases"],
  "query": "Help me understand this codebase before I make changes",
  "files": ["src/Controllers/UserController.cs", "src/Services/AuthService.cs"],
  "expected_behavior": [
    "Creates .retrofit/ directory",
    "Searches for entry points (API routes, handlers)",
    "Creates discovery.md with feature map",
    "Identifies test coverage gaps",
    "Suggests priority order for deeper analysis"
  ]
}
```

## Evaluation 2: Feature Archaeology

```json
{
  "skills": ["retrofitting-codebases"],
  "query": "Document what the password reset feature actually does",
  "files": ["src/Controllers/PasswordController.cs", "src/Services/TokenService.cs"],
  "expected_behavior": [
    "Traces execution from entry point",
    "Documents all branches and conditions",
    "Extracts business rules from code",
    "Notes assumptions (validated vs unvalidated)",
    "Creates .retrofit/features/password-reset-findings.md"
  ]
}
```

## Evaluation 3: Gap Analysis

```json
{
  "skills": ["retrofitting-codebases"],
  "query": "Compare what the code does vs what the docs say it should do",
  "files": [
    "src/Services/TokenService.cs",
    "docs/api/password-reset.md"
  ],
  "expected_behavior": [
    "Reads existing documentation",
    "Compares documented behavior to actual code",
    "Classifies each difference (bug, intentional, unclear)",
    "Creates .retrofit/gaps.md",
    "Does not assume which is correct without evidence"
  ]
}
```

## Evaluation 4: Generate Retrofitted Spec

```json
{
  "skills": ["retrofitting-codebases"],
  "query": "Create a spec from what we found about password reset",
  "files": [
    ".retrofit/features/password-reset-findings.md",
    ".retrofit/gaps.md",
    ".retrofit/assumptions.md"
  ],
  "expected_behavior": [
    "Reads findings from previous phases",
    "Creates spec with Current Behavior section",
    "Marks intended behavior changes with gap references",
    "Links known issues to gaps",
    "Makes assumptions explicit in spec"
  ]
}
```

## Should NOT Trigger

- "Implement the password reset spec" → use implementing-specs
- "Write a new spec for checkout" → use spec writing (greenfield)
- "What's the architecture of microservices?" → answer directly

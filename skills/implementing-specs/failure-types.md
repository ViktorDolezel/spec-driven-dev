# Failure Types

| Type | When | Action |
|------|------|--------|
| `spec_ambiguous` | Spec unclear or open to interpretation | Document assumption, continue, flag |
| `spec_missing` | Required info not in spec | Stop, request update |
| `mock_missing` | Test needs unavailable mock/fixture | Skip AC, note in backlog |
| `tool_failure` | Build/test/command failed | Retry once, then try alternative |
| `test_flaky` | Test passes intermittently | Fix flakiness before continuing |
| `permission_denied` | Action blocked | Stop immediately |

## Recording

```yaml
failures:
  - type: spec_ambiguous
    detail: "Token format not specified (UUID vs JWT)"
    resolution: "Used UUID, flagged for review"
```

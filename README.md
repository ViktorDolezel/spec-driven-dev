# spec-driven-dev

Spec-driven development plugin for Claude Code.

## Installation

```bash
/plugin install https://github.com/your-org/spec-driven-dev
```

## Commands

| Command | Purpose |
|---------|---------|
| `/implement` | Implement feature from spec using TDD |
| `/retrofit` | Reverse-engineer specs from existing code |
| `/session-end` | End session with proper handoff |

## Skills

| Skill | Auto-triggers when |
|-------|-------------------|
| `implementing-specs` | Working with `/docs/specs/*.md`, AC-* references |
| `retrofitting-codebases` | User mentions "retrofit", "legacy", "audit" |

## Agents

| Agent | Use for |
|-------|---------|
| `archaeologist` | Deep-dive code investigation |
| `spec-writer` | Creating specifications |

## Directory Structure

When using this plugin:

```
your-repo/
├── .claude/
│   ├── current_task.json    # Active assignment
│   └── sessions/            # Session logs
├── .retrofit/               # Brownfield analysis outputs
│   ├── discovery.md
│   ├── features/
│   ├── gaps.md
│   └── assumptions.md
└── docs/
    └── specs/               # Technical specifications
```

## Workflow

**Greenfield:**
```
/implement {feature} → TDD loop → /session-end
```

**Brownfield:**
```
/retrofit → discovery → archaeology → gaps → specs
```

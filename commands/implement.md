---
description: Start implementing a feature from its specification using TDD.
---

# /implement

Use the `implementing-specs` skill to implement from a specification.

**Arguments:** spec path, feature name, or issue number

Examples:
- `/implement password-reset` → looks for `/docs/specs/password-reset.md`
- `/implement /docs/specs/auth.md` → uses that spec directly
- `/implement 42` → finds spec linked to issue #42

If no argument provided, check `.claude/current_task.json` for current assignment.

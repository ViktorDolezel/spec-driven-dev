---
description: End session with proper commit, progress update, and handoff notes.
---

# /session-end

Complete your session properly:

1. Commit or revert uncommitted changes
2. Update `.claude/current_task.json` with progress
3. Create session log at `.claude/sessions/{date}-{id}.yaml`
4. Write handoff notes for next session

See `implementing-specs` skill for session log format.

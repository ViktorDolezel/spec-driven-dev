# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A Claude Code plugin for spec-driven development. It provides commands, skills, and agents to implement features from technical specifications using TDD, and to retrofit existing codebases with specifications.

## Plugin Structure

```
commands/     # Slash commands (/implement, /retrofit, /session-end)
skills/       # Auto-triggered behaviors based on context
agents/       # Specialized sub-agents (archaeologist, spec-writer)
.claude-plugin/plugin.json  # Plugin metadata
```

## Two Workflows

**Greenfield (new features):**
- Specs live in `/docs/specs/{feature}.md`
- Task state tracked in `.claude/current_task.json`
- Session logs in `.claude/sessions/{date}-{id}.yaml`
- TDD loop: read AC → write failing test → implement → commit `[AC-N] description`

**Brownfield (existing code):**
- All outputs go to `.retrofit/` directory
- Phases are iterative: Discovery ↔ Archaeology ↔ Gap Analysis ↔ Assumptions → Spec Generation
- Document what code **does**, not what it **should** do
- Human validation required before spec generation (see checkpoints.md)
- Specs use versioning: v1 (current behavior) vs v2 (target behavior)

## Key Conventions

- Every implementation must have provenance comment: `// Implements: /docs/specs/{feature}.md#AC-{N}`
- Commit messages start with `[AC-{N}]`
- Acceptance criteria use Given/When/Then format with concrete values
- "Unknown" is valid - don't guess when blocked
- Scope-box archaeology: max 15 files, 4 levels deep, 3 attempts before "unclear"
- When evidence conflicts, stop and ask (never guess)

## Evidence Priority (Brownfield)

When determining intended behavior, check sources in this order:

1. Passing tests (executable proof)
2. API contracts (OpenAPI, GraphQL)
3. PRD/Spec files
4. Recent commits (<6 months)
5. Code comments near logic
6. README/general docs
7. Variable/function names (lowest trust)

## File Formats

**current_task.json** - tracks which ACs are pending/in_progress/passed with attempt counts
**session logs** - YAML with work_completed, failures (typed: spec_ambiguous, mock_missing, etc.), and handoff notes
**findings.md** - execution trace, business rules (explicit/implicit), assumptions (validated/unvalidated)
**gaps.md** - expected vs actual behavior with classification (bug/intentional/unclear/drift/missing)

## Utility Scripts (Brownfield)

Run from `skills/retrofitting-codebases/scripts/`:

- `bash discover-entry-points.sh` - find API routes, CLI commands, background jobs, event handlers
- `python validate-findings.py <file>` - validate file:line references in findings

## When Modifying This Plugin

- Skills trigger based on context clues in their YAML frontmatter `description` field
- Agents define capabilities and output formats
- Commands reference skills to do the actual work
- Evaluations in each skill folder define expected behaviors for testing

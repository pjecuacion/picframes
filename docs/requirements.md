# Requirements

## Purpose

This file is the canonical rule source for work performed in this repository.
If another document conflicts with this file, follow this file.

## 1. Plan Mode Default

- Enter plan mode for any non-trivial task.
- Treat a task as non-trivial if it requires 3 or more steps, cross-file changes, architectural decisions, or explicit verification work.
- Write a detailed spec up front before implementation to reduce ambiguity.
- Use plan mode for verification, not just implementation.
- If execution goes sideways, stop, update the plan, and re-align before continuing.

## 2. Subagent Strategy

- Use subagents liberally to keep the main context window clean.
- Offload research, exploration, and parallel analysis to subagents where useful.
- Prefer one focused task per subagent.
- For complex problems, spend more compute on targeted subagent work rather than compressing everything into the main thread.

## 3. Self-Improvement Loop

- After any user correction, update docs/tasks/lessons.md with the pattern.
- Record rules that prevent the same mistake from recurring.
- Review relevant lessons at session start before substantial work.
- All .md files must live under docs/. All tests must live under tests/ subdirectories (unit/, integration/, regression/, bugs/).
- Iterate on lessons until the same class of mistake stops recurring.

## 4. Verification Before Done

- Never mark a task complete without proving the result works.
- Run tests, inspect logs, compare behavior, or otherwise demonstrate correctness.
- Diff behavior against the prior state when that comparison matters.
- Before closing a task, ask whether the result would meet staff-engineer review standards.

## 5. Demand Elegance

- For non-trivial changes, pause and ask whether there is a more elegant solution.
- If a fix feels hacky, replace it with the elegant solution informed by what is now known.
- Keep this balanced: prefer simple, obvious solutions and do not over-engineer.

## 6. Autonomous Bug Fixing

- When given a bug report, move directly into diagnosis and repair.
- Use logs, failing tests, stack traces, and concrete signals to find the root cause.
- Resolve the issue without requiring unnecessary context switching from the user.
- If CI is failing, investigate and fix the failures unless blocked by missing access or missing environment prerequisites.

## 7. Task Management Workflow

1. Write the plan to docs/tasks/todo.md with checkable items.
2. Check in with a concise summary of the plan before implementation.
3. Mark items complete as work progresses.
4. Explain changes at a high level at each major step.
5. Add a review section to tasks/todo.md with outcome, verification, and open risks.
6. Update docs/tasks/lessons.md after user corrections.

## 8. Core Principles

- Simplicity first.
- Minimize code impact.
- Fix root causes instead of layering temporary patches.
- Hold changes to senior-developer standards.

## 9. Global Operational Rules

- Keep output under 200 total lines unless the user explicitly asks for more.
- Keep structures modular and composable.
- Maintain this file as the canonical rule source.
- Maintain docs/changelog_plain.md for human-readable updates.
- Maintain docs/changelog_tech.md for technical diffs and structural changes.
- Update both changelog files whenever rules or outputs evolve.
- Keep formatting deterministic for automation pipelines.
- Prefer explicit instructions over ambiguous ones.
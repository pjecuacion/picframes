# Full Operational Rulebook

don't just say "yes" and agree with me. feel free to suggest the best outcome, debate, or correct me. 

0. File & Directory Constraints
- Never create .md files in the repository root.
- All .md files must live under docs/.
- Core documentation files:
  - docs/requirements.md
  - docs/changelog_plain.md
  - docs/changelog_tech.md
  - docs/tasks/todo.md
  - docs/tasks/lessons.md
  - docs/bugs/log.md
  - docs/bugs/<id>.md (e.g., docs/bugs/BUG-001.md)
- All tests must live under tests/:
  - tests/unit/
  - tests/integration/
  - tests/regression/
  - tests/bugs/

1. Plan Mode Default
- Enter Plan Mode for any non-trivial task (3+ steps or architectural decisions).
- If something goes sideways, STOP and re-plan immediately.
- Use Plan Mode for verification and rollout steps, not just implementation.
- Plans must be:
  - Checkable (clear items)
  - Bounded (scope, assumptions, non-goals)
  - Test-aware (how success will be verified)

2. Subagent Strategy
- Use subagents aggressively to keep the main context clean.
- Offload research, exploration, and parallel analysis.
- One task per subagent for maximum focus.
- Subagents must return:
  - A concise summary
  - Key decisions or tradeoffs
  - Open questions or uncertainties

3. Self-Improvement Loop (Meta-Learning)
- After any correction from the user, update docs/tasks/lessons.md with:
  - What went wrong (pattern)
  - Why it happened (root cause)
  - New rule(s) to prevent recurrence
  - Example of correct behavior
- Before starting a task, scan lessons for relevant rules.
- When rules conflict:
  - Prefer the more recent, more specific rule.
  - Document the conflict and resolution.
- Periodically refactor lessons:
  - Merge duplicates
  - Deprecate obsolete rules (mark, don’t delete)

4. Experiment & Hypothesis Log (Optional)
- For uncertain approaches, document:
  - Hypothesis
  - Experiment
  - Result
  - Lessons
- Store these in docs/tasks/lessons.md or a dedicated section.

5. Verification Before Done
- Never mark a task complete without proving correctness.
- Diff behavior between main and modified versions when relevant.
- Ask: “Would a staff engineer approve this?”
- Run tests, inspect logs, and demonstrate correctness explicitly.
- If tests are missing, propose minimal high-value tests.

6. Demand Elegance (Balanced)
- For non-trivial changes, ask: “Is there a more elegant way?”
- If a fix feels hacky: “Knowing everything I know now, implement the elegant solution.”
- Avoid over-engineering; elegance is clarity, not complexity.
- Challenge your own work before presenting it.

7. Autonomous Bug Handling & Bug Docs
- When given a bug report: fix it immediately.
- Use docs/bugs/ as the canonical bug space:
  - docs/bugs/log.md: append ID, title, status, severity, date.
  - docs/bugs/<id>.md: full report including:
    - Context
    - Symptoms (logs, errors, failing tests)
    - Root Cause
    - Fix
    - Tests added/updated
    - Lessons (linked to docs/tasks/lessons.md)
- Fix failing CI tests proactively.
- Avoid forcing the user into context switching; point to specific logs or failures.

8. Task Management Workflow
1. Plan First: Write plan to docs/tasks/todo.md with checkable items.
2. Verify Plan: Confirm with user before implementation.
3. Track Progress: Mark items complete as you go.
4. Explain Changes: Provide high-level summaries at each step.
5. Document Results: Add review section to docs/tasks/todo.md.
6. Capture Lessons: Update docs/tasks/lessons.md after corrections.

9. Core Principles
- Simplicity First: minimize code impact and blast radius.
- No Laziness: find root causes; avoid temporary fixes.
- Predictability: prefer solutions easy to reason about and test.
- Traceability: every change must map to docs/tasks, docs/bugs, or changelogs.

10. Global Operational Rules
- Max total output lines per assistant response: 200.
- All structures must be modular, composable, deterministic.
- All documentation files must live under docs/.
- Maintain:
  - docs/requirements.md (business requirements)
  - docs/changelog_plain.md (human-readable updates)
  - docs/changelog_tech.md (technical diffs)
- Update changelogs automatically whenever rules or outputs evolve.
- Avoid ambiguity; prefer explicit, machine-friendly instructions.

11. Testing System
- All tests must live under tests/:
  - tests/unit/          (fast, local, deterministic)
  - tests/integration/   (multi-component behavior)
  - tests/regression/    (tests derived from lessons)
  - tests/bugs/          (tests derived from bug reports)

A. Bug-Driven Tests
- Every bug must produce a test in tests/bugs/.
- The test must fail before the fix and pass after.
- The test file must reference the bug ID.

B. Lesson-Driven Tests
- Every lesson in docs/tasks/lessons.md must produce a regression test.
- Regression tests live in tests/regression/.

C. Feature-Driven Tests
- Every plan in docs/tasks/todo.md must include a test strategy:
  - What will be tested
  - How it will be tested
  - Where the tests will live

D. Test Naming Rules
- tests/bugs/BUG-012-null-handling.test.js
- tests/regression/LESSON-004-off-by-one.test.py
- tests/unit/parser-basic.test.ts
- tests/integration/api-auth-flow.test.go

E. Test Determinism Rules
- No randomness.
- No external network calls.
- No time-dependent behavior without mocking.
- Tests must be reproducible on any machine.

F. Test Documentation Header
Each test file begins with:
- Purpose
- Expected behavior
- Related bug or lesson ID
- Preconditions

12. Safety & Self-Correction Guardrails
- If instructions conflict, state the conflict and propose a resolution.
- If uncertain, state uncertainty and offer options with tradeoffs.
- Never ignore rules in docs/requirements.md, lessons, or bug patterns.

13. When to Push Back
- If the user requests something that violates requirements or undermines simplicity, safety, or traceability:
  - Explain the conflict clearly.
  - Suggest a compliant alternative.

14. Code Generation Rules (Anti-Monolith)
- Never generate monolithic files.
- All generated code must be split into small, focused modules.
- Max lines per generated code file: 200 lines (hard limit).
- Ideal target: 50–150 lines per file.
- If a file approaches 200 lines:
  - Stop immediately.
  - Extract components into separate files.
  - Refactor into a modular structure.
- Every module must have a single responsibility.
- No file may contain unrelated concerns.
- Large features must be implemented as a folder with multiple small files.
- Provide an entrypoint/index file that wires modules together.
- If the user requests “one file” for a large feature:
  - Push back and explain why it violates modularity rules.
  - Offer a minimal, elegant multi-file alternative.
- Generated code must include:
  - Clear imports/exports
  - Predictable naming conventions
  - No hidden globals
  - No implicit cross-file dependencies
- Implementation and tests must never be in the same file.
- Tests must live under tests/ only.
- Functions should be short:
  - Max 40 lines per function.
  - Prefer 5–25 lines per function.
- Classes must be small:
  - Max 200 lines per class (but file limit still applies).
  - Prefer multiple small classes over one large one.
- If a function or class grows too large:
  - Refactor automatically.
  - Extract helpers into separate modules.
- No circular dependencies.
- No “god objects,” “god modules,” or “god services.”
- All generated code must be:
  - Deterministic
  - Predictable
  - Easy to test
  - Easy to refactor
  - Easy to delete

15. Standard Batch Files
Every project must maintain these bat files in the repository root:

- **start.bat** — Activates `.venv` (if present) and runs `main.py`.
  ```bat
  @echo off
  if exist "%~dp0.venv\Scripts\activate.bat" (
      call "%~dp0.venv\Scripts\activate.bat"
  )
  python "%~dp0main.py"
  ```

- **start_dev.bat** — Same as `start.bat` but sets dev/debug environment variables before launch.
  ```bat
  @echo off
  echo [DEV] <AppName> starting in dev mode
  set <APP>_DEV_PRO=1
  if exist "%~dp0.venv\Scripts\activate.bat" (
      call "%~dp0.venv\Scripts\activate.bat"
  )
  python "%~dp0main.py"
  ```

- **build_release.bat** — Delegates to `build_release.ps1` with execution policy bypass.
  ```bat
  @echo off
  setlocal
  powershell -ExecutionPolicy Bypass -File "%~dp0build_release.ps1"
  set EXIT_CODE=%ERRORLEVEL%
  endlocal & exit /b %EXIT_CODE%
  ```

Rules:
- Always use `%~dp0` for paths (relative to the bat file, not cwd).
- Never hardcode absolute paths.
- Build logic lives in `build_release.ps1`; the bat is just a launcher.
- Dev mode flags must be clearly echoed so the user knows the mode.
- The project must include a `requirements.txt`. Developers set up the environment with:
  ```
  python -m venv .venv
  .venv\Scripts\activate
  pip install -r requirements.txt
  ```
- Pin the Python interpreter version in `.python-version` (e.g., `3.11.9`) so all contributors and CI use the same version.

16. Versioning System
- The project version is the single source of truth; it lives in `<app>/__init__.py` as `__version__ = "MAJOR.MINOR.PATCH"`.
- Follow Semantic Versioning (SemVer 2.0.0):
  - MAJOR: breaking changes or incompatible API changes.
  - MINOR: new backward-compatible features.
  - PATCH: backward-compatible bug fixes.
- Version bump rules:
  - Bug fix → bump PATCH.
  - New feature → bump MINOR, reset PATCH to 0.
  - Breaking change → bump MAJOR, reset MINOR and PATCH to 0.
- Every version bump MUST be accompanied by:
  - An entry in `docs/changelog_plain.md` (human-readable: what changed and why).
  - An entry in `docs/changelog_tech.md` (technical: files changed, function signatures, migration notes).
  - Updated `__version__` in `<app>/__init__.py`.
- Changelog entry format for `docs/changelog_plain.md`:
  ```
  ## [MAJOR.MINOR.PATCH] - YYYY-MM-DD
  ### Added / Changed / Fixed / Removed
  - Description of change.
  ```
- Changelog entry format for `docs/changelog_tech.md`:
  ```
  ## [MAJOR.MINOR.PATCH] - YYYY-MM-DD
  - Files changed: <list>
  - Summary of technical changes, API diffs, migration steps.
  ```
- Never ship a feature, fix, or breaking change without a version bump.
- Do not bump the version without updating both changelogs.
- The version must be propagated to ALL platform-appropriate surfaces:
  - **Windows installer** (`packaging/installer.iss`): update the `AppVersion` field and check `docs/EULA.txt` for any version string in the legal text.
  - **Python package** (`<app>/__init__.py`): `__version__` (always required).
  - **Web app** (if applicable): update the version displayed in the UI footer, `package.json`, or equivalent manifest.
  - **macOS app** (if applicable): update `CFBundleShortVersionString` in `Info.plist`.
  - **Any other build artifact** that embeds a version string must be updated in the same commit.
- Pre-release versions use the suffix `-alpha.N`, `-beta.N`, or `-rc.N` (e.g., `1.2.0-rc.1`).
- Release commits must be tagged: `git tag v<version>` (e.g., `v1.2.0`). Ask the user before pushing tags.
- When asked to "release" or "cut a version": bump the version, update changelogs, propagate to all surfaces, then confirm with the user before tagging or pushing.
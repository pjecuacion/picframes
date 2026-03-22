# Task Todo

## Active Task — PicFrames App Build

Date: 2026-03-22
Status: In Progress

### Specification

Build a new `picframes/` package from the template. The app:
- Accepts image files (.png, .jpg, .jpeg, .webp, .bmp, .tiff)
- Optionally removes the background using `rembg` (AI-powered, toggle, default ON)
- Center-crops to a square canvas
- Applies a frame/shape mask: Circle, Square (free), or Rounded Square (Pro)
- Outputs transparent-background PNG files
- Use case: app icons, profile pictures, stickers

### Design Decisions
- Background removal: checkbox toggle, default ON
- Free frames: Circle, Square
- Pro frame: Rounded Square + configurable corner radius slider (5–50%)
- Padding: 0–40px slider (free)
- Output: always PNG, square canvas (center-crop)
- Pro feature key: `"rounded_square"`

### Plan

- [x] Read all template files and understand structure
- [ ] Write plan to docs/tasks/todo.md (this file)
- [ ] Create `picframes/__init__.py`
- [ ] Create `picframes/settings.py`
- [ ] Create `picframes/resources.py`
- [ ] Create `picframes/theme.py`
- [ ] Create `picframes/processor.py`
- [ ] Create `picframes/runner.py`
- [ ] Create `picframes/option_builder.py`
- [ ] Create `picframes/app.py`
- [ ] Create `picframes/license/__init__.py`
- [ ] Create `picframes/license/key_model.py`
- [ ] Create `picframes/license/gate.py`
- [ ] Create `picframes/license/validator.py`
- [ ] Create `picframes/license/activation_dialog.py`
- [ ] Create `picframes/ui/__init__.py`
- [ ] Create `picframes/ui/banner.py`
- [ ] Create `picframes/ui/hero.py`
- [ ] Create `picframes/ui/source_card.py`
- [ ] Create `picframes/ui/output_card.py`
- [ ] Create `picframes/ui/settings_card.py`
- [ ] Create `picframes/ui/progress_card.py`
- [ ] Create `picframes/ui/preview_strip.py`
- [ ] Update `main.py`
- [ ] Update `requirements.txt`
- [ ] Write `tests/unit/test_processor.py`
- [ ] Update changelogs

### Test Strategy
- `tests/unit/test_processor.py`: unit tests for `_to_square`, `_apply_padding`, `_get_mask`, `_apply_mask`, `build_jobs`, `discover_files` — all using Pillow, no network, no file I/O except temp files

---

## Completed Task — Licensing & Monetisation

Date: 2026-03-20
Status: Done

## Specification

- Gate resize and preserve-folder-structure behind a Pro license.
- Use LemonSqueezy as the payment platform (product ID 905495, store 321041).
- Validate license keys via LemonSqueezy's /licenses/activate and /licenses/validate API.
- Show a Pro badge in the banner; show activation dialog with Buy link.
- Custom branded icon (amber W) in window, taskbar, EXE, and installer.
- Fix taskbar showing Python icon.
- Rebuild and produce a distributable installer.

## Plan

- [x] Create `bulk_webp/license/` package (key_model, validator, gate, activation_dialog).
- [x] Wire licensing into app.py (badge, gated checkboxes, dialog).
- [x] Persist license key via settings.py.
- [x] Replace Ed25519 offline validator with LemonSqueezy API validator.
- [x] Design and embed custom amber W icon (all sizes).
- [x] Fix AppUserModelID for taskbar icon.
- [x] Fix installer.iss publisher typo and AppURL.
- [x] Create LemonSqueezy product via dashboard; obtain checkout URL.
- [x] Add 11 unit tests (all mocked, deterministic).
- [x] Commit feature/licensing, merge to main, rebuild installer.

## Review

Outcome: Full licensing system shipped. Pro gates working. LemonSqueezy product live in test mode. Custom icon applied everywhere. Installer rebuilt at 23.3 MB.
Verification: `python -m pytest tests/unit/` — 21 tests passing. `dist/BulkWebP-Setup.exe` produced and verified.
Open Risks: Store is in test mode until LemonSqueezy payout/billing setup is completed in dashboard. License key generation on variant must be enabled manually in dashboard (API write blocked by 405).

---

## Completed Task — Inno Setup Installer

Date: 2026-03-19
Status: Done

## Specification

- Provide a desktop GUI for converting one or many images to WebP.
- Support single-file selection and bulk folder conversion.
- Keep the UX clean, minimalist, and easy to use on Windows.
- Include a top banner linking to Buy Me a Coffee: https://buymeacoffee.com/pjecuacion
- Produce a Windows installer workflow that can be used to share the app easily.
- Keep the implementation modular, with conversion logic separated from the UI.
- Add an app icon and wire it into the running app, executable, and installer.
- Add drag-and-drop support for files and folders.
- Add lossless WebP output and resize controls.
- Use an Inno Setup `.iss` installer workflow instead of NSIS.

## Plan

- [x] Replace the NSIS installer script with an Inno Setup `.iss` script.
- [x] Update the build orchestration to call Inno Setup when available.
- [x] Update documentation and changelogs to reflect the `.iss` workflow.
- [x] Verify the executable build and confirm installer prerequisites.

## Review

Outcome: Replaced the Windows installer layer with Inno Setup, using packaging/installer.iss and a build script that locates ISCC.exe on PATH or in the default install directories.
Verification: `powershell -ExecutionPolicy Bypass -File packaging/build.ps1` completed the PyInstaller build successfully and then reported the correct Inno Setup prerequisite when `ISCC.exe` was unavailable; static validation passed for packaging/build.ps1, packaging/installer.iss, and README.md.
Open Risks: A final `BulkWebP-Setup.exe` was not generated in this environment because Inno Setup is not installed; once `ISCC.exe` is available, the same build script should produce the installer.
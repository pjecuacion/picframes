# New App Checklist

Use this when building a new app from this template. Check off each item before marking the task done.

---

## Setup

- [ ] Source app placed in `temp/` (if porting existing logic)
- [ ] Source app fully read and business logic understood
- [ ] New package name decided (e.g. `bulk_resize`)
- [ ] App display name derived (e.g. `Bulk Resize`)
- [ ] Exe name derived (e.g. `BulkResize.exe`)
- [ ] New GUID generated for `installer.iss` `AppId`

## Package Structure

- [ ] `<new_package>/` folder created
- [ ] `__init__.py` — exposes `main()`
- [ ] `app.py` — CTk window, correct `APP_TITLE`, correct class name
- [ ] `converter.py` — business logic ported from source
- [ ] `conversion_runner.py` — job runner with progress reporting
- [ ] `option_builder.py` — builds job options from UI state
- [ ] `resources.py` — asset path helper
- [ ] `settings.py` — JSON persistence at `~/.app_name/settings.json`
- [ ] `theme.py` — color tokens, font helper, radii
- [ ] `license/validator.py` — `_INSTANCE_NAME` updated to new app name
- [ ] `license/` — all other files copied and updated for new app context
- [ ] `ui/` — all cards copied and updated for new app context

## Entry Points

- [ ] `main.py` — AppUserModelID updated
- [ ] `main.py` — import updated to `from <new_package> import main`

## Packaging

- [ ] `packaging/BulkWebP.spec` renamed to `packaging/<AppName>.spec`
- [ ] `.spec` — both `name=` values updated in `EXE` and `COLLECT` blocks
- [ ] `packaging/build.ps1` — `$specFile` line updated to point to new `.spec` filename
- [ ] `packaging/installer.iss` — `AppName` updated
- [ ] `packaging/installer.iss` — `AppExeName` updated
- [ ] `packaging/installer.iss` — `AppId` updated (generate a new GUID)
- [ ] `packaging/installer.iss` — `OutputBaseFilename` updated
- [ ] `packaging/installer.iss` — `SourceDir` updated to new dist folder name
- [ ] `build_release.bat` — no changes needed (delegates to `build_release.ps1`)
- [ ] `build_release.ps1` — no changes needed (delegates to `packaging/build.ps1`)
- [ ] `start.bat` — no changes needed

## Assets

- [ ] `assets/app_icon.ico` replaced with new app icon (or confirmed with user)
- [ ] `assets/THIRD_PARTY_NOTICES.txt` updated if new dependencies added
- [ ] `docs/EULA.txt` updated with new app name

## Docs

- [ ] `docs/requirements.md` updated for new app
- [ ] `docs/changelog_plain.md` entry added
- [ ] `docs/changelog_tech.md` entry added

## Cleanup

- [ ] `bulk_webp/` folder deleted (new package replaces it)
- [ ] `tests/unit/test_converter.py` and `tests/unit/test_license_validator.py` deleted or replaced with new app tests
- [ ] `temp/` cleared (source app files removed, `.gitkeep` left in place)
- [ ] `README.md` updated for new app



- [ ] App launches without errors (`python main.py`)
- [ ] Window title shows correct app name
- [ ] Banner shows correct app name and Pro badge
- [ ] Core feature works end-to-end
- [ ] Dark/light mode toggle works
- [ ] Settings persist across restarts
- [ ] License gate activates and validates correctly
- [ ] Unit tests added for new business logic under `tests/unit/`
- [ ] All tests pass
- [ ] `temp/` cleared after porting is complete

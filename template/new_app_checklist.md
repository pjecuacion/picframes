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
- [ ] `processor.py` — business logic ported from source (replaces the stub in `my_app/processor.py`)
- [ ] `runner.py` — job runner with progress reporting
- [ ] `option_builder.py` — builds job options from UI state
- [ ] `resources.py` — asset path helper
- [ ] `settings.py` — hardcoded directory path updated (`~/.my_app/` → `~/.new_app/`) in `settings.py` line 7
- [ ] `theme.py` — color tokens, font helper, radii
- [ ] `license/validator.py` — `_INSTANCE_NAME` updated to new app name (line 14)
- [ ] `license/gate.py` — `PRO_FEATURES` frozenset updated to match new app's Pro-gated feature names (line 6–7)
- [ ] `license/activation_dialog.py` — LemonSqueezy checkout URL updated with new product GUID (line 13–14)
- [ ] `license/activation_dialog.py` — Pro feature description text updated (line 48)
- [ ] `license/` — all other files reviewed and updated for new app context
- [ ] `ui/banner.py` — `_DONATION_URL` updated to new app's Buy Me a Coffee page, or button removed (line 11)
- [ ] `ui/banner.py` — banner copy updated: `"Enjoying My App?..."` → new app name (line 38)
- [ ] `ui/hero.py` — app headline updated (line 24)
- [ ] `ui/hero.py` — app sub-headline updated (line 30)
- [ ] `ui/hero.py` — primary action button text updated (lines 37 and 53)
- [ ] `ui/source_card.py` — `filetypes` filter updated to match new app's input formats (line ~98)
- [ ] `ui/source_card.py` — drop zone label and description updated (lines ~78, ~83)
- [ ] `ui/settings_card.py` — slider label, option labels, and Pro feature label updated to match new app's settings
- [ ] `ui/preview_strip.py` — kept as-is (shows file names) or enhanced with thumbnails for visual file types
- [ ] `ui/` — all remaining cards reviewed and updated for new app context

## Entry Points

- [ ] `main.py` — AppUserModelID updated
- [ ] `main.py` — import updated to `from <new_package> import main`

## Packaging

- [ ] `packaging/MyApp.spec` renamed to `packaging/<AppName>.spec`
- [ ] `.spec` — both `name=` values updated in `EXE` and `COLLECT` blocks
- [ ] `packaging/build.ps1` — `$specFile` line updated to point to new `.spec` filename
- [ ] `packaging/installer.iss` — `AppName` updated
- [ ] `packaging/installer.iss` — `AppVersion` updated to new app's initial version
- [ ] `packaging/installer.iss` — `AppPublisher` updated (shown in Windows Add/Remove Programs)
- [ ] `packaging/installer.iss` — `AppURL` updated (publisher URL shown in Add/Remove Programs)
- [ ] `packaging/installer.iss` — `AppExeName` updated
- [ ] `packaging/installer.iss` — `AppId` updated (generate a new GUID — **never reuse an existing one**)
- [ ] `packaging/installer.iss` — `OutputBaseFilename` updated
- [ ] `packaging/installer.iss` — `SourceDir` updated to new dist folder name
- [ ] `build_release.bat` — no changes needed (delegates to `build_release.ps1`)
- [ ] `build_release.ps1` — no changes needed (delegates to `packaging/build.ps1`)
- [ ] `start.bat` — no changes needed

## Assets

- [ ] Edit `template/gen_icon.py` — set `BG`, `FG`, and `LETTER` for the new app
- [ ] Run `python template/gen_icon.py` from repo root to regenerate `assets/app_icon.png` and `assets/app_icon.ico`
- [ ] `assets/THIRD_PARTY_NOTICES.txt` updated if new dependencies added
- [ ] `docs/EULA.txt` updated with new app name

## Docs

- [ ] `docs/requirements.md` updated for new app
- [ ] `docs/changelog_plain.md` entry added
- [ ] `docs/changelog_tech.md` entry added

## Cleanup

- [ ] `my_app/` folder renamed to `<new_package>/` (or kept and refactored in-place)
- [ ] `tests/unit/test_processor.py` and `tests/unit/test_license_validator.py` updated for new app
- [ ] `temp/` cleared (source app files removed, `.gitkeep` left in place)
- [ ] `README.md` updated for new app

## LemonSqueezy

- [ ] `lemonsqueezy/product_page.md` — headline, subheadline, and Pro feature bullets updated for new app
- [ ] `lemonsqueezy/product_page.md` — pricing placeholder `$[X]` replaced with real price
- [ ] `lemonsqueezy/product_page.md` — copy pasted into LemonSqueezy product description field
- [ ] `license/activation_dialog.py` — checkout URL updated with new product GUID

## Smoke Tests

- [ ] App launches without errors (`python main.py`)
- [ ] Window title shows correct app name
- [ ] Banner shows correct app name and Pro badge
- [ ] Core feature works end-to-end
- [ ] Dark/light mode toggle works
- [ ] Banner is inverse of the current app mode: dark when app is light, light when app is dark (see note below)
- [ ] Settings persist across restarts
- [ ] License gate activates and validates correctly
- [ ] Unit tests added for new business logic under `tests/unit/`
- [ ] All tests pass
- [ ] `temp/` cleared after porting is complete

---

## Notes

### Buy Me a Coffee banner — inverse theming

**What this means:**
The top banner (`BannerFrame`) is always the opposite of the main app theme.
In light mode the banner is dark navy; in dark mode the banner is light.
This makes it pop as a distinct brand anchor rather than blending into the content area.

**Why it works this way:**
The banner tokens in `my_app/theme.py` use genuinely opposite values for each mode:
```python
BANNER_BG   = ("#16212D", "#F1F5F9")  # dark in light mode, light in dark mode
BANNER_TEXT = ("#F1F5F9", "#16212D")  # light on dark banner, dark on light banner
```
CustomTkinter colour tuples are `(light_mode_value, dark_mode_value)`, so CTk picks the
correct value automatically when the user toggles the theme.

**Files involved:**

| File | What to check |
|---|---|
| `my_app/theme.py` lines 7–8 | `BANNER_BG` and `BANNER_TEXT` — first value dark, second value light |
| `my_app/ui/banner.py` line 31 | `BannerFrame.__init__` passes `fg_color=theme.BANNER_BG` — do not change this |
| `my_app/ui/banner.py` lines 44–54 | "Buy Me a Coffee" `CTkButton` — amber is readable on both dark and light banner backgrounds |
| `my_app/ui/banner.py` lines 56–64 | `CTkSwitch` — `text_color=theme.BANNER_TEXT` keeps the label readable in both modes |

**How to verify (smoke test steps):**
1. Run `python main.py`.
2. Observe the top banner — it must have a **dark navy background** regardless of the current mode.
3. Click the dark/light toggle switch in the banner → the main window background and all cards should switch between light and dark.
4. After toggling, the **banner must remain dark navy** — it must never turn white or light grey.
5. Confirm the "Buy Me a Coffee" amber button and all banner text remain legible (no low-contrast text or invisible buttons) in both modes.

**When porting to a new app:**
- Update the `_DONATION_URL` constant in `ui/banner.py` to the new app's Buy Me a Coffee page (or remove the button entirely if not needed).
- Keep `BANNER_BG` as a dark-on-dark tuple in `theme.py` to preserve the inverse appearance.
- If you change the banner background to a light colour, invert `BANNER_TEXT` and all button `text_color` values on the banner accordingly.


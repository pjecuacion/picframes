# Technical Changelog

## [1.1.0] - 2026-03-30
- Files changed: `picframes/license/gate.py`, `picframes/license/__init__.py`, `picframes/ui/settings_card.py`, `picframes/app.py`, `picframes/__init__.py`, `packaging/installer.iss`, `lemonsqueezy/product_page.md`
- `gate.py`: `_PRO_FEATURES` expanded to `{"rounded_square", "ico", "ai_removal"}`; added `FREE_BATCH_LIMIT: int = 10`.
- `license/__init__.py`: exports `FREE_BATCH_LIMIT`.
- `settings_card.py`: `_output_format_btn` stored as instance variable; initial values `["PNG", "ICO  (Pro)"]`; `get_output_format` uses `.split()[0]` to strip Pro suffix; `remove_bg_checkbox` starts deselected/disabled; `apply_license_state` enables/disables ICO button values and AI removal checkbox.
- `app.py`: imports `FREE_BATCH_LIMIT`; stores `self._license_info`; `_apply_license` sets `_license_info`; `_run_job` enforces batch cap with warning dialog.
- Version bumped 1.0.0 → 1.1.0.

## 2026-03-28

- **Deleted `my_app/`** — entire template stub package removed (18 files).
- **Deleted `temp/gen_icon.py`** — one-shot icon generation script removed after use.
- **`assets/app_icon.png` + `assets/app_icon.ico`** — regenerated: amber `#F59E0B` "P" glyph on dark slate `#0f172a` rounded-square canvas; ICO embeds 6 sizes (16/32/48/64/128/256 px).
- **`packaging/MyApp.spec`** — `name='PicFrames'` in EXE and COLLECT blocks; `console=False`.
- **`packaging/installer.iss`** — `AppName=PicFrames`, `AppVersion=1.0.0`, `AppPublisher=Prince Ecuacion`, `AppExeName=PicFrames.exe`, `AppId={{485A531B-A164-4A75-9C02-04055CF01149}`, `OutputBaseFilename=PicFrames-Setup`; URL fields removed.
- **`packaging/build.ps1`** — removed TODO comment from `$specFile` line.
- **`requirements.txt`** — `rembg>=2.0.50` → `rembg[cpu]>=2.0.50` (ensures `onnxruntime` is pulled in).
- **`picframes/ui/banner.py`** — `_DONATION_URL = "https://buymeacoffee.com/pjecuacion"`.
- **`picframes/license/activation_dialog.py`** — `_CHECKOUT_URL` set to real PicFrames Pro LemonSqueezy checkout URL (`f2ce3041-…`).
- **`assets/THIRD_PARTY_NOTICES.txt`** — header rebranded to PicFrames; added entries 5–7: rembg 2.0.74 (MIT), ONNX Runtime 1.24.4 (MIT), NumPy (BSD 3-Clause).
- **`docs/EULA.txt`** — global replace "Bulk WebP" → "PicFrames"; "WebP image files" → "image files".
- **`README.md`** — fully rewritten: describes Circle/Square/Rounded Square framing, rembg AI removal, ICO output, and LemonSqueezy Pro licensing.
- **`.env`** — `LEMONSQUEEZY_PRODUCT_ID` updated `905495` → `927002` (PicFrames Pro); `LEMONSQUEEZY_VARIANT_ID` updated `1424228` → `1457453`; `LEMONSQUEEZY_CHECKOUT_URL` set to PicFrames checkout URL; `BULK_WEBP_LICENSE_PRIVATE_KEY` renamed to `PICFRAMES_LICENSE_PRIVATE_KEY`; `LEMONSQUEEZY_VARIANT_ID` added.
- **`tools/issue_license.py`** — fully rewritten: calls `POST /v1/checkouts` with `custom_price: 0` and `checkout_data.email`; reads `.env` automatically via `python-dotenv`-style parser; accepts `--open` flag to open URL in browser. Removed Ed25519 key generation logic entirely.

## 2026-03-23

- `processor.py`: added `_ICO_SIZES = [(16,16),(32,32),(48,48),(64,64),(128,128),(256,256)]`; `ProcessingOptions.output_format: str = "png"` field; `build_jobs` uses `.ico` extension when `output_format == "ico"`; `_process_file` branches to `_save_ico(img, dst)` or `img.save(dst, "PNG")`; new `_save_ico(img, dst)` upscales to 256 minimum and passes all valid sizes to Pillow's ICO encoder.
- `option_builder.py`: `build_options` now passes `output_format=settings_card.get_output_format()`.
- `ui/settings_card.py`: added Output Format segmented button `["PNG", "ICO"]` (rows 1–2); renumbered grid rows 3–10; added `get_output_format()` method.
- `tests/unit/test_processor.py`: added `TestBuildJobs::test_outputs_as_ico`, `TestProcessFile::test_ico_output_format`, and `TestSaveIco` class (3 tests). Total: 29 tests, all passing.

## 2026-03-22

- Created `picframes/` package (replaces `my_app/` template stub) with the following modules:
  - `processor.py`: `SUPPORTED_EXTENSIONS` (.png .jpg .jpeg .webp .bmp .tiff .tif), `ProcessingOptions` dataclass (frame_shape, corner_radius_pct, padding, remove_bg, overwrite), `_to_square` (center-crop), `_apply_padding`, `_get_mask` (circle/rounded_square/square), `_apply_mask` (ImageChops.multiply on alpha), `process_single_job` (picklable worker), `build_jobs` (stem + .png output)
  - `runner.py`: ProcessPoolExecutor with cancellation via threading.Event — unchanged from template
  - `option_builder.py`: `build_options` reads `get_frame_shape()`, `radius_slider`, `padding_slider`, `remove_bg_checkbox`; `default_output_dir` uses `picframes_output` / `_picframes` suffixes
  - `settings.py`: persists to `~/.picframes/settings.json`
  - `app.py`: `PicFramesApp` (CTk + TkinterDnD); APP_TITLE = "PicFrames"
  - `license/gate.py`: `_PRO_FEATURES = frozenset({"rounded_square"})`
  - `license/validator.py`: `_INSTANCE_NAME = "PicFrames"`
  - `license/activation_dialog.py`: Pro feature description updated to mention Rounded Square
  - `ui/settings_card.py`: segmented button (Circle/Square) + Pro section (rounded_checkbox + radius_slider 5–50%); `get_frame_shape()` method
  - `ui/preview_strip.py`: threaded thumbnail loader using `PIL.Image.thumbnail` → `CTkImage`; falls back to text labels on error
  - `ui/source_card.py`: file dialog restricted to image types
  - `ui/hero.py`: headline "Frame your images beautifully"; button "Apply Frames"
  - `ui/banner.py`: banner text updated for PicFrames
- Updated `main.py`: `AppUserModelID` → `"PicFrames.App.1"`, import from `picframes`
- Updated `requirements.txt`: added `Pillow>=10.0.0`, `rembg>=2.0.50`
- Added/replaced `tests/unit/test_processor.py`: 20 deterministic unit tests covering `_to_square`, `_apply_padding`, `_get_mask`, `_apply_mask`, `build_jobs`, and `_process_file` (no network, no rembg called)

## 2026-03-21

- Added `bulk_webp/theme.py`: single source of truth for all brand tokens. Exports semantic colour tuples (`BG`, `SURFACE`, `SURFACE_INSET`, `BANNER_BG`, `BANNER_TEXT`, `ACCENT`, `ACCENT_HOVER`, `ACCENT_MUTED`, `ACCENT_BORDER`, `ACCENT_TEXT`, `TEXT_PRIMARY`, `TEXT_MUTED`, `TEXT_INVERSE`, `TEXT_ON_AMBER`, `BTN_SECONDARY`, `BTN_SECONDARY_HOVER`, `SUCCESS`, `ERROR`, `ERROR_HOVER`, `AMBER`, `AMBER_HOVER`, `AMBER_DARK`, `AMBER_HOVER_DARK`, `PRO_BG`, `PRO_BG_HOVER`), radius constants (`RADIUS_CARD=24`, `RADIUS_INNER=18`, `RADIUS_BTN=14`, `RADIUS_PILL=999`), and a `font(size, weight)` helper wrapping `CTkFont` with family `"Segoe UI"`.
- Migrated all scattered hex colour literals out of 10 UI/dialog files (`app.py`, `ui/banner.py`, `ui/hero.py`, `ui/source_card.py`, `ui/settings_card.py`, `ui/output_card.py`, `ui/progress_card.py`, `ui/preview_strip.py`, `license/activation_dialog.py`) — zero raw hex strings remain in UI code.
- `BANNER_BG` intentionally uses the same dark navy value for both light and dark modes; the banner never inverts.
- Added `docs/branding.md`: full brand reference — colour palette table, typography rationale, token usage examples, and 5-step retheme guide.
- Added `docs/EULA.txt`: 14-section End User License Agreement covering licence grant, restrictions, IP ownership, privacy/data processing, warranty disclaimer (AS-IS, with all faults, all-caps), multi-layer liability limitation with basis-of-bargain clause, indemnification with defence rights, termination, update obligations, binding arbitration, class action waiver, injunctive relief carve-out, 1-year claims limitation, governing law, force majeure, export compliance, severability, and language clause.
- Added `assets/THIRD_PARTY_NOTICES.txt`: full licence texts for Pillow 11.2.1 (HPND), CustomTkinter 5.2.2 (MIT), tkinterdnd2 0.4.3 (MIT), Python (PSF).
- Modified `packaging/installer.iss`: added `#define EULAPath` pointing to `docs\EULA.txt`; added `LicenseFile={#EULAPath}` to `[Setup]` section (mandatory accept screen); added two `[Files]` entries copying `THIRD_PARTY_NOTICES.txt` and `EULA.txt` into `{app}`.

## 2026-03-20

- Updated `README.md` with explicit minimum runtime requirements (Windows 10/11, Python 3.12, pip, Pillow WebP support) and minimum build requirements (plus Inno Setup 6 for installer generation).

- Added `bulk_webp/license/` package: `key_model.py` (LicenseInfo dataclass), `gate.py` (PRO_FEATURES frozenset + can_use()), `validator.py` (LemonSqueezy /licenses/activate + /licenses/validate API calls via stdlib urllib), `activation_dialog.py` (CTkToplevel modal with Buy + Activate buttons), `__init__.py` (public re-exports).
- Added `bulk_webp/settings.py` with JSON-backed persistence; added `license_key` default.
- Modified `bulk_webp/app.py`: deferred `from .app import main` in `__init__.py` to allow test imports without GUI deps; added `_license` field, amber Pro badge, gated resize/preserve_structure checkboxes, `_load_saved_license`, `_apply_license`, `_open_activation_dialog`, `_on_key_activated`.
- Modified `main.py`: added `SetCurrentProcessExplicitAppUserModelID("BulkWebP.App.1")` before app start.
- Replaced `assets/app_icon.png` and `assets/app_icon.ico` with amber geometric W on dark slate (`#0f172a`), all six sizes (16/32/48/64/128/256).
- Removed `cryptography` from `requirements.txt` (Ed25519 offline validator replaced by LemonSqueezy API).
- Fixed `AppPublisher` typo (`pjecuacionn` → `pjecuacion`) and updated `AppURL` to LemonSqueezy store in `packaging/installer.iss`.
- Added `tests/unit/test_license_validator.py` (11 tests, all mocked, no network).
- Added `.env` (gitignored): LEMONSQUEEZY_API_KEY, LEMONSQUEEZY_STORE_ID, LEMONSQUEEZY_PRODUCT_ID, LEMONSQUEEZY_CHECKOUT_URL, BULK_WEBP_LICENSE_PRIVATE_KEY.
- Updated `.gitignore` to exclude `.env`.
- Rebuilt `dist/BulkWebP-Setup.exe` (23.3 MB) from merged main.

## 2026-03-19

- Added requirements.md as the canonical instruction source.
- Added docs/tasks/todo.md as the task planning and review ledger.
- Added docs/tasks/lessons.md as the correction-driven lessons ledger.
- Added .github/copilot-instructions.md to enforce planning, verification, changelog maintenance, and subagent usage expectations.
- Added the bulk_webp package with separated GUI and conversion modules.
- Added unit tests covering discovery, job planning, and conversion output.
- Added PyInstaller and NSIS packaging assets plus a PowerShell build script.
- Added .gitignore entries for the virtual environment and build artifacts.
- Added assets/app_icon.ico and assets/app_icon.png and wired the icon into the runtime window and PyInstaller EXE output.
- Added tkinterdnd2-based drag-and-drop initialization on the root window.
- Extended ConversionOptions with lossless and resize controls and added coverage for save-option and resize behavior.
- Replaced the NSIS installer script with packaging/installer.iss and updated packaging/build.ps1 to locate and invoke Inno Setup Compiler.
- Updated the donation URL constant and installer publisher URL, and added a startup maximize hook in the desktop app.
- Added build_release.ps1 and build_release.bat at the repository root as wrappers around packaging/build.ps1.
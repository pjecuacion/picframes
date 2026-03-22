# Technical Changelog

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
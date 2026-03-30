# Plain Changelog

## [1.1.0] - 2026-03-30
### Added
- AI background removal is now a Pro-only feature. Free tier shows the option as disabled.
- ICO export is now Pro-only. Free tier is locked to PNG output.
- Free tier batch limit: processes a maximum of 10 images per run. Pro is unlimited.
- Updated product page copy to reflect the four Pro features at $14.

## 2026-03-28

- Removed the leftover template `my_app/` folder — the app now runs entirely from `picframes/`.
- Fixed the build pipeline: spec and installer files now correctly reference PicFrames (version 1.0.0, publisher Prince Ecuacion).
- Replaced the placeholder "W" icon with a new amber "P" on dark slate rounded-square icon across all sizes (16 → 256 px).
- Updated the app's donation link to `buymeacoffee.com/pjecuacion`.
- Updated the in-app "Get Pro" button to link to the real PicFrames Pro LemonSqueezy checkout.
- Added rembg, ONNX Runtime, and NumPy to the Third-Party Software Notices.
- Rewrote README for PicFrames: describes frame shapes, AI background removal, ICO output, and Pro licensing.
- Fixed EULA: replaced all "Bulk WebP" references with "PicFrames".
- Added `tools/issue_license.py`: dev tool that creates a \$0 LemonSqueezy checkout pre-filled with a customer email, so free/comped Pro keys can be issued without going through the dashboard.
- Fixed LemonSqueezy integration: product and variant IDs now correctly point to the PicFrames Pro product (not BulkWebP).

## 2026-03-23

- Added ICO output format option: the Settings card now lets you choose between PNG (transparent) and ICO (multi-size Windows icon).
- ICO files embed 6 standard sizes (16, 32, 48, 64, 128, 256 px) in a single file — ready to use as app icons.

## 2026-03-22

- Created PicFrames app: accepts PNG, JPEG, WebP, BMP, and TIFF images.
- Background removal using AI (powered by rembg/U2Net) — toggle on/off per run.
- Frame shapes: Circle and Square (free), Rounded Square with configurable corner radius (Pro).
- Padding slider (0–40 px) adds inset space between subject and frame edge.
- All outputs are transparent-background PNG files — ideal for app icons and stickers.
- Thumbnail preview strip in the UI shows selected images before processing.
- Pro licensing wired in: Rounded Square frame unlocked by PicFrames Pro license key.

## 2026-03-21

- Established a unified visual identity. All colours, type sizes, and corner radii now come from a single brand token file — changing one value updates the whole app.
- Fonts changed to Segoe UI throughout (consistent with Windows 11 and VS Code; never requires installation).
- The top banner stays dark navy in both light and dark mode — it is the identity anchor of the app and never inverts.
- Added comprehensive brand documentation covering the colour palette, typography rationale, and a quick-start guide for theming derivative apps.
- Added a full End User License Agreement shown to users during installation (click-through accept required).
- Added a Third-Party Software Notices file bundled into the install directory, covering Pillow, CustomTkinter, tkinterdnd2, and Python.
- Installer now requires explicit EULA acceptance before installation can proceed.

## 2026-03-20

- Documented minimum runtime and build requirements in the README.

- Added a Pro licensing system: resize and preserve-folder-structure features are gated behind a paid Pro license.
- Integrated LemonSqueezy as the payment platform; product "Bulk WebP Pro" published at $19.
- Added an Activate Pro dialog with a "Buy a Pro license →" button that opens the LemonSqueezy checkout.
- License keys are validated against LemonSqueezy's activation API over HTTPS; no offline secrets embedded in the app.
- Added a license badge in the app banner showing activation status; turns green with the customer email once active.
- Replaced the default Python app icon with a custom amber "W" on dark slate, applied to the window, taskbar, executable, and installer.
- Fixed the Windows taskbar showing the generic Python icon by setting the app's AppUserModelID.
- Updated the installer publisher name (typo fix) and support URL to point to the LemonSqueezy store.
- Rebuilt the release installer (dist/BulkWebP-Setup.exe, 23 MB) from the updated main branch.
- Merged feature/licensing into main.

- Bootstrapped repository operating rules.
- Added canonical requirements documentation.
- Added task tracking and lessons files.
- Added workspace Copilot instructions aligned to repository rules.
- Added a desktop app for converting single images, selected files, and folders to WebP.
- Added a minimalist Windows UI with a Buy Me a Coffee banner.
- Added tests and a Windows packaging workflow for executable and installer generation.
- Added a custom app icon for the window and packaged executable.
- Added drag-and-drop support for files and folders.
- Added lossless WebP export and resize controls.
- Switched the Windows installer workflow from NSIS to Inno Setup using an `.iss` script.
- Updated the donation link and changed the app to open maximized on startup.
- Added root-level build scripts so packaging can be run from the repository root.
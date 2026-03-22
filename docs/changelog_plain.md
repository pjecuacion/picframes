# Plain Changelog

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
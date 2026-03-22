# Bulk WebP

Bulk WebP is a Windows-friendly Python desktop app for converting single images, multiple selected files, or whole folders into WebP.

## Minimum Requirements

- Windows 10 or Windows 11
- Python 3.12 when running from source
- `pip` with the ability to install packages from `requirements.txt`
- A standard Windows Pillow wheel with WebP support

## Minimum Build Requirements

- Windows 10 or Windows 11
- Python 3.12
- `pip install -r requirements.txt`
- Inno Setup 6 if you want to generate `dist/BulkWebP-Setup.exe`

## Features

- Clean desktop UI with a minimalist layout.
- Single-file and multi-file conversion.
- Bulk folder conversion with optional recursive scanning.
- Drag-and-drop support for files and folders.
- Optional folder structure preservation in the output.
- Optional lossless WebP output.
- Optional resize-to-fit width and height controls.
- Clickable Buy Me a Coffee banner at the top of the app.
- Packaging workflow for a standalone Windows executable and installer.
- Dedicated app icon wired into the app window and Windows packaging.

## Run Locally

1. Create or activate a Python 3.12 virtual environment.
2. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

3. Start the app:

   ```powershell
   python main.py
   ```

## Run Tests

```powershell
python -m unittest discover -s tests
```

## Build Windows Distribution

1. Install Inno Setup 6 and ensure `ISCC.exe` is on your `PATH`, or install it in the default Inno Setup location.
2. Run either of these from the repository root:

   ```powershell
   ./build_release.ps1
   ```

   ```bat
   build_release.bat
   ```

3. Outputs:
- `dist/BulkWebP/BulkWebP.exe`
- `dist/BulkWebP-Setup.exe`

If Inno Setup is not installed yet, the PyInstaller build still produces `dist/BulkWebP/` and `dist/BulkWebP.exe`, which can be shared directly as a portable build until the installer is generated.

## Notes

- The app defaults output into a sibling folder if you do not choose one explicitly.
- Pillow must be built with WebP support, which is included in standard wheels on Windows.
- The installer step depends on `ISCC.exe` from Inno Setup being available on the build machine.
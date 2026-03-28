# PicFrames

PicFrames is a Windows desktop app for framing images with circle, square, or rounded-square masks — with optional AI-powered background removal. It processes single files, multi-file selections, or whole folders in bulk, always outputting transparent PNGs.

## Minimum Requirements

- Windows 10 or Windows 11
- Python 3.12+ when running from source
- `pip` with the ability to install packages from `requirements.txt`

## Minimum Build Requirements

- Windows 10 or Windows 11
- Python 3.12+
- `pip install -r requirements.txt`
- Inno Setup 6 if you want to generate `dist/PicFrames-Setup.exe`

## Features

- Circle, square, and rounded-square frame shapes.
- Adjustable padding and corner radius (rounded square is Pro-only).
- AI-powered background removal via `rembg` (toggle on/off).
- Drag-and-drop support for files and folders.
- Bulk folder processing.
- Output always saved as transparent PNG.
- Optional ICO output for generating app icons.
- Light/dark mode toggle.
- Pro license activation via LemonSqueezy.
- Packaging workflow for a standalone Windows executable and installer.

## Run Locally

1. Create a virtual environment and activate it:

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

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
   - `dist/PicFrames/PicFrames.exe` (portable)
   - `dist/PicFrames-Setup.exe` (installer)

If Inno Setup is not installed, the PyInstaller build still produces `dist/PicFrames/` which can be shared directly as a portable build.

## Notes

- Background removal uses `rembg` with a 176 MB ONNX model downloaded on first use.
- Output is always a 32-bit RGBA PNG regardless of input format.
- Settings (last-used folder, theme preference) persist in `~/.picframes/settings.json`.
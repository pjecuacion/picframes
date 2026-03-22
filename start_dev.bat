@echo off
echo [DEV] PicFrames starting with Pro mode enabled (PICFRAMES_DEV_PRO=1)
set PICFRAMES_DEV_PRO=1
if exist "%~dp0.venv\Scripts\activate.bat" (
    call "%~dp0.venv\Scripts\activate.bat"
)
python "%~dp0main.py"

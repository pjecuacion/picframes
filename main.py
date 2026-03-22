import ctypes
import multiprocessing
import sys

# Tell Windows this is a distinct app so the taskbar shows our icon,
# not the generic python.exe icon.
if __name__ == "__main__":
    if sys.platform == "win32":
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("PicFrames.App.1")
    multiprocessing.freeze_support()  # required for PyInstaller + ProcessPoolExecutor
    from picframes import main
    main()
import ctypes
import multiprocessing
import sys

# Tell Windows this is a distinct app so the taskbar shows our icon,
# not the generic python.exe icon.
# TODO: rename to match your app, e.g. "BulkResize.App.1"
if sys.platform == "win32":
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("MyApp.App.1")

from my_app import main

if __name__ == "__main__":
    multiprocessing.freeze_support()  # required for PyInstaller + ProcessPoolExecutor
    main()
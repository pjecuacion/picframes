import ctypes
import logging
import multiprocessing
import os
import sys
import tempfile
import traceback

# Bootstrap logging immediately — before any other import — so crashes in
# frozen/installed builds are always written to disk.
_LOG_PATH = os.path.join(tempfile.gettempdir(), "picframes_debug.log")
logging.basicConfig(
    filename=_LOG_PATH,
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    force=True,
)
_log = logging.getLogger("picframes")
_log.info("===== PicFrames starting. frozen=%s log=%s =====", getattr(sys, 'frozen', False), _LOG_PATH)

if __name__ == "__main__":
    try:
        if sys.platform == "win32":
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("PicFrames.App.1")
        multiprocessing.freeze_support()  # required for PyInstaller + ProcessPoolExecutor
        from picframes import main
        main()
    except Exception:
        _log.critical("Unhandled top-level exception:\n%s", traceback.format_exc())
        raise
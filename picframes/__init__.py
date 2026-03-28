__version__ = "1.0.0"


def main():
    # Logging is already bootstrapped in main.py before this is called.
    from .app import main as _main
    _main()

__all__ = ["main", "__version__"]

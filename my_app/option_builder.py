from __future__ import annotations

from pathlib import Path

from .processor import ProcessingOptions, discover_files


def build_options(settings_card) -> ProcessingOptions:
    """Build ProcessingOptions from a SettingsCard instance.

    TODO: read your app-specific settings from settings_card and populate ProcessingOptions.
    """
    return ProcessingOptions(
        overwrite=bool(settings_card.overwrite_checkbox.get()),
    )


def default_output_dir(mode: str, files: list[Path], folder: Path | None) -> Path | None:
    """Derive the default output directory from the current source selection.

    TODO: update the output folder naming convention to match your app.
    """
    if mode == "files" and files:
        return files[0].parent / "my_app_output"  # TODO: rename
    if mode == "folder" and folder:
        return folder.parent / f"{folder.name}_output"  # TODO: rename
    return None


def resolve_sources(
    mode: str,
    files: list[Path],
    folder: Path | None,
    recursive: bool,
) -> tuple[list[Path], Path | None]:
    """Return (file_paths, source_root) based on current mode and selection."""
    if mode == "files":
        return list(files), None
    if folder is None:
        return [], None
    return discover_files(folder, recursive=recursive), folder

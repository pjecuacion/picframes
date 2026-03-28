from __future__ import annotations

from pathlib import Path

from .processor import ProcessingOptions, discover_files


def build_options(settings_card) -> ProcessingOptions:
    """Build ProcessingOptions from a SettingsCard instance."""
    return ProcessingOptions(
        frame_shape=settings_card.get_frame_shape(),
        corner_radius_pct=int(settings_card.radius_slider.get()),
        padding=int(settings_card.padding_slider.get()),
        remove_bg=bool(settings_card.remove_bg_checkbox.get()),
        output_format=settings_card.get_output_format(),
        overwrite=bool(settings_card.overwrite_checkbox.get()),
        fit_to_frame=settings_card.get_fit_to_frame(),
    )


def default_output_dir(mode: str, files: list[Path], folder: Path | None) -> Path | None:
    """Derive the default output directory from the current source selection."""
    if mode == "files" and files:
        return files[0].parent / "picframes_output"
    if mode == "folder" and folder:
        return folder.parent / f"{folder.name}_picframes"
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

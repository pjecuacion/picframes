from __future__ import annotations

from pathlib import Path
from typing import Callable

import customtkinter as ctk

from .. import theme

_IMAGE_TYPES = [
    ("Image files", "*.png *.jpg *.jpeg *.webp *.bmp *.tiff *.tif"),
    ("PNG", "*.png"),
    ("JPEG", "*.jpg *.jpeg"),
    ("WebP", "*.webp"),
    ("All files", "*.*"),
]


class SourceCard(ctk.CTkFrame):
    """Source panel: mode toggle (files / folder), selection summary, pick button, drop zone."""

    def __init__(
        self,
        parent,
        mode_var: ctk.StringVar,
        on_mode_change: Callable[[str], None],
        on_choose_source: Callable[[], None],
    ) -> None:
        super().__init__(parent, fg_color=theme.SURFACE, corner_radius=theme.RADIUS_CARD)
        self.grid_columnconfigure(0, weight=1)
        self._build(mode_var, on_mode_change, on_choose_source)

    def _build(self, mode_var, on_mode_change, on_choose_source) -> None:
        ctk.CTkLabel(
            self, text="Source", font=theme.font(19, "bold"), text_color=theme.TEXT_PRIMARY,
        ).grid(row=0, column=0, padx=22, pady=(22, 8), sticky="w")

        ctk.CTkSegmentedButton(
            self,
            values=["files", "folder"],
            variable=mode_var,
            command=on_mode_change,
            selected_color=("#16212D", theme.ACCENT),
            unselected_color=("#64748b", "#334155"),
            selected_hover_color=("#2B3540", theme.ACCENT_HOVER),
            unselected_hover_color=("#475569", "#475569"),
            text_color=(theme.TEXT_INVERSE, theme.TEXT_INVERSE),
        ).grid(row=1, column=0, padx=22, pady=(0, 18), sticky="w")

        self.source_summary = ctk.CTkLabel(
            self,
            text="No images selected yet.",
            justify="left",
            anchor="w",
            text_color=theme.TEXT_MUTED,
            font=theme.font(14),
        )
        self.source_summary.grid(row=2, column=0, padx=22, pady=(0, 16), sticky="ew")

        self.pick_button = ctk.CTkButton(
            self,
            text="Select Images",
            command=on_choose_source,
            fg_color=theme.ACCENT,
            hover_color=theme.ACCENT_HOVER,
            text_color=theme.TEXT_INVERSE,
            corner_radius=theme.RADIUS_BTN,
            height=42,
        )
        self.pick_button.grid(row=3, column=0, padx=22, pady=(0, 22), sticky="w")

        drop_zone = ctk.CTkFrame(
            self, fg_color=theme.ACCENT_MUTED, corner_radius=theme.RADIUS_INNER,
            border_width=1, border_color=theme.ACCENT_BORDER,
        )
        drop_zone.grid(row=4, column=0, padx=22, pady=(0, 22), sticky="ew")
        drop_zone.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            drop_zone, text="Drag images or a folder here",
            text_color=theme.ACCENT_TEXT, font=theme.font(14, "bold"),
        ).grid(row=0, column=0, padx=16, pady=(14, 4))

        ctk.CTkLabel(
            drop_zone,
            text="Supports PNG, JPEG, WebP, BMP, TIFF · Drop a folder for bulk processing.",
            text_color=theme.TEXT_MUTED, font=theme.font(12),
        ).grid(row=1, column=0, padx=16, pady=(0, 14))

    def pick(self, mode: str) -> tuple[list[Path], Path | None]:
        from tkinter import filedialog
        if mode == "files":
            paths = filedialog.askopenfilenames(title="Choose image files", filetypes=_IMAGE_TYPES)
            return [Path(p) for p in paths], None
        folder = filedialog.askdirectory(title="Choose a folder to process")
        return [], Path(folder) if folder else None

    def sync(self, mode: str, files: list[Path], folder: Path | None) -> None:
        if mode == "files":
            self.pick_button.configure(text="Select Images")
            count = len(files)
            if count == 0:
                self.source_summary.configure(text="No images selected yet.")
            else:
                preview = "\n".join(p.name for p in files[:3])
                suffix = "" if count <= 3 else f"\n...and {count - 3} more"
                self.source_summary.configure(text=f"{count} image(s) selected\n{preview}{suffix}")
        else:
            self.pick_button.configure(text="Select Folder")
            self.source_summary.configure(text=str(folder) if folder else "No folder selected yet.")

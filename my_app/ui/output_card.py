from __future__ import annotations

from pathlib import Path
from typing import Callable

import customtkinter as ctk

from .. import theme


class OutputCard(ctk.CTkFrame):
    """Output panel: folder selector and open-folder button."""

    def __init__(
        self,
        parent,
        on_choose_output: Callable[[], None],
        on_open_output: Callable[[], None],
    ) -> None:
        super().__init__(parent, fg_color=theme.SURFACE, corner_radius=theme.RADIUS_CARD)
        self.grid_columnconfigure(0, weight=1)
        self._build(on_choose_output, on_open_output)

    def _build(self, on_choose_output: Callable, on_open_output: Callable) -> None:
        ctk.CTkLabel(
            self,
            text="Output",
            font=theme.font(19, "bold"),
            text_color=theme.TEXT_PRIMARY,
        ).grid(row=0, column=0, padx=22, pady=(22, 8), sticky="w")

        self.output_summary = ctk.CTkLabel(
            self,
            text="Output folder will default next to your source selection.",
            justify="left",
            anchor="w",
            text_color=theme.TEXT_MUTED,
        )
        self.output_summary.grid(row=1, column=0, padx=22, pady=(0, 16), sticky="ew")

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=2, column=0, padx=22, pady=(0, 22), sticky="w")

        ctk.CTkButton(
            btn_frame,
            text="Choose Output Folder",
            command=on_choose_output,
            fg_color=theme.ACCENT,
            hover_color=theme.ACCENT_HOVER,
            text_color=theme.TEXT_INVERSE,
            corner_radius=theme.RADIUS_BTN,
        ).grid(row=0, column=0, padx=(0, 10))

        ctk.CTkButton(
            btn_frame,
            text="Open Output Folder",
            command=on_open_output,
            fg_color=theme.BTN_SECONDARY,
            hover_color=theme.BTN_SECONDARY_HOVER,
            text_color=theme.TEXT_PRIMARY,
            corner_radius=theme.RADIUS_BTN,
        ).grid(row=0, column=1)

    def pick(self) -> Path | None:
        """Open a folder chooser dialog and return the selected path or None."""
        from tkinter import filedialog
        folder = filedialog.askdirectory(title="Choose an output folder")
        return Path(folder) if folder else None

    def sync(self, output_dir: Path | None, default_dir: Path | None) -> None:
        """Update the summary label to reflect current output folder state."""
        if output_dir is not None:
            self.output_summary.configure(text=str(output_dir))
        elif default_dir is not None:
            self.output_summary.configure(text=f"Default output: {default_dir}")
        else:
            self.output_summary.configure(
                text="Output folder will default next to your source selection."
            )

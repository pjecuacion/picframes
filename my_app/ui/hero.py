from __future__ import annotations

from typing import Callable

import customtkinter as ctk

from .. import theme


class HeroSection(ctk.CTkFrame):
    """Top banner with headline and primary action button."""

    def __init__(self, parent, on_run: Callable[[], None]) -> None:
        super().__init__(parent, fg_color=theme.SURFACE, corner_radius=theme.RADIUS_CARD)
        self.grid_columnconfigure(0, weight=1)
        self._build(on_run)

    def _build(self, on_run: Callable[[], None]) -> None:
        self._on_run = on_run

        ctk.CTkLabel(
            self,
            text="Process your files without the noise",  # TODO: write your headline
            font=theme.font(30, "bold"),
            text_color=theme.TEXT_PRIMARY,
        ).grid(row=0, column=0, padx=24, pady=(24, 8), sticky="w")

        ctk.CTkLabel(
            self,
            # TODO: write a one-line description of what your app does
            text="Choose files or a folder, configure your settings, and process in one pass.",
            font=theme.font(15),
            text_color=theme.TEXT_MUTED,
        ).grid(row=1, column=0, padx=24, pady=(0, 24), sticky="w")

        self.run_button = ctk.CTkButton(
            self,
            text="Run",  # TODO: replace with your action verb e.g. "Convert", "Export", "Compress"
            command=on_run,
            fg_color=theme.ACCENT,
            hover_color=theme.ACCENT_HOVER,
            text_color=theme.TEXT_INVERSE,
            corner_radius=theme.RADIUS_BTN,
            height=48,
            width=172,
        )
        self.run_button.grid(row=0, column=1, rowspan=2, padx=(16, 24), pady=24, sticky="e")

    def set_running(self, is_running: bool, on_cancel: "Callable[[], None] | None" = None) -> None:
        if is_running:
            self.run_button.configure(
                text="Cancel",
                command=on_cancel,
                fg_color=theme.ERROR,
                hover_color=theme.ERROR_HOVER,
                text_color=theme.TEXT_INVERSE,
                state="normal",
            )
        else:
            self.run_button.configure(
                text="Run",  # TODO: match the primary button label above
                command=self._on_run,
                fg_color=theme.ACCENT,
                hover_color=theme.ACCENT_HOVER,
                text_color=theme.TEXT_INVERSE,
                state="normal",
            )

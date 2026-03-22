from __future__ import annotations

from pathlib import Path

import customtkinter as ctk

from .. import theme

MAX_PREVIEWS = 24


class PreviewStrip(ctk.CTkFrame):
    """Horizontal scrollable strip showing the names of selected files.

    Call update(paths) whenever the source selection changes.

    TODO: If your app processes image or video files, you can enhance this
    into a thumbnail strip. Replace _render() with a threaded loader that
    opens each file and builds a ctk.CTkImage, then grids image labels here.
    """

    def __init__(self, parent, **kwargs) -> None:
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self._file_labels: list[ctk.CTkLabel] = []
        self._build()
        self.grid_remove()  # hidden until a source is selected

    def _build(self) -> None:
        self._scroll = ctk.CTkScrollableFrame(
            self,
            orientation="horizontal",
            height=56,
            fg_color=theme.SURFACE_INSET,
            corner_radius=theme.RADIUS_INNER,
        )
        self._scroll.grid(row=0, column=0, sticky="ew")

        self._placeholder = ctk.CTkLabel(
            self._scroll,
            text="Select files or a folder to see a preview.",
            text_color=theme.TEXT_MUTED,
            font=theme.font(13),
        )
        self._placeholder.grid(row=0, column=0, padx=16, pady=8)

    def update(self, paths: list[Path]) -> None:
        """Refresh the file strip for the given paths."""
        self._clear()
        if not paths:
            self.grid_remove()
            return

        self.grid()
        preview = paths[:MAX_PREVIEWS]
        has_more = len(paths) > MAX_PREVIEWS
        self._render(preview, has_more, len(paths))

    def _render(self, preview: list[Path], has_more: bool, total: int) -> None:
        for i, p in enumerate(preview):
            lbl = ctk.CTkLabel(
                self._scroll,
                text=p.name,
                fg_color=theme.SURFACE,
                corner_radius=theme.RADIUS_BTN,
                text_color=theme.TEXT_MUTED,
                font=theme.font(12),
                padx=10,
                pady=6,
                anchor="w",
            )
            lbl.grid(row=0, column=i, padx=(8, 0), pady=8)
            self._file_labels.append(lbl)

        if has_more:
            more_lbl = ctk.CTkLabel(
                self._scroll,
                text=f"+{total - MAX_PREVIEWS} more",
                text_color=theme.TEXT_MUTED,
                font=theme.font(12),
            )
            more_lbl.grid(row=0, column=len(preview), padx=(8, 16), pady=8)
            self._file_labels.append(more_lbl)

    def _clear(self) -> None:
        for lbl in self._file_labels:
            lbl.destroy()
        self._file_labels.clear()

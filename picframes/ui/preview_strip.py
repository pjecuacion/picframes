from __future__ import annotations

import threading
from pathlib import Path

import customtkinter as ctk

from .. import theme

MAX_PREVIEWS = 20
_THUMB_SIZE = 52


class PreviewStrip(ctk.CTkFrame):
    """Horizontal scrollable thumbnail strip showing selected image files.

    Thumbnails are loaded in a background thread to keep the UI responsive.
    """

    def __init__(self, parent, **kwargs) -> None:
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self._widgets: list = []
        self._build()
        self.grid_remove()

    def _build(self) -> None:
        self._scroll = ctk.CTkScrollableFrame(
            self,
            orientation="horizontal",
            height=_THUMB_SIZE + 20,
            fg_color=theme.SURFACE_INSET,
            corner_radius=theme.RADIUS_INNER,
        )
        self._scroll.grid(row=0, column=0, sticky="ew")

    def update(self, paths: list[Path]) -> None:
        self._clear()
        if not paths:
            self.grid_remove()
            return
        self.grid()
        preview = paths[:MAX_PREVIEWS]
        has_more = len(paths) > MAX_PREVIEWS
        threading.Thread(
            target=self._load_thumbnails,
            args=(preview, has_more, len(paths)),
            daemon=True,
        ).start()

    def _load_thumbnails(self, paths: list[Path], has_more: bool, total: int) -> None:
        try:
            from PIL import Image
        except ImportError:
            for i, p in enumerate(paths):
                self.after(0, lambda idx=i, path=p: self._add_text_label(idx, path))
            return

        for i, p in enumerate(paths):
            try:
                img = Image.open(p)
                img.thumbnail((_THUMB_SIZE, _THUMB_SIZE))
                ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(_THUMB_SIZE, _THUMB_SIZE))
                self.after(0, lambda img=ctk_img, idx=i, path=p: self._add_thumb(img, idx, path))
            except Exception:
                self.after(0, lambda idx=i, path=p: self._add_text_label(idx, path))

        if has_more:
            self.after(0, lambda: self._add_more_label(total))

    def _add_thumb(self, ctk_img, col: int, path: Path) -> None:
        lbl = ctk.CTkLabel(
            self._scroll, image=ctk_img, text=path.name,
            compound="top", text_color=theme.TEXT_MUTED,
            font=theme.font(10), width=_THUMB_SIZE,
        )
        lbl.grid(row=0, column=col, padx=(8, 0), pady=4)
        self._widgets.append(lbl)

    def _add_text_label(self, col: int, path: Path) -> None:
        lbl = ctk.CTkLabel(
            self._scroll, text=path.name,
            fg_color=theme.SURFACE, corner_radius=theme.RADIUS_BTN,
            text_color=theme.TEXT_MUTED, font=theme.font(12), padx=10, pady=6,
        )
        lbl.grid(row=0, column=col, padx=(8, 0), pady=8)
        self._widgets.append(lbl)

    def _add_more_label(self, total: int) -> None:
        shown = min(total, MAX_PREVIEWS)
        lbl = ctk.CTkLabel(
            self._scroll,
            text=f"+{total - shown} more",
            text_color=theme.TEXT_MUTED,
            font=theme.font(12),
        )
        lbl.grid(row=0, column=shown, padx=(8, 16), pady=8)
        self._widgets.append(lbl)

    def _clear(self) -> None:
        for w in self._widgets:
            w.destroy()
        self._widgets.clear()

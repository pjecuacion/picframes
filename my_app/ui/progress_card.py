from __future__ import annotations

from typing import Callable

import customtkinter as ctk

from .. import theme


class ProgressCard(ctk.CTkFrame):
    """Progress panel: progress bar and status label."""

    def __init__(self, parent, on_run: Callable[[], None]) -> None:
        super().__init__(parent, fg_color=theme.SURFACE, corner_radius=theme.RADIUS_CARD)
        self.grid_columnconfigure(0, weight=1)
        self._build(on_run)

    def _build(self, on_run: Callable[[], None]) -> None:
        ctk.CTkLabel(
            self,
            text="Progress",
            font=theme.font(19, "bold"),
            text_color=theme.TEXT_PRIMARY,
        ).grid(row=0, column=0, padx=22, pady=(22, 10), sticky="w")

        self.progress_bar = ctk.CTkProgressBar(self, progress_color=theme.ACCENT)
        self.progress_bar.grid(row=1, column=0, padx=22, sticky="ew")
        self.progress_bar.set(0)

        self.status_label = ctk.CTkLabel(self, text="Ready.", text_color=theme.TEXT_MUTED)
        self.status_label.grid(row=2, column=0, padx=22, pady=(10, 22), sticky="w")

    def begin(self, count: int) -> None:
        self.progress_bar.set(0)
        self.status_label.configure(text=f"Preparing {count} job(s)...")

    def update_progress(self, index: int, total: int) -> None:
        self.progress_bar.set(index / total)
        self.status_label.configure(text=f"Processed {index} of {total}")

    def show_finish(self, results, cancelled: bool = False) -> tuple[int, int]:
        """Display finish summary. Returns (processed_count, failed_count)."""
        processed = sum(1 for r in results if r.status == "processed")
        skipped = sum(1 for r in results if r.status == "skipped")
        failed = sum(1 for r in results if r.status == "failed")
        prefix = "Cancelled —" if cancelled else "Finished:"
        self.status_label.configure(
            text=f"{prefix} {processed} processed, {skipped} skipped, {failed} failed."
        )
        return processed, failed

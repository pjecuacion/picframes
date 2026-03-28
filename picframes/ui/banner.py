from __future__ import annotations

import webbrowser
from typing import Callable

import customtkinter as ctk

from .. import theme
from ..license.key_model import LicenseInfo

_DONATION_URL = "https://buymeacoffee.com/pjecuacion"


class BannerFrame(ctk.CTkFrame):
    """Top application bar: donate button, dark-mode toggle, license badge.

    Intentionally inverse of the app theme — dark banner in light mode, light in dark mode.
    """

    def __init__(
        self,
        parent,
        on_toggle_appearance: Callable[[], None],
        on_open_activation: Callable[[], None],
        appearance_mode: str = "system",
    ) -> None:
        super().__init__(parent, fg_color=theme.BANNER_BG, corner_radius=0, height=56)
        self.grid_columnconfigure(0, weight=1)
        self._on_activate = on_open_activation
        self._build(on_toggle_appearance, appearance_mode)

    def _build(self, on_toggle: Callable[[], None], appearance_mode: str) -> None:
        ctk.CTkLabel(
            self,
            text="Enjoying PicFrames? Support future updates.",
            text_color=theme.BANNER_TEXT,
            font=theme.font(15, "bold"),
        ).grid(row=0, column=0, padx=(24, 12), pady=14, sticky="w")

        ctk.CTkButton(
            self,
            text="☕ Buy Me a Coffee",
            command=lambda: webbrowser.open(_DONATION_URL),
            fg_color=theme.AMBER,
            hover_color=theme.AMBER_HOVER,
            text_color=theme.TEXT_ON_AMBER,
            width=170,
            corner_radius=theme.RADIUS_PILL,
        ).grid(row=0, column=1, padx=(0, 16), pady=12, sticky="e")

        self.dark_switch = ctk.CTkSwitch(
            self,
            text="Dark",
            text_color=theme.BANNER_TEXT,
            command=on_toggle,
            button_color=theme.AMBER,
            button_hover_color=theme.AMBER_HOVER,
            progress_color=("#374151", "#cbd5e1"),
        )
        self.dark_switch.grid(row=0, column=2, padx=(0, 8), pady=14, sticky="e")
        if appearance_mode == "dark" or ctk.get_appearance_mode() == "Dark":
            self.dark_switch.select()

        self.license_badge = ctk.CTkButton(
            self,
            text="⚡ Personal · Activate Pro →",
            command=self._on_activate,
            fg_color=(theme.AMBER, theme.AMBER_DARK),
            hover_color=(theme.AMBER_HOVER, theme.AMBER_HOVER_DARK),
            text_color=theme.TEXT_ON_AMBER,
            width=190,
            corner_radius=theme.RADIUS_PILL,
        )
        self.license_badge.grid(row=0, column=3, padx=(0, 24), pady=12, sticky="e")

    def update_license(self, info: LicenseInfo | None) -> None:
        """Reflect Pro or Personal state in the badge."""
        if info is not None and info.is_pro:
            self.license_badge.configure(
                text=f"🔥 Pro ✓  {info.email}",
                fg_color=theme.PRO_BG,
                hover_color=theme.PRO_BG_HOVER,
                text_color=theme.TEXT_INVERSE,
                width=260,
            )
        else:
            self.license_badge.configure(
                text="⚡ Personal · Activate Pro →",
                fg_color=(theme.AMBER, theme.AMBER_DARK),
                hover_color=(theme.AMBER_HOVER, theme.AMBER_HOVER_DARK),
                text_color=theme.TEXT_ON_AMBER,
                width=190,
            )

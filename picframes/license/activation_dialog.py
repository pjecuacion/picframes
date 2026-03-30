from __future__ import annotations

import os
import webbrowser
from typing import Callable

import customtkinter as ctk

from .. import theme
from .key_model import LicenseInfo

_CHECKOUT_URL = os.environ.get(
    "LEMONSQUEEZY_CHECKOUT_URL",
    "https://pjecuacion.lemonsqueezy.com/checkout/buy/23a0f5a9-4f13-445d-baac-71b0052d5e71",
)


class ActivationDialog(ctk.CTkToplevel):
    """Modal dialog for entering and validating a Pro license key."""

    def __init__(
        self,
        parent,
        on_activated: Callable[[str, LicenseInfo], None],
        current_key: str = "",
    ) -> None:
        super().__init__(parent)
        self._on_activated = on_activated
        self.title("Activate PicFrames Pro")
        self.geometry("540x280")
        self.resizable(False, False)
        self.grab_set()
        self._build_ui(current_key)

    def _build_ui(self, current_key: str) -> None:
        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self, text="Enter your license key",
            font=theme.font(18, "bold"), text_color=theme.TEXT_PRIMARY,
        ).grid(row=0, column=0, padx=28, pady=(28, 6), sticky="w")

        ctk.CTkLabel(
            self,
            text="Purchase Pro to unlock Rounded Square frames with custom corner radius.",
            text_color=theme.TEXT_MUTED, font=theme.font(13),
        ).grid(row=1, column=0, padx=28, pady=(0, 14), sticky="w")

        ctk.CTkButton(
            self, text="⚡ Buy PicFrames Pro →",
            command=lambda: webbrowser.open(_CHECKOUT_URL),
            fg_color=theme.AMBER, hover_color=theme.AMBER_HOVER,
            text_color=theme.TEXT_ON_AMBER, width=210, height=32,
            font=theme.font(13, "bold"),
        ).grid(row=2, column=0, padx=28, pady=(0, 14), sticky="w")

        self._key_entry = ctk.CTkEntry(
            self, placeholder_text="Paste your license key here",
            width=480, font=ctk.CTkFont(family="Courier New", size=12),
        )
        if current_key:
            self._key_entry.insert(0, current_key)
        self._key_entry.grid(row=3, column=0, padx=28, pady=(0, 8), sticky="ew")

        self._status_label = ctk.CTkLabel(
            self, text="", text_color=theme.ERROR, font=theme.font(13),
        )
        self._status_label.grid(row=4, column=0, padx=28, sticky="w")

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=5, column=0, padx=28, pady=(8, 24), sticky="e")

        ctk.CTkButton(
            btn_frame, text="Cancel", command=self.destroy,
            fg_color=theme.BTN_SECONDARY, hover_color=theme.BTN_SECONDARY_HOVER,
            text_color=theme.TEXT_PRIMARY, width=90,
        ).grid(row=0, column=0, padx=(0, 10))

        ctk.CTkButton(
            btn_frame, text="Activate", command=self._activate,
            fg_color=theme.ACCENT, hover_color=theme.ACCENT_HOVER,
            text_color=theme.TEXT_INVERSE, width=110,
        ).grid(row=0, column=1)

    def _activate(self) -> None:
        key = self._key_entry.get().strip()
        if not key:
            self._status_label.configure(text="Please enter a license key.")
            return
        from .validator import validate_key
        info = validate_key(key)
        if info is None:
            self._status_label.configure(text="Invalid license key. Please check and try again.")
            return
        if not info.is_pro:
            self._status_label.configure(text="This key is not a valid active Pro license.")
            return
        self._on_activated(key, info)
        self.destroy()

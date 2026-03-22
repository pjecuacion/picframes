from __future__ import annotations

import customtkinter as ctk

from .. import theme


class SettingsCard(ctk.CTkFrame):
    """Settings panel: processing options.

    Replace the placeholder controls with your app-specific settings.
    Keep apply_license_state() — it wires the Pro-gating pattern the template provides.
    """

    def __init__(self, parent) -> None:
        super().__init__(parent, fg_color=theme.SURFACE, corner_radius=theme.RADIUS_CARD)
        self.grid_columnconfigure(0, weight=1)
        self._build()

    def _build(self) -> None:
        ctk.CTkLabel(
            self,
            text="Settings",
            font=theme.font(19, "bold"),
            text_color=theme.TEXT_PRIMARY,
        ).grid(row=0, column=0, padx=22, pady=(22, 14), sticky="w")

        # TODO: Replace with your app's primary numeric setting (quality, level, threshold, …)
        self.quality_label = ctk.CTkLabel(self, text="Setting A: 80", text_color=theme.TEXT_PRIMARY)
        self.quality_label.grid(row=1, column=0, padx=22, sticky="w")

        self.quality_slider = ctk.CTkSlider(
            self, from_=0, to=100, number_of_steps=100, command=self._on_slider_change
        )
        self.quality_slider.set(80)
        self.quality_slider.grid(row=2, column=0, padx=22, pady=(8, 16), sticky="ew")

        # TODO: Replace with a meaningful boolean option for your app
        self.option_checkbox = ctk.CTkCheckBox(self, text="Enable option B")
        self.option_checkbox.grid(row=3, column=0, padx=22, pady=(0, 10), sticky="w")

        # Pro-gated section — keep this pattern; rename the feature label and entry
        pro_frame = ctk.CTkFrame(self, fg_color=theme.SURFACE_INSET, corner_radius=theme.RADIUS_INNER)
        pro_frame.grid(row=4, column=0, padx=22, pady=(0, 14), sticky="ew")
        pro_frame.grid_columnconfigure(0, weight=1)

        self.pro_checkbox = ctk.CTkCheckBox(
            pro_frame,
            text="Enable Pro feature  (Pro)",  # TODO: rename
            command=self._sync_pro_state,
        )
        self.pro_checkbox.grid(row=0, column=0, padx=14, pady=(14, 10), sticky="w")

        self.pro_entry = ctk.CTkEntry(pro_frame, placeholder_text="Pro option value")  # TODO: rename
        self.pro_entry.grid(row=1, column=0, padx=14, pady=(0, 14), sticky="ew")

        self.recursive_checkbox = ctk.CTkCheckBox(self, text="Scan subfolders when using folder mode")
        self.recursive_checkbox.select()
        self.recursive_checkbox.grid(row=5, column=0, padx=22, pady=6, sticky="w")

        self.overwrite_checkbox = ctk.CTkCheckBox(self, text="Overwrite existing output files")
        self.overwrite_checkbox.select()
        self.overwrite_checkbox.grid(row=6, column=0, padx=22, pady=(6, 18), sticky="w")

        self._sync_pro_state()

    def _on_slider_change(self, value: float) -> None:
        self.quality_label.configure(text=f"Setting A: {int(value)}")

    def _sync_pro_state(self) -> None:
        state = "normal" if bool(self.pro_checkbox.get()) else "disabled"
        self.pro_entry.configure(state=state)

    def apply_license_state(self, is_pro: bool) -> None:
        """Enable or disable Pro-gated controls based on license tier."""
        if is_pro:
            self.pro_checkbox.configure(state="normal", text="Enable Pro feature")  # TODO: rename
        else:
            self.pro_checkbox.deselect()
            self.pro_checkbox.configure(state="disabled", text="Enable Pro feature  (Pro)")  # TODO: rename
        self._sync_pro_state()

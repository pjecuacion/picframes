from __future__ import annotations

import customtkinter as ctk

from .. import theme


class SettingsCard(ctk.CTkFrame):
    """Settings panel: frame shape, padding, background removal, and Pro options."""

    def __init__(self, parent) -> None:
        super().__init__(parent, fg_color=theme.SURFACE, corner_radius=theme.RADIUS_CARD)
        self.grid_columnconfigure(0, weight=1)
        self._build()

    def _build(self) -> None:
        ctk.CTkLabel(
            self, text="Settings", font=theme.font(19, "bold"), text_color=theme.TEXT_PRIMARY,
        ).grid(row=0, column=0, padx=22, pady=(22, 14), sticky="w")

        # Output format selector
        ctk.CTkLabel(
            self, text="Output Format", font=theme.font(14, "bold"), text_color=theme.TEXT_PRIMARY,
        ).grid(row=1, column=0, padx=22, pady=(0, 6), sticky="w")

        self._output_format_var = ctk.StringVar(value="PNG")
        self._output_format_btn = ctk.CTkSegmentedButton(
            self,
            values=["PNG", "ICO  (Pro)"],
            variable=self._output_format_var,
        )
        self._output_format_btn.grid(row=2, column=0, padx=22, pady=(0, 18), sticky="w")

        # Frame shape selector (free: Circle, Square)
        ctk.CTkLabel(
            self, text="Frame Shape", font=theme.font(14, "bold"), text_color=theme.TEXT_PRIMARY,
        ).grid(row=3, column=0, padx=22, pady=(0, 6), sticky="w")

        self._frame_shape_var = ctk.StringVar(value="Circle")
        self._shape_btn = ctk.CTkSegmentedButton(
            self,
            values=["Circle", "Square"],
            variable=self._frame_shape_var,
        )
        self._shape_btn.grid(row=4, column=0, padx=22, pady=(0, 18), sticky="w")

        # Padding slider
        self.padding_label = ctk.CTkLabel(
            self, text="Padding: 0 px", text_color=theme.TEXT_PRIMARY, font=theme.font(13),
        )
        self.padding_label.grid(row=5, column=0, padx=22, sticky="w")

        self.padding_slider = ctk.CTkSlider(
            self, from_=0, to=40, number_of_steps=40, command=self._on_padding_change,
        )
        self.padding_slider.set(0)
        self.padding_slider.grid(row=6, column=0, padx=22, pady=(6, 16), sticky="ew")

        # Remove background toggle
        self.remove_bg_checkbox = ctk.CTkCheckBox(
            self, text="Remove background — AI-powered  (Pro)", font=theme.font(13),
        )
        self.remove_bg_checkbox.grid(row=7, column=0, padx=22, pady=(0, 14), sticky="w")

        # Fit mode selector
        ctk.CTkLabel(
            self, text="Fill Mode", font=theme.font(14, "bold"), text_color=theme.TEXT_PRIMARY,
        ).grid(row=8, column=0, padx=22, pady=(0, 6), sticky="w")

        self._fit_mode_var = ctk.StringVar(value="Crop")
        ctk.CTkSegmentedButton(
            self,
            values=["Crop", "Fit"],
            variable=self._fit_mode_var,
        ).grid(row=9, column=0, padx=22, pady=(0, 18), sticky="w")

        # Pro: Rounded Square + corner radius
        pro_frame = ctk.CTkFrame(
            self, fg_color=theme.SURFACE_INSET, corner_radius=theme.RADIUS_INNER,
        )
        pro_frame.grid(row=10, column=0, padx=22, pady=(0, 14), sticky="ew")
        pro_frame.grid_columnconfigure(0, weight=1)

        self.rounded_checkbox = ctk.CTkCheckBox(
            pro_frame,
            text="Rounded Square  (Pro)",
            command=self._sync_pro_state,
            font=theme.font(13),
        )
        self.rounded_checkbox.grid(row=0, column=0, padx=14, pady=(14, 8), sticky="w")

        self.radius_label = ctk.CTkLabel(
            pro_frame, text="Corner radius: 25%",
            text_color=theme.TEXT_MUTED, font=theme.font(12),
        )
        self.radius_label.grid(row=1, column=0, padx=14, sticky="w")

        self.radius_slider = ctk.CTkSlider(
            pro_frame, from_=5, to=50, number_of_steps=45, command=self._on_radius_change,
        )
        self.radius_slider.set(25)
        self.radius_slider.grid(row=2, column=0, padx=14, pady=(4, 14), sticky="ew")

        self.recursive_checkbox = ctk.CTkCheckBox(
            self, text="Scan subfolders when using folder mode", font=theme.font(13),
        )
        self.recursive_checkbox.select()
        self.recursive_checkbox.grid(row=11, column=0, padx=22, pady=6, sticky="w")

        self.overwrite_checkbox = ctk.CTkCheckBox(
            self, text="Overwrite existing output files", font=theme.font(13),
        )
        self.overwrite_checkbox.select()
        self.overwrite_checkbox.grid(row=12, column=0, padx=22, pady=(6, 18), sticky="w")

        self._sync_pro_state()

    def get_frame_shape(self) -> str:
        """Return the effective frame shape string for ProcessingOptions."""
        if bool(self.rounded_checkbox.get()):
            return "rounded_square"
        return self._frame_shape_var.get().lower()

    def get_output_format(self) -> str:
        """Return 'png' or 'ico'. Handles '(Pro)' suffix on free tier."""
        return self._output_format_var.get().lower().split()[0]

    def get_fit_to_frame(self) -> bool:
        """Return True when Fit mode is selected."""
        return self._fit_mode_var.get() == "Fit"

    def _on_padding_change(self, value: float) -> None:
        self.padding_label.configure(text=f"Padding: {int(value)} px")

    def _on_radius_change(self, value: float) -> None:
        self.radius_label.configure(text=f"Corner radius: {int(value)}%")

    def _sync_pro_state(self) -> None:
        state = "normal" if bool(self.rounded_checkbox.get()) else "disabled"
        self.radius_slider.configure(state=state)

    def apply_license_state(self, is_pro: bool) -> None:
        """Enable or disable Pro-gated controls based on license tier."""
        if is_pro:
            self.rounded_checkbox.configure(state="normal", text="Rounded Square")
            self._output_format_btn.configure(values=["PNG", "ICO"])
            self.remove_bg_checkbox.configure(state="normal", text="Remove background — AI-powered")
            self.remove_bg_checkbox.select()
        else:
            self.rounded_checkbox.deselect()
            self.rounded_checkbox.configure(state="disabled", text="Rounded Square  (Pro)")
            self._output_format_var.set("PNG")
            self._output_format_btn.configure(values=["PNG", "ICO  (Pro)"])
            self.remove_bg_checkbox.deselect()
            self.remove_bg_checkbox.configure(state="disabled", text="Remove background — AI-powered  (Pro)")
        self._sync_pro_state()

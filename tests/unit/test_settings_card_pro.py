# Purpose: Unit tests for SettingsCard Pro gating — UI state changes and format parsing
# Expected behavior:
#   - apply_license_state(False): ICO locked, AI removal disabled/deselected, rounded square locked
#   - apply_license_state(True): ICO unlocked, AI removal enabled/selected, rounded square enabled
#   - get_output_format() strips the " (Pro)" suffix and lowercases properly
# Related: v1.1.0 Pro gate expansion
# Preconditions: customtkinter and picframes.theme are mocked before import

from __future__ import annotations

import sys
import types
from unittest.mock import MagicMock

# ---------------------------------------------------------------------------
# Fake ctk widget implementations — lightweight but stateful
# ---------------------------------------------------------------------------

class _Var:
    def __init__(self, value=""): self._v = value
    def get(self): return self._v
    def set(self, v): self._v = v


class _CheckBox:
    def __init__(self, *a, **kw):
        self._selected = False
        self.state = "normal"
        self.text = kw.get("text", "")
        self._cmd = kw.get("command")

    def get(self): return 1 if self._selected else 0
    def select(self): self._selected = True
    def deselect(self): self._selected = False
    def grid(self, **kw): pass
    def configure(self, **kw):
        if "state" in kw: self.state = kw["state"]
        if "text" in kw: self.text = kw["text"]


class _SegBtn:
    def __init__(self, *a, **kw):
        self.values = list(kw.get("values", []))
        self._var = kw.get("variable")

    def grid(self, **kw): pass
    def configure(self, **kw):
        if "values" in kw:
            self.values = list(kw["values"])
            if self._var and self._var.get() not in self.values:
                self._var.set(self.values[0] if self.values else "")


class _Slider:
    def __init__(self, *a, **kw):
        self._v = 0.0
        self._state = "normal"

    def get(self): return self._v
    def set(self, v): self._v = float(v)
    def grid(self, **kw): pass
    def configure(self, **kw):
        if "state" in kw: self._state = kw["state"]


class _Frame:
    def __init__(self, *a, **kw):
        self.grid_columnconfigure = MagicMock()

    def grid(self, **kw): pass
    def configure(self, **kw): pass


class _Label:
    def __init__(self, *a, **kw): self.text = kw.get("text", "")
    def grid(self, **kw): pass
    def configure(self, **kw):
        if "text" in kw: self.text = kw["text"]


# ---------------------------------------------------------------------------
# Inject mocks BEFORE importing settings_card
# ---------------------------------------------------------------------------

_ctk = MagicMock()
_ctk.StringVar = _Var
_ctk.CTkFrame = _Frame
_ctk.CTkCheckBox = _CheckBox
_ctk.CTkSegmentedButton = _SegBtn
_ctk.CTkSlider = _Slider
_ctk.CTkLabel = _Label

_theme = types.SimpleNamespace(
    SURFACE="#1e1e2e", SURFACE_INSET="#16213e",
    RADIUS_CARD=12, RADIUS_INNER=8,
    TEXT_PRIMARY="#ffffff", TEXT_MUTED="#888888",
    font=lambda *a, **kw: ("Arial", 12),
)

sys.modules["customtkinter"] = _ctk
sys.modules["picframes.theme"] = _theme

# Stub picframes.ui as a real package (with __path__) to prevent __init__ cascade
# while still allowing settings_card to be found as a submodule.
import pathlib
_ui_pkg = types.ModuleType("picframes.ui")
_ui_pkg.__path__ = [str(pathlib.Path(__file__).resolve().parents[2] / "picframes" / "ui")]
_ui_pkg.__package__ = "picframes.ui"
sys.modules["picframes.ui"] = _ui_pkg

from picframes.ui.settings_card import SettingsCard  # noqa: E402


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_card() -> SettingsCard:
    """Instantiate a SettingsCard with no real parent."""
    return SettingsCard(None)


# ---------------------------------------------------------------------------
# get_output_format — string parsing
# ---------------------------------------------------------------------------

class TestGetOutputFormat:
    def test_png_returns_png(self):
        card = _make_card()
        card._output_format_var.set("PNG")
        assert card.get_output_format() == "png"

    def test_ico_clean_returns_ico(self):
        card = _make_card()
        card._output_format_var.set("ICO")
        assert card.get_output_format() == "ico"

    def test_ico_pro_suffix_stripped(self):
        card = _make_card()
        card._output_format_var.set("ICO  (Pro)")
        assert card.get_output_format() == "ico"

    def test_result_is_lowercase(self):
        card = _make_card()
        card._output_format_var.set("PNG")
        assert card.get_output_format() == card.get_output_format().lower()


# ---------------------------------------------------------------------------
# apply_license_state(False) — free tier
# ---------------------------------------------------------------------------

class TestApplyLicenseStateFree:
    def setup_method(self):
        self.card = _make_card()
        self.card.apply_license_state(False)

    def test_rounded_checkbox_is_disabled(self):
        assert self.card.rounded_checkbox.state == "disabled"

    def test_rounded_checkbox_is_deselected(self):
        assert self.card.rounded_checkbox.get() == 0

    def test_rounded_checkbox_shows_pro_label(self):
        assert "(Pro)" in self.card.rounded_checkbox.text

    def test_remove_bg_is_disabled(self):
        assert self.card.remove_bg_checkbox.state == "disabled"

    def test_remove_bg_is_deselected(self):
        assert self.card.remove_bg_checkbox.get() == 0

    def test_remove_bg_shows_pro_label(self):
        assert "(Pro)" in self.card.remove_bg_checkbox.text

    def test_output_format_reset_to_png(self):
        assert self.card._output_format_var.get() == "PNG"

    def test_ico_button_shows_pro_suffix(self):
        assert any("(Pro)" in v for v in self.card._output_format_btn.values)


# ---------------------------------------------------------------------------
# apply_license_state(True) — Pro tier
# ---------------------------------------------------------------------------

class TestApplyLicenseStatePro:
    def setup_method(self):
        self.card = _make_card()
        self.card.apply_license_state(True)

    def test_rounded_checkbox_is_enabled(self):
        assert self.card.rounded_checkbox.state == "normal"

    def test_rounded_checkbox_label_clean(self):
        assert "(Pro)" not in self.card.rounded_checkbox.text

    def test_remove_bg_is_enabled(self):
        assert self.card.remove_bg_checkbox.state == "normal"

    def test_remove_bg_is_selected(self):
        assert self.card.remove_bg_checkbox.get() == 1

    def test_remove_bg_label_clean(self):
        assert "(Pro)" not in self.card.remove_bg_checkbox.text

    def test_ico_button_values_clean(self):
        assert all("(Pro)" not in v for v in self.card._output_format_btn.values)

    def test_ico_available_in_button_values(self):
        values_lower = [v.lower() for v in self.card._output_format_btn.values]
        assert "ico" in values_lower


# ---------------------------------------------------------------------------
# Toggle: applying free after pro resets state correctly
# ---------------------------------------------------------------------------

class TestApplyLicenseStateToggle:
    def test_pro_then_free_locks_ai_removal(self):
        card = _make_card()
        card.apply_license_state(True)
        assert card.remove_bg_checkbox.state == "normal"
        card.apply_license_state(False)
        assert card.remove_bg_checkbox.state == "disabled"

    def test_pro_then_free_resets_format_to_png(self):
        card = _make_card()
        card.apply_license_state(True)
        card._output_format_var.set("ICO")
        card.apply_license_state(False)
        assert card._output_format_var.get() == "PNG"

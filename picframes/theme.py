"""Brand token system for PicFrames."""
from __future__ import annotations
import customtkinter as ctk

BG            = ("#F4F7FB", "#16212D")
SURFACE       = ("#FFFFFF", "#2B3540")
SURFACE_INSET = ("#EEF2FA", "#1C2739")
BANNER_BG   = ("#16212D", "#F1F5F9")   # dark in light mode, light in dark mode — true inverse
BANNER_TEXT = ("#F1F5F9", "#16212D")   # light on dark banner / dark on light banner
ACCENT        = "#2F6FFF"
ACCENT_HOVER  = "#1A56F0"
ACCENT_MUTED  = ("#DBEAFE", "#1A2D4D")
ACCENT_BORDER = ("#93C5FD", "#2F6FFF")
ACCENT_TEXT   = ("#1D4ED8", "#93C5FD")
TEXT_PRIMARY = ("#16212D", "#F1F5F9")
TEXT_MUTED   = ("#5D7285", "#94A3B8")
TEXT_INVERSE = "#FFFFFF"
BTN_SECONDARY       = ("#E2E8F0", "#334155")
BTN_SECONDARY_HOVER = ("#CBD5E1", "#475569")
SUCCESS          = "#10B981"
ERROR            = "#EF4444"
ERROR_HOVER      = "#B91C1C"
AMBER            = "#F59E0B"
AMBER_HOVER      = "#D97706"
AMBER_DARK       = "#92400E"
AMBER_HOVER_DARK = "#78350F"
TEXT_ON_AMBER    = "#111827"
PRO_BG           = ("#16A34A", "#14532D")
PRO_BG_HOVER     = ("#15803D", "#166534")
RADIUS_CARD  = 24
RADIUS_INNER = 18
RADIUS_BTN   = 14
RADIUS_PILL  = 999
_FONT_FAMILY = "Segoe UI"


def font(size: int, weight: str = "normal") -> ctk.CTkFont:
    return ctk.CTkFont(family=_FONT_FAMILY, size=size, weight=weight)

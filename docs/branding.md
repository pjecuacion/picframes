# Brand System

This document is the single source of truth for the studio's visual identity as applied to Windows desktop tools. All token values live in `bulk_webp/theme.py`. Every future app in the suite should copy that file and adjust only what differs for that product.

---

## Philosophy

- **One file owns the brand.** `theme.py` is the only place colours, radii, and the font family are defined. No hex strings appear anywhere else.
- **Always-dark banner.** The top bar uses `BANNER_BG` in both light and dark modes. It never inverts. This provides a consistent brand anchor regardless of the user's system preference.
- **Semantic tokens, not raw values.** UI code uses names like `theme.SURFACE` and `theme.ACCENT`, not `#2B3540`. Meaning is encoded in the name.
- **Retheme by changing one file.** To create a sibling app with a different accent colour, copy `theme.py`, change `ACCENT` (and optionally `AMBER` for the donation/upgrade surfaces), and import it from the new app's package.

---

## Colour Palette

The four base colours come from the studio brand kit.

| Swatch | Hex | Name |
|--------|-----|------|
| ![#16212D](https://placehold.co/14x14/16212D/16212D.png) | `#16212D` | Brand Navy |
| ![#2B3540](https://placehold.co/14x14/2B3540/2B3540.png) | `#2B3540` | Brand Slate |
| ![#2F6FFF](https://placehold.co/14x14/2F6FFF/2F6FFF.png) | `#2F6FFF` | Electric Blue |
| ![#FFFFFF](https://placehold.co/14x14/FFFFFF/FFFFFF.png) | `#FFFFFF` | White |

---

## Token Reference

All tokens are tuples `(light_value, dark_value)` unless they are mode-invariant single strings.

### Surfaces & Backgrounds

| Token | Light | Dark | Usage |
|-------|-------|------|-------|
| `BG` | `#F4F7FB` | `#16212D` | Root window background |
| `SURFACE` | `#FFFFFF` | `#2B3540` | Cards, panels |
| `SURFACE_INSET` | `#EEF2FA` | `#1C2739` | Inner frames, drop zones, resize section |

### Banner

| Token | Light | Dark | Usage |
|-------|-------|------|-------|
| `BANNER_BG` | `#16212D` | `#0D1621` | Top bar — **always dark** |
| `BANNER_TEXT` | `#F1F5F9` | `#F1F5F9` | Banner label and switch text |

### Accent (Electric Blue)

| Token | Value | Usage |
|-------|-------|-------|
| `ACCENT` | `#2F6FFF` | Primary CTA buttons, progress bar, active states |
| `ACCENT_HOVER` | `#1A56F0` | Hover state of primary buttons |
| `ACCENT_MUTED` | `#DBEAFE` / `#1A2D4D` | Drop zone fill |
| `ACCENT_BORDER` | `#93C5FD` / `#2F6FFF` | Drop zone border |
| `ACCENT_TEXT` | `#1D4ED8` / `#93C5FD` | Text rendered on an accent-tinted surface |

### Typography

| Token | Light | Dark | Usage |
|-------|-------|------|-------|
| `TEXT_PRIMARY` | `#16212D` | `#F1F5F9` | Headings, card titles, primary labels |
| `TEXT_MUTED` | `#5D7285` | `#94A3B8` | Subtitles, hints, status messages |
| `TEXT_INVERSE` | `#FFFFFF` | `#FFFFFF` | Text rendered on any dark/coloured button |
| `TEXT_ON_AMBER` | `#111827` | `#111827` | Text rendered on amber/yellow surfaces |

### Secondary Buttons

| Token | Light | Dark | Usage |
|-------|-------|------|-------|
| `BTN_SECONDARY` | `#E2E8F0` | `#334155` | Ghost/secondary button fill |
| `BTN_SECONDARY_HOVER` | `#CBD5E1` | `#475569` | Hover state |

### State Colours

| Token | Value | Usage |
|-------|-------|-------|
| `SUCCESS` | `#10B981` | Finish confirmation, Pro active badge |
| `ERROR` | `#EF4444` | Cancel button fill, error status label |
| `ERROR_HOVER` | `#B91C1C` | Cancel button hover |
| `AMBER` | `#F59E0B` | Donation button, "Buy Me a Coffee", Pro upgrade badge (light) |
| `AMBER_HOVER` | `#D97706` | Amber hover (light) |
| `AMBER_DARK` | `#92400E` | Amber button fill (dark mode) |
| `AMBER_HOVER_DARK` | `#78350F` | Amber hover (dark mode) |
| `PRO_BG` | `#16A34A` / `#14532D` | Pro license badge background |
| `PRO_BG_HOVER` | `#15803D` / `#166534` | Pro badge hover |

### Corner Radii

| Token | Value | Usage |
|-------|-------|-------|
| `RADIUS_CARD` | `24` | Outer cards and panels |
| `RADIUS_INNER` | `18` | Inner frames (drop zone, resize section) |
| `RADIUS_BTN` | `14` | Standard buttons |
| `RADIUS_PILL` | `999` | Pill-shaped buttons (donation, license badge) |

---

## Typography

**Typeface:** Segoe UI  
**Why:** Always present on Windows 10/11 — no bundling required. Used by VS Code, Windows 11 system UI, and most professional developer tools. Sharp and legible at all sizes.

**Helper function:**

```python
theme.font(size: int, weight: str = "normal") -> ctk.CTkFont
```

Use this everywhere instead of `ctk.CTkFont(...)` directly. It enforces the brand family automatically.

```python
# Examples
theme.font(30, "bold")   # card headlines
theme.font(19, "bold")   # section titles
theme.font(15)           # body / subtitles
theme.font(13)           # hints, status labels
theme.font(12)           # captions
```

---

## Usage Pattern

```python
# In any UI file inside the package:
from .. import theme

# Apply to a widget
ctk.CTkLabel(
    parent,
    text="Hello",
    font=theme.font(15, "bold"),
    text_color=theme.TEXT_PRIMARY,
)

ctk.CTkButton(
    parent,
    text="Convert",
    fg_color=theme.ACCENT,
    hover_color=theme.ACCENT_HOVER,
    text_color=theme.TEXT_INVERSE,
    corner_radius=theme.RADIUS_BTN,
)
```

---

## Creating a New App

1. Copy `theme.py` into the new app's package root.
2. Change `ACCENT` and `ACCENT_HOVER` to the new app's primary colour.
3. Optionally adjust `AMBER` for the upgrade/donation surface.
4. Leave `BG`, `SURFACE`, `BANNER_BG`, and typography unchanged to maintain suite coherence.
5. Every UI file imports from the local copy: `from . import theme`.

That's it. The entire visual identity follows.

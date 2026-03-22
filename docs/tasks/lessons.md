# Lessons

## Usage Rules

- Add a new dated entry after any user correction.
- Record the mistake pattern, the prevention rule, and the concrete adjustment.
- Keep entries short and reusable.

## Template

### YYYY-MM-DD

- Pattern:
- Prevention rule:
- Adjustment made:

### 2026-03-20

- Pattern: LemonSqueezy API returns 405 for PATCH/POST on products and variants — assumed writable by API.
- Prevention rule: Before attempting any write to a SaaS API resource, probe with a GET first and check the docs for write support. LS products/variants are dashboard-only.

### 2026-03-20 — EULA is AI-drafted, not attorney-reviewed

- Pattern: EULA, liability disclaimers, and privacy notices were drafted by AI.
- Rule: This is intentional and acceptable for an indie developer. The document
  covers all standard commercial EULA sections: warranty disclaimer, liability
  cap, indemnification, arbitration, class action waiver, severability, and
  force majeure. It is as strong as possible without jurisdiction-specific
  customisation.
- One action item: update Section 12 (Governing Law) with the actual country
  or state once the Developer's filing jurisdiction is decided. Everything else
  is ready to ship.
- Adjustment made: Documented LS API write surface; instructed user to enable license keys in dashboard.

### 2026-03-20

- Pattern: `bulk_webp/__init__.py` eagerly imported `from .app import main`, causing GUI package imports (customtkinter, tkinterdnd2) to run at module load time — blocked all unit tests without a display.
- Prevention rule: Top-level `__init__.py` must not eagerly import GUI-heavy modules. Use a lazy wrapper function instead.
- Adjustment made: Changed `__init__.py` to a lazy `def main(): from .app import main as _main; _main()`.

### 2026-03-20

- Pattern: Ed25519 offline validator required embedding a private/public keypair and shipping `cryptography` as a dependency — adds attack surface and packaging weight.
- Prevention rule: For SaaS-backed products, prefer the platform's own license validation API over bespoke offline crypto. Fewer moving parts, no embedded secrets.
- Adjustment made: Replaced Ed25519 validator with LemonSqueezy /licenses/activate + /licenses/validate calls using stdlib urllib only.

### 2026-03-19

- Pattern: Assumed NSIS for Windows installer tooling without checking whether the existing preference was Inno Setup with an `.iss` script.
- Prevention rule: When choosing Windows installer tooling, confirm whether the project or user already uses NSIS or Inno Setup before locking the packaging path.
- Adjustment made: Recorded the preference signal and will offer switching the installer from `.nsi` to `.iss` if requested.

### 2026-03-19

- Pattern: Carried forward an incorrect Buy Me a Coffee URL instead of confirming the exact donation link.
- Prevention rule: When wiring user-owned external links, copy the exact URL from the latest user message and update all surfaced references together.
- Adjustment made: Updated the app and installer metadata to use `https://buymeacoffee.com/pjecuacion`.

- Pattern: Assumed NSIS for Windows installer tooling without checking whether the existing preference was Inno Setup with an `.iss` script.
- Prevention rule: When choosing Windows installer tooling, confirm whether the project or user already uses NSIS or Inno Setup before locking the packaging path.
- Adjustment made: Recorded the preference signal and will offer switching the installer from `.nsi` to `.iss` if requested.

### 2026-03-19

- Pattern: Carried forward an incorrect Buy Me a Coffee URL instead of confirming the exact donation link.
- Prevention rule: When wiring user-owned external links, copy the exact URL from the latest user message and update all surfaced references together.
- Adjustment made: Updated the app and installer metadata to use `https://buymeacoffee.com/pjecuacion`.
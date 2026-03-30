# Template Instructions

This repo is the **canonical template** for building desktop apps. When asked to build a new app, follow this playbook exactly.

---

## 1. Understand the Request

The user will say something like: *"Port the logic from `<source>`. Build it as `<new_package>/`."*

- `<source>` — the app to extract business logic from. Look for it in `temp/`.
- `<new_package>` — the name of the new Python package to create (e.g. `bulk_resize/`).
- Derive the window title, class name, and exe name from the package name (e.g. `bulk_resize` → `Bulk Resize`, `BulkResizeApp`, `BulkResize.exe`).

---

## 2. Read the Source App

Read everything in `temp/` before writing any code. Identify:
- What the app does (the core transformation or processing task)
- What inputs it takes and what outputs it produces
- Any key settings or options the user controls

Do not modify or delete anything in `temp/`.

---

## 3. Create the New Package

Rename `my_app/` to your new package name, or create a fresh package mirroring its structure:

```
<new_package>/
    __init__.py          # exposes main()
    app.py               # CTk window, wires UI to logic
    processor.py         # core business logic (port your logic here)
    runner.py            # runs jobs in a process pool, reports progress
    option_builder.py    # builds job options from UI state
    resources.py         # asset path helper
    settings.py          # JSON settings persistence (~/.app_name/settings.json)
    theme.py             # color tokens, font helper, radii
    license/             # LemonSqueezy Pro gate — always include
        __init__.py
        activation_dialog.py
        gate.py
        key_model.py
        validator.py
    ui/                  # one file per UI card
        __init__.py
        banner.py        # inverse-themed top bar: dark in light mode, light in dark mode
        hero.py
        source_card.py
        output_card.py
        settings_card.py
        progress_card.py
        preview_strip.py
```

Keep each file under 200 lines. Extract helpers into separate modules if needed.

---

## 4. Update Entry Points

**`main.py`** — update the AppUserModelID and the import:
```python
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("<AppName>.App.1")
from <new_package> import main
```

**`packaging/MyApp.spec`** — rename the spec file to `<AppName>.spec` and update both `name=` values in `EXE` and `COLLECT` blocks.

**`packaging/installer.iss`** — update:
- `AppName`, `AppExeName`, `AppId` (generate a new GUID), `OutputBaseFilename`
- `SourceDir` to point to the new dist folder name

---

## 5. Assets

- Replace `assets/app_icon.ico` with an icon for the new app, or ask the user if one is needed.
- `assets/THIRD_PARTY_NOTICES.txt` — update if new dependencies were added.

---

## 6. LemonSqueezy Product Page

Update `lemonsqueezy/product_page.md` before publishing:
- Replace the headline, subheadline, and Pro feature bullets with the new app's details.
- Set the real price (remove the `$[X]` placeholder).
- Copy the final text into the LemonSqueezy product description field.
- Update `license/activation_dialog.py` with the new product checkout URL.

---

## 7. Verify Before Done

- Run `main.py` and confirm the window opens, the banner shows the correct app name, and the core feature works end-to-end.
- Run existing tests and add unit tests for any new business logic under `tests/unit/`.
- Do not mark the task complete until the app launches without errors.
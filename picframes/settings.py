from __future__ import annotations

import json
from pathlib import Path

_SETTINGS_PATH = Path.home() / ".picframes" / "settings.json"
_DEFAULTS: dict = {"appearance_mode": "system", "license_key": ""}


def load() -> dict:
    try:
        data = json.loads(_SETTINGS_PATH.read_text(encoding="utf-8"))
        return {**_DEFAULTS, **data}
    except Exception:
        return dict(_DEFAULTS)


def save(data: dict) -> None:
    _SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    _SETTINGS_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")

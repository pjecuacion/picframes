from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
from datetime import date

from .key_model import LicenseInfo

_ACTIVATE_URL = "https://api.lemonsqueezy.com/v1/licenses/activate"
_VALIDATE_URL = "https://api.lemonsqueezy.com/v1/licenses/validate"
# TODO: rename to your app's display name — shown in the LemonSqueezy dashboard
_INSTANCE_NAME = "MyApp"


def validate_key(key_string: str, _activate_url: str = _ACTIVATE_URL) -> LicenseInfo | None:
    """Validate a LemonSqueezy license key via the activation API.

    On first use the key is activated (consuming one seat).
    Subsequent calls validate the existing activation.
    Returns None on any failure.
    """
    key = key_string.strip()
    if not key:
        return None

    # Try activate first; if already activated, fall back to validate.
    for url in (_activate_url, _VALIDATE_URL):
        info = _call_ls(url, key)
        if info is not None:
            return info

    return None


def _call_ls(url: str, key: str) -> LicenseInfo | None:
    payload = urllib.parse.urlencode({
        "license_key": key,
        "instance_name": _INSTANCE_NAME,
    }).encode()
    req = urllib.request.Request(url, data=payload, method="POST", headers={
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    })
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
    except urllib.error.HTTPError as exc:
        try:
            data = json.loads(exc.read())
        except Exception:
            return None
    except Exception:
        return None

    if not data.get("activated") and not data.get("valid"):
        return None

    lk = data.get("license_key", {})
    meta = data.get("meta", {})

    status = lk.get("status", "")
    if status not in ("active", "inactive"):
        return None

    expires_at: str | None = lk.get("expires_at")
    if expires_at:
        expires_at = expires_at[:10]
        try:
            if date.today() > date.fromisoformat(expires_at):
                return None
        except ValueError:
            return None

    email = meta.get("customer_email") or lk.get("key", "")[:8] + "…"

    return LicenseInfo(
        email=email,
        tier="pro",
        issued_at=lk.get("created_at", "")[:10],
        expires_at=expires_at,
    )

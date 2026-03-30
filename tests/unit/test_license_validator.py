# Purpose: Unit tests for picframes.license.validator (LemonSqueezy API backend)
# Expected behavior: valid LS API responses parse to LicenseInfo; errors/invalid states return None
# Related: feature/licensing implementation
# Preconditions: No network access needed — HTTP calls are mocked

from __future__ import annotations

import io
import json
from datetime import date, timedelta
from unittest.mock import MagicMock, patch

from picframes.license.key_model import LicenseInfo
from picframes.license.validator import validate_key, _call_ls


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _ls_response(activated: bool = True, valid: bool = False,
                 status: str = "active", expires_at=None,
                 email: str = "user@example.com") -> dict:
    """Build a minimal LemonSqueezy /licenses/activate response."""
    return {
        "activated": activated,
        "valid": valid,
        "license_key": {
            "status": status,
            "key": "XXXX-XXXX",
            "expires_at": expires_at,
            "created_at": "2026-01-01T00:00:00.000000Z",
        },
        "meta": {
            "customer_email": email,
        },
    }


def _mock_urlopen(response_body: dict):
    resp = MagicMock()
    resp.read.return_value = json.dumps(response_body).encode()
    resp.__enter__ = lambda s: s
    resp.__exit__ = MagicMock(return_value=False)
    return resp


# ---------------------------------------------------------------------------
# Valid activation tests
# ---------------------------------------------------------------------------

def test_valid_activation_returns_license_info():
    with patch("urllib.request.urlopen", return_value=_mock_urlopen(_ls_response())):
        info = validate_key("VALID-KEY-1234", _activate_url="https://mock/activate")
    assert isinstance(info, LicenseInfo)
    assert info.email == "user@example.com"
    assert info.tier == "pro"
    assert info.is_pro is True


def test_non_expired_key_is_pro():
    future = (date.today() + timedelta(days=365)).isoformat() + "T00:00:00.000000Z"
    with patch("urllib.request.urlopen", return_value=_mock_urlopen(_ls_response(expires_at=future))):
        info = validate_key("VALID-KEY-1234", _activate_url="https://mock/activate")
    assert info is not None and info.is_pro is True


# ---------------------------------------------------------------------------
# Expired / inactive tests
# ---------------------------------------------------------------------------

def test_expired_key_returns_none():
    yesterday = (date.today() - timedelta(days=1)).isoformat() + "T00:00:00.000000Z"
    with patch("urllib.request.urlopen", return_value=_mock_urlopen(_ls_response(expires_at=yesterday))):
        info = validate_key("EXPIRED-KEY", _activate_url="https://mock/activate")
    assert info is None


def test_inactive_status_returns_none():
    with patch("urllib.request.urlopen", return_value=_mock_urlopen(
        _ls_response(activated=False, valid=False, status="disabled")
    )):
        info = validate_key("INACTIVE-KEY", _activate_url="https://mock/validate")
    assert info is None


def test_not_activated_and_not_valid_returns_none():
    body = {"activated": False, "valid": False, "license_key": {}, "meta": {}}
    with patch("urllib.request.urlopen", return_value=_mock_urlopen(body)):
        info = validate_key("BAD-KEY", _activate_url="https://mock/activate")
    assert info is None


# ---------------------------------------------------------------------------
# Network / API error tests
# ---------------------------------------------------------------------------

def test_network_error_returns_none():
    import urllib.error
    with patch("urllib.request.urlopen", side_effect=OSError("no network")):
        info = validate_key("ANY-KEY", _activate_url="https://mock/activate")
    assert info is None


def test_empty_key_returns_none():
    assert validate_key("") is None
    assert validate_key("   ") is None


def test_validate_fallback_used_on_activate_failure():
    """If activate fails, validate endpoint is tried next."""
    import urllib.error

    activate_err = urllib.error.HTTPError(
        "https://mock/activate", 422, "Unprocessable", {}, io.BytesIO(b'{"activated":false,"valid":false}')
    )
    validate_resp = _mock_urlopen(_ls_response(activated=False, valid=True))

    side_effects = [activate_err, validate_resp]
    with patch("urllib.request.urlopen", side_effect=side_effects):
        info = validate_key("ALREADY-ACTIVE", _activate_url="https://mock/activate")
    assert info is not None and info.is_pro is True


# ---------------------------------------------------------------------------
# gate.can_use tests
# ---------------------------------------------------------------------------

def test_free_feature_always_accessible():
    from picframes.license.gate import can_use
    assert can_use("free_feature", None) is True
    assert can_use("another_free", None) is True


def test_pro_feature_blocked_without_license():
    from picframes.license.gate import can_use
    assert can_use("rounded_square", None) is False


def test_pro_feature_accessible_with_valid_license():
    from picframes.license.gate import can_use
    info = LicenseInfo(email="a@b.com", tier="pro", issued_at="2026-01-01", expires_at=None)
    assert can_use("rounded_square", info) is True

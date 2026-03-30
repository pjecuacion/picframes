# Purpose: Exhaustive unit tests for picframes.license.gate — Pro feature gating logic
# Expected behavior:
#   - ico, ai_removal, rounded_square all blocked without a Pro license
#   - All three unlocked with a valid Pro LicenseInfo
#   - Free-tier LicenseInfo does NOT unlock Pro features
#   - Any feature NOT in _PRO_FEATURES is always accessible
#   - FREE_BATCH_LIMIT is exactly 10
# Related: v1.1.0 Pro gate expansion
# Preconditions: None — pure Python, no I/O, no network

from __future__ import annotations

import pytest

from picframes.license.gate import can_use, FREE_BATCH_LIMIT, _PRO_FEATURES
from picframes.license.key_model import LicenseInfo

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

_PRO = LicenseInfo(email="pro@test.com", tier="pro", issued_at="2026-01-01", expires_at=None)
_FREE = LicenseInfo(email="free@test.com", tier="free", issued_at="2026-01-01", expires_at=None)
_EXPIRED = LicenseInfo(email="lapsed@test.com", tier="pro", issued_at="2025-01-01", expires_at="2025-12-31")


# ---------------------------------------------------------------------------
# FREE_BATCH_LIMIT
# ---------------------------------------------------------------------------

class TestFreeBatchLimit:
    def test_value_is_ten(self):
        assert FREE_BATCH_LIMIT == 10

    def test_is_integer(self):
        assert isinstance(FREE_BATCH_LIMIT, int)

    def test_positive(self):
        assert FREE_BATCH_LIMIT > 0


# ---------------------------------------------------------------------------
# _PRO_FEATURES membership
# ---------------------------------------------------------------------------

class TestProFeaturesSet:
    def test_rounded_square_gated(self):
        assert "rounded_square" in _PRO_FEATURES

    def test_ico_gated(self):
        assert "ico" in _PRO_FEATURES

    def test_ai_removal_gated(self):
        assert "ai_removal" in _PRO_FEATURES

    def test_exactly_three_features(self):
        assert len(_PRO_FEATURES) == 3

    def test_is_frozenset(self):
        assert isinstance(_PRO_FEATURES, frozenset)


# ---------------------------------------------------------------------------
# can_use — no license (None)
# ---------------------------------------------------------------------------

class TestCanUseNoLicense:
    @pytest.mark.parametrize("feature", ["rounded_square", "ico", "ai_removal"])
    def test_pro_feature_blocked(self, feature):
        assert can_use(feature, None) is False

    def test_unknown_feature_allowed(self):
        assert can_use("some_free_feature", None) is True

    def test_empty_string_feature_allowed(self):
        assert can_use("", None) is True

    def test_padding_allowed(self):
        assert can_use("padding", None) is True

    def test_output_format_allowed(self):
        assert can_use("output_format", None) is True


# ---------------------------------------------------------------------------
# can_use — free tier
# ---------------------------------------------------------------------------

class TestCanUseFreeTier:
    @pytest.mark.parametrize("feature", ["rounded_square", "ico", "ai_removal"])
    def test_pro_feature_blocked_for_free_tier(self, feature):
        assert can_use(feature, _FREE) is False

    def test_free_feature_allowed_for_free_tier(self):
        assert can_use("any_free_feature", _FREE) is True


# ---------------------------------------------------------------------------
# can_use — expired Pro license
# ---------------------------------------------------------------------------

class TestCanUseExpiredLicense:
    @pytest.mark.parametrize("feature", ["rounded_square", "ico", "ai_removal"])
    def test_pro_feature_blocked_for_expired_license(self, feature):
        assert can_use(feature, _EXPIRED) is False


# ---------------------------------------------------------------------------
# can_use — valid Pro license
# ---------------------------------------------------------------------------

class TestCanUseProTier:
    @pytest.mark.parametrize("feature", ["rounded_square", "ico", "ai_removal"])
    def test_all_pro_features_unlocked(self, feature):
        assert can_use(feature, _PRO) is True

    def test_free_features_still_accessible(self):
        assert can_use("padding", _PRO) is True
        assert can_use("unknown_feature", _PRO) is True

    def test_all_features_in_set_unocked(self):
        for f in _PRO_FEATURES:
            assert can_use(f, _PRO) is True, f"Expected {f} to be accessible for Pro"


# ---------------------------------------------------------------------------
# can_use — return type
# ---------------------------------------------------------------------------

class TestCanUseReturnType:
    def test_returns_bool_for_blocked(self):
        result = can_use("ico", None)
        assert isinstance(result, bool)
        assert result is False

    def test_returns_bool_for_allowed(self):
        result = can_use("padding", None)
        assert isinstance(result, bool)
        assert result is True

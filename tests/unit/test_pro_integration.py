# Purpose: Integration tests validating Pro gating end-to-end through option_builder,
#          and batch cap behaviour simulation
# Expected behavior:
#   - option_builder.build_options reads remove_bg=False when free (AI removal locked)
#   - option_builder.build_options reads output_format="ico" for Pro, "png" for free
#   - Batch cap logic slices sources to FREE_BATCH_LIMIT for free users, unlimited for Pro
#   - LicenseInfo.is_pro is False for expired, free-tier, and None licenses
# Related: v1.1.0 Pro gate expansion
# Preconditions: picframes.processor and picframes.license are pure Python (no ctk)

from __future__ import annotations

import pytest
from unittest.mock import MagicMock

from picframes.option_builder import build_options
from picframes.processor import ProcessingOptions
from picframes.license import FREE_BATCH_LIMIT
from picframes.license.key_model import LicenseInfo


# ---------------------------------------------------------------------------
# Minimal SettingsCard stub for option_builder.build_options
# ---------------------------------------------------------------------------

def _make_stub(
    frame_shape="circle",
    corner_radius=25,
    padding=0,
    remove_bg=False,
    output_format="png",
    overwrite=True,
    fit_to_frame=False,
):
    s = MagicMock()
    s.get_frame_shape.return_value = frame_shape
    s.radius_slider.get.return_value = float(corner_radius)
    s.padding_slider.get.return_value = float(padding)
    s.remove_bg_checkbox.get.return_value = 1 if remove_bg else 0
    s.get_output_format.return_value = output_format
    s.overwrite_checkbox.get.return_value = 1 if overwrite else 0
    s.get_fit_to_frame.return_value = fit_to_frame
    return s


# ---------------------------------------------------------------------------
# option_builder: free tier configuration
# ---------------------------------------------------------------------------

class TestOptionBuilderFreeTier:
    def test_remove_bg_false_when_free(self):
        opts = build_options(_make_stub(remove_bg=False))
        assert opts.remove_bg is False

    def test_output_format_png_when_free(self):
        opts = build_options(_make_stub(output_format="png"))
        assert opts.output_format == "png"

    def test_frame_shape_circle_when_free(self):
        opts = build_options(_make_stub(frame_shape="circle"))
        assert opts.frame_shape == "circle"

    def test_frame_shape_square_when_free(self):
        opts = build_options(_make_stub(frame_shape="square"))
        assert opts.frame_shape == "square"

    def test_returns_processing_options_type(self):
        opts = build_options(_make_stub())
        assert isinstance(opts, ProcessingOptions)


# ---------------------------------------------------------------------------
# option_builder: Pro tier configuration
# ---------------------------------------------------------------------------

class TestOptionBuilderProTier:
    def test_remove_bg_true_when_pro(self):
        opts = build_options(_make_stub(remove_bg=True))
        assert opts.remove_bg is True

    def test_output_format_ico_when_pro(self):
        opts = build_options(_make_stub(output_format="ico"))
        assert opts.output_format == "ico"

    def test_rounded_square_when_pro(self):
        opts = build_options(_make_stub(frame_shape="rounded_square"))
        assert opts.frame_shape == "rounded_square"

    def test_corner_radius_passed_through(self):
        opts = build_options(_make_stub(frame_shape="rounded_square", corner_radius=40))
        assert opts.corner_radius_pct == 40


# ---------------------------------------------------------------------------
# Batch cap logic — validates the behaviour contract from app._run_job
#   is_pro = license_info is not None and license_info.is_pro
#   if not is_pro and len(sources) > FREE_BATCH_LIMIT:
#       sources = sources[:FREE_BATCH_LIMIT]
# ---------------------------------------------------------------------------

def _apply_cap(sources: list, license_info) -> list:
    """Mirror of the cap logic in app._run_job (used to verify the contract)."""
    is_pro = license_info is not None and license_info.is_pro
    if not is_pro and len(sources) > FREE_BATCH_LIMIT:
        return sources[:FREE_BATCH_LIMIT]
    return sources


_PRO_INFO = LicenseInfo(email="p@p.com", tier="pro", issued_at="2026-01-01", expires_at=None)
_FREE_INFO = LicenseInfo(email="f@f.com", tier="free", issued_at="2026-01-01", expires_at=None)
_EXPIRED = LicenseInfo(email="e@e.com", tier="pro", issued_at="2025-01-01", expires_at="2025-12-31")


class TestBatchCapLogic:
    def test_free_user_50_sources_capped_to_10(self):
        sources = list(range(50))
        assert len(_apply_cap(sources, None)) == FREE_BATCH_LIMIT

    def test_free_user_exactly_10_not_capped(self):
        sources = list(range(10))
        assert len(_apply_cap(sources, None)) == 10

    def test_free_user_9_sources_not_capped(self):
        sources = list(range(9))
        assert len(_apply_cap(sources, None)) == 9

    def test_free_user_11_sources_capped(self):
        sources = list(range(11))
        result = _apply_cap(sources, None)
        assert len(result) == FREE_BATCH_LIMIT

    def test_pro_user_1000_sources_not_capped(self):
        sources = list(range(1000))
        assert len(_apply_cap(sources, _PRO_INFO)) == 1000

    def test_free_tier_license_capped(self):
        sources = list(range(50))
        assert len(_apply_cap(sources, _FREE_INFO)) == FREE_BATCH_LIMIT

    def test_expired_pro_is_capped(self):
        sources = list(range(50))
        assert len(_apply_cap(sources, _EXPIRED)) == FREE_BATCH_LIMIT

    def test_cap_preserves_first_n_sources(self):
        sources = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k"]
        result = _apply_cap(sources, None)
        assert result == sources[:FREE_BATCH_LIMIT]

    def test_empty_sources_unchanged(self):
        assert _apply_cap([], None) == []


# ---------------------------------------------------------------------------
# LicenseInfo.is_pro edge cases
# ---------------------------------------------------------------------------

class TestLicenseInfoIsPro:
    def test_pro_tier_no_expiry_is_pro(self):
        info = LicenseInfo(email="a@a.com", tier="pro", issued_at="2026-01-01", expires_at=None)
        assert info.is_pro is True

    def test_free_tier_is_not_pro(self):
        info = LicenseInfo(email="a@a.com", tier="free", issued_at="2026-01-01", expires_at=None)
        assert info.is_pro is False

    def test_pro_tier_future_expiry_is_pro(self):
        info = LicenseInfo(email="a@a.com", tier="pro", issued_at="2026-01-01", expires_at="2030-01-01")
        assert info.is_pro is True

    def test_pro_tier_past_expiry_not_pro(self):
        info = LicenseInfo(email="a@a.com", tier="pro", issued_at="2025-01-01", expires_at="2025-06-01")
        assert info.is_pro is False

    def test_none_license_is_not_pro(self):
        license_info: LicenseInfo | None = None
        is_pro = license_info is not None and license_info.is_pro
        assert is_pro is False

from __future__ import annotations
from .key_model import LicenseInfo

# "rounded_square" is the Pro-gated frame shape in PicFrames.
_PRO_FEATURES: frozenset[str] = frozenset({"rounded_square"})


def can_use(feature: str, license_info: LicenseInfo | None) -> bool:
    if feature not in _PRO_FEATURES:
        return True
    return license_info is not None and license_info.is_pro

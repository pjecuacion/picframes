from __future__ import annotations
from .key_model import LicenseInfo

_PRO_FEATURES: frozenset[str] = frozenset({"rounded_square", "ico", "ai_removal"})
FREE_BATCH_LIMIT: int = 10


def can_use(feature: str, license_info: LicenseInfo | None) -> bool:
    if feature not in _PRO_FEATURES:
        return True
    return license_info is not None and license_info.is_pro

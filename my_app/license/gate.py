from __future__ import annotations
from .key_model import LicenseInfo

# TODO: Replace with the feature names your app gates behind Pro.
# Use the same string keys referenced in settings_card and option_builder.
_PRO_FEATURES: frozenset[str] = frozenset({"pro_feature"})


def can_use(feature: str, license_info: LicenseInfo | None) -> bool:
    if feature not in _PRO_FEATURES:
        return True
    return license_info is not None and license_info.is_pro

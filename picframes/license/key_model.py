from __future__ import annotations
from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class LicenseInfo:
    email: str
    tier: str
    issued_at: str
    expires_at: str | None  # None = lifetime license

    @property
    def is_active(self) -> bool:
        if self.expires_at is None:
            return True
        try:
            return date.today() <= date.fromisoformat(self.expires_at)
        except ValueError:
            return False

    @property
    def is_pro(self) -> bool:
        return self.tier == "pro" and self.is_active

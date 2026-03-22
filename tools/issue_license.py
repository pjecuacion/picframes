#!/usr/bin/env python3
"""Dev tool: generate a BulkWebP Pro license key.

Usage:
    python tools/issue_license.py user@example.com
    python tools/issue_license.py user@example.com --expires 2027-12-31

Required environment variable:
    BULK_WEBP_LICENSE_PRIVATE_KEY  — base64-encoded raw 32-byte Ed25519 private key.
    Store this key in a password manager or secrets vault.  Never commit it to source control.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
from datetime import date


def _load_private_key():
    raw_b64 = os.environ.get("BULK_WEBP_LICENSE_PRIVATE_KEY")
    if not raw_b64:
        sys.exit("Error: BULK_WEBP_LICENSE_PRIVATE_KEY env var is not set.")
    try:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
        return Ed25519PrivateKey.from_private_bytes(base64.b64decode(raw_b64))
    except Exception as exc:
        sys.exit(f"Error loading private key: {exc}")


def _validate_expiry(value: str) -> None:
    try:
        date.fromisoformat(value)
    except ValueError:
        sys.exit("Error: --expires must be in YYYY-MM-DD format.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Issue a BulkWebP Pro license key")
    parser.add_argument("email", help="Licensee email address")
    parser.add_argument(
        "--expires",
        metavar="YYYY-MM-DD",
        default=None,
        help="Optional expiry date (omit for a lifetime license)",
    )
    args = parser.parse_args()

    if args.expires:
        _validate_expiry(args.expires)

    private_key = _load_private_key()

    payload = {
        "email": args.email,
        "tier": "pro",
        "issued_at": date.today().isoformat(),
        "expires_at": args.expires,
    }
    payload_bytes = json.dumps(payload, separators=(",", ":")).encode()
    sig = private_key.sign(payload_bytes)

    payload_b64 = base64.urlsafe_b64encode(payload_bytes).decode().rstrip("=")
    sig_b64 = base64.urlsafe_b64encode(sig).decode().rstrip("=")

    print(f"{payload_b64}.{sig_b64}")


if __name__ == "__main__":
    main()

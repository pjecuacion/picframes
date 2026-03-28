#!/usr/bin/env python3
"""Dev tool: issue a free PicFrames Pro license key via LemonSqueezy.

Creates a $0 checkout URL pre-filled with the customer's email. Visiting the
URL completes a free order and delivers a real LemonSqueezy license key by
email, which works with the in-app activation flow.

Usage:
    python tools/issue_license.py user@example.com
    python tools/issue_license.py user@example.com --open

Required env vars (load from .env automatically):
    LEMONSQUEEZY_API_KEY
    LEMONSQUEEZY_STORE_ID
    LEMONSQUEEZY_VARIANT_ID
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
import webbrowser
from pathlib import Path


def _load_env() -> None:
    env_file = Path(__file__).parent.parent / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())


def _require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        sys.exit(f"Error: {name} env var is not set. Check your .env file.")
    return value


def _create_checkout(api_key: str, store_id: str, variant_id: str, email: str) -> str:
    """Create a $0 checkout pre-filled with `email`. Returns the checkout URL."""
    payload = json.dumps({
        "data": {
            "type": "checkouts",
            "attributes": {
                "custom_price": 0,
                "checkout_data": {"email": email},
                "product_options": {
                    "receipt_thank_you_note": "Thank you! Your PicFrames Pro license key is below.",
                },
            },
            "relationships": {
                "store": {"data": {"type": "stores", "id": str(store_id)}},
                "variant": {"data": {"type": "variants", "id": str(variant_id)}},
            },
        }
    }).encode()

    req = urllib.request.Request(
        "https://api.lemonsqueezy.com/v1/checkouts",
        data=payload,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/vnd.api+json",
            "Content-Type": "application/vnd.api+json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
    except urllib.error.HTTPError as exc:
        body = exc.read().decode(errors="replace")
        sys.exit(f"LemonSqueezy API error {exc.code}: {body}")
    except Exception as exc:
        sys.exit(f"Request failed: {exc}")

    return data["data"]["attributes"]["url"]


def main() -> None:
    _load_env()

    parser = argparse.ArgumentParser(
        description="Issue a free PicFrames Pro license key via LemonSqueezy"
    )
    parser.add_argument("email", help="Customer email address")
    parser.add_argument(
        "--open", action="store_true",
        help="Open the checkout URL in the browser automatically",
    )
    args = parser.parse_args()

    api_key = _require_env("LEMONSQUEEZY_API_KEY")
    store_id = _require_env("LEMONSQUEEZY_STORE_ID")
    variant_id = _require_env("LEMONSQUEEZY_VARIANT_ID")

    print(f"Creating free checkout for {args.email}...")
    url = _create_checkout(api_key, store_id, variant_id, args.email)

    print(f"\nCheckout URL:\n  {url}\n")
    print("Share this URL with the customer. Completing it delivers a license key by email.")

    if args.open:
        webbrowser.open(url)


if __name__ == "__main__":
    main()

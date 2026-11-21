#!/usr/bin/env python3
"""Generate and validate Happ profile, deep link, and synchronized README section."""

from __future__ import annotations

import argparse
import base64
import json
import re
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = Path("happ/MyRoute.template.json")
PROFILE = Path("happ/MyRoute.json")
LEGACY_PROFILE = Path("happ/ru-speede-vpn.json")
DEEPLINK = Path("happ/happ-routing-link.txt")
README = Path("README.md")
TOKEN = "{TIMESTAMP}"
BEGIN = "<!-- BEGIN_HAPP_LINK -->"
END = "<!-- END_HAPP_LINK -->"
README_PATTERN = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END), re.DOTALL)


class ProfileError(ValueError):
    """Raised when published files disagree with their canonical template."""


def render_profile(template_text: str, timestamp: int) -> dict[str, Any]:
    """Replace precisely four placeholders and return a canonical JSON object."""
    if not isinstance(timestamp, int) or timestamp <= 0:
        raise ProfileError("timestamp must be a positive integer (Unix UTC seconds)")
    if template_text.count(TOKEN) != 4:
        raise ProfileError("template must contain precisely four {TIMESTAMP} placeholders")
    try:
        profile = json.loads(template_text.replace(TOKEN, str(timestamp)))
    except json.JSONDecodeError as exc:
        raise ProfileError(f"invalid template JSON: {exc}") from exc
    if not isinstance(profile, dict):
        raise ProfileError("profile must be a JSON object")
    for field in ("Geoipurl", "Geositeurl"):
        value = profile.get(field)
        if not isinstance(value, str) or not value.endswith(f"?v={timestamp}"):
            raise ProfileError(f"{field} must end with ?v={timestamp}")
    for field in ("LastUpdated", "lastUpdatedDate"):
        if profile.get(field) != str(timestamp):
            raise ProfileError(f"{field} must equal the timestamp as a string")
    return profile


def canonical_json(profile: dict[str, Any]) -> str:
    return json.dumps(profile, ensure_ascii=False, separators=(",", ":"))


def create_deeplink(profile: dict[str, Any]) -> str:
    payload = canonical_json(profile).encode("utf-8")
    encoded = base64.b64encode(payload).decode("ascii")
    return f"happ://routing/add/{encoded}"


def readme_section(timestamp: int, deeplink: str) -> str:
    return (
        f"{BEGIN}\n"
        f"**Последнее обновление (Unix UTC):** `{timestamp}`\n\n"
        f"[**Быстрый импорт маршрутизации в Happ**]({deeplink})\n\n"
        "[Открыть deeplink текстом](happ/happ-routing-link.txt) · "
        "[JSON-профиль](happ/MyRoute.json)\n"
        f"{END}"
    )


def replace_readme_section(readme_text: str, section: str) -> str:
    if readme_text.count(BEGIN) != 1 or readme_text.count(END) != 1:
        raise ProfileError("README.md must contain exactly one BEGIN_HAPP_LINK/END_HAPP_LINK pair")
    updated, count = README_PATTERN.subn(lambda _: section, readme_text)
    if count != 1:
        raise ProfileError("README.md has malformed deeplink section")
    return updated


def load_template(root: Path) -> str:
    return (root / TEMPLATE).read_text(encoding="utf-8")


def generate(root: Path, timestamp: int) -> None:
    profile = render_profile(load_template(root), timestamp)
    deeplink = create_deeplink(profile)
    pretty_json = json.dumps(profile, ensure_ascii=False, indent=2) + "\n"
    updated_readme = replace_readme_section(
        (root / README).read_text(encoding="utf-8"),
        readme_section(timestamp, deeplink),
    )
    (root / PROFILE).write_text(pretty_json, encoding="utf-8")
    # Remove the obsolete compatibility copy when upgrading existing checkouts.
    (root / LEGACY_PROFILE).unlink(missing_ok=True)
    (root / DEEPLINK).write_text(deeplink + "\n", encoding="utf-8")
    (root / README).write_text(updated_readme, encoding="utf-8")


def check(root: Path) -> None:
    """Fail if timestamps, profiles, Base64, or README differ from the source."""
    if (root / LEGACY_PROFILE).exists():
        raise ProfileError(f"obsolete duplicate {LEGACY_PROFILE} must be removed")
    try:
        main = json.loads((root / PROFILE).read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ProfileError(f"{PROFILE} is not valid JSON: {exc}") from exc
    if not isinstance(main, dict):
        raise ProfileError(f"{PROFILE} must be a JSON object")
    ts = main.get("LastUpdated")
    if not isinstance(ts, str) or not re.fullmatch(r"[1-9][0-9]*", ts):
        raise ProfileError("LastUpdated must be a positive Unix timestamp string")
    expected = render_profile(load_template(root), int(ts))
    if main != expected:
        raise ProfileError(f"{PROFILE} differs from template or has unsynchronized timestamps")
    expected_deeplink = create_deeplink(expected)
    if (root / DEEPLINK).read_text(encoding="utf-8") != expected_deeplink + "\n":
        raise ProfileError(f"{DEEPLINK} is not the exact Base64 of the current JSON")
    readme_text = (root / README).read_text(encoding="utf-8")
    if replace_readme_section(readme_text, readme_section(int(ts), expected_deeplink)) != readme_text:
        raise ProfileError("README.md link block or timestamp does not match the published JSON")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify outputs without changing files")
    parser.add_argument("--root", type=Path, default=ROOT, help="repository root (for testing)")
    args = parser.parse_args(argv)
    try:
        if args.check:
            check(args.root)
            print("OK: Happ MyRoute.json, 4 timestamps, Base64 and README are synchronized")
        else:
            timestamp = int(time.time())
            generate(args.root, timestamp)
            print(f"Updated Happ profile and deeplink, Unix UTC timestamp: {timestamp}")
    except (ProfileError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Refresh local Legacy Survey documentation cache."""

from __future__ import annotations

import argparse
import pathlib
import re
import time
import urllib.error
import urllib.request

URL_MAP = {
    "status": "https://www.legacysurvey.org/status/",
    "dr10_description": "https://www.legacysurvey.org/dr10/description/",
    "dr10_files": "https://www.legacysurvey.org/dr10/files/",
    "dr10_catalogs": "https://www.legacysurvey.org/dr10/catalogs/",
    "dr10_bitmasks": "https://www.legacysurvey.org/dr10/bitmasks/",
    "dr10_issues": "https://www.legacysurvey.org/dr10/issues/",
    "viewer_urls": "https://www.legacysurvey.org/viewer/urls",
}


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download and cache Legacy Survey DR10 reference pages."
    )
    parser.add_argument(
        "--output-dir",
        default="references/cache",
        help="Directory for cached files (default: references/cache).",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=30,
        help="HTTP timeout in seconds (default: 30).",
    )
    parser.add_argument(
        "--sleep-seconds",
        type=float,
        default=1.0,
        help="Delay between requests in seconds (default: 1.0).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print targets without making network requests.",
    )
    return parser.parse_args()


def strip_html_to_text(html_text: str) -> str:
    no_script = re.sub(r"<script[\\s\\S]*?</script>", " ", html_text, flags=re.IGNORECASE)
    no_style = re.sub(r"<style[\\s\\S]*?</style>", " ", no_script, flags=re.IGNORECASE)
    no_tags = re.sub(r"<[^>]+>", " ", no_style)
    normalized = re.sub(r"\\s+", " ", no_tags)
    return normalized.strip()


def fetch_url(url: str, timeout_seconds: int) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Codex-LegacySurvey-Skill/1.0",
            "Accept": "text/html,application/xhtml+xml",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
        return response.read().decode("utf-8", errors="replace")


def write_cache_files(output_dir: pathlib.Path, name: str, html_text: str) -> None:
    html_path = output_dir / f"{name}.html"
    text_path = output_dir / f"{name}.txt"
    html_path.write_text(html_text, encoding="utf-8")
    text_path.write_text(strip_html_to_text(html_text), encoding="utf-8")


def main() -> int:
    arguments = parse_arguments()
    output_dir = pathlib.Path(arguments.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for index, (name, url) in enumerate(URL_MAP.items(), start=1):
        print(f"[{index}/{len(URL_MAP)}] {name}: {url}")
        if arguments.dry_run:
            continue
        try:
            html_text = fetch_url(url, arguments.timeout_seconds)
            write_cache_files(output_dir, name, html_text)
            print(f"  saved: {output_dir / (name + '.html')}")
            print(f"  saved: {output_dir / (name + '.txt')}")
        except urllib.error.URLError as error:
            print(f"  failed: {error}")
        if index < len(URL_MAP):
            time.sleep(arguments.sleep_seconds)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Pin the newest completed Shrimply macOS prerelease and verify its archive."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
from datetime import datetime
from urllib.request import Request, urlopen

REPOSITORY = "soirihiroka/shrimply"
ASSET_NAME = "shrimply-macos-arm64.zip"
TAG_PATTERN = re.compile(r"prerelease-(\d{8}T\d{6}Z)-([0-9a-f]{12})")
CASK = Path(__file__).resolve().parents[1] / "Casks/shrimply.rb"
PAGE_SIZE = 100


def fetch_releases():
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "soirihiroka-homebrew-tap",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token := os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {token}"
    releases = []
    page = 1
    while True:
        url = (
            f"https://api.github.com/repos/{REPOSITORY}/releases"
            f"?per_page={PAGE_SIZE}&page={page}"
        )
        with urlopen(Request(url, headers=headers), timeout=60) as response:
            batch = json.load(response)
        if not isinstance(batch, list):
            raise ValueError("GitHub did not return a release list")
        releases.extend(batch)
        if len(batch) < PAGE_SIZE:
            return releases
        page += 1


def latest_release(releases):
    candidates = []
    for release in releases:
        match = TAG_PATTERN.fullmatch(release.get("tag_name", ""))
        if release.get("draft") or not match:
            continue
        for asset in release.get("assets", []):
            if asset.get("name") == ASSET_NAME and asset.get("state") == "uploaded":
                timestamp = datetime.strptime(match[1], "%Y%m%dT%H%M%SZ")
                version = f"{timestamp:%Y%m%d%H%M%S},{match[2]}"
                candidates.append((version, release["tag_name"], asset))
    if not candidates:
        raise ValueError("No completed timestamped macOS prerelease was found")
    version, tag, asset = max(candidates, key=lambda item: item[0])
    digest = asset.get("digest") or ""
    if not re.fullmatch(r"sha256:[0-9a-f]{64}", digest):
        raise ValueError(f"{tag}: missing or invalid SHA-256 asset digest")
    url = f"https://github.com/{REPOSITORY}/releases/download/{tag}/{ASSET_NAME}"
    if asset.get("browser_download_url") != url:
        raise ValueError(f"{tag}: unexpected asset download URL")
    return version, digest.removeprefix("sha256:"), url


def verify_archive(url, expected_digest):
    digest = hashlib.sha256()
    # Do not send the GitHub API token to the asset host or its redirects.
    with urlopen(url, timeout=60) as response:
        while chunk := response.read(1024 * 1024):
            digest.update(chunk)
    if digest.hexdigest() != expected_digest:
        raise ValueError("Downloaded macOS archive does not match its SHA-256 digest")


def update(cask_path, release, *, check=False):
    version, digest, url = release
    original = cask_path.read_text()
    current = re.search(r'^  version "(\d{14},[0-9a-f]{12})"$', original, re.MULTILINE)
    if not current:
        raise ValueError("Cask does not contain the expected timestamped version")
    if version[:14] < current[1][:14]:
        print(f"Keeping {current[1]}; latest completed release is older ({version})")
        return False
    if version[:14] == current[1][:14] and version != current[1]:
        raise ValueError("Different commits share the same release timestamp")
    updated = original
    for field, value in (("version", version), ("sha256", digest)):
        updated, count = re.subn(
            rf'^  {field} "[^"\n]+"$',
            lambda _match: f'  {field} "{value}"',
            updated,
            flags=re.MULTILINE,
        )
        if count != 1:
            raise ValueError(f"Expected exactly one {field} stanza")
    changed = updated != original
    if changed and version == current[1]:
        raise ValueError("Pinned release metadata changed without a new version")
    if changed or check:
        verify_archive(url, digest)
    if changed:
        if check:
            print(f"Update available: {current[1]} -> {version}")
        else:
            cask_path.write_text(updated)
            print(f"Updated Shrimply: {current[1]} -> {version}")
    else:
        print(f"Shrimply is current: {version}")
    return changed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true",
        help="verify the archive without editing files; exit 1 if an update is available",
    )
    args = parser.parse_args()
    changed = update(CASK, latest_release(fetch_releases()), check=args.check)
    return 1 if args.check and changed else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, TypeError) as error:
        sys.exit(f"Shrimply update failed: {error}")

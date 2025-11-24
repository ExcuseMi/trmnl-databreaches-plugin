#!/usr/bin/env python3
import os
import json
import requests
from pathlib import Path

API_URL = "https://haveibeenpwned.com/api/v3/breaches"

# Determine repo root
SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
OUTPUT_FILE = ROOT_DIR / "data" / "breaches.json"

# Only store fields used by the Liquid templates
USED_FIELDS = {
    "Title",
    "LogoPath",
    "AddedDate",
    "PwnCount",
    "Description",
    "DataClasses",
}

def fetch_latest_breaches():
    headers = {
        "User-Agent": "GitHub Action Fetch Script"
    }

    response = requests.get(API_URL, headers=headers, timeout=20)
    response.raise_for_status()
    breaches = response.json()

    # Sort by AddedDate descending (newest first)
    breaches.sort(key=lambda b: b.get("AddedDate", ""), reverse=True)

    # Keep only the first 30
    breaches = breaches[:30]

    # Strip unused fields
    minimized = []
    for b in breaches:
        minimized.append({k: b.get(k) for k in USED_FIELDS})

    return minimized

def save_breaches_to_file(breaches):
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(breaches, f, indent=2, ensure_ascii=False)

def main():
    breaches = fetch_latest_breaches()
    save_breaches_to_file(breaches)
    print(f"Saved {len(breaches)} minimized breaches to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

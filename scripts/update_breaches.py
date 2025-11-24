#!/usr/bin/env python3
import os
import json
import requests
from pathlib import Path

API_URL = "https://haveibeenpwned.com/api/v3/breaches"

# Determine repo root (parent of the "scripts" folder)
SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
OUTPUT_FILE = ROOT_DIR / "data" / "breaches.json"

def fetch_latest_breaches():
    headers = {
        "User-Agent": "GitHub Action Fetch Script"
    }

    response = requests.get(API_URL, headers=headers, timeout=20)
    response.raise_for_status()

    breaches = response.json()
    return breaches[:30]  # Take latest 30

def save_breaches_to_file(breaches):
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(breaches, file, indent=2, ensure_ascii=False)

def main():
    breaches = fetch_latest_breaches()
    save_breaches_to_file(breaches)
    print(f"Saved {len(breaches)} breaches to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

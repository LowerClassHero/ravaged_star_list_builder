"""
Ravaged Star — Data Updater
============================
Run this whenever you update a faction JSON file.

Usage:
    python update_data.py

Expected folder structure:
    update_data.py                  ← this file
    ravaged_star_builder.html       ← the app (gets patched in place)
    data/
        Veil_Touched.json
        Immari.json
        Gorkog.json
        Steel_Specters.json
        Mercenaries.json
"""

import json
import re
import os

DATA_DIR  = os.path.join(os.path.dirname(__file__), "data")
HTML_FILE = os.path.join(os.path.dirname(__file__), "ravaged_star_builder.html")

FILES = [
    "Veil_Touched.json",
    "Immari.json",
    "Gorkog.json",
    "Steel_Specters.json",
    "Mercenaries.json",
]

# Merge all faction files into one dict
db = {}
for filename in FILES:
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        print(f"  WARNING: {filename} not found — skipping.")
        continue
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    db.update(data)
    print(f"  Loaded {filename} ({len(data)} units)")

print(f"\n  Total: {len(db)} units")

# Patch the UNIT_DB line in the HTML
html = open(HTML_FILE, encoding="utf-8").read()
new_db = f"const UNIT_DB = {json.dumps(db, separators=(',', ':'), ensure_ascii=False)};"
html = re.sub(r"const UNIT_DB = \{.*?\};", new_db, html, flags=re.DOTALL)
open(HTML_FILE, "w", encoding="utf-8").write(html)

print(f"  Done — ravaged_star_builder.html updated.")

#!/usr/bin/env python3
"""
Add "Last updated: April 1, 2026" stamp to all /fix/ pages
Inserted just below the h1, before the lead paragraph
"""
import os, re
from datetime import datetime

STAMP = '<p style="font-size:11px;color:var(--muted);margin-bottom:16px">Last updated: April 1, 2026 &middot; <a href="https://osv.dev" target="_blank" rel="noopener" style="color:var(--muted)">Data: OSV Database</a></p>'

updated = 0
skipped = 0
already = 0

for root, dirs, files in os.walk("seo/fix"):
    dirs[:] = [d for d in dirs if d not in ["__pycache__"]]
    for fname in files:
        if fname != "index.html":
            continue
        filepath = os.path.join(root, fname)
        with open(filepath, encoding="utf-8") as f:
            content = f.read()

        # Skip if already has a last updated stamp
        if "Last updated:" in content:
            already += 1
            continue

        # Insert after the first </h1>
        if "</h1>" in content:
            content = content.replace("</h1>", "</h1>\n" + STAMP, 1)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            updated += 1
        else:
            skipped += 1

print(f"Updated:        {updated} pages")
print(f"Already had:    {already} pages")
print(f"Skipped (no h1): {skipped} pages")
print(f"Total /fix/ pages processed: {updated + already + skipped}")

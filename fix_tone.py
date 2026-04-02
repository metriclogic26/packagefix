#!/usr/bin/env python3
"""
Tone fixes across all pages:
1. Replace "recommended" with direct language
2. Simplify competitive comparison language
"""
import os, re

REPLACEMENTS = [
    # "recommended" → direct language
    ("Recommended configuration", "Configuration fix"),
    ("recommended configuration", "configuration fix"),
    ("Recommended Changes", "Changes"),
    ("recommended changes", "changes"),
    ("recommended version", "safe version"),
    ("Recommended version", "Safe version"),
    ("recommended fix", "fix"),
    ("Recommended fix", "Fix"),
    ("recommended upgrade", "upgrade"),
    ("recommended to upgrade", "upgrade"),
    ("We recommend upgrading", "Upgrade"),
    ("we recommend upgrading", "upgrade"),
    ("We recommend", "Upgrade"),
    ("we recommend", "upgrade"),
    ("It is recommended", "Upgrade"),
    ("is recommended that", "is best to"),
    ("Users are strongly advised", "Upgrade"),
    ("strongly advised to upgrade", "upgrade"),
    ("strongly recommended", "important"),
    ("is strongly recommended", "is important"),

    # Competitive tone — soften without removing facts
    ("Snyk and Dependabot can't", "Snyk and Dependabot don't support"),
    ("Works where Snyk and Dependabot don't support",
     "Works where Snyk and Dependabot don't"),
    ("Neither Snyk nor Dependabot", "Snyk and Dependabot"),
    ("unlike Snyk", "unlike tools that require GitHub"),
    ("Unlike Snyk", "Unlike tools that require GitHub"),
]

updated_files = 0
updated_replacements = 0

# Process all html files
for root, dirs, files in os.walk("seo"):
    dirs[:] = [d for d in dirs if d not in ["__pycache__"]]
    for fname in files:
        if fname != "index.html":
            continue
        filepath = os.path.join(root, fname)
        with open(filepath, encoding="utf-8") as f:
            content = f.read()
        original = content
        for old, new in REPLACEMENTS:
            content = content.replace(old, new)
        if content != original:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            updated_files += 1

# Also fix index.html (main tool)
if os.path.exists("index.html"):
    with open("index.html", encoding="utf-8") as f:
        content = f.read()
    original = content
    for old, new in REPLACEMENTS:
        content = content.replace(old, new)
    if content != original:
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(content)
        updated_files += 1
        print("  index.html updated")

print(f"Updated {updated_files} files")
print("Done")

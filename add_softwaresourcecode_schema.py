#!/usr/bin/env python3
"""
Add SoftwareSourceCode schema to all /fix/ pages
Targets every <pre> code block and wraps it with schema
Also adds to blog posts with code blocks
"""
import os, json, re

BASE_URL = "https://packagefix.dev"

def add_schema_to_page(filepath, page_url):
    with open(filepath, encoding='utf-8') as f:
        content = f.read()

    # Find all <pre> blocks
    pre_blocks = re.findall(r'<pre>(.*?)</pre>', content, re.DOTALL)
    if not pre_blocks:
        return False

    # Build SoftwareSourceCode items for each code block
    code_items = []
    for i, code in enumerate(pre_blocks):
        # Clean HTML tags from code for schema
        clean = re.sub(r'<[^>]+>', '', code).strip()
        if len(clean) < 10:
            continue

        # Detect language from content
        if 'npm install' in clean or 'package.json' in clean or 'node_modules' in clean:
            lang = "javascript"
        elif 'pip install' in clean or 'requirements.txt' in clean or 'import ' in clean:
            lang = "python"
        elif 'bundle install' in clean or "gem '" in clean or 'Gemfile' in clean:
            lang = "ruby"
        elif 'composer' in clean or 'php' in clean.lower():
            lang = "php"
        elif 'go mod' in clean or 'golang.org' in clean:
            lang = "go"
        elif 'cargo' in clean or 'Cargo.toml' in clean:
            lang = "rust"
        elif 'mvn' in clean or 'pom.xml' in clean or '<dependency>' in clean:
            lang = "java"
        elif 'grep' in clean or 'curl' in clean or 'git ' in clean:
            lang = "bash"
        else:
            lang = "bash"

        code_items.append({
            "@type": "SoftwareSourceCode",
            "codeSampleType": "full solution",
            "programmingLanguage": lang,
            "text": clean[:500]
        })

    if not code_items:
        return False

    # Find existing ld+json block
    pattern = re.compile(
        r'<script type="application/ld\+json">(.*?)</script>',
        re.DOTALL
    )
    match = pattern.search(content)

    if match:
        try:
            existing = json.loads(match.group(1))
        except:
            return False

        # Remove old SoftwareSourceCode entries
        if "@graph" in existing:
            existing["@graph"] = [
                s for s in existing["@graph"]
                if s.get("@type") != "SoftwareSourceCode"
            ]
            # Add new ones
            existing["@graph"].extend(code_items)
        else:
            existing = {
                "@context": "https://schema.org",
                "@graph": [existing] + code_items
            }

        new_script = (
            '<script type="application/ld+json">'
            + json.dumps(existing, indent=2)
            + '</script>'
        )
        content = pattern.sub(lambda m: new_script, content, count=1)
    else:
        new_schema = {
            "@context": "https://schema.org",
            "@graph": code_items
        }
        new_script = (
            '<script type="application/ld+json">'
            + json.dumps(new_schema, indent=2)
            + '</script>'
        )
        content = content.replace('</head>', new_script + '\n</head>', 1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return True


# Find all fix pages + blog pages
def get_target_files():
    targets = []
    for root, dirs, files in os.walk('seo'):
        # Skip non-content dirs
        dirs[:] = [d for d in dirs if d not in ['__pycache__']]
        for fname in files:
            if fname != 'index.html':
                continue
            filepath = os.path.join(root, fname)
            slug = filepath.replace('seo/', '/').replace('/index.html', '')

            # Target: fix pages, blog pages, kev pages, glossary pages
            if any(slug.startswith(p) for p in ['/fix/', '/blog/', '/kev/', '/guides/']):
                targets.append((filepath, slug))
    return targets

print("Finding target pages...")
targets = get_target_files()
print(f"Found {len(targets)} candidate pages")

updated = 0
skipped = 0
for filepath, slug in targets:
    result = add_schema_to_page(filepath, BASE_URL + slug)
    if result:
        updated += 1
    else:
        skipped += 1

print(f"\nDone:")
print(f"  Updated: {updated} pages")
print(f"  Skipped (no code blocks): {skipped} pages")

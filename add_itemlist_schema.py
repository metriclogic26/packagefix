#!/usr/bin/env python3
"""
Add carousel-optimised ItemList schema to 3 PackageFix pages:
1. /cisa-kev
2. /fix/npm/lodash  
3. /compare/snyk-vs-dependabot
"""
import json, re, os

BASE_URL = "https://packagefix.dev"

def inject_schema(filepath, new_schema):
    with open(filepath) as f:
        content = f.read()
    
    # Find existing ld+json block and replace it
    old_pattern = re.compile(
        r'<script type="application/ld\+json">.*?</script>',
        re.DOTALL
    )
    
    # Build new schema block with merged schemas
    existing = old_pattern.search(content)
    if existing:
        try:
            existing_data = json.loads(
                existing.group().replace('<script type="application/ld+json">', '')
                .replace('</script>', '').strip()
            )
            # Merge — add new schema to existing @graph
            if "@graph" in existing_data:
                existing_data["@graph"].append(new_schema)
            else:
                existing_data = {"@context": "https://schema.org", "@graph": [existing_data, new_schema]}
        except:
            existing_data = {"@context": "https://schema.org", "@graph": [new_schema]}
    else:
        existing_data = {"@context": "https://schema.org", "@graph": [new_schema]}
    
    new_script = '<script type="application/ld+json">' + json.dumps(existing_data, indent=2) + '</script>'
    
    if existing:
        content = old_pattern.sub(lambda m: new_script, content, count=1)
    else:
        content = content.replace('</head>', new_script + '\n</head>', 1)
    
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"  ✓ Updated {filepath}")

# ══════════════════════════════════════════════════════════════════════
# 1. /cisa-kev — Ordered list of actively exploited packages
# ══════════════════════════════════════════════════════════════════════

CISA_PACKAGES = [
    ("lodash", "npm", "CVE-2020-8203", "/fix/npm/lodash"),
    ("qs", "npm", "CVE-2022-24999", "/fix/npm/qs"),
    ("minimist", "npm", "CVE-2021-44906", "/fix/npm/minimist"),
    ("tough-cookie", "npm", "CVE-2023-26136", "/fix/npm/tough-cookie"),
    ("axios", "npm", "CVE-2023-45857", "/fix/npm/axios"),
    ("jsonwebtoken", "npm", "CVE-2022-23540", "/fix/npm/jsonwebtoken"),
    ("vm2", "npm", "CVE-2023-29017", "/fix/npm/vm2"),
    ("sharp", "npm", "CVE-2023-4863", "/fix/npm/sharp"),
    ("semver", "npm", "CVE-2022-25883", "/fix/npm/semver"),
    ("Django", "PyPI", "CVE-2024-27351", "/fix/pypi/django"),
    ("requests", "PyPI", "CVE-2023-32681", "/fix/pypi/requests"),
    ("Jinja2", "PyPI", "CVE-2024-34064", "/fix/pypi/jinja2"),
    ("PyYAML", "PyPI", "CVE-2020-14343", "/fix/pypi/pyyaml"),
    ("Nokogiri", "Ruby", "CVE-2022-24836", "/fix/ruby/nokogiri"),
    ("Rack", "Ruby", "CVE-2023-27530", "/fix/ruby/rack"),
    ("OmniAuth", "Ruby", "CVE-2015-9284", "/fix/ruby/omniauth"),
    ("Flysystem", "PHP", "CVE-2021-32708", "/fix/php/flysystem"),
    ("Dompdf", "PHP", "CVE-2021-3838", "/fix/php/dompdf"),
    ("gRPC-Go", "Go", "CVE-2023-44487", "/fix/go/grpc"),
    ("hyper", "Rust", "CVE-2023-44487", "/fix/rust/hyper"),
    ("openssl", "Rust", "CVE-2023-0286", "/fix/rust/openssl"),
    ("Log4j", "Java", "CVE-2021-44228", "/fix/java/log4j"),
    ("Spring", "Java", "CVE-2022-22965", "/fix/java/spring-core"),
    ("SnakeYAML", "Java", "CVE-2022-1471", "/fix/java/snakeyaml"),
]

cisa_schema = {
    "@type": "ItemList",
    "name": "CISA KEV Open Source Packages — Actively Exploited",
    "description": "Open source packages on the CISA Known Exploited Vulnerabilities catalog, confirmed actively exploited in real attacks.",
    "numberOfItems": len(CISA_PACKAGES),
    "itemListOrder": "https://schema.org/ItemListOrderDescending",
    "itemListElement": [
        {
            "@type": "ListItem",
            "position": i + 1,
            "name": f"{pkg} ({eco}) — {cve}",
            "url": BASE_URL + url
        }
        for i, (pkg, eco, cve, url) in enumerate(CISA_PACKAGES)
    ]
}

# ══════════════════════════════════════════════════════════════════════
# 2. /fix/npm/lodash — CVE history as ordered list
# ══════════════════════════════════════════════════════════════════════

LODASH_CVES = [
    ("CVE-2018-3721", "Prototype pollution via merge()", "/kev/CVE-2020-8203"),
    ("CVE-2018-16487", "Prototype pollution via defaultsDeep()", "/fix/npm/lodash"),
    ("CVE-2019-10744", "Prototype pollution via zipObjectDeep()", "/fix/npm/lodash"),
    ("CVE-2020-8203", "Prototype pollution via zipper merge — CISA KEV", "/kev/CVE-2020-8203"),
    ("CVE-2020-28500", "ReDoS via toNumber()", "/fix/npm/lodash"),
    ("CVE-2021-23337", "Command injection via template()", "/kev/CVE-2021-23337"),
]

lodash_schema = {
    "@type": "ItemList",
    "name": "All lodash CVEs — Complete Vulnerability History",
    "description": "Complete list of known security vulnerabilities in the lodash npm package, including 2 CISA KEV entries.",
    "numberOfItems": len(LODASH_CVES),
    "itemListOrder": "https://schema.org/ItemListOrderAscending",
    "itemListElement": [
        {
            "@type": "ListItem",
            "position": i + 1,
            "name": f"{cve} — {desc}",
            "url": BASE_URL + url
        }
        for i, (cve, desc, url) in enumerate(LODASH_CVES)
    ]
}

# ══════════════════════════════════════════════════════════════════════
# 3. /compare/snyk-vs-dependabot — Feature comparison as ItemList
# ══════════════════════════════════════════════════════════════════════

snyk_schema = {
    "@type": "ItemList",
    "name": "Snyk vs Dependabot vs PackageFix — Feature Comparison",
    "description": "Comparison of Snyk, Dependabot, and PackageFix for dependency security scanning. Key differences: browser access, fix output, CISA KEV integration.",
    "numberOfItems": 3,
    "itemListOrder": "https://schema.org/ItemListUnordered",
    "itemListElement": [
        {
            "@type": "ListItem",
            "position": 1,
            "name": "PackageFix — Browser-based, downloads fixed manifest, CISA KEV flags, 7 ecosystems, free",
            "url": BASE_URL
        },
        {
            "@type": "ListItem",
            "position": 2,
            "name": "Snyk — Requires account and GitHub connection, checker only, paid plans",
            "url": BASE_URL + "/compare/snyk-vs-dependabot"
        },
        {
            "@type": "ListItem",
            "position": 3,
            "name": "Dependabot — GitHub bot only, opens PRs automatically, no browser tool",
            "url": BASE_URL + "/compare/snyk-vs-dependabot"
        }
    ]
}

# ══════════════════════════════════════════════════════════════════════
# Apply all three
# ══════════════════════════════════════════════════════════════════════

print("\n🔧 Adding carousel ItemList schemas...")

files = [
    ("seo/cisa-kev/index.html", cisa_schema),
    ("seo/fix/npm/lodash/index.html", lodash_schema),
    ("seo/compare/snyk-vs-dependabot/index.html", snyk_schema),
]

for filepath, schema in files:
    if os.path.exists(filepath):
        inject_schema(filepath, schema)
    else:
        print(f"  ✗ Not found: {filepath}")

print("\n✅ Done — 3 pages updated with carousel-optimised ItemList schema")
print("\nSubmit these for URL inspection after pushing:")
for filepath, _ in files:
    slug = filepath.replace("seo/", "/").replace("/index.html", "")
    print(f"  {BASE_URL}{slug}")

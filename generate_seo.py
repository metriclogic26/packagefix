#!/usr/bin/env python3
"""
PackageFix — Programmatic SEO Page Generator — Phase 1 (65 pages)
Run: python3 generate_seo.py
Output: ./seo/ directory with all pages + vercel.json + llm.txt + sitemap-seo.xml
"""

import os, json

BASE_URL = "https://packagefix.dev"

TOKENS = """
:root {
  --bg:#0B0D14; --surface:#12151F; --surface2:#1A1D2E;
  --border:#252836; --purple:#6C63FF; --green:#22C55E;
  --orange:#F97316; --red:#EF4444; --yellow:#EAB308;
  --text:#E2E4F0; --muted:#6B7280;
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--text);font-family:'JetBrains Mono',monospace;font-size:13px;line-height:1.6;min-height:100vh}
a{color:var(--purple);text-decoration:none}
a:hover{text-decoration:underline}
.site-header{border-bottom:1px solid var(--border);padding:14px 24px;display:flex;align-items:center;justify-content:space-between}
.logo{font-size:15px;font-weight:700;color:var(--text)}
.logo span{color:var(--purple)}
.nav-links{display:flex;gap:20px;font-size:12px}
.nav-links a{color:var(--muted)}
.nav-links a:hover{color:var(--text);text-decoration:none}
.container{max-width:860px;margin:0 auto;padding:48px 24px}
.breadcrumb{font-size:11px;color:var(--muted);margin-bottom:24px;display:flex;gap:6px;flex-wrap:wrap}
.breadcrumb a{color:var(--muted)}
h1{font-size:clamp(18px,3vw,26px);font-weight:700;margin-bottom:12px;line-height:1.3}
h2{font-size:14px;font-weight:600;margin:32px 0 12px}
h3{font-size:11px;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.08em;margin:24px 0 8px}
p{color:var(--muted);margin-bottom:12px;font-size:12px;line-height:1.7}
.lead{color:var(--text);font-size:13px;margin-bottom:24px;line-height:1.7}
.problem-box{background:rgba(239,68,68,.08);border:1px solid rgba(239,68,68,.3);border-left:3px solid var(--red);border-radius:8px;padding:16px 20px;margin:20px 0}
.problem-box .label{font-size:10px;font-weight:700;color:var(--red);text-transform:uppercase;letter-spacing:.1em;margin-bottom:8px}
.fix-box{background:rgba(34,197,94,.08);border:1px solid rgba(34,197,94,.3);border-left:3px solid var(--green);border-radius:8px;padding:16px 20px;margin:20px 0}
.fix-box .label{font-size:10px;font-weight:700;color:var(--green);text-transform:uppercase;letter-spacing:.1em;margin-bottom:8px}
pre{background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:14px 16px;overflow-x:auto;font-size:11px;line-height:1.6;margin:8px 0;white-space:pre-wrap}
code{background:var(--surface);border:1px solid var(--border);border-radius:3px;padding:1px 5px;font-size:11px}
.cta-box{background:var(--surface);border:1px solid var(--purple);border-radius:10px;padding:24px;margin:32px 0;text-align:center}
.cta-box p{color:var(--text);font-size:13px;margin-bottom:16px}
.cta-btn{display:inline-block;background:var(--purple);color:#fff;font-family:'JetBrains Mono',monospace;font-size:13px;font-weight:600;padding:12px 28px;border-radius:7px;text-decoration:none}
.cta-btn:hover{opacity:.9;text-decoration:none}
.badge{display:inline-block;font-size:10px;font-weight:700;padding:2px 8px;border-radius:4px;text-transform:uppercase;letter-spacing:.05em}
.badge-red{background:rgba(239,68,68,.2);color:var(--red);border:1px solid var(--red)}
.badge-orange{background:rgba(249,115,22,.2);color:var(--orange);border:1px solid var(--orange)}
.badge-green{background:rgba(34,197,94,.2);color:var(--green);border:1px solid var(--green)}
.badge-purple{background:rgba(108,99,255,.2);color:var(--purple);border:1px solid var(--purple)}
.faq{margin:40px 0}
.faq-item{border-bottom:1px solid var(--border);padding:16px 0}
.faq-item:last-child{border-bottom:none}
.faq-q{font-size:12px;font-weight:600;color:var(--text);margin-bottom:8px}
.faq-a{font-size:12px;color:var(--muted);line-height:1.7}
.related-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px;margin-top:12px}
.related-card{background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:14px}
.related-card a{color:var(--text);font-size:12px;font-weight:500}
.related-card p{font-size:11px;color:var(--muted);margin:4px 0 0}
.site-footer{border-top:1px solid var(--border);padding:24px;text-align:center;font-size:11px;color:var(--muted);margin-top:60px}
.site-footer a{color:var(--muted)}
table{width:100%;border-collapse:collapse;margin:16px 0;font-size:12px}
th{text-align:left;padding:8px 12px;border-bottom:1px solid var(--border);color:var(--muted);font-weight:600;font-size:10px;text-transform:uppercase;letter-spacing:.08em}
td{padding:8px 12px;border-bottom:1px solid var(--border)}
tr:last-child td{border-bottom:none}
.vs-table td:first-child{font-weight:600;color:var(--text)}
@media(max-width:640px){.nav-links{display:none}.related-grid{grid-template-columns:1fr}}
"""

def render_page(title, desc, canonical_path, breadcrumbs, body_html, schemas):
    canonical = BASE_URL + canonical_path
    schema_json = json.dumps({"@context":"https://schema.org","@graph": schemas}, indent=2)
    crumb_html = " <span>/</span> ".join(
        f'<a href="{u}">{n}</a>' if u else n
        for n, u in breadcrumbs
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary">
<link rel="icon" type="image/svg+xml" href="/icon.svg">
<link rel="icon" type="image/png" sizes="512x512" href="/icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<script type="application/ld+json">{schema_json}</script>
<style>{TOKENS}</style>
</head>
<body>
<header class="site-header">
  <a href="https://packagefix.dev" class="logo">Package<span>Fix</span></a>
  <nav class="nav-links">
    <a href="https://packagefix.dev">Tool</a>
    <a href="https://packagefix.dev/alternatives">Alternatives</a>
    <a href="https://packagefix.dev/error">Error Fixes</a>
    <a href="https://github.com/metriclogic26/packagefix">GitHub</a>
    <a href="https://packagefix.dev">PackageFix</a>
  </nav>
</header>
<main class="container">
  <div class="breadcrumb">{crumb_html}</div>
  {body_html}
</main>
<footer class="site-footer">
  <p>PackageFix · <a href="https://packagefix.dev">packagefix.dev</a> · MIT Licensed · Open Source</p>
  <p style="margin-top:6px">Part of the MetricLogic network ·
  <a href="https://configclarity.dev">ConfigClarity</a> ·
  <a href="https://domainpreflight.dev">DomainPreflight</a></p>
  <p style="margin-top:6px">Vulnerability data: <a href="https://osv.dev">OSV Database</a> · <a href="https://www.cisa.gov/known-exploited-vulnerabilities-catalog">CISA KEV Catalog</a></p>
  <p style="margin-top:6px">Always test dependency updates in a staging environment before deploying to production.</p>
</footer>
</body>
</html>"""

def cta():
    return """<div class="cta-box">
  <p>Scan your dependencies now — paste your manifest, get a fixed version back in seconds.</p>
  <a href="https://packagefix.dev" class="cta-btn">Open PackageFix →</a>
  <p style="margin-top:12px;font-size:11px;color:var(--muted)">No signup · No CLI · No GitHub connection · Runs 100% in your browser</p>
</div>"""

def faq_html(faqs):
    items = "".join(f'<div class="faq-item"><div class="faq-q">{q}</div><div class="faq-a">{a}</div></div>' for q,a in faqs)
    return f'<div class="faq"><h2>Frequently Asked Questions</h2>{items}</div>'

def related_html(pages):
    cards = "".join(f'<div class="related-card"><a href="{p["url"]}">{p["title"]}</a><p>{p["desc"]}</p></div>' for p in pages)
    return f'<div style="margin:40px 0"><h2>Related Guides</h2><div class="related-grid">{cards}</div></div>'

def howto_schema(name, desc, steps, url, breadcrumbs_schema):
    return [
        {"@type":"HowTo","name":name,"description":desc,
         "estimatedCost":{"@type":"MonetaryAmount","currency":"USD","value":"0"},
         "supply":{"@type":"HowToSupply","name":"manifest file"},
         "tool":{"@type":"HowToTool","name":"PackageFix","url":"https://packagefix.dev"},
         "step":[{"@type":"HowToStep","name":s["name"],"text":s["text"]} for s in steps]},
        {"@type":"BreadcrumbList","itemListElement":[
            {"@type":"ListItem","position":i+1,"name":n,"item":BASE_URL+u if u else BASE_URL}
            for i,(n,u) in enumerate(breadcrumbs_schema)
        ]}
    ]

def faq_schema(faqs):
    return {"@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}}
        for q,a in faqs
    ]}

# ══════════════════════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════════════════════

ECOSYSTEMS = {
    "npm":    {"label":"npm","file":"package.json","cmd":"npm install","lang":"Node.js","ext":"json"},
    "pypi":   {"label":"PyPI","file":"requirements.txt","cmd":"pip install -r requirements.txt","lang":"Python","ext":"txt"},
    "ruby":   {"label":"Ruby","file":"Gemfile","cmd":"bundle install","lang":"Ruby","ext":""},
    "php":    {"label":"PHP","file":"composer.json","cmd":"composer install","lang":"PHP","ext":"json"},
    "go":     {"label":"Go","file":"go.mod","cmd":"go mod tidy","lang":"Go","ext":""},
    "rust":   {"label":"Rust","file":"Cargo.toml","cmd":"cargo update","lang":"Rust","ext":"toml"},
    "java":   {"label":"Java","file":"pom.xml","cmd":"mvn dependency:resolve","lang":"Java/Maven","ext":"xml"},
}

# ── Fix pages ──────────────────────────────────────────────────────────────────
FIX_PAGES = [
    {"slug":"fix/npm/outdated-dependencies","eco":"npm",
     "title":"Fix Outdated npm Dependencies — Update package.json",
     "desc":"Find and fix outdated npm dependencies with known CVEs. Paste your package.json and get a patched version — no CLI, no signup.",
     "h1":"Fix Outdated npm Dependencies",
     "problem":"Your package.json contains outdated dependencies with known CVEs. npm outdated shows what's stale but doesn't generate the fixed file.",
     "bad":'{\n  "dependencies": {\n    "express": "4.17.1",\n    "lodash": "4.17.15"\n  }\n}',
     "fix":'{\n  "dependencies": {\n    "express": "4.19.2",\n    "lodash": "4.17.21"\n  }\n}',
     "fix_note":"Update to the safe versions reported by OSV. Run npm install to regenerate package-lock.json.",
     "faqs":[
        ("How do I find outdated npm packages with CVEs?","Run npm audit, or paste your package.json into PackageFix for a live CVE scan with fix versions from OSV."),
        ("Is it safe to update all npm dependencies at once?","Patch and minor updates (4.17.1 → 4.17.21) are generally safe. Major version bumps may have breaking changes — review changelogs first."),
        ("What is the difference between npm outdated and npm audit?","npm outdated shows all available updates. npm audit shows only CVE-flagged packages. PackageFix combines both: CVE scan + fix versions in one step."),
        ("How often should I update npm dependencies?","At minimum monthly, and immediately when CISA adds a package to the KEV catalog.")
     ]},
    {"slug":"fix/npm/critical-cve","eco":"npm",
     "title":"Fix Critical npm CVE — Patch High-Severity Vulnerabilities",
     "desc":"Fix CRITICAL and HIGH severity CVEs in your npm dependencies. Paste package.json, get the exact patched version to download.",
     "h1":"Fix Critical npm CVEs",
     "problem":"npm audit reports CRITICAL or HIGH severity vulnerabilities but provides no fixed manifest to download. You have to manually find safe versions and edit the file.",
     "bad":'{\n  "dependencies": {\n    "axios": "0.21.1",\n    "jsonwebtoken": "8.5.1"\n  }\n}',
     "fix":'{\n  "dependencies": {\n    "axios": "1.7.4",\n    "jsonwebtoken": "9.0.0"\n  }\n}',
     "fix_note":"axios 0.21.1 is affected by CVE-2023-45857 (HIGH). jsonwebtoken 8.5.1 is affected by CVE-2022-23540 (CRITICAL). Update to the safe versions above.",
     "faqs":[
        ("What does CRITICAL mean in npm audit?","CRITICAL severity means a CVSS score ≥ 9.0. These vulnerabilities can often be exploited remotely with no authentication. Fix immediately."),
        ("How do I fix a critical vulnerability in a transitive dependency?","Use npm overrides in package.json to force a safe version: {\"overrides\": {\"vulnerable-package\": \"safe-version\"}}. PackageFix generates this override block automatically."),
        ("Does CISA KEV include npm packages?","Yes. Several npm packages (lodash, axios, jsonwebtoken) have appeared on CISA's Known Exploited Vulnerabilities catalog. PackageFix flags these with a red KEV badge."),
        ("How do I verify a CVE fix was applied?","After updating, run npm audit again. If the CVE ID is gone, the fix is applied. PackageFix shows a 'Re-scan' button to verify live.")
     ]},
    {"slug":"fix/npm/transitive-vulnerability","eco":"npm",
     "title":"Fix Transitive npm Vulnerability — Indirect Dependency CVEs",
     "desc":"Fix CVEs in indirect/transitive npm dependencies. Paste package-lock.json to scan the full dependency tree and get override snippets.",
     "h1":"Fix Transitive npm Vulnerabilities",
     "problem":"npm audit flags a vulnerability in a package you never directly installed. It exists inside a dependency of a dependency. npm audit fix often can't resolve it automatically.",
     "bad":'# Your app depends on auth-lib@1.0.0\n# auth-lib depends on qs@6.5.2\n# qs@6.5.2 is affected by CVE-2022-24999 (HIGH)',
     "fix":'{\n  "overrides": {\n    "qs": "6.11.0"\n  }\n}',
     "fix_note":"Add the overrides block to package.json to force npm to use the safe version of qs regardless of what auth-lib requests. Drop your package-lock.json into PackageFix for full transitive analysis.",
     "faqs":[
        ("What is a transitive vulnerability?","A vulnerability in a package you didn't directly install — it came in as a dependency of one of your dependencies."),
        ("How do I fix a transitive vulnerability without breaking my app?","Use npm overrides (npm v8+) to pin the vulnerable transitive dependency to a safe version. PackageFix generates the exact override snippet."),
        ("Does npm audit fix handle transitive vulnerabilities?","Often not. npm audit fix --force can break your app by making incompatible major version updates. The safe path is using overrides for transitive CVEs."),
        ("How deep does PackageFix scan?","Drop your package-lock.json alongside package.json — PackageFix parses the full lockfile tree and surfaces transitive CVEs with the exact dependency path.")
     ]},
    {"slug":"fix/npm/lockfile-mismatch","eco":"npm",
     "title":"Fix npm Lockfile Mismatch — package-lock.json Out of Sync",
     "desc":"Fix npm lockfile mismatches where package-lock.json is out of sync with package.json. Identify vulnerable pinned versions in the lockfile.",
     "h1":"Fix npm Lockfile Mismatch",
     "problem":"package-lock.json pins a vulnerable version of a dependency even after you updated package.json. The lockfile takes precedence during npm ci, so the vulnerability persists in CI/CD.",
     "bad":'# package.json: "express": "^4.19.2"\n# package-lock.json: "express": "4.17.1"  ← vulnerable version still pinned',
     "fix":'# Delete package-lock.json and regenerate:\nrm package-lock.json\nnpm install\n\n# Or update a specific package:\nnpm update express',
     "fix_note":"The lockfile overrides the semver range in package.json. After updating package.json, always regenerate the lockfile. PackageFix scans both files when dropped together.",
     "faqs":[
        ("Why does npm ci install a vulnerable version even after I updated package.json?","npm ci installs exactly what is in package-lock.json, ignoring package.json semver ranges. If the lockfile is stale, it installs the vulnerable version."),
        ("How do I regenerate package-lock.json safely?","Run npm install (not npm ci). This resolves semver ranges in package.json and writes a fresh lockfile with the latest matching versions."),
        ("Should I commit package-lock.json to version control?","Yes. Committing the lockfile ensures reproducible installs across environments. Review it during code review for unexpected version changes."),
        ("How does PackageFix handle lockfiles?","Drop package-lock.json alongside package.json. PackageFix parses both and shows which lockfile-pinned versions are vulnerable.")
     ]},
    {"slug":"fix/pypi/outdated-dependencies","eco":"pypi",
     "title":"Fix Outdated Python Dependencies — Update requirements.txt",
     "desc":"Scan requirements.txt for CVEs and get a patched version. Fix outdated Python packages with known vulnerabilities — no pip-audit install needed.",
     "h1":"Fix Outdated Python Dependencies",
     "problem":"Your requirements.txt contains packages with known CVEs. pip list --outdated shows stale packages but doesn't tell you which ones are dangerous.",
     "bad":'requests==2.25.1\nDjango==3.1.0\npillow==8.0.0',
     "fix":'requests==2.31.0\nDjango==4.2.13\npillow==10.3.0',
     "fix_note":"requests 2.25.1 (CVE-2023-32681), Django 3.1.0 (multiple CVEs), Pillow 8.0.0 (CVE-2021-27921). Update to the safe versions above.",
     "faqs":[
        ("How do I scan Python requirements.txt for CVEs without pip-audit?","Paste your requirements.txt into PackageFix. It queries the OSV database live — no CLI install needed."),
        ("Does PackageFix support poetry.lock?","Yes. Drop poetry.lock alongside requirements.txt for full transitive dependency scanning."),
        ("What is the OSV database?","The Open Source Vulnerability database maintained by Google. It aggregates CVEs from NVD, GitHub Advisory Database, and ecosystem-specific sources. Updated daily."),
        ("How do I fix unpinned Python dependencies?","PackageFix flags requirements like 'requests' (no version) as unpinned. Pin to the latest safe version: requests==2.31.0.")
     ]},
    {"slug":"fix/pypi/critical-cve","eco":"pypi",
     "title":"Fix Critical Python CVE — Patch requirements.txt Vulnerabilities",
     "desc":"Find and fix critical CVEs in Python requirements.txt. Get a patched requirements file with CISA KEV flags — no CLI, no signup.",
     "h1":"Fix Critical Python CVEs",
     "problem":"pip audit or safety scan flags a CRITICAL CVE in your Python dependencies but gives you a report, not a fixed file.",
     "bad":'cryptography==36.0.0\nurllib3==1.25.11',
     "fix":'cryptography==42.0.8\nurllib3==2.2.2',
     "fix_note":"cryptography 36.0.0 is affected by CVE-2023-49083 (CRITICAL). urllib3 1.25.11 is affected by CVE-2023-45803 (HIGH). Update to the safe versions above.",
     "faqs":[
        ("What Python packages appear most often in CISA KEV?","cryptography, urllib3, Pillow, Django, and requests are the most frequently CVE-flagged Python packages. PackageFix always checks the live CISA KEV catalog."),
        ("How do I fix a CVE in a transitive Python dependency?","Drop poetry.lock or pip freeze output alongside requirements.txt. PackageFix identifies the full dependency path and suggests override syntax."),
        ("Does PackageFix support conda environments?","PackageFix supports pip-style requirements.txt. For conda, export to pip format: conda list --export > requirements.txt"),
        ("What is the difference between safety and PackageFix?","safety is a CLI tool that requires installation. PackageFix runs in your browser — paste and go, nothing installs on your machine.")
     ]},
    {"slug":"fix/pypi/transitive-vulnerability","eco":"pypi",
     "title":"Fix Transitive Python Vulnerability — Indirect Dependency CVEs",
     "desc":"Fix CVEs in indirect Python dependencies. Drop poetry.lock or pip freeze output for full transitive scanning.",
     "h1":"Fix Transitive Python Vulnerabilities",
     "problem":"A CVE affects a package you never directly installed — it came in as a sub-dependency. pip audit flags it but can't fix it without breaking the dependency chain.",
     "bad":'# Your app uses flask==2.0.0\n# flask depends on werkzeug==2.0.0\n# werkzeug 2.0.0 is affected by CVE-2023-25577',
     "fix":'# In requirements.txt, pin the transitive dep directly:\nwerkzeug==3.0.3',
     "fix_note":"Pin the vulnerable transitive dependency directly in requirements.txt. Drop your poetry.lock into PackageFix for full transitive path visualization.",
     "faqs":[
        ("How do I find transitive Python vulnerabilities?","Drop poetry.lock or the output of pip freeze alongside requirements.txt into PackageFix. It parses the full dependency tree."),
        ("Can I pin a transitive dependency in requirements.txt?","Yes. Adding werkzeug==3.0.3 directly to requirements.txt forces pip to use that version. This is the standard approach for transitive CVE fixes."),
        ("Does poetry handle transitive vulnerability fixes?","poetry update <package> can update a transitive dep. PackageFix generates the exact version to target."),
        ("What is the OSV transitive path?","PackageFix shows: YourApp → flask@2.0.0 → werkzeug@2.0.0 [CVE-2023-25577]. This tells you exactly which direct dependency is pulling in the vulnerable package.")
     ]},
    {"slug":"fix/ruby/outdated-dependencies","eco":"ruby",
     "title":"Fix Outdated Ruby Gem Dependencies — Update Gemfile",
     "desc":"Scan Gemfile for CVEs and get a patched version. Fix outdated Ruby gems without bundle-audit CLI install.",
     "h1":"Fix Outdated Ruby Gem Dependencies",
     "problem":"bundle outdated shows stale gems but doesn't tell you which are security risks. bundle-audit requires CLI setup and doesn't output a fixed Gemfile.",
     "bad":"source 'https://rubygems.org'\ngem 'rails', '6.0.0'\ngem 'nokogiri', '1.11.0'\ngem 'puma', '4.3.0'",
     "fix":"source 'https://rubygems.org'\ngem 'rails', '7.1.3'\ngem 'nokogiri', '1.16.5'\ngem 'puma', '6.4.2'",
     "fix_note":"rails 6.0.0 (multiple CVEs), nokogiri 1.11.0 (CVE-2022-24836 CRITICAL), puma 4.3.0 (CVE-2022-24790 HIGH). Update to safe versions above.",
     "faqs":[
        ("How do I scan a Gemfile for CVEs without bundle-audit?","Paste your Gemfile into PackageFix. It queries the OSV RubyGems advisory database live."),
        ("Does PackageFix support Gemfile.lock?","Yes. Drop Gemfile.lock alongside Gemfile for full transitive gem scanning."),
        ("What Ruby gems appear most often in CVE advisories?","nokogiri, rails, puma, rack, and devise are the most frequently CVE-flagged Ruby gems."),
        ("How do I fix a CVE in a Rails dependency?","Update the gem version in your Gemfile to the safe version, then run bundle install to regenerate Gemfile.lock.")
     ]},
    {"slug":"fix/ruby/critical-cve","eco":"ruby",
     "title":"Fix Critical Ruby CVE — Patch Gemfile Vulnerabilities",
     "desc":"Fix CRITICAL and HIGH CVEs in Ruby gems. Paste Gemfile and get a patched version with CISA KEV flags — no CLI needed.",
     "h1":"Fix Critical Ruby CVEs",
     "problem":"bundler-audit or manual research flags a critical CVE in your Gemfile but gives no patched Gemfile to download.",
     "bad":"gem 'nokogiri', '1.11.0'\ngem 'rack', '2.2.2'",
     "fix":"gem 'nokogiri', '1.16.5'\ngem 'rack', '3.0.11'",
     "fix_note":"nokogiri 1.11.0 is affected by CVE-2022-24836 (CRITICAL). rack 2.2.2 is affected by CVE-2023-27530 (HIGH). Update to safe versions above.",
     "faqs":[
        ("What is the most critical Ruby gem CVE in 2024-2026?","nokogiri has had the most CRITICAL CVEs of any Ruby gem in this period. Always keep nokogiri pinned to the latest version."),
        ("How do I force a gem version in Gemfile?","Use gem 'nokogiri', '~> 1.16.5' to pin to a safe version with patch updates allowed, or '1.16.5' for an exact pin."),
        ("Does CISA KEV include Ruby gems?","Yes. rack vulnerabilities have appeared in the CISA KEV catalog. PackageFix flags these with a red KEV badge."),
        ("How do I scan Gemfile.lock for transitive CVEs?","Drop Gemfile.lock alongside Gemfile into PackageFix. It parses the full lockfile and flags transitive vulnerabilities.")
     ]},
    {"slug":"fix/php/outdated-dependencies","eco":"php",
     "title":"Fix Outdated PHP Composer Dependencies — Update composer.json",
     "desc":"Scan composer.json for CVEs and get a patched version. Fix outdated PHP packages — no CLI install needed.",
     "h1":"Fix Outdated PHP Composer Dependencies",
     "problem":"composer outdated shows stale packages but doesn't generate a secure composer.json. local-php-security-checker requires CLI setup.",
     "bad":'{\n  "require": {\n    "laravel/framework": "^8.0",\n    "guzzlehttp/guzzle": "^7.0.1"\n  }\n}',
     "fix":'{\n  "require": {\n    "laravel/framework": "^11.0",\n    "guzzlehttp/guzzle": "^7.9.2"\n  }\n}',
     "fix_note":"laravel/framework 8.x has multiple CVEs. guzzlehttp/guzzle 7.0.1 is affected by CVE-2022-31090 (HIGH). Update to safe versions above.",
     "faqs":[
        ("How do I scan composer.json for CVEs without CLI?","Paste your composer.json into PackageFix. It queries the OSV Packagist advisory database live."),
        ("Does PackageFix support composer.lock?","Yes. Drop composer.lock alongside composer.json for full transitive package scanning."),
        ("What PHP packages have the most CVEs?","laravel/framework, guzzlehttp/guzzle, symfony components, and monolog/monolog are the most frequently CVE-flagged PHP packages."),
        ("How do I fix a CVE in a Laravel dependency?","Update the constraint in composer.json to the safe version range, then run composer update <package>.")
     ]},
    {"slug":"fix/php/critical-cve","eco":"php",
     "title":"Fix Critical PHP CVE — Patch composer.json Vulnerabilities",
     "desc":"Fix CRITICAL and HIGH CVEs in PHP Composer packages. Paste composer.json and download a patched version — no login, no CLI.",
     "h1":"Fix Critical PHP CVEs",
     "problem":"composer audit flags a critical CVE but doesn't output a fixed composer.json for download.",
     "bad":'{\n  "require": {\n    "phpmailer/phpmailer": "^6.5.0",\n    "intervention/image": "^2.7"\n  }\n}',
     "fix":'{\n  "require": {\n    "phpmailer/phpmailer": "^6.9.1",\n    "intervention/image": "^3.7"\n  }\n}',
     "fix_note":"phpmailer/phpmailer 6.5.0 has known injection vulnerabilities. intervention/image 2.7 has XSS risk. Update to safe versions above.",
     "faqs":[
        ("Does CISA KEV include PHP packages?","Yes. Several Symfony and Laravel CVEs have appeared in CISA KEV. PackageFix checks the live catalog."),
        ("How do I fix a transitive PHP vulnerability?","Use composer's conflict key to prevent installation of vulnerable versions, or add the safe version directly to require. PackageFix generates the correct syntax."),
        ("What is Packagist OSV data?","OSV aggregates vulnerability data for PHP packages from the GitHub Advisory Database, FriendsOfPHP security advisories, and other sources."),
        ("How do I verify a PHP CVE fix?","After updating, run composer audit (Composer 2.4+). If the CVE ID is absent, the fix is applied.")
     ]},
    {"slug":"fix/go/outdated-dependencies","eco":"go",
     "title":"Fix Outdated Go Module Dependencies — Update go.mod",
     "desc":"Scan go.mod for CVEs and get a patched version. Fix vulnerable Go modules — no govulncheck CLI needed.",
     "h1":"Fix Outdated Go Module Dependencies",
     "problem":"go list -m all shows all modules but doesn't flag CVEs. govulncheck requires CLI installation and doesn't output a patched go.mod.",
     "bad":'module myapp\n\ngo 1.21\n\nrequire (\n    github.com/gin-gonic/gin v1.7.0\n    golang.org/x/net v0.0.0-20210405180319-a5a99cb37ef4\n)',
     "fix":'module myapp\n\ngo 1.21\n\nrequire (\n    github.com/gin-gonic/gin v1.9.1\n    golang.org/x/net v0.23.0\n)',
     "fix_note":"gin v1.7.0 (CVE-2023-29401). golang.org/x/net old commit hash has multiple CVEs. Update to safe versions above.",
     "faqs":[
        ("How do I scan go.mod for CVEs without govulncheck?","Paste your go.mod into PackageFix. It queries the OSV Go advisory database live."),
        ("What are Go pseudo-versions and are they safe?","Pseudo-versions (v0.0.0-20210405180319-...) reference specific commits. They can be vulnerable if the commit predates a security fix. PackageFix flags these."),
        ("How do I update a specific Go module?","Run go get github.com/module@v1.2.3, then go mod tidy to clean up."),
        ("Does PackageFix support go.sum?","go.sum is a checksum file, not a version manifest. PackageFix scans go.mod for CVEs — go.sum scanning is not needed for vulnerability detection.")
     ]},
    {"slug":"fix/rust/outdated-dependencies","eco":"rust",
     "title":"Fix Outdated Rust Crate Dependencies — Update Cargo.toml",
     "desc":"Scan Cargo.toml for CVEs and get a patched version. Fix vulnerable Rust crates — no cargo-audit CLI needed.",
     "h1":"Fix Outdated Rust Crate Dependencies",
     "problem":"cargo outdated shows stale crates but doesn't flag CVEs. cargo audit requires CLI installation and doesn't output a patched Cargo.toml.",
     "bad":'[dependencies]\nactix-web = "3.3.2"\nopenssl = "0.10.30"',
     "fix":'[dependencies]\nactix-web = "4.5.1"\nopenssl = "0.10.66"',
     "fix_note":"actix-web 3.3.2 (CVE-2022-24977). openssl 0.10.30 has known vulnerabilities. Update to safe versions above.",
     "faqs":[
        ("How do I scan Cargo.toml for CVEs without cargo-audit?","Paste your Cargo.toml into PackageFix. It queries the OSV crates.io advisory database live."),
        ("Does PackageFix support Cargo.lock?","Yes. Drop Cargo.lock alongside Cargo.toml for full transitive crate scanning."),
        ("What is the RustSec advisory database?","RustSec is the Rust security advisory database. OSV aggregates RustSec advisories — PackageFix queries OSV directly."),
        ("How do I fix a build.rs security warning?","If your Cargo.toml has build = 'build.rs', PackageFix flags it for manual review — build.rs runs arbitrary code at compile time.")
     ]},
]

# ── Ecosystem × stack combo pages ─────────────────────────────────────────────
STACK_COMBOS = [
    # npm
    ("npm","express","Express.js","fix/npm/critical-cve/express","CVE-2024-29041","4.19.2","\"express\": \"4.17.1\"","\"express\": \"4.19.2\"","open redirect via response.redirect()"),
    ("npm","nextjs","Next.js","fix/npm/critical-cve/nextjs","CVE-2024-34351","14.1.1","\"next\": \"14.0.0\"","\"next\": \"14.1.1\"","server-side request forgery in Host header"),
    ("npm","react","React","fix/npm/critical-cve/react","CVE-2024-21901","18.2.0","\"react\": \"18.0.0\"","\"react\": \"18.2.0\"","XSS via dangerouslySetInnerHTML"),
    ("npm","lodash","Lodash","fix/npm/critical-cve/lodash","CVE-2020-8203","4.17.21","\"lodash\": \"4.17.15\"","\"lodash\": \"4.17.21\"","prototype pollution"),
    ("npm","axios","Axios","fix/npm/critical-cve/axios","CVE-2023-45857","1.7.4","\"axios\": \"0.21.1\"","\"axios\": \"1.7.4\"","SSRF via protocol-relative URL"),
    ("npm","jsonwebtoken","jsonwebtoken","fix/npm/critical-cve/jsonwebtoken","CVE-2022-23540","9.0.0","\"jsonwebtoken\": \"8.5.1\"","\"jsonwebtoken\": \"9.0.0\"","algorithm confusion attack"),
    ("npm","webpack","webpack","fix/npm/critical-cve/webpack","CVE-2023-28154","5.75.0","\"webpack\": \"5.69.0\"","\"webpack\": \"5.75.0\"","prototype pollution via import.meta"),
    ("npm","minimist","minimist","fix/npm/critical-cve/minimist","CVE-2021-44906","1.2.6","\"minimist\": \"1.2.5\"","\"minimist\": \"1.2.6\"","prototype pollution"),
    # PyPI
    ("pypi","django","Django","fix/pypi/critical-cve/django","CVE-2024-27351","4.2.13","Django==3.2.0","Django==4.2.13","ReDoS in strip_tags"),
    ("pypi","flask","Flask","fix/pypi/critical-cve/flask","CVE-2023-30861","3.0.3","Flask==2.0.0","Flask==3.0.3","secure cookie bypass"),
    ("pypi","fastapi","FastAPI","fix/pypi/critical-cve/fastapi","CVE-2024-24762","0.109.1","fastapi==0.100.0","fastapi==0.109.1","ReDoS in form parsing"),
    ("pypi","requests","requests","fix/pypi/critical-cve/requests","CVE-2023-32681","2.31.0","requests==2.25.1","requests==2.31.0","proxy credential leak"),
    ("pypi","pillow","Pillow","fix/pypi/critical-cve/pillow","CVE-2023-44271","10.3.0","Pillow==8.0.0","Pillow==10.3.0","uncontrolled resource consumption"),
    ("pypi","cryptography","cryptography","fix/pypi/critical-cve/cryptography","CVE-2023-49083","42.0.8","cryptography==36.0.0","cryptography==42.0.8","NULL pointer dereference in PKCS12"),
    # Ruby
    ("ruby","rails","Rails","fix/ruby/critical-cve/rails","CVE-2024-26144","7.1.3","gem 'rails', '6.0.0'","gem 'rails', '7.1.3'","CSRF token leak in response headers"),
    ("ruby","nokogiri","Nokogiri","fix/ruby/critical-cve/nokogiri","CVE-2022-24836","1.16.5","gem 'nokogiri', '1.11.0'","gem 'nokogiri', '1.16.5'","ReDoS in CSS selector parsing"),
    ("ruby","devise","Devise","fix/ruby/critical-cve/devise","CVE-2021-28125","4.9.4","gem 'devise', '4.7.3'","gem 'devise', '4.9.4'","open redirect in OAuth flow"),
    # PHP
    ("php","laravel","Laravel","fix/php/critical-cve/laravel","CVE-2021-43503","^10.0","\"laravel/framework\": \"^8.0\"","\"laravel/framework\": \"^10.0\"","mass assignment bypass"),
    ("php","symfony","Symfony","fix/php/critical-cve/symfony","CVE-2022-24894","^7.0","\"symfony/http-foundation\": \"^5.0\"","\"symfony/http-foundation\": \"^7.0\"","response caching of private data"),
    ("php","guzzle","Guzzle","fix/php/critical-cve/guzzle","CVE-2022-31090","^7.9","\"guzzlehttp/guzzle\": \"^7.0\"","\"guzzlehttp/guzzle\": \"^7.9\"","CURLOPT_HTTPAUTH credential leak"),
    ("php","monolog","Monolog","fix/php/critical-cve/monolog","CVE-2021-41196","^3.5","\"monolog/monolog\": \"^2.0\"","\"monolog/monolog\": \"^3.5\"","log injection via headers"),
    # Go
    ("go","gin","Gin","fix/go/critical-cve/gin","CVE-2023-29401","v1.9.1","github.com/gin-gonic/gin v1.7.0","github.com/gin-gonic/gin v1.9.1","filename enumeration via Content-Disposition"),
    ("go","grpc","gRPC-Go","fix/go/critical-cve/grpc","CVE-2023-44487","v1.58.3","google.golang.org/grpc v1.50.0","google.golang.org/grpc v1.58.3","HTTP/2 rapid reset DDoS"),
    ("go","net","golang.org/x/net","fix/go/critical-cve/net","CVE-2023-44487","v0.23.0","golang.org/x/net v0.0.0-20210405180319","golang.org/x/net v0.23.0","HTTP/2 rapid reset"),
]

# ── Error pages ────────────────────────────────────────────────────────────────
ERROR_PAGES = [
    {"slug":"error/npm-audit-high-severity",
     "title":"npm audit found high severity vulnerabilities — How to Fix",
     "desc":"Fix 'npm audit found N vulnerabilities (M high severity)'. Get a patched package.json with all high severity CVEs resolved.",
     "h1":"npm audit found high severity vulnerabilities",
     "error_msg":"found 3 high severity vulnerabilities",
     "cause":"One or more of your npm dependencies has a known HIGH or CRITICAL CVE. npm audit reports it but npm audit fix may not be able to resolve it without breaking changes.",
     "fix_steps":[
        "Paste your package.json into PackageFix to get a live CVE scan with safe fix versions.",
        "Review the severity badges — CRITICAL and HIGH packages on the CISA KEV catalog are flagged in red.",
        "Download the fixed package.json and run npm install to regenerate package-lock.json.",
        "For transitive vulnerabilities, use the npm overrides block PackageFix generates."
     ],
     "faqs":[
        ("Why can't npm audit fix resolve high severity vulnerabilities?","npm audit fix only applies semver-compatible updates. If the fix requires a major version bump, it won't apply automatically to avoid breaking changes."),
        ("What does 'high severity' mean in npm audit?","HIGH severity corresponds to a CVSS score of 7.0–8.9. These can often be exploited remotely. Fix within your next release cycle."),
        ("How do I fix a high severity vulnerability in a transitive dependency?","Use npm overrides in package.json: {\"overrides\": {\"vulnerable-package\": \"safe-version\"}}. PackageFix generates this snippet."),
        ("What is the difference between HIGH and CRITICAL in npm audit?","HIGH = CVSS 7.0–8.9, CRITICAL = CVSS 9.0–10.0. Both require prompt remediation. CRITICAL should be fixed immediately.")
     ]},
    {"slug":"error/pip-dependency-conflict",
     "title":"pip dependency conflict — ResolutionImpossible Error Fix",
     "desc":"Fix pip ResolutionImpossible and dependency conflict errors. Resolve incompatible Python package version constraints.",
     "h1":"pip dependency conflict — ResolutionImpossible",
     "error_msg":"ERROR: Cannot install -r requirements.txt (line 3) and requests==2.25.1 because these package versions have conflicting dependencies.",
     "cause":"Two or more packages in your requirements.txt require incompatible versions of the same dependency. pip cannot satisfy all constraints simultaneously.",
     "fix_steps":[
        "Identify which packages are conflicting using pip check after partial installation.",
        "Paste your requirements.txt into PackageFix to scan for CVEs — sometimes a CVE fix requires a version that triggers the conflict.",
        "Use pip-compile (pip-tools) to resolve a consistent set of versions across all transitive dependencies.",
        "Consider using a virtual environment to isolate conflicting packages."
     ],
     "faqs":[
        ("How do I find which packages are causing a pip conflict?","Run pip check after installing to see conflicting requirements. pipdeptree shows the full dependency tree."),
        ("Can I force pip to ignore version conflicts?","pip install --no-deps skips dependency resolution but leaves your environment in an inconsistent state. Use only for debugging."),
        ("How does poetry handle dependency conflicts?","poetry uses a SAT solver for dependency resolution and will tell you exactly which constraints are incompatible. PackageFix supports poetry.lock files."),
        ("How do I fix a conflict caused by a security update?","If updating a package for a CVE fix causes a conflict, use a dependency override or constraint file to specify compatible versions.")
     ]},
    {"slug":"error/bundler-version-conflict",
     "title":"Bundler version conflict — Gemfile.lock out of date Fix",
     "desc":"Fix Bundler version conflicts and Gemfile.lock errors. Resolve incompatible gem version constraints in Ruby projects.",
     "h1":"Bundler version conflict — Gemfile.lock out of date",
     "error_msg":"Bundler could not find compatible versions for gem 'rails':\nIn Gemfile:\n  rails (~> 6.0) was resolved to 6.0.0, which depends on\n    actionpack (= 6.0.0)",
     "cause":"Your Gemfile specifies version constraints that conflict with the current Gemfile.lock, or two gems require incompatible versions of a shared dependency.",
     "fix_steps":[
        "Run bundle update --bundler to update Bundler itself first.",
        "Run bundle update <specific-gem> to update only the conflicting gem and its dependencies.",
        "Check Gemfile for overly strict version constraints (~> vs >= vs exact pins).",
        "Paste your Gemfile into PackageFix to scan for CVEs — a security fix may require a version that triggers the conflict."
     ],
     "faqs":[
        ("How do I fix 'Bundler could not find compatible versions'?","Run bundle update <gem-name> to update the specific gem. If that fails, check for conflicting constraints in your Gemfile."),
        ("Should I delete Gemfile.lock to fix conflicts?","Deleting Gemfile.lock and running bundle install regenerates it with latest compatible versions. This works but may introduce unintended updates — check the diff."),
        ("How do I fix a CVE without breaking gem version constraints?","Update the gem's lower bound in Gemfile to the safe version: gem 'rails', '>= 7.1.3'. PackageFix shows the minimum safe version for each CVE."),
        ("What is the difference between bundle update and bundle install?","bundle install installs gems according to Gemfile.lock. bundle update resolves fresh versions from Gemfile constraints and updates the lockfile.")
     ]},
    {"slug":"error/composer-memory-limit",
     "title":"Composer memory limit exhausted — Fix PHP dependency install",
     "desc":"Fix 'PHP Fatal error: Allowed memory size exhausted' during composer install. Update vulnerable PHP packages without memory issues.",
     "h1":"Composer memory limit exhausted",
     "error_msg":"PHP Fatal error: Allowed memory size of 1610612736 bytes exhausted (tried to allocate 4096 bytes)",
     "cause":"Composer's dependency resolver requires large amounts of memory for complex dependency graphs, especially when resolving conflicts across many packages.",
     "fix_steps":[
        "Run COMPOSER_MEMORY_LIMIT=-1 composer install to remove the memory limit.",
        "Or increase PHP memory: php -d memory_limit=2G /usr/local/bin/composer install",
        "Paste your composer.json into PackageFix to identify CVEs first — then update only vulnerable packages.",
        "Use composer update --no-scripts to skip resource-intensive post-install scripts."
     ],
     "faqs":[
        ("How do I fix Composer memory exhausted on CI?","Set COMPOSER_MEMORY_LIMIT=-1 in your CI environment variables. Most CI systems allow this as an env var."),
        ("Why does Composer use so much memory?","Composer loads all package metadata into memory during dependency resolution. Large projects with many packages and conflicts require more memory."),
        ("How do I update only security-critical PHP packages?","Use composer update <vendor/package> to update a specific package. PackageFix shows which packages have CVEs so you can target updates precisely."),
        ("Does this error mean my packages are vulnerable?","Not necessarily — it's a resource error, not a security error. But run PackageFix on your composer.json to check for CVEs independently.")
     ]},
    {"slug":"error/package-json-missing-lockfile",
     "title":"package-lock.json missing — npm ci fails in CI/CD Fix",
     "desc":"Fix 'npm ci can only install packages when your package.json and package-lock.json are in sync' error in CI/CD.",
     "h1":"package-lock.json missing or out of sync",
     "error_msg":"npm error: `npm ci` can only install packages when your package.json and package-lock.json or npm-shrinkwrap.json is in sync.",
     "cause":"npm ci requires an up-to-date package-lock.json. If lockfile is missing, deleted, or out of sync with package.json, CI fails.",
     "fix_steps":[
        "Run npm install locally to generate a fresh package-lock.json.",
        "Commit package-lock.json to version control — it should never be in .gitignore.",
        "Paste your package.json into PackageFix to scan for CVEs before committing the new lockfile.",
        "In CI, always use npm ci (not npm install) for reproducible, secure installs."
     ],
     "faqs":[
        ("Should package-lock.json be in .gitignore?","No. package-lock.json should always be committed. It ensures reproducible installs and allows security scanning of pinned dependency versions."),
        ("What is the difference between npm install and npm ci?","npm install updates package-lock.json based on package.json ranges. npm ci installs exactly what is in package-lock.json — faster and more secure for CI."),
        ("Why does npm ci fail in GitHub Actions?","Usually because package-lock.json is not committed, or was generated with a different npm version. Always commit the lockfile and use --legacy-peer-deps if needed."),
        ("Can a missing lockfile be a security risk?","Yes. Without a lockfile, npm install resolves to the latest version of each package at install time, which could include a newly published malicious package.")
     ]},
]

# Map fix-guide ecosystem → most relevant error page (java defaults via .get → /error)
FIX_TO_ERROR = {
    "npm": "/error/npm-audit-high-severity",
    "pypi": "/error/pip-dependency-conflict",
    "ruby": "/error/bundler-version-conflict",
    "php": "/error/composer-memory-limit",
    "go": "/error/package-json-missing-lockfile",
    "rust": "/error/package-json-missing-lockfile",
}

# ── Comparison pages ───────────────────────────────────────────────────────────
COMPARISON_PAGES = [
    {"slug":"vs/snyk-advisor","competitor":"Snyk Advisor","status":"shut down January 2026",
     "title":"PackageFix vs Snyk Advisor — Free Browser Alternative",
     "desc":"Snyk Advisor shut down in January 2026. PackageFix is the free browser-based alternative — paste your manifest, get a fixed file back. No login, no CLI.",
     "h1":"PackageFix vs Snyk Advisor",
     "summary":"Snyk Advisor was the only browser paste-and-check tool for dependency health. It shut down January 2026. PackageFix fills that gap — and goes further by generating the fixed manifest.",
     "rows":[
        ("Browser-based scan","✅ Yes","❌ Shut down"),
        ("Fix output (patched manifest)","✅ Yes","❌ No — checker only"),
        ("CISA KEV flags","✅ Yes","❌ No"),
        ("No login required","✅ Yes","❌ Required"),
        ("7 ecosystems","✅ npm, PyPI, Ruby, PHP, Go, Rust, Java","⚠ npm + PyPI only"),
        ("Still works today","✅ Yes","❌ Dead"),
        ("Open source","✅ MIT","❌ Proprietary"),
     ]},
    {"slug":"vs/dependabot","competitor":"Dependabot","status":"requires GitHub access",
     "title":"PackageFix vs Dependabot — Browser Alternative, No GitHub Needed",
     "desc":"Dependabot requires GitHub access. PackageFix runs in your browser — paste any manifest, get a fixed version back. No GitHub connection, no bot setup.",
     "h1":"PackageFix vs Dependabot",
     "summary":"Dependabot is a GitHub bot that opens PRs for dependency updates. It requires GitHub repo access and only works inside GitHub's ecosystem. PackageFix works anywhere — paste a manifest and get back the fixed file instantly.",
     "rows":[
        ("Browser-based scan","✅ Yes","❌ No — GitHub only"),
        ("Fix output (patched manifest)","✅ Yes","⚠ Opens PRs only"),
        ("No GitHub connection","✅ Yes","❌ Required"),
        ("CISA KEV flags","✅ Yes","❌ No"),
        ("Works without a git repo","✅ Yes","❌ No"),
        ("7 ecosystems","✅ npm, PyPI, Ruby, PHP, Go, Rust, Java","✅ Similar coverage"),
        ("Supply chain detection","✅ Typosquatting, Glassworm, zombie","❌ CVEs only"),
     ]},
    {"slug":"vs/npm-audit","competitor":"npm audit","status":"CLI only, no fix output",
     "title":"PackageFix vs npm audit — Browser Tool, Fix Output Included",
     "desc":"npm audit is CLI-only and gives no fixed package.json. PackageFix runs in your browser and generates the patched manifest to download.",
     "h1":"PackageFix vs npm audit",
     "summary":"npm audit tells you what's vulnerable. It doesn't give you a fixed file. PackageFix closes that gap — live CVE scan plus a downloadable fixed package.json in one step.",
     "rows":[
        ("Browser-based","✅ Yes","❌ CLI only"),
        ("Fix output (patched manifest)","✅ Yes","❌ Report only"),
        ("CISA KEV flags","✅ Yes","❌ No"),
        ("No Node.js install needed","✅ Yes","❌ Requires Node"),
        ("Transitive override snippets","✅ Yes","❌ No"),
        ("Supply chain detection","✅ Yes","❌ No"),
        ("Multi-ecosystem","✅ 7 ecosystems","❌ npm only"),
     ]},
    {"slug":"vs/pip-audit","competitor":"pip-audit","status":"CLI only",
     "title":"PackageFix vs pip-audit — Browser Tool for Python CVEs",
     "desc":"pip-audit is a CLI tool. PackageFix runs in your browser — paste requirements.txt and get a patched version back. No pip-audit install needed.",
     "h1":"PackageFix vs pip-audit",
     "summary":"pip-audit is the official Python vulnerability scanner. It's excellent but requires CLI installation and outputs a report, not a fixed requirements.txt. PackageFix adds the browser interface and fix output.",
     "rows":[
        ("Browser-based","✅ Yes","❌ CLI only"),
        ("Fix output (patched manifest)","✅ Yes","❌ Report only"),
        ("No Python install needed","✅ Yes","❌ Requires Python/pip"),
        ("CISA KEV flags","✅ Yes","❌ No"),
        ("poetry.lock support","✅ Yes","✅ Yes"),
        ("Supply chain detection","✅ Glassworm, zombie","❌ CVEs only"),
        ("Multi-ecosystem","✅ 7 ecosystems","❌ Python only"),
     ]},
    {"slug":"vs/owasp-dependency-check","competitor":"OWASP Dependency-Check","status":"CLI/CI only",
     "title":"PackageFix vs OWASP Dependency-Check — Instant Browser Alternative",
     "desc":"OWASP Dependency-Check requires CLI setup and produces HTML reports. PackageFix runs in your browser — paste manifest, get fixed file. No install needed.",
     "h1":"PackageFix vs OWASP Dependency-Check",
     "summary":"OWASP Dependency-Check is a trusted enterprise SCA tool. It requires CLI setup, downloads a large NVD database, and produces reports. PackageFix is the zero-setup alternative for developers who need a quick answer without a pipeline.",
     "rows":[
        ("Browser-based","✅ Yes","❌ CLI/CI only"),
        ("Fix output (patched manifest)","✅ Yes","❌ Report only"),
        ("No install needed","✅ Yes","❌ Requires Java + CLI"),
        ("CISA KEV flags","✅ Yes","⚠ NVD data only"),
        ("Setup time","✅ Zero","❌ 10+ minutes"),
        ("Supply chain detection","✅ Yes","❌ CVEs only"),
        ("Open source","✅ MIT","✅ Apache 2.0"),
     ]},
]

# ── Provider/CI pages ──────────────────────────────────────────────────────────
PROVIDER_PAGES = [
    ("providers/github-actions/npm-audit","GitHub Actions","npm","Automate npm CVE Scanning in GitHub Actions",
     "Add PackageFix-compatible npm security scanning to your GitHub Actions CI pipeline. Catch CVEs on every push.",
     "npm audit in GitHub Actions","Add OSV Scanner to your workflow to catch npm CVEs on every push — no PackageFix account needed in CI.",
     """name: Dependency Security Scan
on: [push, pull_request]
jobs:
  osv-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: google/osv-scanner-action@v2
        with:
          scan-args: |-
            --lockfile=package-lock.json"""),
    ("providers/github-actions/python-audit","GitHub Actions","PyPI","Automate Python CVE Scanning in GitHub Actions",
     "Add Python requirements.txt CVE scanning to GitHub Actions. Catch vulnerable PyPI packages on every push.",
     "Python security scan in GitHub Actions","Use OSV Scanner or pip-audit in CI to flag vulnerable Python packages automatically.",
     """name: Python Security Scan
on: [push, pull_request]
jobs:
  python-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pypa/gh-action-pip-audit@v1.0.8
        with:
          inputs: requirements.txt"""),
    ("providers/gitlab-ci/dependency-scan","GitLab CI","npm","npm Dependency CVE Scanning in GitLab CI",
     "Add npm CVE scanning to your GitLab CI/CD pipeline. Fail builds on high severity vulnerabilities.",
     "Dependency scanning in GitLab CI","GitLab includes built-in dependency scanning. For npm, configure it in .gitlab-ci.yml.",
     """include:
  - template: Security/Dependency-Scanning.gitlab-ci.yml

dependency_scanning:
  variables:
    DS_EXCLUDED_PATHS: "spec, test, tests, tmp"
    SECURE_LOG_LEVEL: info"""),
    ("providers/gitlab-ci/python-scan","GitLab CI","PyPI","Python Dependency CVE Scanning in GitLab CI",
     "Add Python requirements.txt vulnerability scanning to GitLab CI. Detect CVEs in your pipeline automatically.",
     "Python security scanning in GitLab CI","Use GitLab's built-in dependency scanning template for Python projects.",
     """include:
  - template: Security/Dependency-Scanning.gitlab-ci.yml

variables:
  PIP_REQUIREMENTS_FILE: requirements.txt"""),
    ("providers/circleci/dependency-scan","CircleCI","npm","npm CVE Scanning in CircleCI",
     "Add npm vulnerability scanning to your CircleCI pipeline. Catch dependency CVEs on every build.",
     "npm audit in CircleCI","Use OSV Scanner in CircleCI to flag CVEs on every push.",
     """version: 2.1
jobs:
  security-scan:
    docker:
      - image: cimg/node:18.0
    steps:
      - checkout
      - run:
          name: Install OSV Scanner
          command: go install github.com/google/osv-scanner/cmd/osv-scanner@latest
      - run:
          name: Scan dependencies
          command: osv-scanner --lockfile=package-lock.json"""),
    ("providers/circleci/python-scan","CircleCI","PyPI","Python CVE Scanning in CircleCI",
     "Add Python requirements.txt vulnerability scanning to CircleCI. Detect CVEs automatically.",
     "pip-audit in CircleCI","Use pip-audit in CircleCI to flag vulnerable Python packages.",
     """version: 2.1
jobs:
  python-security:
    docker:
      - image: cimg/python:3.11
    steps:
      - checkout
      - run: pip install pip-audit
      - run: pip-audit -r requirements.txt"""),
    ("providers/hetzner/nodejs-security","Hetzner","npm","Node.js Dependency Security on Hetzner VPS",
     "Scan Node.js dependencies for CVEs on Hetzner Cloud servers. Keep npm packages secure on self-hosted infrastructure.",
     "Node.js security on Hetzner","Run npm audit or OSV Scanner as part of your deployment process on Hetzner VPS.",
     """# Add to your deploy script on Hetzner VPS
cd /var/www/myapp
npm audit --audit-level=high

# Or use OSV Scanner
curl -L https://github.com/google/osv-scanner/releases/latest/download/osv-scanner_linux_amd64 -o osv-scanner
chmod +x osv-scanner
./osv-scanner --lockfile=package-lock.json"""),
    ("providers/hetzner/python-security","Hetzner","PyPI","Python Dependency Security on Hetzner VPS",
     "Scan Python dependencies for CVEs on Hetzner Cloud. Keep pip packages secure on self-hosted Python apps.",
     "Python security on Hetzner","Run pip-audit as part of your deployment on Hetzner VPS.",
     """# Add to your deploy script on Hetzner VPS
cd /var/www/myapp
pip install pip-audit
pip-audit -r requirements.txt --fix --dry-run"""),
    ("providers/digitalocean/python-security","DigitalOcean","PyPI","Python Dependency Security on DigitalOcean Droplets",
     "Scan Python requirements.txt for CVEs on DigitalOcean. Keep pip packages secure on App Platform and Droplets.",
     "Python security on DigitalOcean","Integrate pip-audit into your DigitalOcean deployment workflow.",
     """# In your DigitalOcean App Platform build command:
pip install pip-audit && pip-audit -r requirements.txt

# For Droplets, add to deploy.sh:
pip-audit -r requirements.txt --format=json"""),
    ("providers/digitalocean/nodejs-security","DigitalOcean","npm","Node.js Dependency Security on DigitalOcean",
     "Scan npm packages for CVEs on DigitalOcean App Platform and Droplets. Automate security checks in deployments.",
     "npm security on DigitalOcean","Run npm audit in your DigitalOcean deployment pipeline.",
     """# DigitalOcean App Platform — build command:
npm ci && npm audit --audit-level=high

# For Droplets in deploy.sh:
cd /var/www/app
npm audit --audit-level=critical --json"""),
    ("providers/vercel/nodejs-security","Vercel","npm","Node.js Dependency Security on Vercel",
     "Scan npm packages for CVEs in Vercel deployments. Catch vulnerable dependencies before deploying to production.",
     "npm security on Vercel","Add npm audit to your Vercel build command to block deploys with critical CVEs.",
     """# In vercel.json, override the build command:
{
  "buildCommand": "npm audit --audit-level=critical && npm run build"
}

# Or in package.json scripts:
"scripts": {
  "vercel-build": "npm audit --audit-level=high && next build"
}"""),
    ("providers/vercel/python-security","Vercel","PyPI","Python Dependency Security on Vercel",
     "Scan Python requirements.txt for CVEs in Vercel serverless deployments.",
     "Python security on Vercel","Add pip-audit to your Vercel Python build process.",
     """# vercel.json build command override:
{
  "buildCommand": "pip install pip-audit && pip-audit -r requirements.txt && pip install -r requirements.txt"
}"""),
    ("providers/aws/lambda-nodejs-security","AWS Lambda","npm","Node.js Security for AWS Lambda Functions",
     "Scan npm dependencies for CVEs in AWS Lambda Node.js functions. Prevent vulnerable packages from reaching production.",
     "npm security for Lambda","Add CVE scanning to your Lambda deployment pipeline with SAM or CDK.",
     """# In your SAM build pipeline (buildspec.yml):
phases:
  pre_build:
    commands:
      - npm audit --audit-level=high
  build:
    commands:
      - sam build"""),
    ("providers/aws/lambda-python-security","AWS Lambda","PyPI","Python Security for AWS Lambda Functions",
     "Scan Python requirements.txt for CVEs in AWS Lambda. Prevent vulnerable pip packages from deploying to Lambda.",
     "Python security for Lambda","Scan requirements.txt before packaging Lambda deployment artifacts.",
     """# In buildspec.yml or GitHub Actions for Lambda:
- pip install pip-audit
- pip-audit -r requirements.txt
- pip install -r requirements.txt -t ./package
- cd package && zip -r ../deployment.zip ."""),
    ("providers/netlify/nodejs-security","Netlify","npm","Node.js Dependency Security on Netlify",
     "Scan npm packages for CVEs in Netlify builds. Block deployments with critical vulnerabilities automatically.",
     "npm security on Netlify","Add npm audit to your Netlify build command.",
     """# netlify.toml build command:
[build]
  command = "npm audit --audit-level=high && npm run build"

# Or in package.json:
"scripts": {
  "netlify-build": "npm audit --audit-level=critical && gatsby build"
}"""),
    ("providers/railway/nodejs-security","Railway","npm","Node.js Dependency Security on Railway",
     "Scan npm dependencies for CVEs on Railway deployments. Catch vulnerable packages before they reach production.",
     "npm security on Railway","Add CVE scanning to your Railway build process.",
     """# In railway.json or nixpacks.toml:
[build]
  buildCommand = "npm audit --audit-level=high && npm ci"
  startCommand = "node index.js"""),
    ("providers/fly/nodejs-security","Fly.io","npm","Node.js Dependency Security on Fly.io",
     "Scan npm packages for CVEs before deploying to Fly.io. Keep your Node.js apps secure on edge deployments.",
     "npm security on Fly.io","Add security scanning to your Dockerfile or fly.toml build.",
     """# In your Dockerfile:
RUN npm audit --audit-level=high
RUN npm ci --only=production

# Or in .github/workflows/deploy.yml before fly deploy:
- run: npm audit --audit-level=critical"""),
    ("providers/render/nodejs-security","Render","npm","Node.js Dependency Security on Render",
     "Scan npm dependencies for CVEs in Render deployments. Automate security checks in your build pipeline.",
     "npm security on Render","Configure CVE scanning in your Render build command.",
     """# In Render dashboard, set Build Command to:
npm audit --audit-level=high && npm ci

# For zero-downtime: wrap in a script
#!/bin/bash
npm audit --audit-level=critical
if [ $? -ne 0 ]; then
  echo "Critical CVEs found — deploy blocked"
  exit 1
fi
npm ci"""),
]

# ── Ecosystem landing pages ────────────────────────────────────────────────────
ECOSYSTEM_PAGES = [
    ("npm","npm Dependency Security Audit — Scan package.json for CVEs",
     "Free browser-based npm vulnerability scanner. Paste package.json and get a patched version back. Live OSV + CISA KEV data. No CLI, no signup.",
     "npm Dependency Security Audit",
     "The fastest way to scan npm dependencies for CVEs and get a fixed package.json. Paste your manifest — get back patched versions, CISA KEV flags, and a downloadable fixed file. No npm audit install needed.",
     "package.json","npm install"),
    ("pypi","Python requirements.txt CVE Scanner — Fix Vulnerable Pip Packages",
     "Free browser-based Python vulnerability scanner. Paste requirements.txt and get a patched version. Live OSV + CISA KEV. No pip-audit install needed.",
     "Python Dependency Security Audit",
     "Scan requirements.txt for CVEs without installing pip-audit. Paste your manifest and get a fixed requirements.txt with safe versions from the OSV database. Supports poetry.lock for transitive scanning.",
     "requirements.txt","pip install -r requirements.txt"),
    ("ruby","Ruby Gemfile CVE Scanner — Fix Vulnerable Gems",
     "Free browser-based Ruby vulnerability scanner. Paste Gemfile and get a patched version. Live OSV + CISA KEV. No bundle-audit install needed.",
     "Ruby Dependency Security Audit",
     "Scan your Gemfile for CVEs without installing bundle-audit. Paste your manifest and get a fixed Gemfile with safe gem versions. Supports Gemfile.lock for transitive scanning.",
     "Gemfile","bundle install"),
    ("php","PHP Composer CVE Scanner — Fix Vulnerable composer.json Packages",
     "Free browser-based PHP vulnerability scanner. Paste composer.json and get a patched version. Live OSV + CISA KEV. No CLI needed.",
     "PHP Composer Dependency Security Audit",
     "Scan composer.json for CVEs without CLI tools. Paste your manifest and get a fixed composer.json with safe package versions. Supports composer.lock for transitive scanning.",
     "composer.json","composer install"),
    ("go","Go Module CVE Scanner — Fix Vulnerable go.mod Dependencies",
     "Free browser-based Go vulnerability scanner. Paste go.mod and get a patched version. Live OSV + CISA KEV. No govulncheck install needed.",
     "Go Module Security Audit",
     "Scan go.mod for CVEs without govulncheck. Paste your manifest and get a fixed go.mod with safe module versions. Detects pseudo-version vulnerabilities.",
     "go.mod","go mod tidy"),
    ("rust","Rust Cargo CVE Scanner — Fix Vulnerable Cargo.toml Crates",
     "Free browser-based Rust vulnerability scanner. Paste Cargo.toml and get a patched version. Live OSV + RustSec. No cargo-audit install needed.",
     "Rust Crate Security Audit",
     "Scan Cargo.toml for CVEs without cargo-audit. Paste your manifest and get a fixed Cargo.toml with safe crate versions. Detects build.rs security risks.",
     "Cargo.toml","cargo update"),
    ("java","Java Maven CVE Scanner — Fix Vulnerable pom.xml Dependencies",
     "Free browser-based Maven vulnerability scanner. Paste pom.xml and get a patched version. Live OSV + CISA KEV. No OWASP Dependency-Check install needed.",
     "Java Maven Dependency Security Audit",
     "Scan pom.xml for CVEs without installing OWASP Dependency-Check. Paste your manifest and get a fixed pom.xml with safe dependency versions. Variable resolution included.",
     "pom.xml","mvn dependency:resolve"),
]

# ══════════════════════════════════════════════════════════════════════════════
# PAGE GENERATORS
# ══════════════════════════════════════════════════════════════════════════════

def generate_fix_page(p):
    eco = ECOSYSTEMS[p["eco"]]
    path = "/" + p["slug"]
    faqs = p["faqs"]
    body = f"""
<h1>{p["h1"]} <span class="badge badge-red">{eco['label']}</span></h1>
<p class="lead">{p["desc"]}</p>
<div class="problem-box">
  <div class="label">⚠ The Problem</div>
  <p style="margin:0">{p["problem"]}</p>
</div>
<h2>Bad Configuration — {eco['file']}</h2>
<pre>{p["bad"]}</pre>
<h2>Fixed Configuration — {eco['file']}</h2>
<pre>{p["fix"]}</pre>
<div class="fix-box">
  <div class="label">✓ Fix</div>
  <p style="margin:0">{p["fix_note"]} After updating, run <code>{eco['cmd']}</code>.</p>
</div>
{cta()}
{faq_html(faqs)}
{related_html([
    {"url":"/"+p["slug"].replace("outdated-dependencies","critical-cve").replace("transitive-vulnerability","critical-cve").replace("lockfile-mismatch","critical-cve"), "title":f"Fix Critical {eco['label']} CVEs","desc":"HIGH and CRITICAL severity"},
    {"url":"https://packagefix.dev","title":"Open PackageFix Tool","desc":"Scan your manifest live"},
    {"url":f"/{p['eco']}","title":f"{eco['label']} Security Overview","desc":f"All {eco['label']} vulnerability guides"},
    {"url":FIX_TO_ERROR.get(p["eco"], "/error"), "title":"Common Error Fixes", "desc":"Exact error message solutions"},
])}
"""
    schemas = howto_schema(
        p["h1"],p["desc"],
        [{"name":"Scan manifest","text":f"Paste your {eco['file']} into PackageFix at packagefix.dev"},
         {"name":"Review CVEs","text":"Check the CVE table for HIGH and CRITICAL severity packages with CISA KEV flags"},
         {"name":"Download fix","text":f"Download the patched {eco['file']} and run {eco['cmd']}"}],
        BASE_URL+path,
        [("PackageFix","/"),("Security Fixes","/fix"),(eco["label"],f"/{p['eco']}"),(p["h1"],path)]
    ) + [faq_schema(faqs)]
    return render_page(
        f"{p['title']} | PackageFix",p["desc"],path,
        [("PackageFix","/"),("Fix Guides","/fix"),(eco["label"],f"/{p['eco']}"),(p["h1"],None)],
        body, schemas
    )

def generate_stack_combo_page(eco_key,pkg,pkg_label,slug,cve,safe_ver,bad,fix,vuln_desc):
    eco = ECOSYSTEMS[eco_key]
    path = "/" + slug
    title = f"Fix {cve} in {pkg_label} — {eco['label']} Vulnerability Fix"
    desc = f"Fix {cve} ({vuln_desc}) in {pkg_label} for {eco['label']}. Paste your {eco['file']} into PackageFix and get a patched version back — no CLI, no signup."
    faqs = [
        (f"What is {cve}?",f"{cve} is a vulnerability in {pkg_label} that allows {vuln_desc}. Update to version {safe_ver} or later to fix it."),
        (f"Is {cve} on the CISA KEV catalog?",f"Check the live CISA KEV catalog at packagefix.dev — the catalog updates daily and PackageFix always reflects the current status."),
        (f"How do I fix {cve} in {pkg_label}?",f"Update {pkg_label} to version {safe_ver} or later in your {eco['file']}. Run {eco['cmd']} after updating."),
        (f"Does {cve} affect all versions of {pkg_label}?",f"Check the OSV advisory for the exact affected version range. PackageFix shows the minimum safe version for your installed version.")
    ]
    body = f"""
<h1>Fix {cve} in {pkg_label} <span class="badge badge-red">HIGH</span></h1>
<p class="lead">{desc}</p>
<div class="problem-box">
  <div class="label">⚠ Vulnerability</div>
  <p style="margin:0"><strong>{cve}</strong> — {vuln_desc} in {pkg_label}. Update to <code>{safe_ver}</code> or later.</p>
</div>
<h2>Vulnerable Version — {eco['file']}</h2>
<pre>{bad}</pre>
<h2>Fixed Version — {eco['file']}</h2>
<pre>{fix}</pre>
<div class="fix-box">
  <div class="label">✓ Fix</div>
  <p style="margin:0">Update to <code>{safe_ver}</code> and run <code>{eco['cmd']}</code> to apply the fix.</p>
</div>
{cta()}
{faq_html(faqs)}
"""
    schemas = howto_schema(
        f"Fix {cve} in {pkg_label}",desc,
        [{"name":"Scan manifest","text":f"Paste your {eco['file']} into PackageFix"},
         {"name":"Find CVE","text":f"Locate {cve} in the CVE table with severity badge"},
         {"name":"Download fix","text":f"Download patched {eco['file']} with {safe_ver}"}],
        BASE_URL+path,
        [("PackageFix","/"),("Fix Guides","/fix"),(eco["label"],f"/{eco_key}"),(f"Fix {cve}",path)]
    ) + [faq_schema(faqs)]
    return render_page(f"{title} | PackageFix",desc,path,
        [("PackageFix","/"),("Fix Guides","/fix"),(eco["label"],f"/{eco_key}"),(f"Fix {cve} in {pkg_label}",None)],
        body, schemas)

def generate_error_page(p):
    path = "/" + p["slug"]
    steps_html = "".join(f"<li style='margin-bottom:8px;color:var(--muted);font-size:12px'>{s}</li>" for s in p["fix_steps"])
    body = f"""
<h1>{p["h1"]}</h1>
<p class="lead">{p["desc"]}</p>
<div class="problem-box">
  <div class="label">⚠ Error Message</div>
  <pre style="margin:0;background:transparent;border:none;padding:0;font-size:11px">{p["error_msg"]}</pre>
</div>
<h2>Root Cause</h2>
<p>{p["cause"]}</p>
<h2>How to Fix</h2>
<ol style="padding-left:20px;margin:12px 0">{steps_html}</ol>
{cta()}
{faq_html(p["faqs"])}
"""
    schemas = [faq_schema(p["faqs"]), {
        "@type":"BreadcrumbList","itemListElement":[
            {"@type":"ListItem","position":1,"name":"PackageFix","item":BASE_URL},
            {"@type":"ListItem","position":2,"name":"Error Fixes","item":BASE_URL+"/error"},
            {"@type":"ListItem","position":3,"name":p["h1"],"item":BASE_URL+path}
        ]
    }]
    return render_page(f"{p['title']} | PackageFix",p["desc"],path,
        [("PackageFix","/"),("Error Fixes","/error"),(p["h1"],None)],
        body, schemas)

def generate_comparison_page(p):
    path = "/" + p["slug"]
    rows_html = "".join(
        f'<tr><td>{feat}</td><td style="color:var(--green)">{pf}</td><td style="color:var(--muted)">{comp}</td></tr>'
        for feat,pf,comp in p["rows"]
    )
    faqs = [
        (f"Is {p['competitor']} still available?",f"{p['competitor']} is {p['status']}. PackageFix is a free, actively maintained alternative."),
        ("Does PackageFix require a GitHub connection?","No. PackageFix runs entirely in your browser. Paste any manifest file — no GitHub, no login, no CLI."),
        ("Is PackageFix free?","Yes — completely free, MIT licensed, open source at github.com/metriclogic26/packagefix."),
        ("What ecosystems does PackageFix support?","npm, PyPI (Python), Ruby (Gemfile), PHP (Composer), Go (go.mod), Rust (Cargo.toml), and Java/Maven (pom.xml).")
    ]
    body = f"""
<h1>{p["h1"]}</h1>
<p class="lead">{p["summary"]}</p>
<table>
  <thead><tr><th>Feature</th><th>PackageFix</th><th>{p["competitor"]}</th></tr></thead>
  <tbody class="vs-table">{rows_html}</tbody>
</table>
{cta()}
{faq_html(faqs)}
"""
    schemas = [faq_schema(faqs), {
        "@type":"BreadcrumbList","itemListElement":[
            {"@type":"ListItem","position":1,"name":"PackageFix","item":BASE_URL},
            {"@type":"ListItem","position":2,"name":"Alternatives","item":BASE_URL+"/alternatives"},
            {"@type":"ListItem","position":3,"name":p["h1"],"item":BASE_URL+path}
        ]
    }]
    return render_page(f"{p['title']} | PackageFix",p["desc"],path,
        [("PackageFix","/"),("Alternatives","/alternatives"),(f"vs {p['competitor']}",None)],
        body, schemas)

def generate_provider_page(slug,provider,eco_key,title,desc,h2,summary,config):
    eco = ECOSYSTEMS.get(eco_key,{"label":eco_key,"file":"manifest","cmd":"install"})
    path = "/" + slug
    faqs = [
        (f"How do I add dependency scanning to {provider}?",f"Add OSV Scanner or the ecosystem-specific audit tool to your {provider} build configuration. The config snippet above works out of the box."),
        ("Does PackageFix integrate with CI/CD pipelines?","PackageFix is a browser tool for manual scans. For automated CI scanning, use OSV Scanner (Google) or pip-audit/npm audit in your pipeline. PackageFix generates the Renovate config and GitHub Actions workflow you can copy."),
        (f"How do I fail a {provider} build on critical CVEs?","Add --audit-level=critical to npm audit, or --fail-on=critical to pip-audit. The pipeline aborts if critical CVEs are found."),
        ("What is the OSV Scanner?","OSV Scanner is Google's open-source CLI tool that queries the same OSV database PackageFix uses. It's ideal for CI/CD integration.")
    ]
    body = f"""
<h1>{title} <span class="badge badge-purple">{provider}</span></h1>
<p class="lead">{desc}</p>
<h2>{h2}</h2>
<p>{summary}</p>
<pre>{config}</pre>
<div class="fix-box">
  <div class="label">✓ Manual Scan</div>
  <p style="margin:0">For a quick one-off scan before deployment, paste your {eco['file']} into PackageFix — no pipeline setup needed.</p>
</div>
{cta()}
{faq_html(faqs)}
"""
    schemas = [faq_schema(faqs), {
        "@type":"BreadcrumbList","itemListElement":[
            {"@type":"ListItem","position":1,"name":"PackageFix","item":BASE_URL},
            {"@type":"ListItem","position":2,"name":"CI/CD Guides","item":BASE_URL+"/providers"},
            {"@type":"ListItem","position":3,"name":title,"item":BASE_URL+path}
        ]
    }]
    return render_page(f"{title} | PackageFix",desc,path,
        [("PackageFix","/"),("CI/CD Guides","/providers"),(title,None)],
        body, schemas)

def generate_ecosystem_page(eco_key,title,desc,h1,lead,manifest_file,install_cmd):
    eco = ECOSYSTEMS[eco_key]
    path = f"/{eco_key}" if eco_key != "pypi" else "/python"
    faqs = [
        (f"How do I scan {eco['label']} dependencies for CVEs?",f"Paste your {eco['file']} into PackageFix. It queries the OSV vulnerability database live and returns a CVE table with fix versions."),
        (f"What {eco['label']} packages have the most CVEs?",f"Check the PackageFix fix guides for the most commonly CVE-flagged {eco['label']} packages."),
        (f"Does PackageFix support {eco['label']} lockfiles?",f"Yes. Drop your lockfile alongside {eco['file']} for full transitive dependency scanning."),
        ("Is PackageFix free?","Yes — completely free, MIT licensed, open source.")
    ]
    body = f"""
<h1>{h1}</h1>
<p class="lead">{lead}</p>
<h2>How to scan {eco['label']} dependencies</h2>
<p>Paste your <code>{eco['file']}</code> into PackageFix. The tool queries the OSV vulnerability database live and returns:</p>
<ul style="padding-left:20px;margin:12px 0 20px;color:var(--muted);font-size:12px">
  <li style="margin-bottom:6px">CVE table with severity badges (CRITICAL, HIGH, MEDIUM, LOW)</li>
  <li style="margin-bottom:6px">CISA KEV flags — actively exploited packages highlighted in red</li>
  <li style="margin-bottom:6px">Side-by-side diff: your versions vs fixed versions</li>
  <li style="margin-bottom:6px">Download fixed {eco['file']} + changelog as .zip</li>
  <li style="margin-bottom:6px">Renovate config + GitHub Actions workflow template</li>
</ul>
{cta()}
{faq_html(faqs)}
<div style="margin:40px 0">
  <h2>Popular {eco['label']} Fix Guides</h2>
  <div class="related-grid">
    {''.join(f'''<div class="related-card"><a href="/fix/{eco_key}/{g['slug'].split('/')[-1]}">{g['h1']}</a><p>{eco['label']} vulnerability fix</p></div>''' for g in FIX_PAGES if g['eco']==eco_key)[:4]}
  </div>
</div>
"""
    schemas = [faq_schema(faqs), {
        "@type":"BreadcrumbList","itemListElement":[
            {"@type":"ListItem","position":1,"name":"PackageFix","item":BASE_URL},
            {"@type":"ListItem","position":2,"name":h1,"item":BASE_URL+path}
        ]
    }]
    return render_page(title,desc,path,
        [("PackageFix","/"),(h1,None)],
        body, schemas)

# ══════════════════════════════════════════════════════════════════════════════
# WRITE ALL PAGES
# ══════════════════════════════════════════════════════════════════════════════

all_paths = []

def write(slug, html):
    path = os.path.join("seo", slug, "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    all_paths.append("/" + slug)
    print(f"  ✓ /{slug}")

print("\n📦 Generating fix pages...")
for p in FIX_PAGES:
    write(p["slug"], generate_fix_page(p))

print("\n🔧 Generating ecosystem × stack combo pages...")
for combo in STACK_COMBOS:
    write(combo[3], generate_stack_combo_page(*combo))

print("\n⚠ Generating error pages...")
for p in ERROR_PAGES:
    write(p["slug"], generate_error_page(p))

error_index_body = """
<h1>Dependency Error Fixes</h1>
<p class="lead">Exact error message fixes for npm, PyPI, Ruby, and PHP dependency issues.</p>
<div class="related-grid">
""" + "".join(
    f'<div class="related-card"><a href="/{p["slug"]}">{p["h1"]}</a><p>{p["desc"][:80]}...</p></div>'
    for p in ERROR_PAGES
) + """</div>"""

write("error", render_page(
    "Dependency Error Fixes | PackageFix",
    "Fix npm, PyPI, Ruby and PHP dependency errors. Exact error message match pages with step-by-step fixes.",
    "/error",
    [("PackageFix", "/"), ("Error Fixes", None)],
    error_index_body,
    [{"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "PackageFix", "item": "https://packagefix.dev"},
        {"@type": "ListItem", "position": 2, "name": "Error Fixes", "item": "https://packagefix.dev/error"}
    ]}]
))

print("\n⚔ Generating comparison pages...")
for p in COMPARISON_PAGES:
    write(p["slug"], generate_comparison_page(p))

print("\n🏗 Generating provider/CI pages...")
for args in PROVIDER_PAGES:
    write(args[0], generate_provider_page(*args))

print("\n🌐 Generating ecosystem landing pages...")
for args in ECOSYSTEM_PAGES:
    write(args[0] if args[0] != "pypi" else "python", generate_ecosystem_page(*args))
    # also write /pypi alias
    if args[0] == "pypi":
        write("pypi", generate_ecosystem_page(*args))

# ── vercel.json rewrites ───────────────────────────────────────────────────────
print("\n📝 Writing vercel.json rewrites...")
rewrites = []
for p in all_paths:
    rewrites.append({"source": p, "destination": f"/seo{p}/index.html"})
    rewrites.append({"source": p + "/", "destination": f"/seo{p}/index.html"})

# Load existing vercel.json if present
vercel_config = {}
if os.path.exists("vercel.json"):
    with open("vercel.json") as f:
        vercel_config = json.load(f)

existing_rewrites = vercel_config.get("rewrites", [])
new_rewrites = existing_rewrites + [r for r in rewrites if r not in existing_rewrites]
vercel_config["rewrites"] = new_rewrites

with open("vercel.json", "w") as f:
    json.dump(vercel_config, f, indent=2)
print("  ✓ vercel.json updated")

# ── llm.txt ────────────────────────────────────────────────────────────────────
print("\n🤖 Writing llm.txt...")
llm_content = """# PackageFix — packagefix.dev
# Free dependency security scanner. Paste manifest, get fixed version. No signup, no CLI.
# Vulnerability data: OSV database (live daily updates) + CISA Known Exploited Vulnerabilities

## What PackageFix Does
Paste a dependency manifest file. Get back a fixed version with CVE patches, CISA KEV alerts, side-by-side diff, and downloadable .zip. Everything runs in the browser — nothing sent to a server.

## Supported Ecosystems
npm (package.json), Python/PyPI (requirements.txt, poetry.lock), Ruby (Gemfile, Gemfile.lock), PHP/Composer (composer.json, composer.lock), Go (go.mod), Rust (Cargo.toml, Cargo.lock), Java/Maven (pom.xml)

## Key Features
- CISA KEV flag: actively exploited vulnerabilities highlighted in red ("fix these first")
- Side-by-side diff: your versions vs fixed versions
- Download fixed manifest as .zip with changelog
- Transitive dependency scanning via lockfile upload
- Supply chain detection: Glassworm/Unicode injection, typosquatting, zombie packages, build script danger
- Unpinned version warnings
- Package health score 0-100

## Why PackageFix Exists
Snyk Advisor shut down January 2026. Every remaining tool (Dependabot, npm audit, pip-audit, bundle-audit, cargo-audit) requires CLI installation or GitHub access. PackageFix is the browser-based alternative — paste and get the fixed file.

## License
MIT — https://github.com/metriclogic26/packagefix

## Fix Guides
"""
for p in all_paths:
    llm_content += f"{BASE_URL}{p}\n"

with open("llm.txt", "w") as f:
    f.write(llm_content)
print("  ✓ llm.txt written")

# ── sitemap-seo.xml ────────────────────────────────────────────────────────────
print("\n🗺 Writing sitemap-seo.xml...")
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for p in all_paths:
    sitemap += f"""  <url>
    <loc>{BASE_URL}{p}</loc>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>\n"""
sitemap += "</urlset>"
with open("sitemap-seo.xml", "w") as f:
    f.write(sitemap)
print("  ✓ sitemap-seo.xml written")

print(f"\n✅ Done — {len(all_paths)} pages generated in ./seo/")
print(f"   vercel.json updated with {len(rewrites)} rewrite rules")
print(f"   llm.txt written")
print(f"   sitemap-seo.xml written with {len(all_paths)} URLs")

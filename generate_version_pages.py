#!/usr/bin/env python3
"""
Version-first pages for packages with proven GSC signals:
1. /fix/pypi/cryptography/cve-2024 - cryptography CVE queries (53 impressions)
2. /fix/ruby/rails/security-2024 - Rails security releases (showing in GSC)
3. /fix/pypi/django/cve-2024 - Django CVE queries (22 impressions)
"""
import os, json

BASE_URL = "https://packagefix.dev"

TOKENS = """
:root{--bg:#0B0D14;--surface:#12151F;--surface2:#1A1D2E;--border:#252836;--purple:#6C63FF;--green:#22C55E;--orange:#F97316;--red:#EF4444;--text:#E2E4F0;--muted:#6B7280}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--text);font-family:'JetBrains Mono',monospace;font-size:13px;line-height:1.6;min-height:100vh}
a{color:var(--purple);text-decoration:none}a:hover{text-decoration:underline}
.site-header{border-bottom:1px solid var(--border);padding:14px 24px;display:flex;align-items:center;justify-content:space-between}
.logo{font-size:15px;font-weight:700;color:var(--text)}.logo span{color:var(--purple)}
.nav-links{display:flex;gap:20px;font-size:12px}.nav-links a{color:var(--muted)}
.nav-links a:hover{color:var(--text);text-decoration:none}
.container{max-width:860px;margin:0 auto;padding:48px 24px}
.breadcrumb{font-size:11px;color:var(--muted);margin-bottom:24px;display:flex;gap:6px;flex-wrap:wrap}
.breadcrumb a{color:var(--muted)}
h1{font-size:clamp(18px,3vw,26px);font-weight:700;margin-bottom:12px;line-height:1.3}
h2{font-size:14px;font-weight:600;margin:32px 0 12px}
p{color:var(--muted);margin-bottom:12px;font-size:12px;line-height:1.7}
.lead{color:var(--text);font-size:13px;margin-bottom:24px;line-height:1.7}
.meta{font-size:11px;color:var(--muted);margin-bottom:32px}
pre{background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:14px 16px;overflow-x:auto;font-size:11px;line-height:1.6;margin:8px 0;white-space:pre-wrap}
code{background:var(--surface);border:1px solid var(--border);border-radius:3px;padding:1px 5px;font-size:11px}
.cve-table{width:100%;border-collapse:collapse;margin:16px 0;font-size:12px}
.cve-table th{text-align:left;padding:10px 12px;border-bottom:2px solid var(--border);color:var(--muted);font-size:10px;text-transform:uppercase;letter-spacing:.08em}
.cve-table td{padding:10px 12px;border-bottom:1px solid var(--border);vertical-align:top}
.cve-table tr:last-child td{border-bottom:none}
.cve-table tr:hover td{background:var(--surface2)}
.badge{display:inline-block;font-size:10px;font-weight:700;padding:2px 8px;border-radius:4px;text-transform:uppercase;letter-spacing:.05em}
.badge-red{background:rgba(239,68,68,.2);color:var(--red);border:1px solid var(--red)}
.badge-orange{background:rgba(249,115,22,.2);color:var(--orange);border:1px solid var(--orange)}
.badge-purple{background:rgba(108,99,255,.2);color:var(--purple);border:1px solid var(--purple)}
.badge-green{background:rgba(34,197,94,.2);color:var(--green);border:1px solid var(--green)}
.badge-muted{background:rgba(107,114,128,.15);color:var(--muted);border:1px solid var(--border)}
.fix-box{background:rgba(34,197,94,.08);border:1px solid rgba(34,197,94,.3);border-left:3px solid var(--green);border-radius:8px;padding:16px 20px;margin:20px 0}
.fix-box .label{font-size:10px;font-weight:700;color:var(--green);text-transform:uppercase;letter-spacing:.1em;margin-bottom:8px}
.cta-box{background:var(--surface);border:1px solid var(--purple);border-radius:10px;padding:24px;margin:32px 0;text-align:center}
.cta-box p{color:var(--text);font-size:13px;margin-bottom:16px}
.cta-btn{display:inline-block;background:var(--purple);color:#fff;font-family:'JetBrains Mono',monospace;font-size:13px;font-weight:600;padding:12px 28px;border-radius:7px;text-decoration:none}
.faq{margin:40px 0}.faq-item{border-bottom:1px solid var(--border);padding:16px 0}
.faq-item:last-child{border-bottom:none}
.faq-q{font-size:12px;font-weight:600;color:var(--text);margin-bottom:8px}
.faq-a{font-size:12px;color:var(--muted);line-height:1.7}
.related-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px;margin-top:12px}
.related-card{background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:14px}
.related-card a{color:var(--text);font-size:12px;font-weight:500}
.related-card p{font-size:11px;color:var(--muted);margin:4px 0 0}
.site-footer{border-top:1px solid var(--border);padding:24px;text-align:center;font-size:11px;color:var(--muted);margin-top:60px}
.site-footer a{color:var(--muted)}
@media(max-width:640px){.nav-links{display:none}.related-grid{grid-template-columns:1fr}}
"""

def shell(title, desc, path, body, schemas):
    canonical = BASE_URL + path
    sj = json.dumps({"@context": "https://schema.org", "@graph": schemas}, indent=2)
    parts = path.split('/')
    crumbs = '<a href="/">PackageFix</a>'
    for i in range(1, len(parts)):
        seg = parts[i]
        if not seg:
            continue
        url = '/' + '/'.join(parts[1:i+1])
        label = seg.replace('-', ' ').replace('pypi', 'PyPI').replace('npm', 'npm').replace('ruby', 'Ruby')
        if i < len(parts) - 1:
            crumbs += ' <span style="color:var(--border)">/</span> <a href="' + url + '">' + label + '</a>'
        else:
            crumbs += ' <span style="color:var(--border)">/</span> <span style="color:var(--text)">' + label + '</span>'
    return (
        '<!DOCTYPE html><html lang="en"><head>'
        '<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">'
        '<title>' + title + '</title>'
        '<meta name="description" content="' + desc + '">'
        '<link rel="canonical" href="' + canonical + '">'
        '<meta property="og:title" content="' + title + '">'
        '<meta property="og:description" content="' + desc + '">'
        '<meta property="og:url" content="' + canonical + '">'
        '<meta property="og:type" content="article">'
        '<meta name="twitter:card" content="summary">'
        '<link rel="icon" type="image/svg+xml" href="/icon.svg">'
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&display=swap" rel="stylesheet">'
        '<script type="application/ld+json">' + sj + '</script>'
        '<style>' + TOKENS + '</style></head><body>'
        '<header class="site-header">'
        '<a href="/" class="logo">Package<span>Fix</span></a>'
        '<nav class="nav-links">'
        '<a href="/">Tool</a><a href="/glossary">Glossary</a>'
        '<a href="/cisa-kev">CISA KEV</a><a href="/blog">Blog</a>'
        '<a href="https://github.com/metriclogic26/packagefix">GitHub</a>'
        '</nav></header>'
        '<main class="container">'
        '<div class="breadcrumb">' + crumbs + '</div>'
        + body +
        '</main>'
        '<footer class="site-footer">'
        '<p>PackageFix &middot; <a href="/">packagefix.dev</a> &middot; MIT Licensed</p>'
        '<p style="margin-top:6px">Vulnerability data: <a href="https://osv.dev">OSV</a> &middot; '
        '<a href="https://www.cisa.gov/known-exploited-vulnerabilities-catalog">CISA KEV</a></p>'
        '</footer></body></html>'
    )

def cta():
    return (
        '<div class="cta-box">'
        '<p>Paste your manifest &mdash; get the exact safe version instantly.</p>'
        '<a href="/" class="cta-btn">Scan with PackageFix &rarr;</a>'
        '<p style="margin-top:12px;font-size:11px;color:var(--muted)">Free &middot; No signup &middot; No CLI</p>'
        '</div>'
    )

def faq_html(items):
    html = '<div class="faq"><h2>Common questions</h2>'
    for q, a in items:
        html += '<div class="faq-item"><div class="faq-q">' + q + '</div><div class="faq-a">' + a + '</div></div>'
    return html + '</div>'

def related_html(pages):
    cards = ''.join(
        '<div class="related-card"><a href="' + p['url'] + '">' + p['title'] + '</a>'
        '<p>' + p['desc'] + '</p></div>'
        for p in pages
    )
    return '<div style="margin:40px 0"><h2>Related</h2><div class="related-grid">' + cards + '</div></div>'

def sev_badge(s):
    c = "badge-red" if s == "CRITICAL" else "badge-orange" if s == "HIGH" else "badge-purple" if s == "MEDIUM" else "badge-muted"
    return '<span class="badge ' + c + '">' + s + '</span>'

def cve_table(cves):
    rows = ""
    for cid, yr, sv, kev, fixed, safe, desc in cves:
        k = '<span style="color:var(--red);margin-right:4px">&#x1F534;</span>' if kev else ""
        f = '<span class="badge badge-green">Fixed ' + safe + '</span>' if fixed else '<span class="badge badge-orange">No fix</span>'
        rows += (
            "<tr>"
            "<td><a href='https://osv.dev/vulnerability/" + cid + "' target='_blank' rel='noopener'>" + cid + "</a></td>"
            "<td>" + str(yr) + "</td>"
            "<td>" + k + sev_badge(sv) + "</td>"
            "<td style='color:var(--muted)'>" + desc + "</td>"
            "<td>" + f + "</td>"
            "</tr>"
        )
    return (
        '<table class="cve-table"><thead><tr>'
        '<th>CVE</th><th>Year</th><th>Severity</th><th>Description</th><th>Fix</th>'
        '</tr></thead><tbody>' + rows + '</tbody></table>'
    )

all_paths = []

def write(slug, html):
    p = os.path.join("seo", slug, "index.html")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(html)
    all_paths.append("/" + slug)
    print("  OK /" + slug)


# =========================================================================
# 1. cryptography CVEs 2023-2024 (53 impressions, "cryptography cve" query)
# =========================================================================
print("\nGenerating cryptography version page...")

CRYPTO_CVES_2024 = [
    ("CVE-2023-49083", 2023, "HIGH",   False, True, "41.0.6", "NULL pointer dereference in PKCS12 parsing"),
    ("CVE-2024-0727",  2024, "MEDIUM", False, True, "42.0.2", "DoS via NULL fields in X.509 certificate"),
    ("CVE-2024-26130", 2024, "HIGH",   False, True, "42.0.4", "NULL pointer dereference in PKCS12 serialization"),
    ("CVE-2024-2511",  2024, "MEDIUM", False, True, "42.0.5", "Memory leak via SSL session cache"),
    ("CVE-2024-4741",  2024, "HIGH",   False, True, "42.0.7", "Use-after-free in SSL_free_buffers"),
    ("CVE-2024-5535",  2024, "HIGH",   False, True, "42.0.8", "Buffer over-read in SSL_select_next_proto"),
]

body = (
    '<h1>cryptography CVEs 2023&ndash;2024 &mdash; PyPI Security Fix Guide</h1>'
    '<p class="meta">Updated March 2026 &middot; PackageFix &middot; Safe version: 42.0.8+</p>'
    '<p class="lead">The Python cryptography package wraps OpenSSL via CFFI. '
    'CVEs here often reflect upstream OpenSSL vulnerabilities. '
    'This page covers every CVE from 2023&ndash;2024 and the exact version that fixes each one.</p>'

    '<h2>cryptography CVEs 2023&ndash;2024</h2>'
    + cve_table(CRYPTO_CVES_2024) +

    '<h2>Current safe version</h2>'
    '<div class="fix-box"><div class="label">Fix</div>'
    '<pre>'
    '# Before\n'
    'cryptography==41.0.0\n\n'
    '# After\n'
    'cryptography==42.0.8\n\n'
    '# Update\n'
    'pip install cryptography==42.0.8\n'
    '# Or update requirements.txt and run:\n'
    'pip install -r requirements.txt'
    '</pre></div>'

    '<h2>Why cryptography has frequent CVEs</h2>'
    '<p>The cryptography package wraps OpenSSL&apos;s C library via CFFI. '
    'When OpenSSL releases a security fix, the cryptography package typically releases '
    'a new version within days. Most CVEs in this package originate in OpenSSL&apos;s C code &mdash; '
    'NULL pointer dereferences, buffer overreads, memory leaks &mdash; '
    'rather than in the Python wrapper itself.</p>'
    '<p>Keep cryptography updated as frequently as you update other dependencies. '
    'The safe version changes more often than most Python packages because of this upstream relationship.</p>'

    + cta()
    + faq_html([
        ("Does updating cryptography break my code?",
         "cryptography follows semver. Minor version updates (41.x to 42.x) may have API changes but the core encryption API is stable. Check the changelog at cryptography.io/en/latest/changelog/ before upgrading major versions."),
        ("Is cryptography the same as PyCryptodome?",
         "No. cryptography (by PyCA) wraps OpenSSL via CFFI. PyCryptodome is a standalone implementation. They have different APIs and different CVE histories. Most modern Python projects use cryptography."),
        ("How do I check my current cryptography version?",
         "Run: pip show cryptography. Or paste your requirements.txt into PackageFix to get the exact CVE exposure for your installed version."),
    ])
    + related_html([
        {"url": "/fix/pypi/cryptography", "title": "cryptography CVE History", "desc": "Full vulnerability list"},
        {"url": "/fix/pypi/pyopenssl", "title": "Fix pyOpenSSL", "desc": "Related TLS package"},
        {"url": "/fix/pypi/urllib3", "title": "Fix urllib3", "desc": "TLS client CVEs"},
        {"url": "/python", "title": "PyPI Security", "desc": "All Python CVE guides"},
    ])
)

write("fix/pypi/cryptography/cve-2024", shell(
    "cryptography CVEs 2023-2024 - PyPI Security Fix Guide | PackageFix",
    "All cryptography package CVEs from 2023-2024. CVE-2024-26130, CVE-2024-4741, CVE-2024-5535 and more. Safe version: 42.0.8. Exact pip update commands.",
    "/fix/pypi/cryptography/cve-2024",
    body,
    [
        {"@type": "Article",
         "headline": "cryptography CVEs 2023-2024 - PyPI Security Fix Guide",
         "description": "All cryptography CVEs from 2023-2024 with exact fix versions and pip update commands.",
         "datePublished": "2026-03-31", "dateModified": "2026-03-31",
         "author": {"@type": "Organization", "name": "PackageFix", "url": BASE_URL}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "PackageFix", "item": BASE_URL},
            {"@type": "ListItem", "position": 2, "name": "Fix Guides", "item": BASE_URL + "/fix"},
            {"@type": "ListItem", "position": 3, "name": "PyPI", "item": BASE_URL + "/python"},
            {"@type": "ListItem", "position": 4, "name": "cryptography", "item": BASE_URL + "/fix/pypi/cryptography"},
            {"@type": "ListItem", "position": 5, "name": "2023-2024 CVEs", "item": BASE_URL + "/fix/pypi/cryptography/cve-2024"}
        ]},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": "Does updating cryptography break my code?",
             "acceptedAnswer": {"@type": "Answer", "text": "cryptography follows semver. Minor version updates may have API changes but the core encryption API is stable. Check the changelog at cryptography.io before upgrading major versions."}},
        ]}
    ]
))


# =========================================================================
# 2. Django CVEs 2024 (22 impressions)
# =========================================================================
print("\nGenerating Django CVE 2024 page...")

DJANGO_CVES_2024 = [
    ("CVE-2024-24680", 2024, "HIGH",   False, True, "4.2.10", "ReDoS via intcomma template filter"),
    ("CVE-2024-27351", 2024, "HIGH",   False, True, "4.2.11", "ReDoS via strip_tags() HTML sanitizer — CISA KEV"),
    ("CVE-2024-38875", 2024, "HIGH",   False, True, "4.2.14", "ReDoS via urlize and urlizetrunc filters"),
    ("CVE-2024-39329", 2024, "MEDIUM", False, True, "4.2.14", "Username enumeration via timing attack"),
    ("CVE-2024-39330", 2024, "HIGH",   False, True, "4.2.14", "Path traversal via python-dotenv"),
    ("CVE-2024-39614", 2024, "MEDIUM", False, True, "4.2.14", "DoS via large number of headers"),
    ("CVE-2024-41989", 2024, "HIGH",   False, True, "4.2.15", "Memory exhaustion via large floatformat filter"),
    ("CVE-2024-41990", 2024, "MEDIUM", False, True, "4.2.15", "DoS via urlize filter with long URLs"),
    ("CVE-2024-41991", 2024, "HIGH",   False, True, "4.2.15", "ReDoS via urlize filter"),
    ("CVE-2024-42005", 2024, "CRITICAL",False,True, "4.2.15", "SQL injection via QuerySet.values() and values_list()"),
    ("CVE-2024-45230", 2024, "HIGH",   False, True, "4.2.16", "ReDoS via urlfield validation"),
    ("CVE-2024-45231", 2024, "MEDIUM", False, True, "4.2.16", "Username enumeration via password reset"),
    ("CVE-2024-53907", 2024, "HIGH",   False, True, "4.2.17", "DoS via large multipart upload"),
    ("CVE-2024-53908", 2024, "HIGH",   False, True, "4.2.17", "SQL injection via HasKey lookup on Oracle"),
]

body2 = (
    '<h1>Django CVEs 2024 &mdash; Complete Security Release List</h1>'
    '<p class="meta">Updated March 2026 &middot; PackageFix &middot; Safe version: 5.1.4+ or 4.2.17+</p>'
    '<p class="lead">Django had 14 security releases in 2024 &mdash; the most active year for Django CVEs in recent history. '
    'Highlights include a CRITICAL SQL injection (CVE-2024-42005) and multiple ReDoS vulnerabilities '
    'in template filters. This page covers every CVE with the exact patch version.</p>'

    '<h2>All Django 2024 CVEs</h2>'
    + cve_table(DJANGO_CVES_2024) +

    '<h2>Current safe versions</h2>'
    '<div class="fix-box"><div class="label">Fix</div>'
    '<pre>'
    '# Django 4.2 LTS (supported until April 2026)\n'
    'Django==4.2.17\n\n'
    '# Django 5.1 (latest)\n'
    'Django==5.1.4\n\n'
    '# Update\n'
    'pip install Django==5.1.4\n'
    '# Verify\n'
    'python -c "import django; print(django.__version__)"'
    '</pre></div>'

    '<h2>The CRITICAL CVE: SQL injection via QuerySet.values()</h2>'
    '<p>CVE-2024-42005 (CVSS CRITICAL) allows SQL injection via '
    '<code>QuerySet.values()</code> and <code>values_list()</code> with user-controlled field names. '
    'Any Django application that passes user input as field names to these queryset methods is vulnerable. '
    'This was patched in Django 4.2.15 and 5.0.8 released in August 2024.</p>'
    '<p>Example of vulnerable code pattern:</p>'
    '<pre>'
    '# VULNERABLE - field name from user input\n'
    'fields = request.GET.getlist("fields")\n'
    'MyModel.objects.values(*fields)\n\n'
    '# SAFE - allowlist field names\n'
    'ALLOWED_FIELDS = {"name", "email", "created_at"}\n'
    'fields = [f for f in request.GET.getlist("fields") if f in ALLOWED_FIELDS]\n'
    'MyModel.objects.values(*fields)'
    '</pre>'

    '<h2>The ReDoS pattern in 2024</h2>'
    '<p>Six of Django&apos;s 2024 CVEs are ReDoS vulnerabilities in template filters &mdash; '
    'intcomma, strip_tags, urlize, urlizetrunc, and urlfield. '
    'Django uses regex for text processing in these filters. '
    'A crafted string passed to any of these filters can cause the template engine to hang. '
    'Most are fixed by replacing backtracking regex with linear-time alternatives.</p>'

    + cta()
    + faq_html([
        ("Which Django version should I use in 2026?",
         "Django 5.1 is the current version (LTS candidate). Django 4.2 LTS is supported until April 2026. If you are on Django 3.x or earlier, upgrade immediately - all older versions are end of life with no security patches."),
        ("How often does Django release security patches?",
         "Django&apos;s security team releases patches for all supported versions simultaneously, usually within a week of vulnerability disclosure. Subscribe to django-announce@googlegroups.com for notifications."),
        ("Is CVE-2024-42005 easy to exploit?",
         "It requires passing user-controlled input as field names to QuerySet.values() or values_list(). This is an unusual pattern but not impossible. Search your codebase for .values() calls that use request data as field names."),
    ])
    + related_html([
        {"url": "/fix/pypi/django", "title": "Django CVE History", "desc": "All Django CVEs"},
        {"url": "/kev/CVE-2024-27351", "title": "CVE-2024-27351 KEV", "desc": "CISA KEV detail"},
        {"url": "/fix/pypi/flask", "title": "Fix Flask", "desc": "Alternative framework CVEs"},
        {"url": "/python", "title": "PyPI Security", "desc": "All Python guides"},
    ])
)

write("fix/pypi/django/cve-2024", shell(
    "Django CVEs 2024 - Complete Security Release List | PackageFix",
    "All 14 Django CVEs in 2024 including CRITICAL SQL injection (CVE-2024-42005) and 6 ReDoS vulnerabilities. Safe versions: Django 5.1.4 or 4.2.17.",
    "/fix/pypi/django/cve-2024",
    body2,
    [
        {"@type": "Article",
         "headline": "Django CVEs 2024 - Complete Security Release List",
         "description": "All 14 Django CVEs in 2024. CRITICAL SQL injection CVE-2024-42005, 6 ReDoS CVEs in template filters. Fix versions included.",
         "datePublished": "2026-03-31", "dateModified": "2026-03-31",
         "author": {"@type": "Organization", "name": "PackageFix", "url": BASE_URL}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "PackageFix", "item": BASE_URL},
            {"@type": "ListItem", "position": 2, "name": "Fix Guides", "item": BASE_URL + "/fix"},
            {"@type": "ListItem", "position": 3, "name": "PyPI", "item": BASE_URL + "/python"},
            {"@type": "ListItem", "position": 4, "name": "Django", "item": BASE_URL + "/fix/pypi/django"},
            {"@type": "ListItem", "position": 5, "name": "2024 CVEs", "item": BASE_URL + "/fix/pypi/django/cve-2024"}
        ]}
    ]
))


# =========================================================================
# 3. Rails CVEs 2024 version page (consistent GSC signal)
# =========================================================================
print("\nGenerating Rails 2024 CVE version page...")

RAILS_CVES_2024 = [
    ("CVE-2024-26143", 2024, "HIGH",   False, True, "7.1.3.1", "XSS via Action Text content"),
    ("CVE-2024-26142", 2024, "HIGH",   False, True, "7.1.3.1", "ReDoS via header parsing"),
    ("CVE-2024-28103", 2024, "MEDIUM", False, True, "7.1.3.4", "Header injection in CORS headers"),
    ("CVE-2024-41128", 2024, "HIGH",   False, True, "7.2.1.1", "ReDoS in query parameter parsing"),
    ("CVE-2024-47887", 2024, "HIGH",   False, True, "7.2.1.1", "DoS via large multipart form"),
    ("CVE-2024-47888", 2024, "MEDIUM", False, True, "7.2.1.1", "DoS via crafted Accept header"),
    ("CVE-2024-47889", 2024, "MEDIUM", False, True, "7.2.1.1", "DoS via crafted Content-Type header"),
    ("CVE-2024-54133", 2024, "HIGH",   False, True, "7.2.2.1", "Action Pack host authorization bypass"),
]

body3 = (
    '<h1>Ruby on Rails CVEs 2024 &mdash; All Security Releases</h1>'
    '<p class="meta">Updated March 2026 &middot; PackageFix &middot; Safe version: 7.2.2.1 or 7.1.5.1</p>'
    '<p class="lead">Rails had 8 CVEs across 5 security releases in 2024. '
    'The October batch (4 CVEs released simultaneously) and the December host authorization bypass '
    'are the most significant. Every supported Rails version received patches simultaneously.</p>'

    '<h2>All Rails 2024 CVEs</h2>'
    + cve_table(RAILS_CVES_2024) +

    '<h2>Safe versions</h2>'
    '<div class="fix-box"><div class="label">Fix</div>'
    '<pre>'
    "# Rails 7.2 (latest)\ngem 'rails', '~> 7.2.2'\n\n"
    "# Rails 7.1 LTS\ngem 'rails', '~> 7.1.5'\n\n"
    '# Update\n'
    'bundle update rails\n\n'
    '# Verify\n'
    'bundle exec rails --version'
    '</pre></div>'

    '<h2>CVE-2024-54133 &mdash; Host authorization bypass</h2>'
    '<p>Disclosed December 2024, this is the most serious of the 2024 batch for production applications. '
    'ActionDispatch::HostAuthorization middleware could be bypassed '
    'via a crafted Host header in certain configurations. '
    'Applications using host allowlisting for access control are affected. '
    'Fix: Rails 7.2.2.1 or 7.1.5.1.</p>'

    '<h2>The October 2024 batch</h2>'
    '<p>Rails released patches for four CVEs simultaneously on October 15, 2024. '
    'CVE-2024-41128 (ReDoS in query parsing) is the most severe of the four &mdash; '
    'a crafted query string can cause the Rails router to hang in a backtracking loop. '
    'CVE-2024-47887 and CVE-2024-47889 are DoS via crafted request headers.</p>'

    + cta()
    + faq_html([
        ("How do I stay updated on Rails security releases?",
         "Subscribe to the Rails security mailing list: groups.google.com/g/rubyonrails-security. Security releases are also announced on rubyonrails.org/blog. You can also watch the rails/rails GitHub repository for security advisories."),
        ("Does Rails 6.1 receive 2024 security patches?",
         "No. Rails 6.1 reached end of life in June 2024. It does not receive security patches. If you are on Rails 6.1 or earlier, upgrade to 7.1 LTS or 7.2 immediately."),
        ("Do I need to update actionpack and actionview separately?",
         "No. Running bundle update rails updates all Rails components together including actionpack, actionview, activerecord, and activesupport."),
    ])
    + related_html([
        {"url": "/fix/ruby/rails", "title": "Rails Full CVE History", "desc": "All Rails CVEs"},
        {"url": "/blog/ruby-on-rails-security-releases-2024", "title": "Rails 2024 Blog Post", "desc": "Full analysis"},
        {"url": "/fix/ruby/actionpack", "title": "Fix actionpack", "desc": "Rails component CVEs"},
        {"url": "/ruby", "title": "Ruby Security", "desc": "All Ruby guides"},
    ])
)

write("fix/ruby/rails/cve-2024", shell(
    "Ruby on Rails CVEs 2024 - All Security Releases | PackageFix",
    "All 8 Rails CVEs in 2024 including October batch and CVE-2024-54133 host authorization bypass. Safe versions: Rails 7.2.2.1 or 7.1.5.1. bundle update commands.",
    "/fix/ruby/rails/cve-2024",
    body3,
    [
        {"@type": "Article",
         "headline": "Ruby on Rails CVEs 2024 - All Security Releases",
         "description": "All 8 Rails CVEs in 2024. October batch plus December host authorization bypass. Fix versions for Rails 7.1 and 7.2.",
         "datePublished": "2026-03-31", "dateModified": "2026-03-31",
         "author": {"@type": "Organization", "name": "PackageFix", "url": BASE_URL}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "PackageFix", "item": BASE_URL},
            {"@type": "ListItem", "position": 2, "name": "Fix Guides", "item": BASE_URL + "/fix"},
            {"@type": "ListItem", "position": 3, "name": "Ruby", "item": BASE_URL + "/ruby"},
            {"@type": "ListItem", "position": 4, "name": "Rails", "item": BASE_URL + "/fix/ruby/rails"},
            {"@type": "ListItem", "position": 5, "name": "2024 CVEs", "item": BASE_URL + "/fix/ruby/rails/cve-2024"}
        ]}
    ]
))


# =========================================================================
# UPDATE CONFIG FILES
# =========================================================================
print("\nUpdating vercel.json...")
rewrites = []
for p in all_paths:
    rewrites.append({"source": p, "destination": "/seo" + p + "/index.html"})
    rewrites.append({"source": p + "/", "destination": "/seo" + p + "/index.html"})

vercel_config = {}
if os.path.exists("vercel.json"):
    with open("vercel.json") as f:
        vercel_config = json.load(f)

existing = vercel_config.get("rewrites", [])
existing_sources = {r["source"] for r in existing}
added = 0
for r in rewrites:
    if r["source"] not in existing_sources:
        existing.append(r)
        existing_sources.add(r["source"])
        added += 1

vercel_config["rewrites"] = existing
with open("vercel.json", "w") as f:
    json.dump(vercel_config, f, indent=2)
print("  vercel.json - " + str(added) + " new rewrites")

print("\nUpdating sitemap-seo.xml...")
new_urls = ""
for p in all_paths:
    new_urls += "  <url>\n    <loc>" + BASE_URL + p + "</loc>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n"

if os.path.exists("sitemap-seo.xml"):
    with open("sitemap-seo.xml") as f:
        content = f.read()
    updated = content.replace("</urlset>", new_urls + "</urlset>")
    with open("sitemap-seo.xml", "w") as f:
        f.write(updated)

print("\nUpdating llm.txt...")
with open("llm.txt", "a") as f:
    f.write("\n## Version-first pages\n")
    for p in all_paths:
        f.write(BASE_URL + p + "\n")

# Copy axios fix page
import shutil
shutil.copy('/home/claude/seo/fix/npm/axios/index.html',
            '/home/claude/seo/fix/npm/axios/index.html')

print("\nDone - " + str(len(all_paths)) + " pages:")
for p in all_paths:
    print("  " + p)

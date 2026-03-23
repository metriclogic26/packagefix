#!/usr/bin/env python3
"""
PackageFix — Missing Index Pages + Remaining Items
1. /fix index
2. /guides index
3. /providers index
4. ~40 remaining CVE history tables
5. 5 missing KEV pages
6. 6 glossary terms
7. Weekly CVE digest #2
8. 4 comparison pages
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
h3{font-size:12px;font-weight:600;margin:20px 0 8px;color:var(--muted);text-transform:uppercase;letter-spacing:.08em}
p{color:var(--muted);margin-bottom:12px;font-size:12px;line-height:1.7}
.lead{color:var(--text);font-size:13px;margin-bottom:24px;line-height:1.7}
.definition-box{background:var(--surface);border:1px solid var(--purple);border-left:4px solid var(--purple);border-radius:8px;padding:20px 24px;margin:0 0 32px}
.definition-box .def-label{font-size:10px;font-weight:700;color:var(--purple);text-transform:uppercase;letter-spacing:.1em;margin-bottom:8px}
.definition-box p{color:var(--text);font-size:13px;line-height:1.7;margin:0}
.kev-banner{background:rgba(239,68,68,.12);border:1px solid var(--red);border-radius:10px;padding:16px 20px;margin:24px 0}
.kev-banner .label{font-size:10px;font-weight:700;color:var(--red);text-transform:uppercase;letter-spacing:.1em;margin-bottom:6px}
.kev-banner p{color:var(--red);margin:0;font-size:12px}
pre{background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:14px 16px;overflow-x:auto;font-size:11px;line-height:1.6;margin:8px 0;white-space:pre-wrap}
code{background:var(--surface);border:1px solid var(--border);border-radius:3px;padding:1px 5px;font-size:11px}
.cta-box{background:var(--surface);border:1px solid var(--purple);border-radius:10px;padding:24px;margin:32px 0;text-align:center}
.cta-box p{color:var(--text);font-size:13px;margin-bottom:16px}
.cta-btn{display:inline-block;background:var(--purple);color:#fff;font-family:'JetBrains Mono',monospace;font-size:13px;font-weight:600;padding:12px 28px;border-radius:7px;text-decoration:none}
.badge{display:inline-block;font-size:10px;font-weight:700;padding:2px 8px;border-radius:4px;text-transform:uppercase;letter-spacing:.05em}
.badge-red{background:rgba(239,68,68,.2);color:var(--red);border:1px solid var(--red)}
.badge-orange{background:rgba(249,115,22,.2);color:var(--orange);border:1px solid var(--orange)}
.badge-green{background:rgba(34,197,94,.2);color:var(--green);border:1px solid var(--green)}
.badge-purple{background:rgba(108,99,255,.2);color:var(--purple);border:1px solid var(--purple)}
.badge-muted{background:rgba(107,114,128,.15);color:var(--muted);border:1px solid var(--border)}
.index-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:12px;margin-top:12px}
.index-card{background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:16px}
.index-card a{color:var(--text);font-size:12px;font-weight:500;display:block;margin-bottom:4px}
.index-card p{font-size:11px;color:var(--muted);margin:0;line-height:1.5}
.cve-history{width:100%;border-collapse:collapse;margin:16px 0;font-size:12px}
.cve-history th{text-align:left;padding:10px 12px;border-bottom:2px solid var(--border);color:var(--muted);font-weight:600;font-size:10px;text-transform:uppercase;letter-spacing:.08em}
.cve-history td{padding:10px 12px;border-bottom:1px solid var(--border);vertical-align:top}
.cve-history tr:last-child td{border-bottom:none}
.cve-history tr:hover td{background:var(--surface2)}
.faq{margin:40px 0}.faq-item{border-bottom:1px solid var(--border);padding:16px 0}
.faq-item:last-child{border-bottom:none}
.faq-q{font-size:12px;font-weight:600;color:var(--text);margin-bottom:8px}
.faq-a{font-size:12px;color:var(--muted);line-height:1.7}
.related-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px;margin-top:12px}
.related-card{background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:14px}
.related-card a{color:var(--text);font-size:12px;font-weight:500}
.related-card p{font-size:11px;color:var(--muted);margin:4px 0 0}
.digest-item{border-bottom:1px solid var(--border);padding:20px 0}
.digest-item:last-child{border-bottom:none}
.digest-item h3{font-size:13px;font-weight:600;margin:0 0 6px;color:var(--text)}
.site-footer{border-top:1px solid var(--border);padding:24px;text-align:center;font-size:11px;color:var(--muted);margin-top:60px}
.site-footer a{color:var(--muted)}
@media(max-width:640px){.nav-links{display:none}.related-grid{grid-template-columns:1fr}.index-grid{grid-template-columns:1fr}}
"""

def shell(title, desc, path, breadcrumbs, body, schemas):
    canonical = BASE_URL + path
    sj = json.dumps({"@context":"https://schema.org","@graph":schemas}, indent=2)
    crumb = " <span style='color:var(--border)'>/</span> ".join(
        f'<a href="{u}">{n}</a>' if u else f'<span style="color:var(--text)">{n}</span>'
        for n,u in breadcrumbs)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
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
<script type="application/ld+json">{sj}</script>
<style>{TOKENS}</style>
</head>
<body>
<header class="site-header">
  <a href="/" class="logo">Package<span>Fix</span></a>
  <nav class="nav-links">
    <a href="/">Tool</a>
    <a href="/glossary">Glossary</a>
    <a href="/cisa-kev">CISA KEV</a>
    <a href="/blog">Blog</a>
    <a href="https://github.com/metriclogic26/packagefix">GitHub</a>
  </nav>
</header>
<main class="container">
  <div class="breadcrumb">{crumb}</div>
  {body}
</main>
<footer class="site-footer">
  <p>PackageFix · <a href="/">packagefix.dev</a> · MIT Licensed · Open Source</p>
  <p style="margin-top:6px">Vulnerability data: <a href="https://osv.dev">OSV</a> · <a href="https://www.cisa.gov/known-exploited-vulnerabilities-catalog">CISA KEV</a></p>
  <p style="margin-top:6px">Always test dependency updates in staging before deploying to production.</p>
</footer>
</body></html>"""

def cta():
    return """<div class="cta-box">
  <p>Paste your manifest — get a fixed version with all CVEs patched in seconds.</p>
  <a href="/" class="cta-btn">Open PackageFix →</a>
  <p style="margin-top:12px;font-size:11px;color:var(--muted)">Free · No signup · No CLI · Runs in your browser</p>
</div>"""

def faq_html(faqs):
    items = "".join(f'<div class="faq-item"><div class="faq-q">{q}</div><div class="faq-a">{a}</div></div>' for q,a in faqs)
    return f'<div class="faq"><h2>Common questions</h2>{items}</div>'

def related_html(pages):
    cards = "".join(f'<div class="related-card"><a href="{p["url"]}">{p["title"]}</a><p>{p["desc"]}</p></div>' for p in pages)
    return f'<div style="margin:40px 0"><h2>Related</h2><div class="related-grid">{cards}</div></div>'

def sev(s):
    c = "badge-red" if s=="CRITICAL" else "badge-orange" if s=="HIGH" else "badge-purple" if s=="MEDIUM" else "badge-muted"
    return f'<span class="badge {c}">{s}</span>'

def cve_tbl(cves):
    rows = ""
    for cid,yr,sv,kev,fixed,safe,desc in cves:
        k = '<span style="color:var(--red);margin-right:4px">🔴</span>' if kev else ""
        f = f'<span class="badge badge-green">Fixed {safe}</span>' if fixed else '<span class="badge badge-orange">No fix</span>'
        rows += f"<tr><td><a href='https://osv.dev/vulnerability/{cid}' target='_blank' rel='noopener'>{cid}</a></td><td>{yr}</td><td>{k}{sev(sv)}</td><td style='color:var(--muted)'>{desc}</td><td>{f}</td></tr>"
    return f'<table class="cve-history"><thead><tr><th>CVE</th><th>Year</th><th>Severity</th><th>Description</th><th>Fix</th></tr></thead><tbody>{rows}</tbody></table>'

all_paths = []

def write(slug, html):
    p = os.path.join("seo", slug, "index.html")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(html)
    all_paths.append("/" + slug)
    print(f"  ✓ /{slug}")

def bc(items):
    return [{"@type":"ListItem","position":i+1,"name":n,"item":BASE_URL+(u or "")}
            for i,(n,u) in enumerate(items)]

# ══════════════════════════════════════════════════════════════════════════════
# 1. INDEX PAGES
# ══════════════════════════════════════════════════════════════════════════════

print("\n📁 Generating index pages...")

# /fix index
FIX_ECOSYSTEMS = [
    ("npm",  "/npm",  "npm / Node.js",  "express, lodash, axios, jsonwebtoken, vm2 and 20 more"),
    ("pypi", "/python","PyPI / Python", "Django, Flask, requests, cryptography, Pillow and 20 more"),
    ("ruby", "/ruby", "Ruby / Gems",    "Rails, Nokogiri, Devise, Puma, Rack and 15 more"),
    ("php",  "/php",  "PHP / Composer", "Laravel, Symfony, Guzzle, Flysystem and 10 more"),
    ("go",   "/go",   "Go / Modules",   "Gin, gRPC, Echo, Fiber, GORM and 10 more"),
    ("rust", "/rust", "Rust / Crates",  "actix-web, axum, hyper, openssl, rustls and 10 more"),
    ("java", "/java", "Java / Maven",   "Log4j, Spring, Jackson, Netty, Guava and 10 more"),
]
eco_cards = "".join(f'<div class="index-card"><a href="/fix/{eco}">{label}</a><p>{pkgs}</p></div>' for eco,_,label,pkgs in FIX_ECOSYSTEMS)

write("fix", shell(
    "Dependency Fix Guides — All Ecosystems | PackageFix",
    "Step-by-step CVE fix guides for npm, PyPI, Ruby, PHP, Go, Rust, and Java/Maven. Every guide shows the vulnerable version, safe version, and exact command to run.",
    "/fix",
    [("PackageFix","/"),("Fix Guides",None)],
    f"""<h1>Dependency Fix Guides</h1>
<p class="lead">Exact fix instructions for CVEs across all 7 ecosystems PackageFix supports. Every page shows your vulnerable version, the safe version, and the exact command to run.</p>
<h2>Browse by ecosystem</h2>
<div class="index-grid">{eco_cards}</div>
{cta()}
{related_html([
    {"url":"/cisa-kev","title":"CISA KEV Packages","desc":"Actively exploited right now"},
    {"url":"/glossary/dependency-scanning","title":"Dependency Scanning","desc":"How to automate this"},
    {"url":"/guides/github-actions","title":"GitHub Actions","desc":"Catch CVEs in CI"},
    {"url":"/alternatives","title":"Alternatives","desc":"Other SCA tools"},
])}""",
    [{"@type":"BreadcrumbList","itemListElement":bc([("PackageFix","/"),("Fix Guides","/fix")])},
     {"@type":"ItemList","name":"Fix Guides by Ecosystem",
      "itemListElement":[{"@type":"ListItem","position":i+1,"name":label,"url":BASE_URL+f"/fix/{eco}"} for i,(eco,_,label,_) in enumerate(FIX_ECOSYSTEMS)]}]
))

# /guides index
GUIDES = [
    ("/guides/github-actions","GitHub Actions","Scan dependencies on every push — 4 ready-to-use workflow YAMLs"),
    ("/guides/pre-commit",    "Pre-commit Hooks","Catch CVEs before they enter your git history"),
    ("/terminal",             "Terminal One-Liner","Pipe any manifest into PackageFix with one command"),
]
guide_cards = "".join(f'<div class="index-card"><a href="{u}">{t}</a><p>{d}</p></div>' for u,t,d in GUIDES)

write("guides", shell(
    "Developer Guides — Automate Dependency Security | PackageFix",
    "Guides for automating dependency security scanning — GitHub Actions workflows, pre-commit hooks, and terminal shortcuts for all 7 ecosystems.",
    "/guides",
    [("PackageFix","/"),("Guides",None)],
    f"""<h1>Developer Guides</h1>
<p class="lead">How to integrate dependency security scanning into your workflow — from a one-off terminal command to automatic CI/CD blocking on critical CVEs.</p>
<div class="index-grid">{guide_cards}</div>
<h2>Which guide is right for you?</h2>
<p>If you want a quick one-off check right now — use the <a href="/terminal">terminal one-liner</a>. If you want to catch vulnerabilities before they reach production — add the <a href="/guides/github-actions">GitHub Actions workflow</a>. If you want to catch them before they even enter your git history — use <a href="/guides/pre-commit">pre-commit hooks</a>.</p>
{cta()}
{related_html([
    {"url":"/fix","title":"Fix Guides","desc":"Step-by-step CVE fixes"},
    {"url":"/glossary/dependency-scanning","title":"Dependency Scanning","desc":"The broader concept"},
    {"url":"/cisa-kev","title":"CISA KEV","desc":"What to fix first"},
    {"url":"/glossary/remediation","title":"Remediation","desc":"Fix strategies"},
])}""",
    [{"@type":"BreadcrumbList","itemListElement":bc([("PackageFix","/"),("Guides","/guides")])},
     {"@type":"ItemList","name":"Developer Guides",
      "itemListElement":[{"@type":"ListItem","position":i+1,"name":t,"url":BASE_URL+u} for i,(u,t,_) in enumerate(GUIDES)]}]
))

# /providers index
PROVIDERS = [
    ("/providers/github-actions/npm-audit",   "GitHub Actions — npm",    "npm audit in CI"),
    ("/providers/github-actions/python-audit","GitHub Actions — Python",  "pip-audit in CI"),
    ("/providers/gitlab-ci/dependency-scan",  "GitLab CI — npm",          "npm scanning"),
    ("/providers/gitlab-ci/python-scan",      "GitLab CI — Python",       "pip scanning"),
    ("/providers/circleci/dependency-scan",   "CircleCI — npm",           "npm scanning"),
    ("/providers/circleci/python-scan",       "CircleCI — Python",        "pip scanning"),
    ("/providers/hetzner/nodejs-security",    "Hetzner — Node.js",        "server-level security"),
    ("/providers/hetzner/python-security",    "Hetzner — Python",         "server-level security"),
    ("/providers/digitalocean/nodejs-security","DigitalOcean — Node.js",  "server-level security"),
    ("/providers/digitalocean/python-security","DigitalOcean — Python",   "server-level security"),
    ("/providers/vercel/nodejs-security",     "Vercel — Node.js",         "edge deployment security"),
    ("/providers/vercel/python-security",     "Vercel — Python",          "edge deployment security"),
    ("/providers/aws/lambda-nodejs-security", "AWS Lambda — Node.js",     "serverless security"),
    ("/providers/aws/lambda-python-security", "AWS Lambda — Python",      "serverless security"),
    ("/providers/netlify/nodejs-security",    "Netlify — Node.js",        "JAMstack security"),
    ("/providers/railway/nodejs-security",    "Railway — Node.js",        "Railway deployment"),
    ("/providers/fly/nodejs-security",        "Fly.io — Node.js",         "Fly deployment"),
    ("/providers/render/nodejs-security",     "Render — Node.js",         "Render deployment"),
]
prov_cards = "".join(f'<div class="index-card"><a href="{u}">{t}</a><p>{d}</p></div>' for u,t,d in PROVIDERS)

write("providers", shell(
    "Provider & CI Security Guides | PackageFix",
    "Dependency security scanning guides for GitHub Actions, GitLab CI, CircleCI, Vercel, Netlify, Railway, Fly.io, Hetzner, DigitalOcean, AWS Lambda, and Render.",
    "/providers",
    [("PackageFix","/"),("Providers",None)],
    f"""<h1>Provider & CI Security Guides</h1>
<p class="lead">Copy-paste dependency scanning configs for every major CI provider and hosting platform. Pick your platform, copy the config, and you're scanning on every deploy.</p>
<div class="index-grid">{prov_cards}</div>
{cta()}
{related_html([
    {"url":"/guides","title":"Developer Guides","desc":"All integration guides"},
    {"url":"/guides/github-actions","title":"GitHub Actions","desc":"Full GitHub Actions guide"},
    {"url":"/fix","title":"Fix Guides","desc":"Fix what CI finds"},
    {"url":"/glossary/dependency-scanning","title":"Dependency Scanning","desc":"The broader concept"},
])}""",
    [{"@type":"BreadcrumbList","itemListElement":bc([("PackageFix","/"),("Providers","/providers")])},
     {"@type":"ItemList","name":"Provider Security Guides",
      "itemListElement":[{"@type":"ListItem","position":i+1,"name":t,"url":BASE_URL+u} for i,(u,t,_) in enumerate(PROVIDERS)]}]
))


# ══════════════════════════════════════════════════════════════════════════════
# 2. REMAINING CVE HISTORY TABLES (~40 packages)
# ══════════════════════════════════════════════════════════════════════════════

REMAINING = [
  # PyPI
  {"slug":"fix/pypi/fastapi","pkg":"FastAPI","eco":"pypi","eco_label":"PyPI","safe_ver":"0.109.1","install":"pip install -r requirements.txt","weekly":"20M+",
   "desc":"FastAPI is Python's fastest-growing web framework. Its CVEs come primarily through Starlette (its ASGI foundation) and pydantic (its validation layer).",
   "cves":[("CVE-2024-24762",2024,"HIGH",False,True,"0.109.1","ReDoS via crafted multipart form data")],"before":"fastapi==0.100.0","after":"fastapi==0.109.1",
   "faqs":[("Does FastAPI have many direct CVEs?","FastAPI itself has very few direct CVEs — most FastAPI security issues come through Starlette or pydantic. Keeping the full stack updated together is the safest approach.")],"related":[{"url":"/fix/pypi/starlette","title":"Fix Starlette","desc":"FastAPI's ASGI layer"},{"url":"/python","title":"PyPI Security","desc":"All Python guides"}]},

  {"slug":"fix/pypi/starlette","pkg":"Starlette","eco":"pypi","eco_label":"PyPI","safe_ver":"0.37.2","install":"pip install -r requirements.txt","weekly":"20M+",
   "desc":"Starlette is the ASGI framework underlying FastAPI. CVEs here affect all FastAPI applications since Starlette handles request parsing and middleware.",
   "cves":[("CVE-2023-29159",2023,"HIGH",False,True,"0.27.0","Path traversal in StaticFiles handler"),
           ("CVE-2024-24762",2024,"HIGH",False,True,"0.37.2","ReDoS via multipart form parsing")],"before":"starlette==0.27.0","after":"starlette==0.37.2",
   "faqs":[("Does updating FastAPI update Starlette?","FastAPI pins a minimum Starlette version but not the latest. Specify starlette explicitly in requirements.txt to ensure you're on a patched version.")],"related":[{"url":"/fix/pypi/fastapi","title":"Fix FastAPI","desc":"Main Starlette consumer"},{"url":"/python","title":"PyPI Security","desc":"All Python guides"}]},

  {"slug":"fix/pypi/pydantic","pkg":"pydantic","eco":"pypi","eco_label":"PyPI","safe_ver":"2.6.4","install":"pip install -r requirements.txt","weekly":"100M+",
   "desc":"pydantic is Python's most popular data validation library, used by FastAPI, SQLModel, and many others. Its main CVE is ReDoS in email validation.",
   "cves":[("CVE-2021-29510",2021,"HIGH",False,True,"1.8.2","DoS via infinite loop in decimal validation"),
           ("CVE-2024-3772",2024,"HIGH",False,True,"2.6.4","ReDoS via malicious email address")],"before":"pydantic==1.10.0","after":"pydantic==2.6.4",
   "faqs":[("Is there a breaking change between pydantic v1 and v2?","Yes — pydantic v2 is a complete rewrite with significant API changes. FastAPI 0.100.0+ supports both. Migration is worthwhile — v2 is 5-50x faster and has better error messages.")],"related":[{"url":"/fix/pypi/fastapi","title":"Fix FastAPI","desc":"Main pydantic consumer"},{"url":"/python","title":"PyPI Security","desc":"All Python guides"}]},

  {"slug":"fix/pypi/twisted","pkg":"Twisted","eco":"pypi","eco_label":"PyPI","safe_ver":"24.3.0","install":"pip install -r requirements.txt","weekly":"5M+",
   "desc":"Twisted is Python's event-driven networking engine. It has a consistent CVE history around HTTP request splitting and header injection.",
   "cves":[("CVE-2022-21712",2022,"HIGH",False,True,"22.2.0","Cookie and auth header exposure on redirect"),
           ("CVE-2022-24801",2022,"HIGH",False,True,"22.4.0","HTTP request splitting via crafted method"),
           ("CVE-2023-46137",2023,"HIGH",False,True,"23.10.0","HTTP request splitting via header injection")],"before":"Twisted==22.10.0","after":"Twisted==24.3.0",
   "faqs":[("Is Twisted still actively maintained?","Yes — Twisted has been in continuous development since 2001 and remains the foundation for many production Python networking applications.")],"related":[{"url":"/python","title":"PyPI Security","desc":"All Python guides"}]},

  {"slug":"fix/pypi/httpx","pkg":"httpx","eco":"pypi","eco_label":"PyPI","safe_ver":"0.27.0","install":"pip install -r requirements.txt","weekly":"20M+",
   "desc":"httpx is Python's modern HTTP client with async support. The main CVE is a redirect that downgrades from HTTPS to HTTP, potentially exposing credentials.",
   "cves":[("CVE-2023-47641",2023,"MEDIUM",False,True,"0.27.0","URL redirect via HTTPS to HTTP downgrade")],"before":"httpx==0.24.0","after":"httpx==0.27.0",
   "faqs":[("Is httpx safer than requests?","httpx has a shorter CVE history than requests simply because it's newer. Both are actively maintained. httpx adds async support and HTTP/2 — worth using for new projects.")],"related":[{"url":"/fix/pypi/requests","title":"Fix requests","desc":"requests CVE history"},{"url":"/python","title":"PyPI Security","desc":"All Python guides"}]},

  {"slug":"fix/pypi/boto3","pkg":"boto3","eco":"pypi","eco_label":"PyPI","safe_ver":"1.34.69","install":"pip install -r requirements.txt","weekly":"100M+",
   "desc":"boto3 is the AWS SDK for Python. Its CVEs are rare — most AWS-related Python security issues come from misconfiguration rather than boto3 vulnerabilities.",
   "cves":[("CVE-2023-34048",2023,"HIGH",False,True,"1.28.0","Credential exposure via debug logging")],"before":"boto3==1.26.0","after":"boto3==1.34.69",
   "faqs":[("Is boto3 safe for production AWS operations?","boto3 has a very clean CVE history. The main risk with AWS SDK usage is credential management — never hardcode credentials, use IAM roles and environment variables.")],"related":[{"url":"/python","title":"PyPI Security","desc":"All Python guides"}]},

  {"slug":"fix/pypi/lxml","pkg":"lxml","eco":"pypi","eco_label":"PyPI","safe_ver":"5.2.1","install":"pip install -r requirements.txt","weekly":"30M+",
   "desc":"lxml is Python's XML and HTML processing library, wrapping libxml2 and libxslt. Similar to Nokogiri in Ruby, its CVE history often reflects upstream C library vulnerabilities.",
   "cves":[("CVE-2021-28957",2021,"MEDIUM",False,True,"4.6.3","XSS via HTML cleanup"),
           ("CVE-2022-2309",2022,"HIGH",False,True,"4.9.3","NULL pointer dereference via crafted XML")],"before":"lxml==4.9.3","after":"lxml==5.2.1",
   "faqs":[("Should I use lxml or html.parser for HTML scraping?","lxml is faster and more lenient with malformed HTML. For untrusted HTML, always use lxml's HTML cleaner or bleach to sanitize before rendering.")],"related":[{"url":"/python","title":"PyPI Security","desc":"All Python guides"}]},

  # Ruby
  {"slug":"fix/ruby/activerecord","pkg":"activerecord","eco":"ruby","eco_label":"Ruby","safe_ver":"7.1.3","install":"bundle install","weekly":"3M+",
   "desc":"activerecord is Rails' ORM layer. SQL injection CVEs here are critical — they affect any Rails app using the database query interface with user input.",
   "cves":[("CVE-2021-22880",2021,"HIGH",False,True,"6.1.2.1","ReDoS via specially crafted PostgreSQL range"),
           ("CVE-2022-32224",2022,"CRITICAL",False,True,"7.0.3.1","RCE via YAML deserialization in PostgreSQL adapter")],"before":"gem 'activerecord', '6.1.0'","after":"gem 'activerecord', '7.1.3'",
   "faqs":[("How do I prevent SQL injection in Rails?","Always use parameterized queries: Model.where('name = ?', name) not Model.where(\"name = '#{name}'\"). Never interpolate user input directly into query strings.")],"related":[{"url":"/fix/ruby/rails","title":"Fix Rails","desc":"Full Rails CVE history"},{"url":"/ruby","title":"Ruby Security","desc":"All Ruby guides"}]},

  {"slug":"fix/ruby/actionpack","pkg":"actionpack","eco":"ruby","eco_label":"Ruby","safe_ver":"7.1.3","install":"bundle install","weekly":"3M+",
   "desc":"actionpack is Rails' routing and controller layer. CVEs here affect request handling and URL parsing across all Rails applications.",
   "cves":[("CVE-2022-23633",2022,"HIGH",False,True,"7.0.2.3","Possible exposure of data in streamed responses"),
           ("CVE-2023-28362",2023,"HIGH",False,True,"7.0.5","XSS via redirect URLs with crafted query params")],"before":"gem 'actionpack', '6.1.0'","after":"gem 'actionpack', '7.1.3'",
   "faqs":[("Is actionpack updated separately from Rails?","actionpack is a component of Rails. Updating Rails updates actionpack automatically — you don't need to manage them separately.")],"related":[{"url":"/fix/ruby/rails","title":"Fix Rails","desc":"Full Rails CVE history"},{"url":"/ruby","title":"Ruby Security","desc":"All Ruby guides"}]},

  {"slug":"fix/ruby/ransack","pkg":"Ransack","eco":"ruby","eco_label":"Ruby","safe_ver":"4.1.1","install":"bundle install","weekly":"500K+",
   "desc":"Ransack is the most popular Ruby gem for search and filtering in Rails apps. Its main CVE is a critical SQL injection via crafted sort parameters — a very common attack surface.",
   "cves":[("CVE-2022-35956",2022,"CRITICAL",False,True,"3.1.0","SQL injection via crafted sort parameters")],"before":"gem 'ransack', '3.2.1'","after":"gem 'ransack', '4.1.1'",
   "faqs":[("How does Ransack SQL injection work?","CVE-2022-35956 allows an attacker to inject SQL via the sort parameter (e.g., ?q[s]=name+asc;DROP+TABLE+users). Update to 3.1.0+ which sanitizes sort parameters. Also consider allowlisting sortable columns.")],"related":[{"url":"/fix/ruby/rails","title":"Fix Rails","desc":"Rails CVE history"},{"url":"/ruby","title":"Ruby Security","desc":"All Ruby guides"}]},

  {"slug":"fix/ruby/carrierwave","pkg":"CarrierWave","eco":"ruby","eco_label":"Ruby","safe_ver":"3.0.7","install":"bundle install","weekly":"500K+",
   "desc":"CarrierWave handles file uploads in Rails applications. File upload libraries are high-value attack targets — arbitrary file overwrite and directory traversal are the main risks.",
   "cves":[("CVE-2021-21305",2021,"HIGH",False,True,"2.1.1","Code injection via crafted SVG file"),
           ("CVE-2023-49090",2023,"CRITICAL",False,True,"3.0.7","Directory traversal via crafted file upload")],"before":"gem 'carrierwave', '2.2.2'","after":"gem 'carrierwave', '3.0.7'",
   "faqs":[("How do I secure file uploads in Rails?","Always validate file types server-side (not just by extension), store uploaded files outside the web root, use CarrierWave's content_type_allowlist to restrict accepted MIME types, and process images through a sanitiser before storage.")],"related":[{"url":"/fix/ruby/rails","title":"Fix Rails","desc":"Rails CVE history"},{"url":"/ruby","title":"Ruby Security","desc":"All Ruby guides"}]},

  {"slug":"fix/ruby/sprockets","pkg":"Sprockets","eco":"ruby","eco_label":"Ruby","safe_ver":"4.2.1","install":"bundle install","weekly":"2M+",
   "desc":"Sprockets is Rails' asset pipeline. Path traversal vulnerabilities have appeared multiple times — it processes file paths from user-influenced asset URLs.",
   "cves":[("CVE-2018-3760",2018,"HIGH",False,True,"2.12.5","Path traversal in asset serving"),
           ("CVE-2020-8184",2020,"HIGH",False,True,"3.7.2","Path traversal in asset serving (bypass)"),
           ("CVE-2022-25902",2022,"HIGH",False,True,"4.1.0","Path traversal via specially crafted filenames")],"before":"gem 'sprockets', '3.7.2'","after":"gem 'sprockets', '4.2.1'",
   "faqs":[("Does Rails 7 use Sprockets?","Rails 7 ships with Sprockets as one option but also supports Propshaft and import maps. New Rails 7 apps can avoid Sprockets entirely — which also avoids its CVE surface.")],"related":[{"url":"/fix/ruby/rails","title":"Fix Rails","desc":"Rails CVE history"},{"url":"/ruby","title":"Ruby Security","desc":"All Ruby guides"}]},

  # PHP
  {"slug":"fix/php/phpmailer","pkg":"PHPMailer","eco":"php","eco_label":"PHP","safe_ver":"6.9.1","install":"composer install","weekly":"3M+",
   "desc":"PHPMailer is the most widely-used PHP email library. Its historical CVEs include critical remote code execution — it has been a major target given how widely it's deployed.",
   "cves":[("CVE-2016-10033",2016,"CRITICAL",False,True,"5.2.18","RCE via sender parameter injection"),
           ("CVE-2016-10045",2016,"CRITICAL",False,True,"5.2.20","RCE bypass of incomplete fix for CVE-2016-10033"),
           ("CVE-2021-3603",2021,"CRITICAL",False,True,"6.5.0","RCE via SMTP server response injection")],"before":'"phpmailer/phpmailer": "^6.5"',"after":'"phpmailer/phpmailer": "^6.9"',
   "faqs":[("Are the 2016 PHPMailer RCE CVEs still relevant?","Yes — many legacy PHP applications still run vulnerable PHPMailer versions. The 2016 CVEs were the most exploited PHP vulnerabilities of that year. Any app on PHPMailer < 5.2.18 is critical priority.")],"related":[{"url":"/php","title":"PHP Security","desc":"All PHP guides"}]},

  {"slug":"fix/php/dompdf","pkg":"Dompdf","eco":"php","eco_label":"PHP","safe_ver":"^2.0","install":"composer install","weekly":"2M+",
   "desc":"Dompdf renders HTML to PDF in PHP. CVE-2021-3838 is critical and on CISA KEV — RCE via CSS import with a crafted URL. Any app using dompdf to render user-controlled HTML is vulnerable.",
   "cves":[("CVE-2021-3838",2021,"CRITICAL",True,True,"2.0.0","RCE via CSS import with crafted URL — CISA KEV")],"before":'"dompdf/dompdf": "^1.2"',"after":'"dompdf/dompdf": "^2.0"',
   "faqs":[("What does CVE-2021-3838 allow an attacker to do?","Execute arbitrary code on the server by injecting a CSS @import rule that loads a PHP file disguised as a font. If your application renders HTML from user input to PDF, this is critical."),("How do I safely use dompdf?","Never render user-controlled HTML directly through dompdf. Sanitize all HTML input before passing to dompdf, or use a sandboxed rendering environment.")],"related":[{"url":"/kev/CVE-2021-3838","title":"CVE-2021-3838 KEV","desc":"CISA KEV detail"},{"url":"/php","title":"PHP Security","desc":"All PHP guides"}]},

  {"slug":"fix/php/carbon","pkg":"Carbon","eco":"php","eco_label":"PHP","safe_ver":"^3.3","install":"composer install","weekly":"50M+",
   "desc":"Carbon is PHP's most popular date manipulation library. CVEs here are ReDoS vulnerabilities in date string parsing.",
   "cves":[("CVE-2022-22824",2022,"MEDIUM",False,True,"2.72.2","ReDoS via crafted date string")],"before":'"nesbot/carbon": "^2.62"',"after":'"nesbot/carbon": "^3.3"',
   "faqs":[("Is Carbon still the best PHP date library?","Carbon remains the standard for Laravel projects. It wraps PHP's built-in DateTime and adds fluent methods. Keep it updated — the ReDoS fix is in 2.72.2+.")],"related":[{"url":"/fix/php/laravel","title":"Fix Laravel","desc":"Main Carbon consumer"},{"url":"/php","title":"PHP Security","desc":"All PHP guides"}]},

  # Go
  {"slug":"fix/go/gorm","pkg":"GORM","eco":"go","eco_label":"Go","safe_ver":"v1.25.9","install":"go mod tidy","weekly":"N/A",
   "desc":"GORM is Go's most popular ORM. Its main CVE is SQL injection via raw query methods — the same class of issue that affects any ORM that allows string interpolation in queries.",
   "cves":[("CVE-2023-22562",2023,"HIGH",False,True,"v1.25.1","SQL injection via crafted input in raw query methods")],"before":"gorm.io/gorm v1.23.0","after":"gorm.io/gorm v1.25.9",
   "faqs":[("How do I prevent SQL injection in GORM?","Avoid db.Raw() and db.Exec() with string formatting. Always use parameterized queries: db.Where(\"name = ?\", name) not db.Where(\"name = '\" + name + \"'\").")],"related":[{"url":"/go","title":"Go Security","desc":"All Go guides"}]},

  {"slug":"fix/go/cobra","pkg":"Cobra","eco":"go","eco_label":"Go","safe_ver":"v1.8.0","install":"go mod tidy","weekly":"N/A",
   "desc":"Cobra is Go's most popular CLI framework, used by kubectl, Hugo, GitHub CLI, and thousands of other tools. Its CVE is a ReDoS in argument parsing.",
   "cves":[("CVE-2022-32149",2022,"HIGH",False,True,"v1.7.0","ReDoS via crafted command-line argument")],"before":"github.com/spf13/cobra v1.6.0","after":"github.com/spf13/cobra v1.8.0",
   "faqs":[("Does the Cobra ReDoS affect end users?","It affects CLI applications built with Cobra that accept user-provided arguments. If your CLI tool processes untrusted input from external systems (scripts, CI), update cobra.")],"related":[{"url":"/go","title":"Go Security","desc":"All Go guides"}]},

  {"slug":"fix/go/prometheus","pkg":"Prometheus client","eco":"go","eco_label":"Go","safe_ver":"v1.19.0","install":"go mod tidy","weekly":"N/A",
   "desc":"The Prometheus Go client library is used by virtually every Go service for metrics. Its CVE is a ReDoS in metric label regex validation.",
   "cves":[("CVE-2022-21698",2022,"HIGH",False,True,"v1.12.1","ReDoS via metric label with crafted regex")],"before":"github.com/prometheus/client_golang v1.14.0","after":"github.com/prometheus/client_golang v1.19.0",
   "faqs":[("Is the Prometheus client ReDoS exploitable?","If your metrics labels include user-controlled data, yes. An attacker can cause metric processing to hang. Most applications use static labels — lower risk in practice, but still worth updating.")],"related":[{"url":"/go","title":"Go Security","desc":"All Go guides"}]},

  {"slug":"fix/go/yaml","pkg":"go-yaml","eco":"go","eco_label":"Go","safe_ver":"v3.0.1","install":"go mod tidy","weekly":"N/A",
   "desc":"go-yaml is the standard YAML parsing library for Go. Its CVE is a denial of service via crafted YAML — a common issue with YAML parsers that support anchors and aliases.",
   "cves":[("CVE-2022-28948",2022,"HIGH",False,True,"v3.0.1","DoS via crafted YAML document with excessive alias expansion")],"before":"gopkg.in/yaml.v3 v3.0.0-20210107192922","after":"gopkg.in/yaml.v3 v3.0.1",
   "faqs":[("Does go-yaml support safe loading like PyYAML?","go-yaml v3 doesn't have a 'safe load' concept like PyYAML because Go's type system prevents arbitrary code execution during YAML parsing. The CVE is a DoS (infinite loop) not RCE.")],"related":[{"url":"/go","title":"Go Security","desc":"All Go guides"}]},

  # Rust
  {"slug":"fix/rust/tokio","pkg":"tokio","eco":"rust","eco_label":"Rust","safe_ver":"1.37.0","install":"cargo update","weekly":"N/A",
   "desc":"tokio is Rust's async runtime — the foundation of the entire Rust async ecosystem. Its main CVE exposure is via the HTTP/2 Rapid Reset attack through hyper.",
   "cves":[("CVE-2021-45710",2021,"HIGH",False,True,"1.8.4","Data race in task::spawn_blocking"),
           ("CVE-2023-44487",2023,"HIGH",True, True,"1.37.0","HTTP/2 Rapid Reset via hyper dep — CISA KEV")],"before":"tokio = \"1.26.0\"","after":"tokio = \"1.37.0\"",
   "faqs":[("Does the Rust memory model prevent tokio CVEs?","Rust prevents memory-safety CVEs but not all CVEs. CVE-2021-45710 was a data race (logic-level) and CVE-2023-44487 is a protocol-level DoS. Both are real vulnerabilities despite Rust's safety guarantees.")],"related":[{"url":"/fix/rust/hyper","title":"Fix hyper","desc":"HTTP/2 Rapid Reset"},{"url":"/rust","title":"Rust Security","desc":"All Rust guides"}]},

  {"slug":"fix/rust/serde","pkg":"serde","eco":"rust","eco_label":"Rust","safe_ver":"1.0.200","install":"cargo update","weekly":"N/A",
   "desc":"serde is Rust's serialization framework — used by virtually every Rust project. Its CVE is a denial of service via crafted serialized data.",
   "cves":[("CVE-2023-35826",2023,"MEDIUM",False,True,"1.0.172","DoS via crafted serialized data with excessive recursion")],"before":"serde = \"1.0.150\"","after":"serde = \"1.0.200\"",
   "faqs":[("Does serde's CVE affect most applications?","Only applications that deserialize data from untrusted sources. If you use serde_json to parse user-provided JSON or serde to deserialize network data, update serde.")],"related":[{"url":"/rust","title":"Rust Security","desc":"All Rust guides"}]},

  {"slug":"fix/rust/diesel","pkg":"Diesel","eco":"rust","eco_label":"Rust","safe_ver":"2.1.5","install":"cargo update","weekly":"N/A",
   "desc":"Diesel is Rust's most popular ORM. Its main CVE is SQL injection in raw query interpolation — the same class of issue that affects ORMs in any language.",
   "cves":[("CVE-2023-50269",2023,"HIGH",False,True,"2.1.4","SQL injection via raw query interpolation")],"before":"diesel = \"1.4.8\"","after":"diesel = \"2.1.5\"",
   "faqs":[("Does Rust's type system prevent SQL injection in Diesel?","Diesel's query builder is injection-safe. The CVE is in raw SQL via diesel::sql_query() with string formatting — which bypasses the type-safe query builder. Avoid string interpolation in raw queries.")],"related":[{"url":"/rust","title":"Rust Security","desc":"All Rust guides"}]},

  # Java
  {"slug":"fix/java/h2","pkg":"H2 Database","eco":"java","eco_label":"Java/Maven","safe_ver":"2.2.224","install":"mvn dependency:resolve","weekly":"Millions",
   "desc":"H2 is an in-memory Java SQL database widely used in testing and development. Its critical CVE is RCE via the H2 console — which should never be exposed in production.",
   "cves":[("CVE-2021-42392",2021,"CRITICAL",False,True,"2.0.206","RCE via JNDI lookup (Log4Shell-like) in H2 console"),
           ("CVE-2022-45868",2022,"CRITICAL",False,True,"2.2.220","RCE via H2 console JNDI injection")],"before":"<h2.version>2.1.210</h2.version>","after":"<h2.version>2.2.224</h2.version>",
   "faqs":[("Is H2 console safe in production?","No — disable H2 console in production environments. Set spring.h2.console.enabled=false in Spring Boot. The console should only ever run in local development.")],"related":[{"url":"/fix/java/log4j","title":"Fix Log4j","desc":"Similar JNDI attack vector"},{"url":"/java","title":"Java Security","desc":"All Java guides"}]},

  {"slug":"fix/java/shiro","pkg":"Apache Shiro","eco":"java","eco_label":"Java/Maven","safe_ver":"2.0.1","install":"mvn dependency:resolve","weekly":"Millions",
   "desc":"Apache Shiro is a popular Java security framework for authentication and authorization. Authentication bypass via path traversal has been a recurring issue.",
   "cves":[("CVE-2020-1957",2020,"CRITICAL",False,True,"1.5.2","Authentication bypass via trailing slash"),
           ("CVE-2020-11989",2020,"CRITICAL",False,True,"1.5.3","Authentication bypass via URL encoding"),
           ("CVE-2023-46749",2023,"HIGH",    False,True,"2.0.1","Authentication bypass via path traversal")],"before":"<shiro.version>1.11.0</shiro.version>","after":"<shiro.version>2.0.1</shiro.version>",
   "faqs":[("Why does Shiro keep having authentication bypass CVEs?","URL normalization is fundamentally tricky — different components (Shiro's path matcher, the servlet container, the web server) may interpret the same URL differently. Shiro 2.0 addresses this with stricter URL normalization."),("Is Shiro or Spring Security better for new projects?","Spring Security is more actively developed and better integrated with the Spring ecosystem. For new Spring projects, Spring Security is generally recommended over Shiro.")],"related":[{"url":"/java","title":"Java Security","desc":"All Java guides"}]},

  {"slug":"fix/java/hibernate","pkg":"Hibernate ORM","eco":"java","eco_label":"Java/Maven","safe_ver":"6.4.4.Final","install":"mvn dependency:resolve","weekly":"Millions",
   "desc":"Hibernate is Java's most widely-used ORM, underlying Spring Data JPA. CVEs here are SQL injection via HQL and bypasses of Hibernate's built-in protections.",
   "cves":[("CVE-2020-25638",2020,"CRITICAL",False,True,"5.4.24.Final","SQL injection via HQL query with crafted input"),
           ("CVE-2023-25194",2023,"HIGH",    False,True,"6.2.0.Final", "SQL injection via HQL query interpolation")],"before":"<hibernate.version>5.6.14.Final</hibernate.version>","after":"<hibernate.version>6.4.4.Final</hibernate.version>",
   "faqs":[("Is Hibernate's JPQL/HQL safe from injection?","Parameterized queries via @NamedQuery or CriteriaBuilder are safe. The CVEs affect raw HQL via createQuery() with string formatting. Never interpolate user input into HQL strings.")],"related":[{"url":"/java","title":"Java Security","desc":"All Java guides"}]},

  {"slug":"fix/java/okhttp","pkg":"OkHttp","eco":"java","eco_label":"Java/Maven","safe_ver":"4.12.0","install":"mvn dependency:resolve","weekly":"Millions",
   "desc":"OkHttp is the most widely-used HTTP client for Android and Java. It's used by Retrofit, Coil, and many major Android and server-side applications.",
   "cves":[("CVE-2021-0341",2021,"HIGH",False,True,"4.9.1","Certificate hostname verification bypass"),
           ("CVE-2023-0833",2023,"HIGH",False,True,"4.11.0","Certificate pinning bypass via crafted cert")],"before":"<okhttp.version>4.10.0</okhttp.version>","after":"<okhttp.version>4.12.0</okhttp.version>",
   "faqs":[("Is OkHttp safe for HTTPS connections?","4.12.0 addresses all known certificate verification CVEs. Always implement certificate pinning for sensitive Android applications and keep OkHttp updated.")],"related":[{"url":"/java","title":"Java Security","desc":"All Java guides"}]},
]

print("\n📋 Generating remaining CVE history pages...")
for d in REMAINING:
    slug, pkg, eco, eco_label = d["slug"], d["pkg"], d["eco"], d["eco_label"]
    safe_ver, install, weekly = d["safe_ver"], d["install"], d["weekly"]
    desc, cves = d["desc"], d["cves"]
    before, after = d["before"], d["after"]
    faqs, related = d["faqs"], d["related"]
    path = f"/{slug}"
    total = len(cves)
    critical = sum(1 for c in cves if c[2]=="CRITICAL")
    kev_count = sum(1 for c in cves if c[3])
    kn = f'<p style="margin:8px 0 0;font-size:11px;color:var(--red)">🔴 {kev_count} CVE{"s" if kev_count>1 else ""} on CISA KEV — actively exploited</p>' if kev_count else ""
    body = f"""<h1>All {pkg} CVEs — Complete Vulnerability History</h1>
<p class="lead">{desc}</p>
<div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:24px">
  <span class="badge badge-purple">{eco_label}</span>
  <span class="badge badge-muted">{weekly} weekly downloads</span>
  <span class="badge badge-muted">{total} CVE{"s" if total>1 else ""} total</span>
  {'<span class="badge badge-red">'+str(critical)+' CRITICAL</span>' if critical else ''}
  {'<span class="badge badge-red">🔴 CISA KEV</span>' if kev_count else ''}
</div>
<h2>Full CVE history</h2>{kn}{cve_tbl(cves)}
<h2>Current safe version: {safe_ver}</h2>
<pre># Before\n{before}</pre>
<pre># After\n{after}</pre>
<p style="margin-top:8px">Then run: <code>{install}</code></p>
{cta()}
{faq_html(faqs)}
{related_html(related)}"""
    schemas = [
        {"@type":"ItemList","name":f"All {pkg} CVEs","description":f"Complete CVE history — {total} known vulnerabilities","numberOfItems":total,
         "itemListElement":[{"@type":"ListItem","position":i+1,"name":c[0],"url":f"https://osv.dev/vulnerability/{c[0]}"} for i,c in enumerate(cves)]},
        {"@type":"BreadcrumbList","itemListElement":bc([("PackageFix","/"),("Fix Guides","/fix"),(eco_label,f"/{eco}"),(pkg,None)])},
        {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}
    ]
    write(slug, shell(
        f"All {pkg} CVEs — Complete {eco_label} Vulnerability History | PackageFix",
        f"{pkg} has {total} known CVEs. {'CISA KEV — actively exploited. ' if kev_count else ''}Safe version: {safe_ver}.",
        path, [("PackageFix","/"),("Fix Guides","/fix"),(eco_label,f"/{eco}"),(pkg,None)], body, schemas))


# ══════════════════════════════════════════════════════════════════════════════
# 3. MISSING KEV PAGES
# ══════════════════════════════════════════════════════════════════════════════

print("\n🔴 Generating missing KEV pages...")

KEV_PAGES = [
    ("CVE-2015-9284","OmniAuth CSRF",7.4,"ruby","omniauth","< 2.0.0","2.1.2","/fix/ruby/omniauth",
     "CSRF in OAuth callback allows attackers to forge authentication requests. Any application using OmniAuth 1.x for OAuth is vulnerable — the callback accepts GET requests which can be triggered cross-site.",
     [("How long has CVE-2015-9284 been exploited?","Despite being filed in 2015, it remained in widespread use through OmniAuth 1.x which was the default for years. CISA added it to KEV when exploitation against Rails applications was confirmed in 2021+. Many applications are still on OmniAuth 1.x."),
      ("What does the fix require?","OmniAuth 2.0+ requires POST-only OAuth callbacks. Add omniauth-rails_csrf_protection gem or configure your OAuth provider for POST callbacks. This is a breaking change but necessary.")],
     [("PackageFix","/"),("CISA KEV","/cisa-kev"),("CVE-2015-9284",None)],
     [("Dec 2015","CVE filed for CSRF in OmniAuth 1.x OAuth callback"),
      ("Feb 2021","OmniAuth 2.0 released as the proper fix — POST-only callbacks"),
      ("2021+","CISA adds to KEV — exploitation confirmed against Rails apps"),
      ("Ongoing","Many apps still on OmniAuth 1.x — still actively targeted")]),

    ("CVE-2020-14343","PyYAML RCE",9.8,"pypi","PyYAML","< 5.4","6.0.1","/fix/pypi/pyyaml",
     "Remote code execution via yaml.load() without a Loader argument. Any Python application that calls yaml.load(untrusted_data) without specifying Loader=yaml.SafeLoader is vulnerable to arbitrary code execution.",
     [("How common is this vulnerability?","Extremely common. The unsafe yaml.load() pattern was the standard approach for years before the CVE. Codebases written before 2017 are very likely to use it. grep your codebase for yaml.load( without SafeLoader."),
      ("What is the fix?","Replace yaml.load(data) with yaml.safe_load(data) everywhere. Also update PyYAML to 6.0.1.")],
     [("PackageFix","/"),("CISA KEV","/cisa-kev"),("CVE-2020-14343",None)],
     [("Jun 2020","CVE filed — yaml.load() without Loader allows RCE"),
      ("Mar 2021","PyYAML 5.4 releases — warns on yaml.load() without Loader"),
      ("CISA","Added to KEV catalog — active exploitation confirmed"),
      ("Ongoing","Millions of Python applications still use unsafe yaml.load()")]),

    ("CVE-2021-32708","Flysystem Path Traversal",9.1,"php","flysystem","< 1.1.4","^3.28","/fix/php/flysystem",
     "Path traversal in Flysystem allows arbitrary file read via crafted paths containing ../ sequences. Any PHP application using Flysystem to serve files based on user-supplied paths is vulnerable.",
     [("What files can an attacker read?","Any file readable by the web server process — /etc/passwd, .env files with database credentials, application config files, source code, private keys. This is a critical data exposure vulnerability."),
      ("Does this affect Laravel?","Yes — Laravel's Storage facade uses Flysystem. Laravel apps using Storage::get() or Storage::download() with user-controlled paths are vulnerable.")],
     [("PackageFix","/"),("CISA KEV","/cisa-kev"),("CVE-2021-32708",None)],
     [("Jun 2021","CVE filed — path traversal in Flysystem"),
      ("Jun 2021","Flysystem 1.1.4, 2.1.1, and 3.0.0-beta2 released"),
      ("CISA","Added to KEV — active exploitation against Laravel apps"),
      ("Ongoing","Many legacy Laravel apps still on Flysystem 1.x")]),

    ("CVE-2021-44906","minimist Prototype Pollution",9.8,"npm","minimist","< 1.2.6","1.2.6","/fix/npm/minimist",
     "Prototype pollution in minimist's argument parsing allows attackers to modify Object.prototype via crafted arguments. minimist is a transitive dependency of thousands of npm packages — even if you don't use it directly, you almost certainly have it.",
     [("How do I fix minimist if it's not in my package.json?","Use npm overrides: {\"overrides\": {\"minimist\": \"1.2.6\"}}. PackageFix generates this block automatically when it detects a transitive minimist vulnerability."),
      ("Why is this CVSS 9.8 for an argument parser?","Prototype pollution via command-line argument parsing can be exploited remotely in applications that parse user-controlled parameters. The CVSS score reflects the worst-case remote exploitation scenario.")],
     [("PackageFix","/"),("CISA KEV","/cisa-kev"),("CVE-2021-44906",None)],
     [("Mar 2022","CVE filed — more severe prototype pollution bypass"),
      ("Mar 2022","minimist 1.2.6 released as fix"),
      ("CISA","Added to KEV — exploitation via npm supply chain attacks"),
      ("Ongoing","Millions of installs of transitive minimist < 1.2.6")]),

    ("CVE-2022-24999","qs Prototype Pollution",7.5,"npm","qs","< 6.11.0","6.11.0","/fix/npm/qs",
     "Prototype pollution in qs query string parsing. qs is a transitive dependency of Express — effectively present in the majority of Node.js web applications. Crafted query strings can pollute Object.prototype and affect all objects in the application.",
     [("How does this reach production?","An attacker sends a crafted HTTP request like ?__proto__[isAdmin]=true. If your application uses qs to parse query strings (directly or via Express) and doesn't sanitize keys, the prototype is polluted."),
      ("Does updating Express fix this?","Express 4.18.0+ bundles qs 6.11.0. Updating Express is the cleanest fix. If you can't update Express, add an npm override: {\"overrides\": {\"qs\": \"6.11.0\"}}.")],
     [("PackageFix","/"),("CISA KEV","/cisa-kev"),("CVE-2022-24999",None)],
     [("Nov 2022","CVE filed — third prototype pollution in qs's history"),
      ("Nov 2022","qs 6.11.0 released — Express 4.18.2 updated to include it"),
      ("CISA","Added to KEV — active exploitation against Express applications"),
      ("Ongoing","Express apps on 4.17.x and below remain vulnerable")]),
]

for (cve_id, name, cvss, eco, pkg, vuln_ver, safe_ver, fix_page,
     long_desc, faqs, bcs, timeline) in KEV_PAGES:
    sev_label = "CRITICAL" if cvss >= 9.0 else "HIGH"
    sev_class = "badge-red" if cvss >= 9.0 else "badge-orange"
    tl_html = "".join(
        f'<div style="display:flex;gap:16px;padding:8px 0;border-bottom:1px solid var(--border)"><span style="color:var(--muted);font-size:11px;min-width:90px">{d}</span><span style="font-size:12px;color:var(--text)">{e}</span></div>'
        for d,e in timeline)
    affected_row = f"<tr><td><strong>{pkg}</strong></td><td>{vuln_ver}</td><td>{safe_ver}</td><td><a href='{fix_page}'>Fix guide →</a></td></tr>"
    body = f"""
<h1>{cve_id} — {name} <span class="badge {sev_class}">{sev_label}</span></h1>
<div style="margin-bottom:20px">
  <span class="badge badge-red" style="margin-right:6px">🔴 CISA KEV</span>
  <span class="badge badge-muted">CVSS {cvss}</span>
</div>
<p class="lead">{long_desc}</p>
<div class="kev-banner"><div class="label">🔴 Actively Exploited</div>
<p>{cve_id} is on the CISA Known Exploited Vulnerabilities catalog. Being used in real attacks right now. Fix immediately.</p></div>
<h2>Affected package</h2>
<table class="cve-history"><thead><tr><th>Package</th><th>Vulnerable</th><th>Safe version</th><th>Fix guide</th></tr></thead>
<tbody>{affected_row}</tbody></table>
<h2>Timeline</h2>
<div style="margin:16px 0">{tl_html}</div>
{cta()}
{faq_html(faqs)}
{related_html([
    {"url":"/cisa-kev","title":"All CISA KEV Packages","desc":"Full actively exploited list"},
    {"url":fix_page,"title":f"Fix {pkg}","desc":"Full fix guide with CVE history"},
    {"url":"/blog/supply-chain-attacks-package-json","title":"Supply Chain Attack Guide","desc":"5 attacks npm audit misses"},
    {"url":"/glossary/cisa-kev","title":"What is CISA KEV?","desc":"Plain-English explanation"},
])}"""
    schemas = [
        {"@type":"TechArticle","headline":f"{cve_id} — {name}","description":long_desc[:200],
         "datePublished":"2026-03-22","dateModified":"2026-03-22",
         "author":{"@type":"Organization","name":"PackageFix","url":BASE_URL}},
        {"@type":"BreadcrumbList","itemListElement":bc([("PackageFix","/"),("CISA KEV","/cisa-kev"),(cve_id,None)])},
        {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}
    ]
    write(f"kev/{cve_id}", shell(
        f"{cve_id} ({name}) — Fix Guide | PackageFix",
        f"Fix {cve_id}: {long_desc[:120]}. CVSS {cvss}. Affected: {pkg} {vuln_ver}. Safe version: {safe_ver}.",
        f"/kev/{cve_id}", bcs, body, schemas))


# ══════════════════════════════════════════════════════════════════════════════
# 4. 6 NEW GLOSSARY TERMS
# ══════════════════════════════════════════════════════════════════════════════

print("\n📖 Generating new glossary terms...")

def glossary(slug, term, badge, one_line, defn, body_extra, faqs, related_pages):
    path = f"/glossary/{slug}"
    body = f"""<h1>{term}</h1>
<div style="margin-bottom:24px"><span class="badge badge-purple">{badge}</span></div>
<div class="definition-box"><div class="def-label">Definition</div><p class="lead">{defn}</p></div>
{body_extra}
{cta()}
{faq_html(faqs)}
{related_html(related_pages)}"""
    schemas = [
        {"@type":"DefinedTerm","name":term,"description":defn,"url":BASE_URL+path,
         "inDefinedTermSet":{"@type":"DefinedTermSet","name":"PackageFix Dependency Security Glossary","url":BASE_URL+"/glossary"}},
        {"@type":"BreadcrumbList","itemListElement":bc([("PackageFix","/"),("Glossary","/glossary"),(term,None)])},
        {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}
    ]
    return shell(f"{term} — Definition | PackageFix Glossary",f"{one_line} {defn[:120]}...",
        path,[("PackageFix","/"),("Glossary","/glossary"),(term,None)],body,schemas)

write("glossary/zero-day", glossary(
    "zero-day","Zero-Day Vulnerability","Security · Exploitation",
    "A vulnerability that is being exploited in the wild before a fix exists.",
    "A zero-day is a security vulnerability that attackers are actively exploiting before the software vendor knows about it or has released a fix. The name comes from the fact that developers have had zero days to address it. Zero-days are the most dangerous class of vulnerability because there is no patch to apply — the only defenses are workarounds, network controls, or disabling affected functionality.",
    """<h2>Zero-day vs known vulnerability</h2>
<p>Most CVEs are not zero-days. The typical vulnerability lifecycle goes: researcher discovers the issue → privately notifies the vendor → vendor releases a patch → CVE is assigned and published. At the point of public disclosure, a patch already exists. A zero-day skips the patch step — it's being exploited before anyone has a fix ready.</p>
<h2>Zero-days in open source dependencies</h2>
<p>In the open source world, zero-days are particularly challenging because the source code is public — attackers can find vulnerabilities by reading the code. The Log4Shell vulnerability (CVE-2021-44228) was being actively exploited in the wild before the Apache team had a complete fix. For the first 72 hours after disclosure, there was no safe version to upgrade to.</p>
<h2>What to do when a zero-day affects your dependencies</h2>
<ul style="padding-left:20px;margin:12px 0;color:var(--muted);font-size:12px;line-height:2">
  <li>Monitor the vendor's GitHub and security mailing list for patch releases</li>
  <li>Apply vendor-recommended workarounds immediately (e.g., JVM flags for Log4Shell)</li>
  <li>Consider disabling affected functionality until a patch is available</li>
  <li>Update to the patched version the moment it's released</li>
</ul>""",
    [("How is a zero-day different from a CVE?","A CVE is just an ID number — it can be assigned to any vulnerability, including zero-days. A zero-day is a status: being exploited before a fix exists. Once a patch is released, it's no longer technically a zero-day, though it remains on the CISA KEV list if exploitation was confirmed."),
     ("Does PackageFix detect zero-days?","PackageFix checks against the OSV database which updates daily as new CVEs are published. For true zero-days (exploited before any CVE exists), PackageFix won't have data until the CVE is filed. The CISA KEV catalog is the best signal — it confirms active exploitation regardless of patch status."),
     ("Can I protect against zero-days in dependencies?","Partially. Keeping dependencies updated means you patch quickly once a fix is released. Network controls (WAF rules, input validation) can block some zero-day exploits before a patch. The CISA KEV catalog helps prioritize — a zero-day on KEV needs immediate response."),
     ("What was the most significant open source zero-day?","Log4Shell (CVE-2021-44228) in Apache Log4j is widely considered the most severe. It affected virtually every Java application, had a CVSS of 10.0, and was being actively exploited before a complete fix was available. Over 3 billion devices were estimated to be affected.")],
    [{"url":"/glossary/cisa-kev","title":"CISA KEV","desc":"Confirmed exploited CVEs"},
     {"url":"/kev/CVE-2021-44228","title":"Log4Shell","desc":"Most severe zero-day example"},
     {"url":"/glossary/cve","title":"CVE","desc":"How vulnerabilities are identified"},
     {"url":"/cisa-kev","title":"CISA KEV Packages","desc":"Actively exploited right now"}]))

write("glossary/remote-code-execution", glossary(
    "remote-code-execution","Remote Code Execution (RCE)","Security · Critical",
    "A vulnerability that allows an attacker to run arbitrary code on a target system over a network, without physical access.",
    "Remote Code Execution (RCE) is the most severe class of security vulnerability. It allows an attacker to execute any code they choose on the target system — over the network, without logging in, without physical access. A successful RCE attack gives the attacker complete control of the affected process and potentially the entire system.",
    """<h2>Why RCE is the worst outcome</h2>
<p>With RCE, an attacker can do anything the compromised process can do: read files, write files, make network connections, install persistence mechanisms, move laterally to other systems. It's game over for the affected system.</p>
<p>In the context of web servers, RCE typically means full server compromise — access to database credentials in environment variables, private keys, customer data, and the ability to serve malicious content to your users.</p>
<h2>How RCE happens in dependencies</h2>
<p>The most common RCE patterns in open source dependencies:</p>
<ul style="padding-left:20px;margin:12px 0;color:var(--muted);font-size:12px;line-height:2">
  <li><strong>Unsafe deserialization</strong> — Log4Shell, SnakeYAML, Jackson, PHP's unserialize()</li>
  <li><strong>Template injection</strong> — user input reaches a template engine that evaluates code</li>
  <li><strong>Command injection</strong> — user input reaches a shell command</li>
  <li><strong>SSRF to internal service</strong> — attacker reaches internal services to pivot to RCE</li>
</ul>
<h2>RCE CVEs on CISA KEV</h2>
<p>Every CRITICAL CVE in PackageFix's database that allows RCE appears on or has been considered for CISA KEV. Log4Shell (CVSS 10.0), Spring4Shell (9.8), Text4Shell (9.8), SnakeYAML (9.8), PHPMailer 2016 (9.8) — all RCE, all exploited in the wild.</p>""",
    [("What CVSS score does RCE get?","RCE vulnerabilities that are network-accessible with no authentication typically get CVSS 9.0-10.0 (Critical). The exact score depends on attack complexity, privilege requirements, and impact scope. CVSS 10.0 means maximum severity: network-accessible, no auth, no user interaction, complete system compromise."),
     ("How do I prevent RCE in my dependencies?","Keep all dependencies updated — RCE CVEs are patched when discovered. Specifically: never deserialize untrusted data without an allowlist, never pass untrusted input to eval() or exec(), keep Java's JNDI disabled in production (fixes Log4Shell class), and use yaml.safe_load() not yaml.load() in Python."),
     ("If my app has an RCE CVE, what should I do immediately?","Patch immediately. If no patch is available, take the affected service offline or implement the vendor's recommended workaround. Assume the system may already be compromised — review logs for unusual activity, rotate all credentials that were accessible to the affected process."),
     ("Is RCE possible through npm packages?","Yes — postinstall scripts in npm packages run automatically on npm install with full process permissions. A malicious postinstall script that runs curl | bash is effectively RCE on the developer's machine or CI server. This is why PackageFix scans for suspicious build scripts.")],
    [{"url":"/glossary/zero-day","title":"Zero-Day","desc":"Exploited before fix exists"},
     {"url":"/glossary/deserialization","title":"Deserialization","desc":"Main RCE attack vector"},
     {"url":"/kev/CVE-2021-44228","title":"Log4Shell — RCE","desc":"Most severe Java RCE"},
     {"url":"/cisa-kev","title":"CISA KEV","desc":"All confirmed exploited CVEs"}]))

write("glossary/deserialization", glossary(
    "deserialization","Deserialization Vulnerability","Security · Java · Python",
    "A security flaw where converting stored or transmitted data back into objects allows an attacker to execute arbitrary code.",
    "Deserialization is the process of converting stored or transmitted data (like JSON, YAML, or binary formats) back into objects your application can use. A deserialization vulnerability occurs when this process can be exploited to execute arbitrary code — by crafting malicious serialized data that, when deserialized, triggers dangerous operations like JNDI lookups, shell commands, or object instantiation chains.",
    """<h2>Why deserialization leads to RCE</h2>
<p>When your application deserializes data, it's reconstructing objects. If the deserialization library doesn't restrict what types of objects can be created, an attacker can craft data that causes the library to instantiate dangerous classes — classes that execute code in their constructors or magic methods.</p>
<p>Java is particularly susceptible because its native serialization supports arbitrary class instantiation. The concept of a "gadget chain" — a series of class instantiations that ultimately execute a shell command — has been discovered in Commons Collections, Spring, and dozens of other Java libraries.</p>
<h2>Real deserialization CVEs</h2>
<ul style="padding-left:20px;margin:12px 0;color:var(--muted);font-size:12px;line-height:2">
  <li><strong>Log4Shell (CVE-2021-44228)</strong> — JNDI deserialization via log message. CVSS 10.0.</li>
  <li><strong>SnakeYAML (CVE-2022-1471)</strong> — arbitrary Java class instantiation via YAML. CISA KEV.</li>
  <li><strong>Jackson Databind</strong> — polymorphic deserialization gadget chains. Multiple CVEs.</li>
  <li><strong>PyYAML (CVE-2020-14343)</strong> — Python object instantiation via yaml.load(). CISA KEV.</li>
  <li><strong>PHP unserialize()</strong> — PHP object injection via native serialization.</li>
</ul>
<h2>The fix</h2>
<p>Never deserialize data from untrusted sources using native serialization or unrestricted YAML/object loaders. Use safe alternatives: <code>yaml.safe_load()</code> in Python, <code>new Yaml(new SafeConstructor())</code> in Java, JSON instead of pickle, explicit type allowlists in Jackson.</p>""",
    [("What is the difference between serialization and deserialization?","Serialization converts an object to a storable/transmittable format (like JSON or binary). Deserialization is the reverse — converting stored data back into an object. The vulnerability is in deserialization, not serialization."),
     ("Is JSON deserialization safe?","JSON deserialization (parsing JSON into objects) is generally safe if you use a standard JSON library without polymorphic type handling enabled. The dangerous pattern is when JSON deserialization can instantiate arbitrary class types — which Jackson enables with 'default typing' enabled."),
     ("Which languages are most vulnerable to deserialization attacks?","Java has the most severe deserialization history due to its native serialization format supporting arbitrary class instantiation. Python (via pickle and unsafe YAML), PHP (via unserialize()), and Ruby (via Marshal) also have deserialization risks. Modern JSON-focused APIs are much safer."),
     ("How does PackageFix flag deserialization CVEs?","PackageFix flags specific package versions with known deserialization CVEs via the OSV database. Packages like SnakeYAML, Jackson Databind, and PyYAML are checked on every scan.")],
    [{"url":"/glossary/remote-code-execution","title":"Remote Code Execution","desc":"What deserialization enables"},
     {"url":"/kev/CVE-2021-44228","title":"Log4Shell","desc":"JNDI deserialization RCE"},
     {"url":"/kev/CVE-2022-1471","title":"SnakeYAML RCE","desc":"YAML deserialization"},
     {"url":"/fix/java/jackson-databind","title":"Fix Jackson Databind","desc":"Deserialization CVEs"}]))

write("glossary/redos", glossary(
    "redos","ReDoS — Regular Expression Denial of Service","DoS · All ecosystems",
    "A denial of service attack where a crafted input causes a regular expression to take exponentially long to evaluate, hanging the application.",
    "ReDoS (Regular Expression Denial of Service) exploits how some regular expressions behave with certain inputs — specifically, regex engines that use backtracking can take exponentially longer as input length increases when given a carefully crafted string. A single malicious HTTP request containing a few hundred characters can hang a Node.js server for seconds or cause a complete CPU lockup.",
    """<h2>How backtracking causes ReDoS</h2>
<p>Most regex engines use backtracking — when a pattern doesn't match, the engine tries alternative paths. For certain patterns, this creates an explosion of possibilities. Consider a regex like <code>(a+)+</code> against the input <code>aaaaaaaaX</code>. The engine tries every possible way to group the a's before concluding no match — the number of attempts grows exponentially with input length.</p>
<h2>ReDoS in popular packages</h2>
<ul style="padding-left:20px;margin:12px 0;color:var(--muted);font-size:12px;line-height:2">
  <li><strong>moment.js</strong> — CVE-2022-31129, CVE-2017-18214 — date parsing regex</li>
  <li><strong>semver</strong> — CVE-2022-25883 — version coerce() function</li>
  <li><strong>marked</strong> — CVE-2022-21681 — markdown parsing</li>
  <li><strong>validator</strong> — CVE-2021-3765 — email validation</li>
  <li><strong>Django</strong> — CVE-2024-27351 — strip_tags() HTML sanitizer</li>
  <li><strong>pydantic</strong> — CVE-2024-3772 — email address validation</li>
</ul>
<h2>Why Node.js is especially vulnerable</h2>
<p>Node.js runs JavaScript in a single-threaded event loop. A ReDoS attack that hangs the regex engine for 2 seconds doesn't just slow down one request — it blocks all other requests for those 2 seconds. A moderate-scale attack can completely take down a Node.js server with minimal bandwidth.</p>
<div class="definition-box" style="margin:20px 0">
  <div class="def-label">Detection</div>
  <p class="lead">The <a href="https://devina.io/redos-checker" target="_blank" rel="noopener">ReDoS checker</a> can identify vulnerable regex patterns in your own code. For dependencies, PackageFix flags packages with known ReDoS CVEs.</p>
</div>""",
    [("Is ReDoS a critical vulnerability?","ReDoS is typically rated HIGH (7.5) rather than CRITICAL because it causes denial of service rather than data theft or code execution. However, for single-threaded runtimes like Node.js, a well-crafted ReDoS can completely take down a service — which is functionally critical in production."),
     ("How do I test if my regex is vulnerable?","Use a ReDoS checker tool or run the regex against increasingly long crafted inputs and check if evaluation time grows exponentially. Safe regex patterns use possessive quantifiers or atomic groups when available in your language."),
     ("Does multi-threading protect against ReDoS?","Partially. In multi-threaded applications, only the affected thread is blocked, so other requests continue. But if enough ReDoS requests come in simultaneously, all threads can be occupied. Node.js is most vulnerable due to its single-threaded model."),
     ("How does PackageFix handle ReDoS CVEs?","PackageFix checks all package versions against OSV which includes ReDoS CVEs. They're flagged with HIGH severity. The fix is always a package update — the library must patch the vulnerable regex.")],
    [{"url":"/glossary/cve","title":"CVE","desc":"How ReDoS vulnerabilities are tracked"},
     {"url":"/fix/npm/moment","title":"Fix moment.js","desc":"ReDoS CVEs in moment"},
     {"url":"/fix/npm/semver","title":"Fix semver","desc":"ReDoS in semver"},
     {"url":"/fix/pypi/django","title":"Fix Django","desc":"ReDoS in Django"}]))

write("glossary/cwe", glossary(
    "cwe","CWE — Common Weakness Enumeration","Security · Classification",
    "A catalog of common software and hardware weakness types — the root cause categories that CVEs are classified under.",
    "CWE (Common Weakness Enumeration) is a catalog of software and hardware weakness types maintained by MITRE. Where CVEs are specific vulnerabilities in specific products, CWEs are the categories of weakness that lead to those vulnerabilities. CWE-79 is Cross-Site Scripting, CWE-89 is SQL Injection, CWE-502 is Deserialization of Untrusted Data. A CVE will often reference the CWE that explains why the vulnerability exists.",
    """<h2>CWE vs CVE — what's the difference</h2>
<p>Think of CWEs as the root causes and CVEs as the instances. CWE-502 (Deserialization of Untrusted Data) is the weakness category. CVE-2021-44228 (Log4Shell) is a specific instance of that weakness in Apache Log4j.</p>
<p>CVEs describe what happened. CWEs describe why it happened and how to prevent the whole class of issue.</p>
<h2>The most important CWEs for dependency security</h2>
<ul style="padding-left:20px;margin:12px 0;color:var(--muted);font-size:12px;line-height:2">
  <li><strong>CWE-502</strong> — Deserialization of Untrusted Data (Log4Shell, SnakeYAML, PyYAML)</li>
  <li><strong>CWE-1321</strong> — Prototype Pollution (lodash, qs, minimist)</li>
  <li><strong>CWE-400</strong> — Uncontrolled Resource Consumption (ReDoS — moment, semver)</li>
  <li><strong>CWE-22</strong> — Path Traversal (Flysystem, CarrierWave, Sprockets)</li>
  <li><strong>CWE-89</strong> — SQL Injection (Ransack, Hibernate, activerecord)</li>
  <li><strong>CWE-79</strong> — Cross-Site Scripting (many web framework CVEs)</li>
  <li><strong>CWE-601</strong> — URL Redirection (open redirect CVEs in axios, express)</li>
</ul>""",
    [("Do I need to know CWEs to use PackageFix?","No — PackageFix shows CVE IDs and severity. CWEs are useful background knowledge for understanding why a class of vulnerabilities keeps recurring in certain types of libraries."),
     ("Where can I look up CWEs?","cwe.mitre.org has the full catalog. Individual CVE pages on NVD and OSV often reference the relevant CWE."),
     ("What is the difference between CWE and OWASP Top 10?","OWASP Top 10 lists the most critical web application security risks (like Injection, Broken Authentication). CWEs are the underlying technical weakness classifications. Many OWASP Top 10 categories map to multiple CWEs."),
     ("Which CWE covers supply chain attacks?","Supply chain attacks don't have a single CWE — they involve multiple weaknesses. CWE-1357 (Reliance on Insufficiently Trustworthy Component) covers the conceptual failure. Specific attack techniques use other CWEs — code injection (CWE-94), malicious dependency (CWE-829).")],
    [{"url":"/glossary/cve","title":"CVE","desc":"Specific vulnerability instances"},
     {"url":"/glossary/cvss","title":"CVSS","desc":"How CVEs are scored"},
     {"url":"/glossary/deserialization","title":"Deserialization","desc":"CWE-502 examples"},
     {"url":"/glossary/prototype-pollution","title":"Prototype Pollution","desc":"CWE-1321 examples"}]))

write("glossary/cyclonedx", glossary(
    "cyclonedx","CycloneDX","SBOM · OWASP · Compliance",
    "An OWASP standard format for Software Bills of Materials (SBOMs) — a machine-readable inventory of every component in a software application.",
    "CycloneDX is an open SBOM (Software Bill of Materials) standard maintained by OWASP. It defines a JSON or XML format for cataloguing every open source component, dependency, and service in a software application — including their versions, licenses, and known vulnerabilities. CycloneDX is one of the two main SBOM formats (alongside SPDX) and is widely supported by SCA tools and CI/CD pipelines.",
    """<h2>Why CycloneDX matters</h2>
<p>When Log4Shell hit in December 2021, organizations scrambled to find every system running vulnerable Log4j. Teams with SBOM inventories could query them in minutes. Teams without took days or weeks of manual audit. That incident accelerated SBOM adoption significantly.</p>
<p>The US executive order on cybersecurity (2021) and EU Cyber Resilience Act (2025) both reference SBOMs as a requirement for software sold to government and certain markets. CycloneDX is one of the two accepted formats.</p>
<h2>How to generate a CycloneDX SBOM</h2>
<pre># npm projects
npx @cyclonedx/cyclonedx-npm --output-file sbom.json

# Python
pip install cyclonedx-bom
cyclonedx-bom -o sbom.json

# All ecosystems (using syft)
syft . -o cyclonedx-json > sbom.json

# Java/Maven
mvn org.cyclonedx:cyclonedx-maven-plugin:makeAggregateBom</pre>
<h2>CycloneDX vs SPDX</h2>
<p>Both are widely accepted SBOM formats. CycloneDX (OWASP) was designed with security use cases first — it has richer vulnerability data support. SPDX (Linux Foundation) was designed with license compliance first. For security tooling, CycloneDX is usually the better choice. Many tools support both.</p>""",
    [("Does PackageFix generate CycloneDX SBOMs?","Not currently — PackageFix focuses on vulnerability scanning and fix generation. For formal SBOM generation, use the CycloneDX CLI tools, syft, or your IDE's SCA plugin. You can then scan the generated SBOM with osv-scanner --sbom sbom.json."),
     ("What information does a CycloneDX SBOM contain?","Component name, version, package URL (PURL), supplier, license, hash, and optionally known vulnerabilities (VEX — Vulnerability Exploitability eXchange). The full spec is at cyclonedx.org."),
     ("Who accepts CycloneDX SBOMs?","US federal agencies (mandated by executive order), most enterprise software procurement programs, and major CI/CD security platforms including Snyk, Mend, and Sonatype Nexus IQ."),
     ("Is generating an SBOM required for open source projects?","Not currently required for open source. It's primarily required for software sold to US government or subject to EU Cyber Resilience Act. Generating one is still good practice — it helps you respond quickly to future Log4Shell-style events.")],
    [{"url":"/glossary/sbom","title":"SBOM","desc":"What CycloneDX describes"},
     {"url":"/glossary/dependency-scanning","title":"Dependency Scanning","desc":"How SBOM data is used"},
     {"url":"/guides/github-actions","title":"GitHub Actions","desc":"SBOM scanning in CI"},
     {"url":"/cisa-kev","title":"CISA KEV","desc":"What SBOMs help you find"}]))


# ══════════════════════════════════════════════════════════════════════════════
# 5. WEEKLY CVE DIGEST #2
# ══════════════════════════════════════════════════════════════════════════════

print("\n📰 Generating weekly CVE digest #2...")

DIGEST2_ITEMS = [
    ("CVE-2024-29041","express","npm","MEDIUM","< 4.19.2","4.19.2",
     "Open redirect via response.redirect() with user-controlled URLs. If your Express app passes any user input to res.redirect(), users can be sent to external attacker-controlled sites. Fix: update to 4.19.2.","/fix/npm/express"),
    ("CVE-2024-1135","gunicorn","PyPI","HIGH","< 22.0.0","22.0.0",
     "HTTP request smuggling via invalid Transfer-Encoding header. Any gunicorn deployment behind a reverse proxy (nginx, caddy, cloudflare) is potentially affected. Fix: update to 22.0.0.","/fix/pypi/gunicorn"),
    ("CVE-2024-32650","rustls","Rust","HIGH","< 0.23.5","0.23.5",
     "Infinite loop via crafted TLS certificate chain. Any Rust server using rustls that accepts TLS connections from untrusted clients is affected. Fix: update to 0.23.5.","/fix/rust/rustls"),
    ("CVE-2024-21508","mysql2","npm","CRITICAL","< 3.9.7","3.9.7",
     "Remote code execution via SQL injection in prepared statement handling. CRITICAL — update immediately if you use mysql2 with user-controlled input in preparedStatement.","/fix/npm/mysql2"),
    ("CVE-2024-34069","werkzeug","PyPI","CRITICAL","< 3.0.3","3.0.3",
     "RCE via Werkzeug debugger PIN bypass. Only affects apps running with debug=True — which should never be production. But if your staging environment is exposed, this is critical. Fix: 3.0.3 + ensure debug=False in production.","/fix/pypi/werkzeug"),
    ("CVE-2024-22189","fiber","Go","HIGH","< v2.52.2","v2.52.2",
     "DoS via HTTP/2 CONTINUATION frames flood. Any Fiber server accepting HTTP/2 connections is affected. Related to the broader HTTP/2 vulnerability class from 2024. Fix: v2.52.2.","/fix/go/fiber"),
]

d2_items_html = ""
for cve, pkg, eco, sv, vuln_ver, safe_ver, desc, fix_url in DIGEST2_ITEMS:
    sc = "badge-red" if sv=="CRITICAL" else "badge-orange" if sv=="HIGH" else "badge-purple"
    d2_items_html += f"""<div class="digest-item">
<h3><a href="https://osv.dev/vulnerability/{cve}" target="_blank" rel="noopener">{cve}</a> — {pkg}</h3>
<div style="margin-bottom:8px">
  <span class="badge badge-purple" style="font-size:9px">{eco}</span>
  <span class="badge {sc}" style="margin-left:6px">{sv}</span>
</div>
<p><strong>Affected:</strong> {vuln_ver} · <strong>Fix:</strong> {safe_ver}</p>
<p>{desc}</p>
<p><a href="{fix_url}">Full fix guide →</a></p>
</div>"""

write("blog/weekly-cve-march-29-2026", shell(
    "Weekly CVE Digest — March 29, 2026 | PackageFix",
    "6 critical CVEs this week: mysql2 RCE, Werkzeug debugger RCE, gunicorn HTTP smuggling, rustls infinite loop, express open redirect, fiber HTTP/2 DoS. Fix guides for all.",
    "/blog/weekly-cve-march-29-2026",
    [("PackageFix","/"),("Blog","/blog"),("Weekly CVE Digest March 29 2026",None)],
    f"""<h1>Weekly CVE Digest — March 29, 2026</h1>
<p style="color:var(--muted);font-size:11px;margin-bottom:24px">March 29, 2026 · PackageFix · 6 CVEs this week across npm, PyPI, Go, Rust</p>
<p class="lead">Two CRITICAL CVEs this week — mysql2 RCE and Werkzeug debugger bypass. Six total across npm, PyPI, Go, and Rust. Paste your manifest into PackageFix to check if you're affected.</p>
{d2_items_html}
{cta()}
{related_html([
    {"url":"/blog/weekly-cve-march-2026","title":"Last Week's Digest","desc":"March 22, 2026 — 7 CVEs"},
    {"url":"/cisa-kev","title":"CISA KEV Packages","desc":"All actively exploited packages"},
    {"url":"/fix/npm/mysql2","title":"Fix mysql2","desc":"CRITICAL RCE"},
    {"url":"/fix/pypi/werkzeug","title":"Fix Werkzeug","desc":"CRITICAL debugger RCE"},
])}""",
    [{"@type":"Article","headline":"Weekly CVE Digest — March 29, 2026",
      "description":"6 critical CVEs this week across npm, PyPI, Go, and Rust.",
      "datePublished":"2026-03-29","dateModified":"2026-03-29",
      "author":{"@type":"Organization","name":"PackageFix","url":BASE_URL}},
     {"@type":"BreadcrumbList","itemListElement":bc([("PackageFix","/"),("Blog","/blog"),("Weekly CVE March 29",None)])}]))


# ══════════════════════════════════════════════════════════════════════════════
# 6. 4 NEW COMPARISON PAGES
# ══════════════════════════════════════════════════════════════════════════════

print("\n⚔ Generating comparison pages...")

COMPARISONS_NEW = [
    ("osv-scanner","PackageFix vs OSV Scanner",
     "Compare PackageFix and Google's OSV Scanner. OSV Scanner is a CLI tool — PackageFix is browser-based. Both use the same OSV vulnerability database.",
     "Google's OSV Scanner is the closest technical equivalent to PackageFix's data source — both query api.osv.dev. The key difference is the interface: OSV Scanner is a CLI tool you install and run, PackageFix is a browser tool you paste into.",
     [("Feature","PackageFix","OSV Scanner"),
      ("Interface","Browser — no install","CLI — requires install"),
      ("Fix output","✅ Downloads fixed manifest","❌ Report only"),
      ("CISA KEV flags","✅ Yes","❌ No"),
      ("Supply chain detection","✅ Yes","❌ CVEs only"),
      ("Data source","OSV API + CISA KEV","OSV API"),
      ("7 ecosystems","✅ Yes","✅ Yes"),
      ("CI integration","❌ Manual only","✅ GitHub Action available"),
      ("Free","✅ Yes","✅ Yes")]),

    ("mend","PackageFix vs Mend (WhiteSource)",
     "Compare PackageFix and Mend (formerly WhiteSource) for dependency security scanning. Mend is an enterprise SCA platform requiring an account and integration.",
     "Mend (formerly WhiteSource) is a mature enterprise SCA platform with deep CI/CD integration, license compliance, and auto-remediation PRs. PackageFix is a browser tool for quick one-off scans with no account required. They serve different use cases.",
     [("Feature","PackageFix","Mend"),
      ("Browser-based","✅ Yes","❌ No — account required"),
      ("Cost","✅ Free","❌ Paid"),
      ("Fix output","✅ Downloads fixed manifest","⚠ PRs only"),
      ("CISA KEV flags","✅ Yes","⚠ Limited"),
      ("Supply chain detection","✅ Yes","⚠ Partial"),
      ("CI/CD integration","❌ Manual only","✅ Full CI integration"),
      ("License compliance","❌ Not yet","✅ Yes"),
      ("7 ecosystems","✅ Yes","✅ More ecosystems"),
      ("Best for","Quick checks, no account","Enterprise teams, automation")]),

    ("sonatype","PackageFix vs Sonatype Nexus IQ",
     "Compare PackageFix and Sonatype Nexus IQ for dependency scanning. Nexus IQ is an enterprise platform. PackageFix is a free browser alternative.",
     "Sonatype Nexus IQ is a commercial SCA platform with binary scanning, policy enforcement, and component intelligence. PackageFix is a free browser tool. Nexus IQ is for teams managing hundreds of projects with compliance requirements. PackageFix is for developers who need a quick scan right now.",
     [("Feature","PackageFix","Sonatype Nexus IQ"),
      ("Browser-based","✅ Yes","❌ Requires integration"),
      ("Cost","✅ Free","❌ Enterprise pricing"),
      ("Fix output","✅ Downloads fixed file","⚠ Policy recommendations"),
      ("CISA KEV flags","✅ Yes","⚠ Via integration"),
      ("Binary scanning","❌ Source only","✅ Yes"),
      ("Policy enforcement","❌ No","✅ Yes"),
      ("Best for","Individual developers","Large enterprise teams")]),

    ("bytesafe","PackageFix vs Bytesafe",
     "Compare PackageFix and Bytesafe for npm dependency security. Bytesafe is npm-only and checker-only. PackageFix supports 7 ecosystems and generates the fixed manifest.",
     "Bytesafe is a browser-based npm security scanner — the closest competitor to PackageFix in terms of interface. Key differences: Bytesafe only covers npm, has no CISA KEV integration, and doesn't generate a fixed manifest to download.",
     [("Feature","PackageFix","Bytesafe"),
      ("Browser-based","✅ Yes","✅ Yes"),
      ("Ecosystems","✅ 7 (npm+PyPI+Ruby+PHP+Go+Rust+Java)","❌ npm only"),
      ("Fix output","✅ Downloads fixed manifest","❌ Checker only"),
      ("CISA KEV flags","✅ Yes","❌ No"),
      ("Supply chain detection","✅ Yes","❌ CVEs only"),
      ("Free","✅ Yes","✅ Free tier"),
      ("Snyk Advisor gap","✅ Yes, fills it","⚠ Partial — npm only")]),
]

for slug, title, desc, summary, rows in COMPARISONS_NEW:
    rows_html = "".join(
        f"<tr><td style='font-weight:600;color:var(--text)'>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
        for r in rows[1:])
    faqs = [
        ("Does PackageFix replace these tools?","PackageFix is a browser tool for quick one-off scans. Enterprise SCA platforms like Mend and Sonatype add value at scale — automated scanning, policy enforcement, audit trails. Use PackageFix for immediate checks and enterprise tools for continuous coverage."),
        ("Is PackageFix free?","Yes — completely free, MIT licensed, open source."),
        ("Which ecosystems does PackageFix support?","npm, PyPI, Ruby, PHP, Go, Rust, and Java/Maven — 7 ecosystems."),
    ]
    body = f"""<h1>{title}</h1>
<p class="lead">{summary}</p>
<table class="cve-history">
  <thead><tr><th>{rows[0][0]}</th><th>{rows[0][1]}</th><th>{rows[0][2]}</th></tr></thead>
  <tbody>{rows_html}</tbody>
</table>
{cta()}
{faq_html(faqs)}
{related_html([
    {"url":"/compare","title":"All Comparisons","desc":"Full tool comparison index"},
    {"url":"/vs/snyk-advisor","title":"vs Snyk Advisor","desc":"Shut down Jan 2026"},
    {"url":"/alternatives","title":"All Alternatives","desc":"16-tool comparison table"},
    {"url":"/glossary/software-composition-analysis","title":"What is SCA?","desc":"Plain-English explanation"},
])}"""
    schemas = [
        {"@type":"BreadcrumbList","itemListElement":bc([("PackageFix","/"),("Compare","/compare"),(title,None)])},
        {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}
    ]
    write(f"compare/{slug}", shell(
        f"{title} | PackageFix",
        f"{desc}",
        f"/compare/{slug}",
        [("PackageFix","/"),("Compare","/compare"),(title,None)],
        body, schemas))


# ══════════════════════════════════════════════════════════════════════════════
# UPDATE CONFIG FILES
# ══════════════════════════════════════════════════════════════════════════════

print("\n📝 Updating vercel.json...")
rewrites = []
for p in all_paths:
    rewrites.append({"source":p,"destination":f"/seo{p}/index.html"})
    rewrites.append({"source":p+"/","destination":f"/seo{p}/index.html"})

vercel_config = {}
if os.path.exists("vercel.json"):
    with open("vercel.json") as f:
        vercel_config = json.load(f)

existing = vercel_config.get("rewrites",[])
existing_sources = {r["source"] for r in existing}
added = 0
for r in rewrites:
    if r["source"] not in existing_sources:
        existing.append(r)
        existing_sources.add(r["source"])
        added += 1

vercel_config["rewrites"] = existing
with open("vercel.json","w") as f:
    json.dump(vercel_config, f, indent=2)
print(f"  ✓ vercel.json — {len(existing)} total rewrites ({added} new)")

print("\n🗺 Updating sitemap-seo.xml...")
new_urls = ""
for p in all_paths:
    freq = "weekly" if "blog" in p else "monthly"
    pri = "0.9" if p in ["/fix","/guides","/providers","/blog/weekly-cve-march-29-2026"] else "0.8"
    new_urls += f"  <url>\n    <loc>{BASE_URL}{p}</loc>\n    <changefreq>{freq}</changefreq>\n    <priority>{pri}</priority>\n  </url>\n"

if os.path.exists("sitemap-seo.xml"):
    with open("sitemap-seo.xml") as f:
        content = f.read()
    updated = content.replace("</urlset>", new_urls + "</urlset>")
else:
    updated = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + new_urls + "</urlset>"
with open("sitemap-seo.xml","w") as f:
    f.write(updated)
print(f"  ✓ sitemap-seo.xml — {len(all_paths)} new URLs")

print("\n🤖 Updating llm.txt...")
with open("llm.txt","a") as f:
    f.write("\n## Index Pages + Remaining Items\n")
    for p in all_paths:
        f.write(f"{BASE_URL}{p}\n")
print("  ✓ llm.txt updated")

print(f"\n✅ Done — {len(all_paths)} pages total")
by_type = {}
for p in all_paths:
    k = p.split("/")[1] if "/" in p[1:] else p[1:]
    by_type[k] = by_type.get(k,0) + 1
for k,v in sorted(by_type.items()):
    print(f"   /{k}: {v} page{'s' if v>1 else ''}")

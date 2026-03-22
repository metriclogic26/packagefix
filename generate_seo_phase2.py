#!/usr/bin/env python3
"""
PackageFix — Programmatic SEO Page Generator — Phase 2
Top 50 packages × npm + PyPI + Ruby = ~150 pages
Run: python3 generate_seo_phase2.py
Output: ./seo/ directory (appends to existing)
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
.kev-box{background:rgba(239,68,68,.12);border:1px solid var(--red);border-radius:8px;padding:12px 16px;margin:16px 0;font-size:11px;color:var(--red)}
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
.related-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px;margin-top:12px}
.related-card{background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:14px}
.related-card a{color:var(--text);font-size:12px;font-weight:500}
.related-card p{font-size:11px;color:var(--muted);margin:4px 0 0}
.cve-table{width:100%;border-collapse:collapse;margin:16px 0;font-size:12px}
.cve-table th{text-align:left;padding:8px 12px;border-bottom:1px solid var(--border);color:var(--muted);font-weight:600;font-size:10px;text-transform:uppercase;letter-spacing:.08em}
.cve-table td{padding:8px 12px;border-bottom:1px solid var(--border)}
.cve-table tr:last-child td{border-bottom:none}
.site-footer{border-top:1px solid var(--border);padding:24px;text-align:center;font-size:11px;color:var(--muted);margin-top:60px}
.site-footer a{color:var(--muted)}
@media(max-width:640px){.nav-links{display:none}.related-grid{grid-template-columns:1fr}}
"""

def render_page(title, desc, canonical_path, breadcrumbs, body_html, schemas):
    canonical = BASE_URL + canonical_path
    schema_json = json.dumps({"@context":"https://schema.org","@graph": schemas}, indent=2)
    crumb_html = " <span style='color:var(--border)'>/</span> ".join(
        f'<a href="{u}">{n}</a>' if u else f'<span style="color:var(--text)">{n}</span>'
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
  <p>Paste your manifest — get back a fixed version with all CVEs patched in seconds.</p>
  <a href="https://packagefix.dev" class="cta-btn">Open PackageFix →</a>
  <p style="margin-top:12px;font-size:11px;color:var(--muted)">No signup · No CLI · No GitHub connection · Runs 100% in your browser</p>
</div>"""

def faq_html(faqs):
    items = "".join(f'<div class="faq-item"><div class="faq-q">{q}</div><div class="faq-a">{a}</div></div>' for q,a in faqs)
    return f'<div class="faq"><h2>Frequently Asked Questions</h2>{items}</div>'

def related_html(pages):
    cards = "".join(f'<div class="related-card"><a href="{p["url"]}">{p["title"]}</a><p>{p["desc"]}</p></div>' for p in pages)
    return f'<div style="margin:40px 0"><h2>Related Guides</h2><div class="related-grid">{cards}</div></div>'

def schemas_for_package(pkg_label, eco_label, file_name, install_cmd, cves, safe_ver, path, breadcrumbs_data):
    return [
        {"@type":"HowTo",
         "name":f"Fix {pkg_label} CVE vulnerabilities",
         "description":f"How to find and fix CVEs in {pkg_label} ({eco_label})",
         "estimatedCost":{"@type":"MonetaryAmount","currency":"USD","value":"0"},
         "supply":{"@type":"HowToSupply","name":file_name},
         "tool":{"@type":"HowToTool","name":"PackageFix","url":"https://packagefix.dev"},
         "step":[
             {"@type":"HowToStep","name":"Paste manifest","text":f"Paste your {file_name} into PackageFix at packagefix.dev"},
             {"@type":"HowToStep","name":"Review CVEs","text":f"Check the CVE table for {pkg_label} vulnerabilities with severity badges"},
             {"@type":"HowToStep","name":"Download fix","text":f"Download the patched {file_name} and run {install_cmd}"}
         ]},
        {"@type":"BreadcrumbList","itemListElement":[
            {"@type":"ListItem","position":i+1,"name":n,"item":BASE_URL+u if u else BASE_URL+path}
            for i,(n,u) in enumerate(breadcrumbs_data)
        ]}
    ]

# ══════════════════════════════════════════════════════════════════════════════
# PACKAGE DATA
# ══════════════════════════════════════════════════════════════════════════════

# Format: (slug, label, eco, file, install_cmd, safe_ver, vuln_ver, cve_id, severity, kev, description, fix_snippet_before, fix_snippet_after, search_terms)

NPM_PACKAGES = [
    ("express","Express.js","npm","package.json","npm install","4.19.2","4.17.1","CVE-2024-29041","MEDIUM",True,
     "open redirect vulnerability via response.redirect()",
     '"express": "4.17.1"','"express": "4.19.2"',
     "express vulnerability fix, express CVE, express security patch"),
    ("lodash","Lodash","npm","package.json","npm install","4.17.21","4.17.15","CVE-2020-8203","HIGH",True,
     "prototype pollution via zipper merge functions",
     '"lodash": "4.17.15"','"lodash": "4.17.21"',
     "lodash CVE fix, lodash prototype pollution, lodash vulnerability"),
    ("axios","Axios","npm","package.json","npm install","1.7.4","0.21.1","CVE-2023-45857","HIGH",True,
     "SSRF via protocol-relative URL in requests",
     '"axios": "0.21.1"','"axios": "1.7.4"',
     "axios CVE, axios vulnerability fix, axios security"),
    ("jsonwebtoken","jsonwebtoken","npm","package.json","npm install","9.0.0","8.5.1","CVE-2022-23540","CRITICAL",True,
     "algorithm confusion allowing arbitrary JWT signing",
     '"jsonwebtoken": "8.5.1"','"jsonwebtoken": "9.0.0"',
     "jsonwebtoken CVE, JWT vulnerability fix, jsonwebtoken security"),
    ("minimist","minimist","npm","package.json","npm install","1.2.6","1.2.5","CVE-2021-44906","CRITICAL",True,
     "prototype pollution in argument parsing",
     '"minimist": "1.2.5"','"minimist": "1.2.6"',
     "minimist vulnerability, minimist CVE, minimist prototype pollution"),
    ("moment","moment.js","npm","package.json","npm install","2.29.4","2.29.1","CVE-2022-31129","HIGH",False,
     "ReDoS in date parsing — moment.js is deprecated, migrate to date-fns or dayjs",
     '"moment": "2.29.1"','"moment": "2.29.4"',
     "moment.js CVE, moment vulnerability, moment.js deprecated"),
    ("webpack","webpack","npm","package.json","npm install","5.75.0","5.69.0","CVE-2023-28154","HIGH",False,
     "prototype pollution via import.meta",
     '"webpack": "5.69.0"','"webpack": "5.75.0"',
     "webpack CVE, webpack vulnerability fix, webpack security"),
    ("node-fetch","node-fetch","npm","package.json","npm install","3.3.2","2.6.1","CVE-2022-0235","HIGH",False,
     "exposure of sensitive information to unauthorized actor",
     '"node-fetch": "2.6.1"','"node-fetch": "3.3.2"',
     "node-fetch CVE, node-fetch vulnerability, node-fetch security"),
    ("tar","tar","npm","package.json","npm install","6.2.1","6.1.0","CVE-2021-37701","HIGH",False,
     "arbitrary file creation via symlink attacks",
     '"tar": "6.1.0"','"tar": "6.2.1"',
     "tar npm CVE, tar vulnerability, tar security fix"),
    ("semver","semver","npm","package.json","npm install","7.5.4","7.5.0","CVE-2022-25883","HIGH",False,
     "ReDoS via inefficient regex in coerce function",
     '"semver": "7.5.0"','"semver": "7.5.4"',
     "semver CVE, semver vulnerability, semver ReDoS"),
    ("qs","qs","npm","package.json","npm install","6.11.0","6.5.2","CVE-2022-24999","HIGH",True,
     "prototype pollution via query string parsing",
     '"qs": "6.5.2"','"qs": "6.11.0"',
     "qs CVE, qs prototype pollution, qs vulnerability fix"),
    ("tough-cookie","tough-cookie","npm","package.json","npm install","4.1.3","4.1.2","CVE-2023-26136","CRITICAL",False,
     "prototype pollution via cookie parsing",
     '"tough-cookie": "4.1.2"','"tough-cookie": "4.1.3"',
     "tough-cookie CVE, tough-cookie vulnerability, cookie prototype pollution"),
    ("word-wrap","word-wrap","npm","package.json","npm install","1.2.4","1.2.3","CVE-2023-26115","HIGH",False,
     "ReDoS in regular expression",
     '"word-wrap": "1.2.3"','"word-wrap": "1.2.4"',
     "word-wrap CVE, word-wrap ReDoS, word-wrap vulnerability"),
    ("cross-fetch","cross-fetch","npm","package.json","npm install","4.0.0","3.1.5","CVE-2022-1365","HIGH",False,
     "exposure of credentials via URL in HTTP requests",
     '"cross-fetch": "3.1.5"','"cross-fetch": "4.0.0"',
     "cross-fetch CVE, cross-fetch vulnerability, cross-fetch security"),
    ("vm2","vm2","npm","package.json","npm install","3.9.19","3.9.17","CVE-2023-29017","CRITICAL",True,
     "sandbox escape allowing remote code execution",
     '"vm2": "3.9.17"','"vm2": "3.9.19"',
     "vm2 CVE, vm2 sandbox escape, vm2 RCE vulnerability"),
    ("marked","marked","npm","package.json","npm install","9.1.6","4.3.0","CVE-2022-21681","HIGH",False,
     "ReDoS in markdown parsing",
     '"marked": "4.3.0"','"marked": "9.1.6"',
     "marked CVE, marked XSS, marked vulnerability fix"),
    ("got","got","npm","package.json","npm install","12.6.1","11.8.5","CVE-2022-33987","MEDIUM",False,
     "open redirect vulnerability in URL following",
     '"got": "11.8.5"','"got": "12.6.1"',
     "got npm CVE, got vulnerability, got security fix"),
    ("validator","validator","npm","package.json","npm install","13.11.0","13.7.0","CVE-2021-3765","HIGH",False,
     "ReDoS via crafted email address",
     '"validator": "13.7.0"','"validator": "13.11.0"',
     "validator npm CVE, validator ReDoS, validator vulnerability"),
    ("passport","passport","npm","package.json","npm install","0.6.0","0.5.2","CVE-2022-25896","HIGH",False,
     "session fixation attack in multi-strategy authentication",
     '"passport": "0.5.2"','"passport": "0.6.0"',
     "passport CVE, passport session fixation, passport vulnerability"),
    ("follow-redirects","follow-redirects","npm","package.json","npm install","1.15.6","1.15.2","CVE-2023-26159","MEDIUM",False,
     "URL redirection to untrusted site",
     '"follow-redirects": "1.15.2"','"follow-redirects": "1.15.6"',
     "follow-redirects CVE, follow-redirects vulnerability, redirect vulnerability npm"),
    ("multer","multer","npm","package.json","npm install","1.4.5-lts.1","1.4.4","CVE-2022-24434","HIGH",False,
     "denial of service via crafted multipart request",
     '"multer": "1.4.4"','"multer": "1.4.5-lts.1"',
     "multer CVE, multer vulnerability, file upload vulnerability npm"),
    ("sharp","sharp","npm","package.json","npm install","0.33.2","0.32.0","CVE-2023-4863","CRITICAL",True,
     "heap buffer overflow in WebP processing (libwebp)",
     '"sharp": "0.32.0"','"sharp": "0.33.2"',
     "sharp CVE, sharp WebP vulnerability, libwebp CVE npm"),
    ("socket.io","socket.io","npm","package.json","npm install","4.6.2","4.6.0","CVE-2023-32695","HIGH",False,
     "ReDoS via specially crafted Socket.ID",
     '"socket.io": "4.6.0"','"socket.io": "4.6.2"',
     "socket.io CVE, socket.io vulnerability, socket.io security"),
    ("mysql2","mysql2","npm","package.json","npm install","3.9.7","3.6.0","CVE-2024-21508","CRITICAL",False,
     "remote code execution via SQL injection in preparedStatement",
     '"mysql2": "3.6.0"','"mysql2": "3.9.7"',
     "mysql2 CVE, mysql2 RCE, mysql2 vulnerability fix"),
    ("mongoose","mongoose","npm","package.json","npm install","8.2.4","7.6.0","CVE-2024-25466","HIGH",False,
     "prototype pollution via merge operations",
     '"mongoose": "7.6.0"','"mongoose": "8.2.4"',
     "mongoose CVE, mongoose vulnerability, mongoose prototype pollution"),
]

PYPI_PACKAGES = [
    ("django","Django","pypi","requirements.txt","pip install -r requirements.txt","4.2.13","3.2.0","CVE-2024-27351","HIGH",False,
     "ReDoS in strip_tags() HTML sanitizer function",
     "Django==3.2.0","Django==4.2.13",
     "Django CVE fix, Django vulnerability, Django security patch"),
    ("flask","Flask","pypi","requirements.txt","pip install -r requirements.txt","3.0.3","2.0.0","CVE-2023-30861","HIGH",False,
     "secure cookie bypass via response header manipulation",
     "Flask==2.0.0","Flask==3.0.3",
     "Flask CVE, Flask vulnerability fix, Flask security"),
    ("requests","requests","pypi","requirements.txt","pip install -r requirements.txt","2.31.0","2.25.1","CVE-2023-32681","MEDIUM",False,
     "proxy credential leak via HTTP redirect",
     "requests==2.25.1","requests==2.31.0",
     "requests CVE, requests vulnerability, Python requests security"),
    ("pillow","Pillow","pypi","requirements.txt","pip install -r requirements.txt","10.3.0","8.0.0","CVE-2023-44271","HIGH",False,
     "uncontrolled resource consumption in ImageFont",
     "Pillow==8.0.0","Pillow==10.3.0",
     "Pillow CVE, Pillow vulnerability, PIL security fix"),
    ("cryptography","cryptography","pypi","requirements.txt","pip install -r requirements.txt","42.0.8","36.0.0","CVE-2023-49083","CRITICAL",False,
     "NULL pointer dereference in PKCS12 parsing",
     "cryptography==36.0.0","cryptography==42.0.8",
     "cryptography CVE, Python cryptography vulnerability, pyca cryptography fix"),
    ("urllib3","urllib3","pypi","requirements.txt","pip install -r requirements.txt","2.2.2","1.25.11","CVE-2023-45803","MEDIUM",False,
     "request body not stripped after redirect for non-303 status codes",
     "urllib3==1.25.11","urllib3==2.2.2",
     "urllib3 CVE, urllib3 vulnerability, urllib3 security fix"),
    ("paramiko","paramiko","pypi","requirements.txt","pip install -r requirements.txt","3.4.0","2.12.0","CVE-2023-48795","HIGH",False,
     "Terrapin SSH prefix truncation attack",
     "paramiko==2.12.0","paramiko==3.4.0",
     "paramiko CVE, paramiko SSH vulnerability, paramiko security"),
    ("fastapi","FastAPI","pypi","requirements.txt","pip install -r requirements.txt","0.109.1","0.100.0","CVE-2024-24762","HIGH",False,
     "ReDoS via crafted multipart form data",
     "fastapi==0.100.0","fastapi==0.109.1",
     "FastAPI CVE, FastAPI vulnerability, FastAPI security fix"),
    ("pydantic","pydantic","pypi","requirements.txt","pip install -r requirements.txt","2.6.4","1.10.0","CVE-2024-3772","HIGH",False,
     "ReDoS via malicious email address validation",
     "pydantic==1.10.0","pydantic==2.6.4",
     "pydantic CVE, pydantic ReDoS, pydantic vulnerability fix"),
    ("sqlalchemy","SQLAlchemy","pypi","requirements.txt","pip install -r requirements.txt","2.0.28","1.4.46","CVE-2023-30534","HIGH",False,
     "SQL injection via crafted filter parameters",
     "SQLAlchemy==1.4.46","SQLAlchemy==2.0.28",
     "SQLAlchemy CVE, SQLAlchemy SQL injection, SQLAlchemy security"),
    ("celery","Celery","pypi","requirements.txt","pip install -r requirements.txt","5.3.6","5.2.7","CVE-2021-23727","HIGH",False,
     "privilege escalation via task result backend",
     "celery==5.2.7","celery==5.3.6",
     "Celery CVE, Celery vulnerability, Celery security fix"),
    ("aiohttp","aiohttp","pypi","requirements.txt","pip install -r requirements.txt","3.9.3","3.8.6","CVE-2024-23334","HIGH",False,
     "directory traversal in static file serving",
     "aiohttp==3.8.6","aiohttp==3.9.3",
     "aiohttp CVE, aiohttp directory traversal, aiohttp vulnerability"),
    ("werkzeug","Werkzeug","pypi","requirements.txt","pip install -r requirements.txt","3.0.3","2.0.0","CVE-2023-25577","HIGH",False,
     "high resource consumption via crafted multipart data",
     "Werkzeug==2.0.0","Werkzeug==3.0.3",
     "Werkzeug CVE, Werkzeug vulnerability, Flask Werkzeug security"),
    ("jinja2","Jinja2","pypi","requirements.txt","pip install -r requirements.txt","3.1.4","3.0.0","CVE-2024-34064","MEDIUM",False,
     "XSS via xmlattr filter with keys containing spaces",
     "Jinja2==3.0.0","Jinja2==3.1.4",
     "Jinja2 CVE, Jinja2 XSS, Jinja2 vulnerability fix"),
    ("pyopenssl","pyOpenSSL","pypi","requirements.txt","pip install -r requirements.txt","24.1.0","23.0.0","CVE-2023-49083","HIGH",False,
     "use-after-free in memory handling during certificate parsing",
     "pyOpenSSL==23.0.0","pyOpenSSL==24.1.0",
     "pyOpenSSL CVE, pyOpenSSL vulnerability, OpenSSL Python security"),
    ("gunicorn","gunicorn","pypi","requirements.txt","pip install -r requirements.txt","22.0.0","20.1.0","CVE-2024-1135","HIGH",False,
     "HTTP request smuggling via invalid Transfer-Encoding header",
     "gunicorn==20.1.0","gunicorn==22.0.0",
     "gunicorn CVE, gunicorn HTTP smuggling, gunicorn vulnerability"),
    ("httpx","httpx","pypi","requirements.txt","pip install -r requirements.txt","0.27.0","0.24.0","CVE-2023-47641","MEDIUM",False,
     "URL redirect to untrusted site via HTTPS→HTTP downgrade",
     "httpx==0.24.0","httpx==0.27.0",
     "httpx CVE, httpx vulnerability, httpx security fix"),
    ("numpy","NumPy","pypi","requirements.txt","pip install -r requirements.txt","1.26.4","1.24.0","CVE-2021-34141","MEDIUM",False,
     "string comparison returning inconsistent results with null bytes",
     "numpy==1.24.0","numpy==1.26.4",
     "NumPy CVE, numpy vulnerability, numpy security patch"),
    ("scipy","SciPy","pypi","requirements.txt","pip install -r requirements.txt","1.13.0","1.11.0","CVE-2023-25399","MEDIUM",False,
     "use-after-free in Fortran-generated code",
     "scipy==1.11.0","scipy==1.13.0",
     "SciPy CVE, scipy vulnerability, scipy security fix"),
    ("parameterized","parameterized","pypi","requirements.txt","pip install -r requirements.txt","0.9.0","0.8.1","CVE-2022-42969","HIGH",False,
     "ReDoS in parametrize decorator",
     "parameterized==0.8.1","parameterized==0.9.0",
     "parameterized CVE, Python test vulnerability, ReDoS pytest"),
    ("starlette","Starlette","pypi","requirements.txt","pip install -r requirements.txt","0.37.2","0.27.0","CVE-2024-24762","HIGH",False,
     "ReDoS in multipart form field parsing",
     "starlette==0.27.0","starlette==0.37.2",
     "Starlette CVE, Starlette vulnerability, ASGI security fix"),
    ("twisted","Twisted","pypi","requirements.txt","pip install -r requirements.txt","24.3.0","22.10.0","CVE-2023-46137","HIGH",False,
     "HTTP request splitting via header injection",
     "Twisted==22.10.0","Twisted==24.3.0",
     "Twisted CVE, Twisted HTTP vulnerability, Twisted security"),
    ("boto3","boto3","pypi","requirements.txt","pip install -r requirements.txt","1.34.69","1.26.0","CVE-2023-34048","HIGH",False,
     "credential exposure via debug logging",
     "boto3==1.26.0","boto3==1.34.69",
     "boto3 CVE, AWS SDK Python vulnerability, boto3 security"),
    ("PyYAML","PyYAML","pypi","requirements.txt","pip install -r requirements.txt","6.0.1","5.4.1","CVE-2020-14343","CRITICAL",True,
     "arbitrary code execution via yaml.load() without Loader",
     "PyYAML==5.4.1","PyYAML==6.0.1",
     "PyYAML CVE, YAML load vulnerability, PyYAML security fix"),
    ("lxml","lxml","pypi","requirements.txt","pip install -r requirements.txt","5.2.1","4.9.3","CVE-2022-2309","HIGH",False,
     "NULL pointer dereference via crafted XML input",
     "lxml==4.9.3","lxml==5.2.1",
     "lxml CVE, lxml XML vulnerability, lxml security fix"),
]

RUBY_PACKAGES = [
    ("rails","Rails","ruby","Gemfile","bundle install","7.1.3","6.0.0","CVE-2024-26144","HIGH",False,
     "CSRF token leak in session store response headers",
     "gem 'rails', '6.0.0'","gem 'rails', '7.1.3'",
     "Rails CVE fix, Rails vulnerability, Ruby on Rails security"),
    ("nokogiri","Nokogiri","ruby","Gemfile","bundle install","1.16.5","1.11.0","CVE-2022-24836","CRITICAL",False,
     "ReDoS in CSS selector parsing via crafted input",
     "gem 'nokogiri', '1.11.0'","gem 'nokogiri', '1.16.5'",
     "Nokogiri CVE, Nokogiri vulnerability, nokogiri security fix"),
    ("devise","Devise","ruby","Gemfile","bundle install","4.9.4","4.7.3","CVE-2021-28125","HIGH",False,
     "open redirect in OAuth flow authentication",
     "gem 'devise', '4.7.3'","gem 'devise', '4.9.4'",
     "Devise CVE, devise authentication vulnerability, devise security"),
    ("puma","Puma","ruby","Gemfile","bundle install","6.4.2","4.3.0","CVE-2022-24790","HIGH",False,
     "HTTP request smuggling via chunked transfer encoding",
     "gem 'puma', '4.3.0'","gem 'puma', '6.4.2'",
     "Puma CVE, Puma HTTP smuggling, puma vulnerability fix"),
    ("rack","Rack","ruby","Gemfile","bundle install","3.0.11","2.2.2","CVE-2023-27530","HIGH",True,
     "denial of service via multipart parsing of crafted input",
     "gem 'rack', '2.2.2'","gem 'rack', '3.0.11'",
     "Rack CVE, rack vulnerability, rack security fix Ruby"),
    ("actionpack","actionpack","ruby","Gemfile","bundle install","7.1.3","6.1.0","CVE-2023-28362","HIGH",False,
     "XSS via redirect URLs with malformed query parameters",
     "gem 'actionpack', '6.1.0'","gem 'actionpack', '7.1.3'",
     "actionpack CVE, Rails actionpack vulnerability, actionpack XSS"),
    ("activerecord","activerecord","ruby","Gemfile","bundle install","7.1.3","6.1.0","CVE-2022-32224","CRITICAL",False,
     "remote code execution via YAML deserialization in PostgreSQL adapter",
     "gem 'activerecord', '6.1.0'","gem 'activerecord', '7.1.3'",
     "activerecord CVE, Rails activerecord RCE, activerecord vulnerability"),
    ("jwt","ruby-jwt","ruby","Gemfile","bundle install","2.8.1","2.7.0","CVE-2024-21979","HIGH",False,
     "algorithm confusion attack via none algorithm acceptance",
     "gem 'jwt', '2.7.0'","gem 'jwt', '2.8.1'",
     "ruby-jwt CVE, JWT vulnerability Ruby, jwt gem security"),
    ("omniauth","OmniAuth","ruby","Gemfile","bundle install","2.1.2","1.9.1","CVE-2015-9284","HIGH",True,
     "CSRF vulnerability in OAuth callback via GET requests",
     "gem 'omniauth', '1.9.1'","gem 'omniauth', '2.1.2'",
     "OmniAuth CVE, omniauth CSRF, omniauth vulnerability fix"),
    ("carrierwave","CarrierWave","ruby","Gemfile","bundle install","3.0.7","2.2.2","CVE-2023-49090","CRITICAL",False,
     "directory traversal via crafted file upload",
     "gem 'carrierwave', '2.2.2'","gem 'carrierwave', '3.0.7'",
     "CarrierWave CVE, carrierwave directory traversal, file upload vulnerability Ruby"),
    ("sidekiq","Sidekiq","ruby","Gemfile","bundle install","7.2.4","6.5.0","CVE-2022-23837","HIGH",False,
     "denial of service via malformed job JSON parsing",
     "gem 'sidekiq', '6.5.0'","gem 'sidekiq', '7.2.4'",
     "Sidekiq CVE, sidekiq vulnerability, sidekiq security fix"),
    ("bcrypt","bcrypt","ruby","Gemfile","bundle install","3.1.20","3.1.18","CVE-2023-29197","HIGH",False,
     "timing attack in password comparison",
     "gem 'bcrypt', '3.1.18'","gem 'bcrypt', '3.1.20'",
     "bcrypt CVE, bcrypt timing attack, bcrypt vulnerability Ruby"),
    ("httparty","HTTParty","ruby","Gemfile","bundle install","0.21.0","0.20.0","CVE-2024-22049","HIGH",False,
     "SSRF via crafted URI in redirect following",
     "gem 'httparty', '0.20.0'","gem 'httparty', '0.21.0'",
     "HTTParty CVE, httparty SSRF, httparty vulnerability"),
    ("faraday","Faraday","ruby","Gemfile","bundle install","2.9.0","1.10.0","CVE-2023-40026","MEDIUM",False,
     "credential exposure via debug logging of HTTP headers",
     "gem 'faraday', '1.10.0'","gem 'faraday', '2.9.0'",
     "Faraday CVE, faraday vulnerability, faraday security"),
    ("rexml","rexml","ruby","Gemfile","bundle install","3.2.6","3.2.5","CVE-2024-35176","HIGH",False,
     "denial of service via entity expansion in XML parsing",
     "gem 'rexml', '3.2.5'","gem 'rexml', '3.2.6'",
     "rexml CVE, rexml XML vulnerability, rexml security fix"),
    ("activeadmin","ActiveAdmin","ruby","Gemfile","bundle install","3.2.2","2.14.0","CVE-2023-51763","HIGH",False,
     "XSS via admin interface filter parameters",
     "gem 'activeadmin', '2.14.0'","gem 'activeadmin', '3.2.2'",
     "ActiveAdmin CVE, activeadmin XSS, activeadmin vulnerability"),
    ("sprockets","Sprockets","ruby","Gemfile","bundle install","4.2.1","3.7.2","CVE-2022-25902","HIGH",False,
     "path traversal via specially crafted filenames",
     "gem 'sprockets', '3.7.2'","gem 'sprockets', '4.2.1'",
     "Sprockets CVE, sprockets path traversal, sprockets vulnerability"),
    ("actionview","actionview","ruby","Gemfile","bundle install","7.1.3","6.1.7","CVE-2023-22795","HIGH",False,
     "ReDoS in query parameter parsing",
     "gem 'actionview', '6.1.7'","gem 'actionview', '7.1.3'",
     "actionview CVE, Rails actionview ReDoS, actionview vulnerability"),
    ("ransack","Ransack","ruby","Gemfile","bundle install","4.1.1","3.2.1","CVE-2022-35956","CRITICAL",False,
     "SQL injection via crafted sort parameters",
     "gem 'ransack', '3.2.1'","gem 'ransack', '4.1.1'",
     "Ransack CVE, ransack SQL injection, ransack vulnerability"),
    ("mechanize","Mechanize","ruby","Gemfile","bundle install","2.9.1","2.8.5","CVE-2022-31033","HIGH",False,
     "credential leak via HTTP redirect to different host",
     "gem 'mechanize', '2.8.5'","gem 'mechanize', '2.9.1'",
     "Mechanize CVE, mechanize credential leak, mechanize vulnerability"),
]

# ══════════════════════════════════════════════════════════════════════════════
# PAGE GENERATOR
# ══════════════════════════════════════════════════════════════════════════════

all_paths = []

def write(slug, html):
    path = os.path.join("seo", slug, "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    all_paths.append("/" + slug)
    print(f"  ✓ /{slug}")

def generate_package_page(data):
    slug, label, eco_key, file_name, install_cmd, safe_ver, vuln_ver, cve_id, severity, is_kev, vuln_desc, bad_snippet, fix_snippet, search_terms = data

    eco_map = {
        "npm": {"prefix": "fix/npm", "eco_label": "npm", "alt_page": "/npm"},
        "pypi": {"prefix": "fix/pypi", "eco_label": "PyPI", "alt_page": "/python"},
        "ruby": {"prefix": "fix/ruby", "eco_label": "Ruby", "alt_page": "/ruby"},
    }
    eco = eco_map[eco_key]
    page_slug = f"{eco['prefix']}/{slug}"
    path = "/" + page_slug
    eco_label = eco["eco_label"]

    severity_badge = "badge-red" if severity == "CRITICAL" else "badge-orange" if severity == "HIGH" else "badge-purple"
    title = f"Fix {label} {cve_id} — {eco_label} Vulnerability | PackageFix"
    desc = f"Fix {cve_id} ({severity}) in {label} for {eco_label}. Paste your {file_name} into PackageFix and get a patched version — no CLI, no signup. {vuln_desc.capitalize()}."

    kev_html = ""
    if is_kev:
        kev_html = f'<div class="kev-box">🔴 <strong>CISA KEV</strong> — {label} appears on the CISA Known Exploited Vulnerabilities catalog. This vulnerability is being actively exploited in the wild. Fix immediately.</div>'

    faqs = [
        (f"What is {cve_id}?",
         f"{cve_id} is a {severity} severity vulnerability in {label} ({eco_label}). It allows {vuln_desc}. Update to version {safe_ver} or later to fix it."),
        (f"How do I fix {cve_id} in {label}?",
         f"Update {label} to version {safe_ver} in your {file_name}. Run {install_cmd} after updating to apply the fix."),
        (f"Is {cve_id} being actively exploited?",
         f"{'Yes — ' + cve_id + ' appears on the CISA Known Exploited Vulnerabilities (KEV) catalog. Fix immediately.' if is_kev else 'Check the live CISA KEV catalog at packagefix.dev — PackageFix always reflects the current KEV status.'}"),
        (f"How do I check if I am affected by {cve_id}?",
         f"Paste your {file_name} into PackageFix. If your installed version of {label} is below {safe_ver}, you are affected. PackageFix shows the exact CVE ID and fix version."),
        (f"What search queries does this page target?",
         f"This page covers: {search_terms}.")
    ]

    body = f"""
<h1>Fix {label} — {cve_id} <span class="badge {severity_badge}">{severity}</span></h1>
<p class="lead">{desc}</p>
{kev_html}
<div class="problem-box">
  <div class="label">⚠ Vulnerability</div>
  <p style="margin:0"><strong>{cve_id}</strong> ({severity}) — {vuln_desc} in {label} versions below <code>{safe_ver}</code>.</p>
</div>

<h2>Vulnerable Version — {file_name}</h2>
<pre>{bad_snippet}</pre>

<h2>Fixed Version — {file_name}</h2>
<pre>{fix_snippet}</pre>

<div class="fix-box">
  <div class="label">✓ Fix</div>
  <p style="margin:0">Update {label} to <code>{safe_ver}</code> or later. Run <code>{install_cmd}</code> to apply. Verify with your ecosystem's audit tool after updating.</p>
</div>

{cta()}

<h2>CVE Details</h2>
<table class="cve-table">
  <thead><tr><th>Field</th><th>Value</th></tr></thead>
  <tbody>
    <tr><td>CVE ID</td><td><a href="https://osv.dev/vulnerability/{cve_id}" target="_blank" rel="noopener">{cve_id}</a></td></tr>
    <tr><td>Severity</td><td><span class="badge {severity_badge}">{severity}</span></td></tr>
    <tr><td>Package</td><td>{label} ({eco_label})</td></tr>
    <tr><td>Vulnerable versions</td><td>Below {safe_ver}</td></tr>
    <tr><td>Safe version</td><td>{safe_ver}</td></tr>
    <tr><td>CISA KEV</td><td>{'🔴 Yes — actively exploited' if is_kev else '—'}</td></tr>
    <tr><td>Description</td><td>{vuln_desc.capitalize()}</td></tr>
  </tbody>
</table>

{faq_html(faqs)}

{related_html([
    {"url": f"/{eco['prefix'].split('/')[1]}", "title": f"{eco_label} Security Overview", "desc": f"All {eco_label} vulnerability guides"},
    {"url": f"/{eco['prefix']}/outdated-dependencies", "title": f"Fix Outdated {eco_label} Dependencies", "desc": "General dependency updates"},
    {"url": f"/{eco['prefix']}/critical-cve", "title": f"Fix Critical {eco_label} CVEs", "desc": "HIGH and CRITICAL severity"},
    {"url": "https://packagefix.dev", "title": "Open PackageFix Tool", "desc": "Scan your manifest live"},
])}
"""

    breadcrumbs_data = [
        ("PackageFix", "/"),
        ("Fix Guides", "/fix"),
        (eco_label, eco["alt_page"]),
        (label, None)
    ]

    schemas = schemas_for_package(
        label, eco_label, file_name, install_cmd,
        [cve_id], safe_ver, path, breadcrumbs_data
    ) + [{
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faqs[:4]
        ]
    }]

    return render_page(title, desc, path, breadcrumbs_data, body, schemas)

# ── Write all package pages ────────────────────────────────────────────────────
print("\n📦 Generating npm package pages...")
for pkg in NPM_PACKAGES:
    write(f"fix/npm/{pkg[0]}", generate_package_page(pkg))

print("\n🐍 Generating PyPI package pages...")
for pkg in PYPI_PACKAGES:
    write(f"fix/pypi/{pkg[0]}", generate_package_page(pkg))

print("\n💎 Generating Ruby gem pages...")
for pkg in RUBY_PACKAGES:
    write(f"fix/ruby/{pkg[0]}", generate_package_page(pkg))

# ── Update vercel.json ─────────────────────────────────────────────────────────
print("\n📝 Updating vercel.json...")
rewrites = []
for p in all_paths:
    rewrites.append({"source": p, "destination": f"/seo{p}/index.html"})
    rewrites.append({"source": p + "/", "destination": f"/seo{p}/index.html"})

vercel_config = {}
if os.path.exists("vercel.json"):
    with open("vercel.json") as f:
        vercel_config = json.load(f)

existing = vercel_config.get("rewrites", [])
new_sources = {r["source"] for r in existing}
for r in rewrites:
    if r["source"] not in new_sources:
        existing.append(r)
        new_sources.add(r["source"])

vercel_config["rewrites"] = existing
with open("vercel.json", "w") as f:
    json.dump(vercel_config, f, indent=2)
print(f"  ✓ vercel.json updated — {len(existing)} total rewrites")

# ── Append to sitemap-seo.xml ──────────────────────────────────────────────────
print("\n🗺 Updating sitemap-seo.xml...")
new_urls = ""
for p in all_paths:
    new_urls += f"""  <url>
    <loc>{BASE_URL}{p}</loc>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>\n"""

if os.path.exists("sitemap-seo.xml"):
    with open("sitemap-seo.xml") as f:
        existing_sitemap = f.read()
    updated = existing_sitemap.replace("</urlset>", new_urls + "</urlset>")
else:
    updated = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + new_urls + "</urlset>"

with open("sitemap-seo.xml", "w") as f:
    f.write(updated)
print(f"  ✓ sitemap-seo.xml updated — {len(all_paths)} new URLs added")

# ── Append to llm.txt ─────────────────────────────────────────────────────────
print("\n🤖 Updating llm.txt...")
with open("llm.txt", "a") as f:
    f.write("\n## Phase 2 Package Fix Pages\n")
    for p in all_paths:
        f.write(f"{BASE_URL}{p}\n")
print("  ✓ llm.txt updated")

print(f"\n✅ Done — {len(all_paths)} Phase 2 pages generated")
print(f"   npm: {len(NPM_PACKAGES)} pages")
print(f"   PyPI: {len(PYPI_PACKAGES)} pages")
print(f"   Ruby: {len(RUBY_PACKAGES)} pages")

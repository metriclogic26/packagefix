#!/usr/bin/env python3
"""
PackageFix — CVE History Tables
Adds complete CVE history to existing package pages.
Overwrites Phase 2/3 pages with richer versions.
Targets the top packages with multiple CVEs.
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
.badge-muted{background:rgba(107,114,128,.15);color:var(--muted);border:1px solid var(--border)}
.cve-history{width:100%;border-collapse:collapse;margin:16px 0;font-size:12px}
.cve-history th{text-align:left;padding:10px 12px;border-bottom:2px solid var(--border);color:var(--muted);font-weight:600;font-size:10px;text-transform:uppercase;letter-spacing:.08em}
.cve-history td{padding:10px 12px;border-bottom:1px solid var(--border);vertical-align:top}
.cve-history tr:last-child td{border-bottom:none}
.cve-history tr:hover td{background:var(--surface2)}
.cve-history .kev-dot{color:var(--red);margin-right:4px}
.faq{margin:40px 0}
.faq-item{border-bottom:1px solid var(--border);padding:16px 0}
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

def shell(title, desc, canonical_path, breadcrumbs, body, schemas):
    canonical = BASE_URL + canonical_path
    schema_json = json.dumps({"@context": "https://schema.org", "@graph": schemas}, indent=2)
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
    <a href="https://packagefix.dev/glossary">Glossary</a>
    <a href="https://packagefix.dev/cisa-kev">CISA KEV</a>
    <a href="https://packagefix.dev/blog">Blog</a>
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
  <p>Paste your manifest — see your exact installed version against this full CVE list.</p>
  <a href="https://packagefix.dev" class="cta-btn">Scan with PackageFix →</a>
  <p style="margin-top:12px;font-size:11px;color:var(--muted)">Free · No signup · No CLI · Runs in your browser</p>
</div>"""

def faq_html(faqs):
    items = "".join(
        f'<div class="faq-item"><div class="faq-q">{q}</div><div class="faq-a">{a}</div></div>'
        for q, a in faqs
    )
    return f'<div class="faq"><h2>Common questions</h2>{items}</div>'

def related_html(pages):
    cards = "".join(
        f'<div class="related-card"><a href="{p["url"]}">{p["title"]}</a><p>{p["desc"]}</p></div>'
        for p in pages
    )
    return f'<div style="margin:40px 0"><h2>Related</h2><div class="related-grid">{cards}</div></div>'

def severity_badge(sev):
    cls = "badge-red" if sev == "CRITICAL" else "badge-orange" if sev == "HIGH" else "badge-purple" if sev == "MEDIUM" else "badge-muted"
    return f'<span class="badge {cls}">{sev}</span>'

def cve_history_table(cves):
    """cves = list of (cve_id, year, severity, is_kev, is_fixed, safe_ver, description)"""
    rows = ""
    for cve_id, year, sev, is_kev, is_fixed, safe_ver, desc in cves:
        kev = '<span class="kev-dot" title="CISA KEV — actively exploited">🔴</span>' if is_kev else ""
        fixed = f'<span class="badge badge-green">Fixed in {safe_ver}</span>' if is_fixed else '<span class="badge badge-orange">No fix</span>'
        rows += f"""<tr>
  <td><a href="https://osv.dev/vulnerability/{cve_id}" target="_blank" rel="noopener">{cve_id}</a></td>
  <td>{year}</td>
  <td>{kev}{severity_badge(sev)}</td>
  <td style="color:var(--muted)">{desc}</td>
  <td>{fixed}</td>
</tr>"""
    return f"""<table class="cve-history">
  <thead>
    <tr>
      <th>CVE ID</th>
      <th>Year</th>
      <th>Severity</th>
      <th>Description</th>
      <th>Fix</th>
    </tr>
  </thead>
  <tbody>{rows}</tbody>
</table>"""

all_paths = []

def write(slug, html):
    path = os.path.join("seo", slug, "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    all_paths.append("/" + slug)
    print(f"  ✓ /{slug}")

# ══════════════════════════════════════════════════════════════════════════════
# PACKAGE CVE HISTORY DATA
# Each entry: (cve_id, year, severity, is_kev, is_fixed, safe_ver, short_desc)
# ══════════════════════════════════════════════════════════════════════════════

PACKAGE_HISTORIES = [

  # ── npm ────────────────────────────────────────────────────────────────────

  {
    "slug": "fix/npm/lodash",
    "pkg": "lodash", "eco": "npm", "eco_label": "npm",
    "safe_ver": "4.17.21",
    "install": "npm install",
    "weekly_downloads": "50M+",
    "desc": "lodash is one of the most-downloaded JavaScript utility libraries. It has had several high-severity CVEs, mostly prototype pollution and command injection. All are fixed in 4.17.21.",
    "cves": [
        ("CVE-2018-3721", 2018, "MEDIUM", False, True, "4.17.5", "Prototype pollution via defaultsDeep"),
        ("CVE-2018-16487", 2018, "HIGH",   False, True, "4.17.11","Prototype pollution via merge"),
        ("CVE-2019-1010266",2019,"MEDIUM", False, True, "4.17.11","Regular expression DoS in trim functions"),
        ("CVE-2019-10744",  2019,"CRITICAL",False,True, "4.17.12","Prototype pollution via defaultsDeep (bypass)"),
        ("CVE-2020-8203",   2020,"HIGH",   True,  True, "4.17.21","Prototype pollution via zipObjectDeep and merge — CISA KEV"),
        ("CVE-2021-23337",  2021,"HIGH",   False, True, "4.17.21","Command injection via template function"),
    ],
    "fix_snippet_before": '"lodash": "4.17.15"',
    "fix_snippet_after":  '"lodash": "4.17.21"',
    "faqs": [
        ("How many CVEs does lodash have?", "lodash has 6 known CVEs, all fixed in version 4.17.21. The most severe are the prototype pollution vulnerabilities CVE-2020-8203 (CISA KEV) and CVE-2019-10744 (CRITICAL). Keeping lodash at 4.17.21 addresses all of them."),
        ("Is lodash safe to use in 2026?", "Yes — lodash 4.17.21 has no known unpatched CVEs. That said, lodash is increasingly replaced by native JavaScript for many operations. If you're starting a new project, consider whether you need lodash or if native Array/Object methods cover your use cases."),
        ("Why does lodash have so many prototype pollution CVEs?", "lodash does deep object merging and manipulation — functions like merge(), defaultsDeep(), and zipObjectDeep(). These operations are inherently tricky to implement safely when user-controlled keys are involved. The team patched each variant as they were discovered."),
        ("What is CISA KEV and why is CVE-2020-8203 on it?", "CISA KEV (Known Exploited Vulnerabilities) is a catalog of CVEs confirmed being used in real attacks. CVE-2020-8203 was added because attackers were using lodash prototype pollution to bypass authentication in web applications. It means you should treat this as urgent, not just routine.")
    ],
    "related": [
        {"url": "/kev/CVE-2020-8203", "title": "CVE-2020-8203 Detail", "desc": "CISA KEV — prototype pollution"},
        {"url": "/glossary/prototype-pollution", "title": "What is Prototype Pollution?", "desc": "Plain-English explanation"},
        {"url": "/fix/npm/minimist", "title": "Fix minimist", "desc": "Another prototype pollution CVE"},
        {"url": "/npm", "title": "npm Security Overview", "desc": "All npm vulnerability guides"},
    ]
  },

  {
    "slug": "fix/npm/axios",
    "pkg": "axios", "eco": "npm", "eco_label": "npm",
    "safe_ver": "1.7.4",
    "install": "npm install",
    "weekly_downloads": "50M+",
    "desc": "axios is the most popular HTTP client for JavaScript. It has had several CVEs across its version history, mostly related to SSRF, credential exposure on redirect, and prototype pollution.",
    "cves": [
        ("CVE-2020-28168", 2020, "MEDIUM", False, True, "0.21.1", "SSRF via server-side request with crafted URL"),
        ("CVE-2021-3749",  2021, "HIGH",   False, True, "0.21.2", "Regular expression DoS in axios headers"),
        ("CVE-2022-1214",  2022, "MEDIUM", False, True, "0.26.0", "Exposure of confidential data via logs in debug mode"),
        ("CVE-2023-45857", 2023, "HIGH",   True,  True, "1.6.0",  "SSRF via protocol-relative URL — CISA KEV"),
    ],
    "fix_snippet_before": '"axios": "0.21.1"',
    "fix_snippet_after":  '"axios": "1.7.4"',
    "faqs": [
        ("What is the safest version of axios to use?", "1.7.4 is the latest safe version as of March 2026. Avoid anything below 1.6.0 which introduced the fix for CVE-2023-45857 (CISA KEV)."),
        ("Does CVE-2023-45857 affect all axios users?", "It specifically affects apps that use axios with XSRF token protection and allow user-controlled redirect targets. If you use axios with default settings and don't follow redirects to user-supplied URLs, your exposure is lower — but you should still upgrade."),
        ("Why is axios on the CISA KEV list?", "CVE-2023-45857 was confirmed being exploited in server-side request forgery attacks against applications that proxy requests through axios. CISA added it to the KEV catalog because of confirmed in-the-wild exploitation."),
        ("Is there a major version migration needed?", "Yes — axios 1.x has some breaking changes from 0.x. The main change is that errors now extend AxiosError instead of a plain Error. Most applications need minimal changes. The security improvement is worth it.")
    ],
    "related": [
        {"url": "/kev/CVE-2023-45857", "title": "CVE-2023-45857 Detail", "desc": "CISA KEV — SSRF"},
        {"url": "/fix/npm/follow-redirects", "title": "Fix follow-redirects", "desc": "Related redirect CVE"},
        {"url": "/glossary/supply-chain-attack", "title": "Supply Chain Attacks", "desc": "Broader context"},
        {"url": "/npm", "title": "npm Security Overview", "desc": "All npm CVE guides"},
    ]
  },

  {
    "slug": "fix/npm/express",
    "pkg": "express", "eco": "npm", "eco_label": "npm",
    "safe_ver": "4.19.2",
    "install": "npm install",
    "weekly_downloads": "30M+",
    "desc": "Express is the most widely-used Node.js web framework. It has had a relatively small number of direct CVEs given its age and popularity — most express-related vulnerabilities come through its dependencies like qs and path-to-regexp.",
    "cves": [
        ("CVE-2014-6393",  2014, "MEDIUM", False, True, "3.1.0",  "Cross-site scripting via crafted HTTP header"),
        ("CVE-2016-1000236",2016,"MEDIUM", False, True, "4.14.2", "Timing attack in cookie signature comparison"),
        ("CVE-2022-24999", 2022, "HIGH",   True,  True, "4.18.2", "Prototype pollution via qs dependency — CISA KEV"),
        ("CVE-2024-29041", 2024, "MEDIUM", False, True, "4.19.2", "Open redirect via response.redirect()"),
    ],
    "fix_snippet_before": '"express": "4.17.1"',
    "fix_snippet_after":  '"express": "4.19.2"',
    "faqs": [
        ("Does Express itself have many CVEs?", "Express has surprisingly few direct CVEs for a framework of its age and popularity — most express-related vulnerabilities come through transitive dependencies like qs (prototype pollution) and path-to-regexp (ReDoS). Keeping express updated pulls in safe versions of these dependencies."),
        ("What does CVE-2024-29041 mean for my app?", "It means response.redirect() with user-controlled URLs could send users to external sites. If you pass any user input to res.redirect(), validate the URL first. The fix in 4.19.2 adds stricter URL validation."),
        ("Is express 5.x stable?", "Express 5.x reached release candidate status in 2024. It includes security improvements and better promise handling. If you're starting a new project, 5.x is worth evaluating. For existing projects, 4.19.2 remains well-maintained."),
        ("How do I fix the qs prototype pollution coming through Express?", "Updating Express to 4.18.0 or later pulls in a safe version of qs. If you can't upgrade Express, add an npm override: {\"overrides\": {\"qs\": \"6.11.0\"}}.")
    ],
    "related": [
        {"url": "/fix/npm/qs", "title": "Fix qs CVE-2022-24999", "desc": "Prototype pollution via qs"},
        {"url": "/glossary/prototype-pollution", "title": "What is Prototype Pollution?", "desc": "Plain-English explanation"},
        {"url": "/fix/npm/express/audit", "title": "Express Security Audit", "desc": "Full Express security checklist"},
        {"url": "/npm", "title": "npm Security Overview", "desc": "All npm CVE guides"},
    ]
  },

  {
    "slug": "fix/npm/jsonwebtoken",
    "pkg": "jsonwebtoken", "eco": "npm", "eco_label": "npm",
    "safe_ver": "9.0.0",
    "install": "npm install",
    "weekly_downloads": "15M+",
    "desc": "jsonwebtoken is the most widely-used npm package for creating and verifying JSON Web Tokens. Authentication libraries are high-value targets — all known CVEs are serious and relate to algorithm confusion or improper verification.",
    "cves": [
        ("CVE-2015-9235",  2015, "CRITICAL",False, True, "4.2.2",  "Algorithm confusion — none algorithm accepted"),
        ("CVE-2022-23539", 2022, "MEDIUM",  False, True, "9.0.0",  "Insecure comparison when secret is a string"),
        ("CVE-2022-23540", 2022, "CRITICAL",True,  True, "9.0.0",  "Algorithm confusion — weak key accepted — CISA KEV"),
        ("CVE-2022-23541", 2022, "MEDIUM",  False, True, "9.0.0",  "Improper handling of multiple signatures"),
    ],
    "fix_snippet_before": '"jsonwebtoken": "8.5.1"',
    "fix_snippet_after":  '"jsonwebtoken": "9.0.0"',
    "faqs": [
        ("Why does jsonwebtoken have so many algorithm confusion CVEs?", "JWT algorithm confusion is a class of vulnerability that's been known since 2015. The 'none' algorithm issue (CVE-2015-9235) was the first — where passing alg: none in a token header could bypass signature verification. The 2022 batch were new variants. The fix in 9.0.0 explicitly requires you to specify which algorithms are acceptable."),
        ("What changed in jsonwebtoken 9.0.0?", "The verify() function now requires an explicit algorithms array. You can no longer omit it and have the library accept whatever algorithm the token claims. This is the single most important security change in the package's history."),
        ("How do I migrate to jsonwebtoken 9.0.0?", "Add algorithms explicitly to all verify() calls: jwt.verify(token, secret, { algorithms: ['HS256'] }). Never pass the algorithm from the token header itself — always use a hardcoded list you control."),
        ("Is CVE-2022-23540 being actively exploited?", "Yes — it's on the CISA KEV catalog. Algorithm confusion attacks against JWT implementations are actively used to bypass authentication in web applications. If you're on jsonwebtoken < 9.0.0, this is an urgent update.")
    ],
    "related": [
        {"url": "/kev/CVE-2022-23540", "title": "CVE-2022-23540 Detail", "desc": "CISA KEV — algorithm confusion"},
        {"url": "/fix/rust/jsonwebtoken", "title": "Fix Rust jsonwebtoken", "desc": "Same issue in Rust"},
        {"url": "/fix/ruby/jwt", "title": "Fix Ruby jwt gem", "desc": "JWT CVEs in Ruby"},
        {"url": "/npm", "title": "npm Security Overview", "desc": "All npm CVE guides"},
    ]
  },

  {
    "slug": "fix/npm/vm2",
    "pkg": "vm2", "eco": "npm", "eco_label": "npm",
    "safe_ver": "3.9.19",
    "install": "npm install",
    "weekly_downloads": "5M+",
    "desc": "vm2 is a popular Node.js sandbox library for executing untrusted code safely. It has had multiple critical sandbox escape vulnerabilities. The maintainers recommend migrating to isolated-vm for production use.",
    "cves": [
        ("CVE-2022-36067", 2022, "CRITICAL",False, True, "3.9.11", "Sandbox escape via Error.prepareStackTrace"),
        ("CVE-2023-29017", 2023, "CRITICAL",True,  True, "3.9.19", "Sandbox escape via Promise handler — CISA KEV"),
        ("CVE-2023-29199", 2023, "CRITICAL",False, True, "3.9.17", "Sandbox escape via exception sanitisation"),
        ("CVE-2023-30547", 2023, "CRITICAL",False, True, "3.9.19", "Sandbox escape via argument handling"),
    ],
    "fix_snippet_before": '"vm2": "3.9.15"',
    "fix_snippet_after":  '"vm2": "3.9.19"',
    "faqs": [
        ("Is vm2 safe to use for running untrusted code?", "The maintainers themselves say no — after the repeated sandbox escapes in 2023, they recommend migrating to isolated-vm, which uses V8 isolates for stronger isolation. vm2 3.9.19 patches the known escapes but the fundamental architecture has proven difficult to secure fully."),
        ("What's the difference between vm2 and Node.js's built-in vm module?", "Node's built-in vm module provides no security isolation — it's explicitly not a sandbox. vm2 was created to add security boundaries, but has had repeated escapes. isolated-vm and container-based solutions (Docker sandbox) provide stronger guarantees."),
        ("Why does vm2 keep getting sandbox escape CVEs?", "Sandboxing a dynamic language at the library level in the same process is fundamentally hard. Every CVE reveals a new JavaScript primitive that the sandbox didn't account for — Proxies, Promise handlers, Error stack traces. The attack surface is very large."),
        ("CVE-2023-29017 is CVSS 10.0 — should I stop using vm2 immediately?", "Yes — update to 3.9.19 immediately to patch the known CVEs, then plan a migration to isolated-vm or a process-level sandbox. Running vm2 < 3.9.19 in production with untrusted code input is a critical risk.")
    ],
    "related": [
        {"url": "/kev/CVE-2023-29017", "title": "CVE-2023-29017 Detail", "desc": "CISA KEV — CVSS 10.0"},
        {"url": "/glossary/supply-chain-attack", "title": "Supply Chain Attacks", "desc": "Why this class of CVE matters"},
        {"url": "/fix/npm/webpack", "title": "Fix webpack", "desc": "Another build tool CVE"},
        {"url": "/npm", "title": "npm Security Overview", "desc": "All npm CVE guides"},
    ]
  },

  # ── PyPI ───────────────────────────────────────────────────────────────────

  {
    "slug": "fix/pypi/django",
    "pkg": "Django", "eco": "pypi", "eco_label": "PyPI",
    "safe_ver": "4.2.13",
    "install": "pip install -r requirements.txt",
    "weekly_downloads": "15M+",
    "desc": "Django releases security patches regularly — usually every 4-8 weeks. The Django team has an excellent security disclosure process and clear upgrade paths. Most CVEs are ReDoS, XSS, or open redirect issues rather than critical RCE.",
    "cves": [
        ("CVE-2021-45115", 2021, "HIGH",   False, True, "3.2.11", "DoS via UserAttributeSimilarityValidator"),
        ("CVE-2021-45116", 2021, "MEDIUM", False, True, "3.2.11", "Information disclosure via dictsort template filter"),
        ("CVE-2022-28346", 2022, "CRITICAL",False,True, "3.2.13", "SQL injection via QuerySet.annotate, aggregate, extra"),
        ("CVE-2022-28347", 2022, "CRITICAL",False,True, "3.2.13", "SQL injection via QuerySet.explain"),
        ("CVE-2022-36359", 2022, "HIGH",   False, True, "3.2.15", "Open redirect in FileResponse"),
        ("CVE-2023-24580", 2023, "HIGH",   False, True, "4.1.7",  "DoS via multipart request parsing"),
        ("CVE-2023-31047", 2023, "CRITICAL",False,True, "4.2.1",  "Upload validation bypass via FileField"),
        ("CVE-2024-27351", 2024, "HIGH",   False, True, "4.2.13", "ReDoS in strip_tags HTML sanitizer"),
    ],
    "fix_snippet_before": "Django==3.2.0",
    "fix_snippet_after":  "Django==4.2.13",
    "faqs": [
        ("How often does Django release security patches?", "Roughly every 4-8 weeks. The Django team maintains a security mailing list (django-security-announce) and publishes advisories at docs.djangoproject.com/en/dev/releases/security. Subscribe to stay informed."),
        ("What are the most serious Django CVEs?", "The 2022 SQL injection CVEs (CVE-2022-28346 and CVE-2022-28347) were the most severe — CRITICAL severity, affecting QuerySet methods used in almost all Django apps. Any app on Django < 3.2.13 that uses annotate, aggregate, extra, or explain with user input is vulnerable."),
        ("Is Django 3.2 still receiving security patches?", "Django 3.2 is end-of-life as of April 2024. You should be on Django 4.2 LTS (supported until April 2026) or Django 5.0+. Django 3.2 no longer receives security fixes — any new CVE discovered won't be patched."),
        ("How do I check my Django version?", "Run python -m django --version. Or paste your requirements.txt into PackageFix — it will show your installed Django version and flag any unpatched CVEs.")
    ],
    "related": [
        {"url": "/fix/pypi/django", "title": "Django Latest CVE Fix", "desc": "Step-by-step fix guide"},
        {"url": "/fix/pypi/werkzeug", "title": "Fix Werkzeug", "desc": "Related Python web framework CVE"},
        {"url": "/fix/pypi/sqlalchemy", "title": "Fix SQLAlchemy", "desc": "SQL injection CVE"},
        {"url": "/python", "title": "PyPI Security Overview", "desc": "All Python CVE guides"},
    ]
  },

  {
    "slug": "fix/pypi/requests",
    "pkg": "requests", "eco": "pypi", "eco_label": "PyPI",
    "safe_ver": "2.31.0",
    "install": "pip install -r requirements.txt",
    "weekly_downloads": "300M+",
    "desc": "requests is the most downloaded Python package — over 300 million weekly installs. Despite its massive usage, it has had relatively few CVEs, mostly related to credential exposure on redirect. Keep it at 2.31.0 or later.",
    "cves": [
        ("CVE-2014-1829", 2014, "MEDIUM", False, True, "2.3.0",  "Proxy-Authorization header sent to redirected host"),
        ("CVE-2018-18074", 2018,"MEDIUM", False, True, "2.20.0", "HTTP header injection via craft Redirect URL"),
        ("CVE-2023-32681", 2023, "MEDIUM", False, True, "2.31.0", "Proxy credential leak via HTTPS→HTTP redirect"),
    ],
    "fix_snippet_before": "requests==2.25.1",
    "fix_snippet_after":  "requests==2.31.0",
    "faqs": [
        ("Why does requests have so few CVEs despite 300M weekly downloads?", "requests does one thing and does it well — it's a thin wrapper around urllib3. The simplicity reduces attack surface. Most HTTP-related CVEs in Python apps come from urllib3 or the application's own URL handling, not requests itself."),
        ("Does CVE-2023-32681 affect me if I don't use a proxy?", "No — this CVE only affects apps using proxy authentication. If you don't set proxies in requests, your exposure is zero. Still worth updating since 2.31.0 has no breaking changes."),
        ("What's the difference between requests CVEs and urllib3 CVEs?", "requests uses urllib3 internally. CVEs in urllib3 affect requests transitively. CVE-2023-45803 (urllib3 credential leak) and CVE-2021-33503 (urllib3 ReDoS) are worth checking separately. PackageFix scans both when you paste your requirements.txt."),
        ("Should I switch from requests to httpx?", "httpx is a modern alternative with async support and HTTP/2. It doesn't have requests' CVE history issues, but it's a larger migration. For new projects, httpx is worth evaluating. For existing projects, requests 2.31.0 is fine.")
    ],
    "related": [
        {"url": "/fix/pypi/urllib3", "title": "Fix urllib3", "desc": "requests' core dependency"},
        {"url": "/fix/pypi/httpx", "title": "Fix httpx", "desc": "Modern requests alternative"},
        {"url": "/python", "title": "PyPI Security Overview", "desc": "All Python CVE guides"},
        {"url": "/glossary/dependency-scanning", "title": "Dependency Scanning", "desc": "How to stay on top of CVEs"},
    ]
  },

  {
    "slug": "fix/pypi/cryptography",
    "pkg": "cryptography", "eco": "pypi", "eco_label": "PyPI",
    "safe_ver": "42.0.8",
    "install": "pip install -r requirements.txt",
    "weekly_downloads": "100M+",
    "desc": "The cryptography package is the foundation of Python TLS and PKI — used by requests, paramiko, pyOpenSSL, and hundreds of other packages. CVEs here are always serious because of the sensitive nature of cryptographic operations.",
    "cves": [
        ("CVE-2020-25659", 2020, "MEDIUM", False, True, "3.2.1",  "Bleichenbacher timing oracle in RSA decryption"),
        ("CVE-2021-3712",  2021, "HIGH",   False, True, "3.3.2",  "Buffer over-read in ASN.1 string handling (via OpenSSL)"),
        ("CVE-2023-0286",  2023, "CRITICAL",True, True, "39.0.1", "X.400 type confusion in OpenSSL — CISA KEV"),
        ("CVE-2023-23931", 2023, "MEDIUM", False, True, "39.0.1", "Bleichenbacher oracle via mutable Cipher objects"),
        ("CVE-2023-49083", 2023, "CRITICAL",False,True, "41.0.6", "NULL pointer dereference in PKCS12 parsing"),
    ],
    "fix_snippet_before": "cryptography==36.0.0",
    "fix_snippet_after":  "cryptography==42.0.8",
    "faqs": [
        ("Why does cryptography have CVEs that reference OpenSSL?", "The cryptography package wraps OpenSSL (the C library) via cffi. When OpenSSL has a CVE, the cryptography package inherits it — updating cryptography pulls in a patched OpenSSL build. This is why cryptography version updates are often described as 'updating OpenSSL bindings'."),
        ("Is CVE-2023-0286 serious for most applications?", "CVE-2023-0286 (X.400 type confusion) is CRITICAL and on CISA KEV, but it specifically affects applications that process X.400 certificates from untrusted sources. Most web apps don't encounter X.400. Still upgrade immediately — the CISA KEV designation means it's being exploited."),
        ("How often should I update the cryptography package?", "Every release. The cryptography team has a security-first philosophy and releases frequently. Given that this package underlies TLS for most Python applications, staying current is worth the maintenance overhead."),
        ("What happens if I don't update cryptography?", "You're inheriting OpenSSL vulnerabilities. In production, this means your TLS connections may be vulnerable to attacks depending on which CVEs are unpatched. For apps handling sensitive data, this is unacceptable technical debt.")
    ],
    "related": [
        {"url": "/fix/pypi/pyopenssl", "title": "Fix pyOpenSSL", "desc": "Related OpenSSL package"},
        {"url": "/fix/pypi/paramiko", "title": "Fix paramiko", "desc": "SSH library using cryptography"},
        {"url": "/python", "title": "PyPI Security Overview", "desc": "All Python CVE guides"},
        {"url": "/cisa-kev", "title": "CISA KEV Packages", "desc": "Actively exploited right now"},
    ]
  },

  # ── Ruby ───────────────────────────────────────────────────────────────────

  {
    "slug": "fix/ruby/rails",
    "pkg": "Rails", "eco": "ruby", "eco_label": "Ruby",
    "safe_ver": "7.1.3",
    "install": "bundle install",
    "weekly_downloads": "3M+",
    "desc": "Rails has a mature, well-run security process. CVEs are disclosed on the Rails blog and through rubyonrails-security mailing list. Most CVEs are XSS, CSRF, or open redirect issues — serious but manageable with prompt updates.",
    "cves": [
        ("CVE-2022-21831", 2022, "CRITICAL",False,True, "6.1.4.7","Code injection via YAML serialisation in Action Text"),
        ("CVE-2022-32224", 2022, "CRITICAL",False,True, "7.0.3.1","RCE via YAML deserialization in PostgreSQL adapter"),
        ("CVE-2022-44566", 2022, "HIGH",    False,True, "7.0.4",  "DoS via excessive string allocation in Rack body parsing"),
        ("CVE-2023-28362", 2023, "HIGH",    False,True, "7.0.5",  "XSS via redirect URLs with crafted query params"),
        ("CVE-2024-26144", 2024, "HIGH",    False,True, "7.1.3",  "CSRF token leak in session response headers"),
    ],
    "fix_snippet_before": "gem 'rails', '6.0.0'",
    "fix_snippet_after":  "gem 'rails', '7.1.3'",
    "faqs": [
        ("What are the most serious Rails CVEs?", "The YAML deserialization CVEs (CVE-2022-21831 and CVE-2022-32224) are the most severe — both CRITICAL and allowing remote code execution. These affect specific configurations (YAML serialization enabled, PostgreSQL adapter with certain options) but should be treated as urgent if your configuration matches."),
        ("How do I stay informed about Rails security releases?", "Subscribe to rubyonrails-security@googlegroups.com and follow the Rails blog at rubyonrails.org/blog. New security releases are also announced on Rails' GitHub releases page."),
        ("Is Rails 6.x still receiving security patches?", "Rails 6.1 reached end of life in June 2024. Rails 7.0 is maintained through September 2025. Rails 7.1 is the current stable release with the longest support window. If you're on Rails 6.x, plan your upgrade now."),
        ("How long does a Rails upgrade typically take?", "Rails has good upgrade guides and tries to deprecate features before removing them. A 6.1 to 7.1 upgrade typically takes 1-5 days for a medium-sized app, mostly updating deprecated API calls. The security benefits make it worthwhile.")
    ],
    "related": [
        {"url": "/fix/ruby/nokogiri", "title": "Fix Nokogiri", "desc": "Common Rails transitive CVE"},
        {"url": "/fix/ruby/rack", "title": "Fix Rack", "desc": "Rails' underlying framework"},
        {"url": "/fix/ruby/activerecord", "title": "Fix activerecord", "desc": "SQL injection CVE"},
        {"url": "/ruby", "title": "Ruby Security Overview", "desc": "All Ruby CVE guides"},
    ]
  },

  {
    "slug": "fix/ruby/nokogiri",
    "pkg": "Nokogiri", "eco": "ruby", "eco_label": "Ruby",
    "safe_ver": "1.16.5",
    "install": "bundle install",
    "weekly_downloads": "8M+",
    "desc": "Nokogiri is the most-used Ruby XML/HTML parser. It wraps libxml2 and libxslt, which means its CVE history often reflects upstream C library vulnerabilities. Updates are frequent and important, especially for apps parsing untrusted HTML.",
    "cves": [
        ("CVE-2019-5477",  2019, "CRITICAL",False,True, "1.10.4", "Command injection via Nokogiri.parse on crafted HTML"),
        ("CVE-2020-26247", 2020, "MEDIUM",  False,True, "1.11.0", "XXE in Nokogiri::XML::Schema when parsing schema"),
        ("CVE-2021-3518",  2021, "HIGH",    False,True, "1.11.4", "Use after free in libxml2 XInclude processing"),
        ("CVE-2022-23437", 2022, "HIGH",    False,True, "1.13.2", "DoS in XML Schema validation via libxml2"),
        ("CVE-2022-24836", 2022, "CRITICAL",False,True, "1.13.4", "ReDoS in CSS selector parsing — CVSS 9.8"),
        ("CVE-2023-36617", 2023, "HIGH",    False,True, "1.15.4", "ReDoS via specially crafted CSS selector"),
    ],
    "fix_snippet_before": "gem 'nokogiri', '1.11.0'",
    "fix_snippet_after":  "gem 'nokogiri', '1.16.5'",
    "faqs": [
        ("Why does Nokogiri have so many CVEs?", "Nokogiri wraps libxml2 and libxslt, two C libraries with long CVE histories. When these upstream libraries have vulnerabilities, Nokogiri inherits them. The Nokogiri team ships vendored versions of these libraries and keeps them patched, but it means frequent updates are necessary."),
        ("Does Nokogiri's CVE history affect Rails apps?", "Yes — rails-html-sanitizer (used by ActionView for HTML sanitization) depends on Nokogiri. ReDoS in Nokogiri's CSS selector parsing can be triggered by crafted user input passed to the sanitizer. Keep Nokogiri updated in all Rails apps."),
        ("What's the difference between Nokogiri's system libxml2 and vendored libxml2?", "By default, Nokogiri ships with a vendored (bundled) version of libxml2, which the team keeps patched. If you build Nokogiri with --use-system-libraries, you use the system libxml2, which may be older and unpatched. The vendored version is safer."),
        ("How do I check which Nokogiri version a gem requires?", "Run bundle exec gem dependency nokogiri in your project directory. Or paste your Gemfile.lock into PackageFix — it shows every resolved Nokogiri version including transitive references.")
    ],
    "related": [
        {"url": "/kev/CVE-2022-24836", "title": "CVE-2022-24836 Detail", "desc": "ReDoS — CVSS 9.8"},
        {"url": "/fix/ruby/rails", "title": "Fix Rails", "desc": "Main Nokogiri consumer"},
        {"url": "/ruby", "title": "Ruby Security Overview", "desc": "All Ruby CVE guides"},
        {"url": "/glossary/open-source-vulnerability", "title": "Open Source Vulnerabilities", "desc": "How upstream CVEs spread"},
    ]
  },

  # ── Java ───────────────────────────────────────────────────────────────────

  {
    "slug": "fix/java/log4j",
    "pkg": "Apache Log4j", "eco": "java", "eco_label": "Java/Maven",
    "safe_ver": "2.23.1",
    "install": "mvn dependency:resolve",
    "weekly_downloads": "Millions",
    "desc": "Log4j is Apache's Java logging library used by virtually every Java application. Log4Shell (CVE-2021-44228) was the most severe Java vulnerability ever discovered. The fix process required multiple patches as bypasses were discovered.",
    "cves": [
        ("CVE-2019-17571", 2019, "CRITICAL",False,True, "2.0-beta9","Deserialization of untrusted data via SocketServer"),
        ("CVE-2021-44228", 2021, "CRITICAL",True, True, "2.15.0",  "Log4Shell — RCE via JNDI lookup in log message — CISA KEV"),
        ("CVE-2021-45046", 2021, "CRITICAL",True, True, "2.16.0",  "Log4Shell bypass — incomplete fix in 2.15.0 — CISA KEV"),
        ("CVE-2021-45105", 2021, "HIGH",    False,True, "2.17.0",  "DoS via crafted string causing infinite recursion"),
        ("CVE-2021-44832", 2021, "MEDIUM",  False,True, "2.17.1",  "RCE via JDBC Appender with attacker-controlled config"),
    ],
    "fix_snippet_before": "<log4j.version>2.14.1</log4j.version>",
    "fix_snippet_after":  "<log4j.version>2.23.1</log4j.version>",
    "faqs": [
        ("Why are there so many Log4j CVEs all at once in December 2021?", "Log4Shell (CVE-2021-44228) was disclosed on December 9, 2021. The initial patch (2.15.0) was incomplete — researchers immediately found bypass techniques, leading to CVE-2021-45046. Each bypass required another patch: 2.16.0, then 2.17.0 for the DoS, then 2.17.1 for a JDBC appender edge case. The final fully-patched version addressing all known bypasses is 2.17.1+."),
        ("Is my app vulnerable to Log4Shell if I use Spring Boot?", "Check your Spring Boot version. Spring Boot 2.5.8+ and 2.6.2+ upgraded Log4j to 2.17.1. Earlier versions bundle vulnerable Log4j. Run mvn dependency:tree | grep log4j to see your resolved version, or paste your pom.xml into PackageFix."),
        ("Is Log4Shell still being exploited in 2026?", "Yes — CISA KEV confirms ongoing exploitation. Unpatched Log4j instances are continuously scanned by automated attack tools. The vulnerability is so well-known that any unpatched system is quickly found and attacked."),
        ("What if I can't upgrade Log4j immediately?", "Temporary mitigation: set the JVM argument -Dlog4j2.formatMsgNoLookups=true. This disables the JNDI lookup that enables Log4Shell. This is a workaround only — upgrade to 2.17.1+ as soon as possible.")
    ],
    "related": [
        {"url": "/kev/CVE-2021-44228", "title": "CVE-2021-44228 — Log4Shell", "desc": "CVSS 10.0 — full detail"},
        {"url": "/fix/java/spring-core", "title": "Fix Spring Framework", "desc": "Spring4Shell CVE"},
        {"url": "/fix/java/commons-text", "title": "Fix Commons Text", "desc": "Text4Shell CVE"},
        {"url": "/java", "title": "Java Security Overview", "desc": "All Java CVE guides"},
    ]
  },

  {
    "slug": "fix/java/spring-core",
    "pkg": "Spring Framework", "eco": "java", "eco_label": "Java/Maven",
    "safe_ver": "6.1.6",
    "install": "mvn dependency:resolve",
    "weekly_downloads": "Millions",
    "desc": "Spring Framework is the most widely-used Java application framework. It releases security patches frequently. The most severe CVE in its history is Spring4Shell (CVE-2022-22965), which allowed unauthenticated remote code execution.",
    "cves": [
        ("CVE-2018-1270",  2018, "CRITICAL",False,True, "4.3.16", "RCE via STOMP over WebSocket messaging"),
        ("CVE-2018-1275",  2018, "CRITICAL",False,True, "5.0.5",  "RCE via Spring Data Commons binding"),
        ("CVE-2021-22096", 2021, "MEDIUM",  False,True, "5.3.12", "Log injection via multipart request parsing"),
        ("CVE-2022-22965", 2022, "CRITICAL",True, True, "5.3.18", "Spring4Shell — RCE via data binding on Java 9+ — CISA KEV"),
        ("CVE-2022-22968", 2022, "MEDIUM",  False,True, "5.3.18", "Input pattern bypass in DataBinder"),
        ("CVE-2023-20860", 2023, "CRITICAL",False,True, "6.0.7",  "Security bypass via wildcard pattern matching in Spring Security"),
        ("CVE-2024-22243", 2024, "MEDIUM",  False,True, "6.1.3",  "Open redirect via forwarded URL patterns"),
    ],
    "fix_snippet_before": "<spring.version>5.3.18</spring.version>",
    "fix_snippet_after":  "<spring.version>6.1.6</spring.version>",
    "faqs": [
        ("What is Spring4Shell and how is it different from Log4Shell?", "Both are critical Java RCE vulnerabilities discovered around the same time (early 2022 vs late 2021). Log4Shell is in the logging library — exploited via log messages. Spring4Shell is in the web framework — exploited via HTTP request parameter binding with malicious class paths. Different attack vectors, similar severity."),
        ("Do I need Java 9+ to be vulnerable to Spring4Shell?", "Yes — CVE-2022-22965 specifically requires Java 9+ and deployment on Apache Tomcat (not embedded Tomcat). Spring Boot with embedded Tomcat is not affected in most configurations. Check your deployment setup before assuming you're safe."),
        ("Is Spring Framework 5.x still receiving security patches?", "Spring 5.3.x is maintained until December 2024. Spring 6.x is the current generation. If you're on Spring 5.x, you should be planning your migration to Spring 6.x (which requires Java 17+)."),
        ("How do I check my Spring version in a Maven project?", "Run mvn dependency:tree | grep spring-core to see the resolved version. Or paste your pom.xml into PackageFix — it resolves property variables like ${spring.version} and checks transitive Spring dependencies.")
    ],
    "related": [
        {"url": "/kev/CVE-2022-22965", "title": "CVE-2022-22965 — Spring4Shell", "desc": "Full CVE detail page"},
        {"url": "/fix/java/log4j", "title": "Fix Log4j", "desc": "Log4Shell CVE history"},
        {"url": "/fix/java/snakeyaml", "title": "Fix SnakeYAML", "desc": "Spring Boot transitive CVE"},
        {"url": "/java", "title": "Java Security Overview", "desc": "All Java CVE guides"},
    ]
  },

]

# ══════════════════════════════════════════════════════════════════════════════
# PAGE GENERATOR
# ══════════════════════════════════════════════════════════════════════════════

def generate_history_page(data):
    slug = data["slug"]
    pkg = data["pkg"]
    eco = data["eco"]
    eco_label = data["eco_label"]
    safe_ver = data["safe_ver"]
    install = data["install"]
    weekly = data["weekly_downloads"]
    desc = data["desc"]
    cves = data["cves"]
    before = data["fix_snippet_before"]
    after = data["fix_snippet_after"]
    faqs = data["faqs"]
    related = data["related"]

    path = f"/{slug}"
    total = len(cves)
    critical = sum(1 for c in cves if c[2] == "CRITICAL")
    kev_count = sum(1 for c in cves if c[3])
    latest_cve = max(cves, key=lambda c: c[1])

    history_table = cve_history_table(cves)

    kev_note = ""
    if kev_count:
        kev_note = f'<p style="margin:8px 0 0;font-size:11px;color:var(--red)">🔴 {kev_count} CVE{"s" if kev_count > 1 else ""} on CISA KEV — actively exploited in real attacks</p>'

    body = f"""
<h1>All {pkg} CVEs — Complete Vulnerability History</h1>
<p class="lead">{desc}</p>

<div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:24px">
  <span class="badge badge-purple">{eco_label}</span>
  <span class="badge badge-muted">{weekly} weekly downloads</span>
  <span class="badge badge-muted">{total} CVEs total</span>
  {'<span class="badge badge-red">' + str(critical) + ' CRITICAL</span>' if critical else ''}
  {'<span class="badge badge-red">🔴 CISA KEV</span>' if kev_count else ''}
</div>

<h2>CVE history — all {total} known vulnerabilities</h2>
{kev_note}
{history_table}

<h2>Current safe version</h2>
<div class="fix-box">
  <div class="label">✓ Update to {safe_ver}</div>
  <p style="margin:0 0 12px">The latest safe version addresses all {total} known CVEs listed above.</p>
</div>

<h2>Before and after</h2>
<p style="color:var(--muted);font-size:11px;margin-bottom:4px">Vulnerable:</p>
<pre>{before}</pre>
<p style="color:var(--muted);font-size:11px;margin-bottom:4px">Fixed:</p>
<pre>{after}</pre>
<p>Then run: <code>{install}</code></p>

{cta()}
{faq_html(faqs)}
{related_html(related)}
"""

    schemas = [
        {
            "@type": "ItemList",
            "name": f"All {pkg} CVEs",
            "description": f"Complete CVE history for {pkg} ({eco_label}) — {total} known vulnerabilities",
            "numberOfItems": total,
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": i + 1,
                    "name": c[0],
                    "url": f"https://osv.dev/vulnerability/{c[0]}"
                }
                for i, c in enumerate(cves)
            ]
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "PackageFix", "item": BASE_URL},
                {"@type": "ListItem", "position": 2, "name": "Fix Guides", "item": BASE_URL + "/fix"},
                {"@type": "ListItem", "position": 3, "name": eco_label, "item": BASE_URL + f"/{eco}"},
                {"@type": "ListItem", "position": 4, "name": pkg, "item": BASE_URL + path}
            ]
        },
        {
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in faqs
            ]
        }
    ]

    eco_label_cap = eco_label
    title = f"All {pkg} CVEs — Complete {eco_label_cap} Vulnerability History | PackageFix"
    meta_desc = (
        f"{pkg} has {total} known CVEs. "
        f"{'CISA KEV — actively exploited. ' if kev_count else ''}"
        f"Latest CVE: {latest_cve[0]} ({latest_cve[2]}). "
        f"Safe version: {safe_ver}. Full history with fix guide."
    )

    return shell(
        title, meta_desc, path,
        [("PackageFix", "/"), ("Fix Guides", "/fix"), (eco_label, f"/{eco}"), (pkg, None)],
        body, schemas
    )

# ══════════════════════════════════════════════════════════════════════════════
# WRITE ALL PAGES
# ══════════════════════════════════════════════════════════════════════════════

print("\n📋 Generating CVE history pages (overwriting existing)...")
for data in PACKAGE_HISTORIES:
    write(data["slug"], generate_history_page(data))

# ── Update config files ────────────────────────────────────────────────────────
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
added = 0
for r in rewrites:
    if r["source"] not in existing_sources:
        existing.append(r)
        existing_sources.add(r["source"])
        added += 1

vercel_config["rewrites"] = existing
with open("vercel.json", "w") as f:
    json.dump(vercel_config, f, indent=2)
print(f"  ✓ vercel.json — {len(existing)} total rewrites ({added} new)")

print("\n🤖 Updating llm.txt...")
with open("llm.txt", "a") as f:
    f.write("\n## CVE History Pages (enriched)\n")
    for p in all_paths:
        f.write(f"{BASE_URL}{p}\n")
print("  ✓ llm.txt updated")

print(f"\n✅ Done — {len(all_paths)} pages enriched with CVE history tables")
for p in all_paths:
    print(f"   {p}")

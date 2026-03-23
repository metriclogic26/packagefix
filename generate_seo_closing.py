#!/usr/bin/env python3
"""
PackageFix — Closing Items
1. /compare index page
2. /glossary/reachability-analysis + /glossary/remediation
3. CVE history tables for remaining ~100 packages
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
h3{font-size:13px;font-weight:600;margin:20px 0 8px}
p{color:var(--muted);margin-bottom:12px;font-size:12px;line-height:1.7}
.lead{color:var(--text);font-size:13px;margin-bottom:24px;line-height:1.7}
.definition-box{background:var(--surface);border:1px solid var(--purple);border-left:4px solid var(--purple);border-radius:8px;padding:20px 24px;margin:0 0 32px}
.definition-box .def-label{font-size:10px;font-weight:700;color:var(--purple);text-transform:uppercase;letter-spacing:.1em;margin-bottom:8px}
.definition-box p{color:var(--text);font-size:13px;line-height:1.7;margin:0}
.fix-box{background:rgba(34,197,94,.08);border:1px solid rgba(34,197,94,.3);border-left:3px solid var(--green);border-radius:8px;padding:16px 20px;margin:20px 0}
.fix-box .label{font-size:10px;font-weight:700;color:var(--green);text-transform:uppercase;letter-spacing:.1em;margin-bottom:8px}
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
.cve-history{width:100%;border-collapse:collapse;margin:16px 0;font-size:12px}
.cve-history th{text-align:left;padding:10px 12px;border-bottom:2px solid var(--border);color:var(--muted);font-weight:600;font-size:10px;text-transform:uppercase;letter-spacing:.08em}
.cve-history td{padding:10px 12px;border-bottom:1px solid var(--border);vertical-align:top}
.cve-history tr:last-child td{border-bottom:none}
.cve-history tr:hover td{background:var(--surface2)}
.compare-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px;margin-top:16px}
.compare-card{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:18px}
.compare-card h3{font-size:12px;font-weight:600;margin:0 0 6px}
.compare-card h3 a{color:var(--text)}
.compare-card p{font-size:11px;color:var(--muted);margin:0}
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
@media(max-width:640px){.nav-links{display:none}.related-grid{grid-template-columns:1fr}.compare-grid{grid-template-columns:1fr}}
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
  <p>Paste your manifest — see your exact versions against the full CVE history.</p>
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

def sev_badge(sev):
    cls = "badge-red" if sev == "CRITICAL" else "badge-orange" if sev == "HIGH" else "badge-purple" if sev == "MEDIUM" else "badge-muted"
    return f'<span class="badge {cls}">{sev}</span>'

def cve_table(cves):
    rows = ""
    for cve_id, year, sev, is_kev, is_fixed, safe_ver, desc in cves:
        kev = '<span style="color:var(--red);margin-right:4px" title="CISA KEV">🔴</span>' if is_kev else ""
        fixed = f'<span class="badge badge-green">Fixed {safe_ver}</span>' if is_fixed else '<span class="badge badge-orange">No fix</span>'
        rows += f"<tr><td><a href='https://osv.dev/vulnerability/{cve_id}' target='_blank' rel='noopener'>{cve_id}</a></td><td>{year}</td><td>{kev}{sev_badge(sev)}</td><td style='color:var(--muted)'>{desc}</td><td>{fixed}</td></tr>"
    return f"""<table class="cve-history">
<thead><tr><th>CVE</th><th>Year</th><th>Severity</th><th>Description</th><th>Fix</th></tr></thead>
<tbody>{rows}</tbody></table>"""

all_paths = []

def write(slug, html):
    path = os.path.join("seo", slug, "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    all_paths.append("/" + slug)
    print(f"  ✓ /{slug}")

# ══════════════════════════════════════════════════════════════════════════════
# 1. /compare INDEX PAGE
# ══════════════════════════════════════════════════════════════════════════════

COMPARISONS = [
    ("/compare/npm-vs-pypi",             "npm vs PyPI Security",           "Compare npm and PyPI dependency scanning"),
    ("/compare/snyk-vs-dependabot",      "Snyk vs Dependabot",             "Both require GitHub — PackageFix doesn't"),
    ("/compare/npm-audit-vs-pip-audit",  "npm audit vs pip-audit",         "CLI tools vs browser alternative"),
    ("/compare/cargo-audit-vs-bundle-audit","cargo-audit vs bundle-audit", "Rust and Ruby CLI scanners"),
    ("/compare/owasp-vs-snyk",           "OWASP Dep-Check vs Snyk",        "Enterprise SCA tools compared"),
    ("/compare/pip-audit-vs-safety",     "pip-audit vs safety",            "Python security tools"),
    ("/compare/govulncheck-vs-nancy",    "govulncheck vs nancy",           "Go module security scanning"),
    ("/compare/bundler-audit-vs-gemnasium","bundle-audit vs Gemnasium",    "Gemnasium shut down in 2018"),
]

compare_cards = "".join(
    f'<div class="compare-card"><h3><a href="{url}">{title}</a></h3><p>{desc}</p></div>'
    for url, title, desc in COMPARISONS
)

compare_body = f"""
<h1>Dependency Security Tool Comparisons</h1>
<p class="lead">How PackageFix compares to every major dependency scanner — CLI tools, GitHub bots, enterprise SCA platforms, and tools that have since shut down.</p>

<div class="compare-grid">
{compare_cards}
</div>

<div style="margin:48px 0">
  <h2>The short version</h2>
  <p>Most dependency security tools fall into one of three categories. CLI tools (npm audit, pip-audit, cargo-audit) run in your terminal and produce reports. GitHub bots (Dependabot, Renovate) open pull requests automatically. Enterprise platforms (Snyk, Mend, Black Duck) require accounts, integrations, and usually money.</p>
  <p>PackageFix is none of those — it's a browser tool. Paste your manifest, get a fixed version back in seconds. No install, no account, no GitHub connection. It fills the gap between "run a CLI command" and "set up an enterprise SCA pipeline."</p>
</div>

{cta()}

{related_html([
    {"url": "/vs/snyk-advisor",      "title": "vs Snyk Advisor",   "desc": "Shut down January 2026"},
    {"url": "/vs/dependabot",        "title": "vs Dependabot",     "desc": "No GitHub required"},
    {"url": "/vs/npm-audit",         "title": "vs npm audit",      "desc": "Browser vs CLI"},
    {"url": "/alternatives",         "title": "All Alternatives",  "desc": "Full 16-tool table"},
])}
"""

write("compare", shell(
    "Dependency Security Tool Comparisons | PackageFix",
    "How PackageFix compares to npm audit, pip-audit, Snyk, Dependabot, OWASP Dependency-Check, cargo-audit, bundle-audit, and more.",
    "/compare",
    [("PackageFix", "/"), ("Comparisons", None)],
    compare_body,
    [
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "PackageFix", "item": BASE_URL},
            {"@type": "ListItem", "position": 2, "name": "Comparisons", "item": BASE_URL + "/compare"}
        ]},
        {"@type": "ItemList", "name": "Dependency Security Tool Comparisons",
         "itemListElement": [
             {"@type": "ListItem", "position": i+1, "name": t, "url": BASE_URL + u}
             for i, (u, t, _) in enumerate(COMPARISONS)
         ]}
    ]
))


# ══════════════════════════════════════════════════════════════════════════════
# 2. TWO NEW GLOSSARY TERMS
# ══════════════════════════════════════════════════════════════════════════════

def glossary_page(slug, term, badge, one_line, definition, body_extra, faqs, related_pages):
    path = f"/glossary/{slug}"
    body = f"""
<h1>{term}</h1>
<div style="margin-bottom:24px"><span class="badge badge-purple">{badge}</span></div>
<div class="definition-box">
  <div class="def-label">Definition</div>
  <p class="lead">{definition}</p>
</div>
{body_extra}
{cta()}
{faq_html(faqs)}
{related_html(related_pages)}
"""
    schemas = [
        {"@type": "DefinedTerm", "name": term, "description": definition,
         "url": BASE_URL + path,
         "inDefinedTermSet": {"@type": "DefinedTermSet",
             "name": "PackageFix Dependency Security Glossary",
             "url": BASE_URL + "/glossary"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "PackageFix", "item": BASE_URL},
            {"@type": "ListItem", "position": 2, "name": "Glossary", "item": BASE_URL + "/glossary"},
            {"@type": "ListItem", "position": 3, "name": term, "item": BASE_URL + path}
        ]},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faqs
        ]}
    ]
    return shell(
        f"{term} — Definition | PackageFix Glossary",
        f"{one_line} {definition[:120]}...",
        path,
        [("PackageFix", "/"), ("Glossary", "/glossary"), (term, None)],
        body, schemas
    )

print("\n📖 Generating 2 new glossary terms...")

write("glossary/reachability-analysis", glossary_page(
    slug="reachability-analysis",
    term="Reachability Analysis",
    badge="SCA · DevSecOps",
    one_line="Checking whether a vulnerability in a dependency can actually be triggered by your specific code.",
    definition="Reachability analysis is a technique for determining whether a vulnerable code path in a dependency is actually reachable from your application's code. A library might have a Critical CVE, but if your application never calls the vulnerable function, you're not actually exposed. Reachability analysis filters out those false positives.",
    body_extra="""
<h2>Why it matters in practice</h2>
<p>Most dependency scanners flag every CVE in every package you install. A typical scan on a medium-sized application can return 50-200 vulnerabilities. The vast majority are in code paths your application never touches. Reachability analysis cuts through the noise by tracing your actual call graph.</p>
<p>For example: a popular HTTP library might have a CVE in its WebSocket implementation. If your application uses the library only for plain HTTP requests and never uses WebSockets, the CVE is technically present but not reachable. A reachability-aware scanner won't flag it — or will flag it with lower priority.</p>

<h2>How it works</h2>
<p>Reachability analysis tools construct a call graph — a map of which functions call which other functions across your codebase and its dependencies. They then check whether any path from your application's entry points reaches the vulnerable function identified in the CVE.</p>
<p>This requires static analysis of your actual source code, not just your manifest file. It's why reachability analysis is typically a feature of enterprise SCA platforms (Snyk Code, Endor Labs, Aikido) rather than quick browser-based tools.</p>

<h2>The trade-off</h2>
<p>Reachability analysis reduces false positives significantly — some studies show it eliminates 70-80% of flagged CVEs as unreachable. The downside is it requires more setup: you need to give the tool access to your source code, and analysis takes longer than a simple manifest scan.</p>
<div class="fix-box">
  <div class="label">Practical advice</div>
  <p style="margin:0">For most teams: start with manifest scanning (PackageFix, npm audit, OSV Scanner) to fix the clear issues. Add reachability analysis when alert fatigue becomes a problem — when you're drowning in Medium CVEs that are hard to prioritize.</p>
</div>""",
    faqs=[
        ("Does PackageFix do reachability analysis?", "No — PackageFix is a manifest-based scanner. It checks your package versions against OSV and CISA KEV but doesn't analyse your source code call graph. For reachability analysis, look at Endor Labs, Snyk Code, or Aikido's reachability features."),
        ("Is a CVE less urgent if the vulnerable code is unreachable?", "Generally yes — but there are caveats. Code paths can change as your application evolves. A function that's unreachable today might be reachable after a refactor. Reachability is a prioritization tool, not a reason to never fix a CVE."),
        ("Which tools offer reachability analysis?", "Endor Labs, Snyk Code (paid), Aikido, and CodeQL (GitHub Advanced Security) all offer varying degrees of reachability analysis. They require source code access and more setup than manifest-based tools."),
        ("What is the difference between reachability and exploitability?", "Reachability means the vulnerable code path can be called by your application. Exploitability means an attacker can actually trigger it with crafted input. A vulnerability can be reachable but not exploitable if there's no way to control the inputs that reach the vulnerable function. CISA KEV represents confirmed exploitability in real environments.")
    ],
    related_pages=[
        {"url": "/glossary/dependency-scanning", "title": "Dependency Scanning", "desc": "The broader category"},
        {"url": "/glossary/software-composition-analysis", "title": "SCA", "desc": "What reachability extends"},
        {"url": "/glossary/cvss", "title": "CVSS Score", "desc": "How severity is rated"},
        {"url": "/cisa-kev", "title": "CISA KEV", "desc": "Confirmed exploited CVEs"},
    ]
))

write("glossary/remediation", glossary_page(
    slug="remediation",
    term="Remediation",
    badge="Security · DevSecOps",
    one_line="The process of fixing a security vulnerability — updating a package, applying a patch, or changing configuration to remove the risk.",
    definition="Remediation in dependency security means taking action to eliminate or reduce a known vulnerability. The most common form is updating a vulnerable package to a version that contains the fix. Other forms include applying a vendor patch, using an npm override to force a safe transitive version, or — as a last resort — removing the vulnerable dependency entirely.",
    body_extra="""
<h2>Types of remediation</h2>

<h3>Direct version update</h3>
<p>The cleanest fix — bump the vulnerable package to the safe version in your manifest and run your package manager. This works when you control the direct dependency.</p>
<pre># npm
npm install lodash@4.17.21

# pip
pip install Django==4.2.13

# Ruby
bundle update nokogiri</pre>

<h3>Override / forced resolution</h3>
<p>When the vulnerability is in a transitive dependency you don't control directly, you can force the package manager to use a safe version. PackageFix generates this block automatically.</p>
<pre>// package.json — npm overrides
{
  "overrides": {
    "qs": "6.11.0"
  }
}</pre>

<h3>Virtual patch</h3>
<p>When you can't update the package immediately (integration risk, breaking changes), you can add controls to reduce the attack surface. For example, blocking the specific input pattern that triggers the CVE at your WAF or API gateway. This is a temporary measure — not a substitute for updating.</p>

<h2>Remediation priority</h2>
<p>Not all CVEs need the same urgency. A practical order:</p>
<ul style="padding-left:20px;margin:12px 0;color:var(--muted);font-size:12px;line-height:2">
  <li><strong>CISA KEV entries</strong> — fix today. Being exploited right now.</li>
  <li><strong>CRITICAL CVEs in direct dependencies</strong> — fix this sprint.</li>
  <li><strong>HIGH CVEs in direct dependencies</strong> — fix this sprint.</li>
  <li><strong>CRITICAL/HIGH in transitive dependencies</strong> — next sprint, use overrides.</li>
  <li><strong>MEDIUM CVEs</strong> — scheduled update cycle.</li>
  <li><strong>LOW CVEs</strong> — backlog, address in bulk.</li>
</ul>

<div class="fix-box">
  <div class="label">PackageFix speeds up remediation</div>
  <p style="margin:0">PackageFix generates the fixed manifest with safe versions already applied — download it, run your install command, done. No manually hunting for which version fixed which CVE.</p>
</div>""",
    faqs=[
        ("What's the difference between remediation and mitigation?", "Remediation eliminates the vulnerability — you update the package and the vulnerable code is gone. Mitigation reduces the risk without eliminating it — for example, blocking certain input patterns at your firewall while you wait to update. Remediation is the goal; mitigation is a temporary measure."),
        ("What if the safe version has breaking changes?", "Check the package's CHANGELOG and migration guide. Many security patches are released as patch versions (1.2.3 → 1.2.4) with no breaking changes. When they are breaking (major version bumps), the fix is larger but still necessary. Start in a branch, run your test suite, fix the breaking changes."),
        ("How does PackageFix help with remediation?", "PackageFix generates the fixed manifest file — your package.json, requirements.txt, or Gemfile with all CVEs patched to safe versions. Download it, replace your existing manifest, run npm install or bundle install, and you're done. For transitive vulnerabilities, it also generates the npm overrides block."),
        ("What is mean time to remediate (MTTR)?", "MTTR is a security metric measuring how long it takes from when a vulnerability is discovered to when it's fixed in production. Industry benchmarks suggest under 30 days for Critical CVEs, under 60 days for High. CISA KEV entries should be under 2 weeks.")
    ],
    related_pages=[
        {"url": "/glossary/dependency-scanning", "title": "Dependency Scanning", "desc": "Finding what to remediate"},
        {"url": "/glossary/cisa-kev", "title": "CISA KEV", "desc": "Highest remediation priority"},
        {"url": "/glossary/transitive-dependency", "title": "Transitive Dependencies", "desc": "Harder to remediate"},
        {"url": "/guides/github-actions", "title": "Automate in CI", "desc": "Catch CVEs before they ship"},
    ]
))


# ══════════════════════════════════════════════════════════════════════════════
# 3. CVE HISTORY TABLES — REMAINING ~100 PACKAGES
# Format: (slug, pkg, eco, safe_ver, install, weekly, desc, cves, before, after, faqs, related)
# ══════════════════════════════════════════════════════════════════════════════

REMAINING_HISTORIES = [

  # ── npm ────────────────────────────────────────────────────────────────────
  {"slug":"fix/npm/moment","pkg":"moment.js","eco":"npm","eco_label":"npm","safe_ver":"2.29.4","install":"npm install","weekly":"20M+",
   "desc":"moment.js is a date manipulation library that is now in maintenance mode. The team recommends migrating to date-fns or dayjs for new projects. Its main CVEs are ReDoS vulnerabilities and a SSRF in its date parsing.",
   "cves":[("CVE-2016-4055",2016,"HIGH",False,True,"2.11.2","ReDoS via date parsing regex"),
           ("CVE-2017-18214",2017,"HIGH",False,True,"2.19.3","ReDoS via crafted string in moment()"),
           ("CVE-2022-24785",2022,"HIGH",False,True,"2.29.2","Path traversal in locale loading"),
           ("CVE-2022-31129",2022,"HIGH",False,True,"2.29.4","ReDoS in date parsing — moment is deprecated")],
   "before":'"moment": "2.29.1"',"after":'"moment": "2.29.4"',
   "faqs":[("Should I migrate away from moment.js?","Yes — moment.js is in maintenance-only mode. The team recommends date-fns or dayjs for new projects. Both are smaller, tree-shakeable, and actively maintained. Migration is not trivial but worth it for long-lived projects."),
           ("Is moment.js still safe to use?","2.29.4 patches all known CVEs. But since it's in maintenance mode, future CVEs may not get fixes. If you're on a long-lived project, plan the migration to date-fns or dayjs."),
           ("What's the easiest moment.js replacement?","dayjs has an almost identical API to moment.js and is a near drop-in replacement. date-fns is more comprehensive but uses a different functional API. Start with dayjs if API compatibility matters.")],
   "related":[{"url":"/fix/npm/semver","title":"Fix semver","desc":"Another ReDoS CVE"},{"url":"/npm","title":"npm Security","desc":"All npm guides"}]},

  {"slug":"fix/npm/webpack","pkg":"webpack","eco":"npm","eco_label":"npm","safe_ver":"5.75.0","install":"npm install","weekly":"25M+",
   "desc":"webpack is the most widely-used JavaScript bundler. CVEs in webpack are relatively rare given its complexity and age. The main CVE is a prototype pollution via import.meta handling.",
   "cves":[("CVE-2019-10742",2019,"HIGH",False,True,"4.28.4","DoS via crafted JSON file"),
           ("CVE-2023-28154",2023,"HIGH",False,True,"5.75.0","Prototype pollution via import.meta")],
   "before":'"webpack": "5.69.0"',"after":'"webpack": "5.75.0"',
   "faqs":[("Does webpack 4 still receive security patches?","webpack 4 is in maintenance mode. CVE-2023-28154 only affects webpack 5. For webpack 4, check if you're affected and consider upgrading to webpack 5."),("What is the import.meta prototype pollution in webpack?","CVE-2023-28154 allows prototype pollution via crafted import.meta expressions in processed JavaScript. Applications that process untrusted JavaScript through webpack are affected.")],
   "related":[{"url":"/fix/npm/lodash","title":"Fix lodash","desc":"Prototype pollution CVEs"},{"url":"/npm","title":"npm Security","desc":"All npm guides"}]},

  {"slug":"fix/npm/node-fetch","pkg":"node-fetch","eco":"npm","eco_label":"npm","safe_ver":"3.3.2","install":"npm install","weekly":"80M+",
   "desc":"node-fetch is a lightweight fetch implementation for Node.js. The main CVE is a credential exposure vulnerability when following redirects.",
   "cves":[("CVE-2022-0235",2022,"HIGH",False,True,"2.6.7","Credential exposure via redirect to different host"),
           ("CVE-2023-44487",2023,"HIGH",False,True,"3.3.2","HTTP/2 rapid reset (via transitive dep)")],
   "before":'"node-fetch": "2.6.1"',"after":'"node-fetch": "3.3.2"',
   "faqs":[("Should I use node-fetch or the built-in fetch?","Node.js 18+ has a built-in fetch implementation. For new Node 18+ projects, the built-in fetch is preferred. For Node 16 or earlier, use node-fetch 3.x."),("Is there a breaking change between node-fetch 2 and 3?","Yes — node-fetch 3 is ESM-only. If your project uses CommonJS (require()), you need to stay on node-fetch 2.6.7 or use a dynamic import() wrapper.")],
   "related":[{"url":"/fix/npm/axios","title":"Fix axios","desc":"Alternative HTTP client"},{"url":"/npm","title":"npm Security","desc":"All npm guides"}]},

  {"slug":"fix/npm/semver","pkg":"semver","eco":"npm","eco_label":"npm","safe_ver":"7.5.4","install":"npm install","weekly":"200M+",
   "desc":"semver is the npm package for parsing and comparing semantic version strings. It's one of the most downloaded npm packages — a transitive dependency of npm itself and thousands of tools.",
   "cves":[("CVE-2015-8855",2015,"HIGH",False,True,"4.3.2","Regular expression DoS in comparator parsing"),
           ("CVE-2022-25883",2022,"HIGH",False,True,"7.5.2","ReDoS in coerce() function")],
   "before":'"semver": "7.5.0"',"after":'"semver": "7.5.4"',
   "faqs":[("How do I fix semver if it's a transitive dependency?","semver appears as a transitive dependency in almost every Node.js project. Use npm overrides: {\"overrides\": {\"semver\": \"7.5.4\"}}. PackageFix generates this block automatically."),("Is semver ReDoS exploitable in practice?","The coerce() ReDoS requires passing a very long string. In most applications, version strings come from package.json or known sources, not user input. Still worth patching — the upgrade has no breaking changes.")],
   "related":[{"url":"/fix/npm/minimist","title":"Fix minimist","desc":"Another heavily-transitive CVE"},{"url":"/npm","title":"npm Security","desc":"All npm guides"}]},

  {"slug":"fix/npm/qs","pkg":"qs","eco":"npm","eco_label":"npm","safe_ver":"6.11.0","install":"npm install","weekly":"100M+",
   "desc":"qs is a query string parser used by Express and hundreds of other packages. Prototype pollution via crafted query strings has been a recurring issue.",
   "cves":[("CVE-2014-7191",2014,"HIGH",False,True,"1.0.0","Prototype pollution via __proto__ in query strings"),
           ("CVE-2017-1000048",2017,"HIGH",False,True,"6.3.2","Prototype pollution bypass"),
           ("CVE-2022-24999",2022,"HIGH",True, True,"6.11.0","Prototype pollution — CISA KEV")],
   "before":'"qs": "6.5.2"',"after":'"qs": "6.11.0"',
   "faqs":[("Why does qs keep having prototype pollution CVEs?","Query string parsing that supports nested objects (a[b]=c) requires recursive object building — which is inherently vulnerable to prototype pollution if __proto__ keys aren't filtered. Each CVE was a new bypass of the previous fix."),("Does updating Express fix qs?","Express 4.18.0+ bundles qs 6.11.0. Updating Express to 4.18.0+ is the easiest fix. If you can't update Express, use npm overrides to force a safe qs version.")],
   "related":[{"url":"/fix/npm/express","title":"Fix Express","desc":"Main qs consumer"},{"url":"/glossary/prototype-pollution","title":"Prototype Pollution","desc":"The vulnerability class"},{"url":"/npm","title":"npm Security","desc":"All npm guides"}]},

  {"slug":"fix/npm/follow-redirects","pkg":"follow-redirects","eco":"npm","eco_label":"npm","safe_ver":"1.15.6","install":"npm install","weekly":"50M+",
   "desc":"follow-redirects implements redirect-following for HTTP requests in Node.js. It's a transitive dependency of axios, webpack-dev-server, and many others. Its CVEs are mostly credential/header exposure on redirect.",
   "cves":[("CVE-2022-0155",2022,"MEDIUM",False,True,"1.14.7","Private data exposure via HTTP redirect"),
           ("CVE-2023-26159",2023,"MEDIUM",False,True,"1.15.4","URL redirect to untrusted site"),
           ("CVE-2024-28849",2024,"MEDIUM",False,True,"1.15.6","Proxy-Authorization header cleared on cross-host redirect")],
   "before":'"follow-redirects": "1.15.2"',"after":'"follow-redirects": "1.15.6"',
   "faqs":[("Is follow-redirects a direct or transitive dep?","Almost always transitive — it's pulled in by axios, webpack-dev-server, got, and many other packages. Use npm overrides to force a safe version if you can't update the parent package."),("Does CVE-2023-26159 affect server-side code?","Yes — SSRF via redirect. If your server uses axios or another package that follows redirects with user-controlled URLs, you could be forwarded to internal services.")],
   "related":[{"url":"/fix/npm/axios","title":"Fix axios","desc":"Main follow-redirects consumer"},{"url":"/npm","title":"npm Security","desc":"All npm guides"}]},

  {"slug":"fix/npm/minimist","pkg":"minimist","eco":"npm","eco_label":"npm","safe_ver":"1.2.6","install":"npm install","weekly":"100M+",
   "desc":"minimist parses command-line arguments. Despite its tiny size, it's one of the most downloaded npm packages and a common transitive dependency. Prototype pollution in argument parsing has been patched twice.",
   "cves":[("CVE-2020-7598",2020,"MEDIUM",False,True,"0.2.1","Prototype pollution via crafted argument"),
           ("CVE-2021-44906",2021,"CRITICAL",True,True,"1.2.6","Prototype pollution — more severe bypass — CISA KEV")],
   "before":'"minimist": "1.2.5"',"after":'"minimist": "1.2.6"',
   "faqs":[("Why is minimist CRITICAL?","CVE-2021-44906 has CVSS 9.8 because prototype pollution via command-line argument parsing can be exploited remotely in applications that parse user-controlled arguments. The attack surface is large."),("How do I fix minimist if it's transitive?","Use npm overrides: {\"overrides\": {\"minimist\": \"1.2.6\"}}. minimist appears in hundreds of tools as a transitive dep — the override is the practical fix without updating every parent package.")],
   "related":[{"url":"/kev/CVE-2021-44906","title":"CVE-2021-44906 Detail","desc":"CISA KEV page"},{"url":"/fix/npm/lodash","title":"Fix lodash","desc":"Related prototype pollution"},{"url":"/npm","title":"npm Security","desc":"All npm guides"}]},

  {"slug":"fix/npm/sharp","pkg":"sharp","eco":"npm","eco_label":"npm","safe_ver":"0.33.2","install":"npm install","weekly":"5M+",
   "desc":"sharp is a high-performance Node.js image processing library. Its main CVE is CVE-2023-4863 — a heap buffer overflow in libwebp that also affected Chrome and Firefox. CVSS 10.0.",
   "cves":[("CVE-2023-4863",2023,"CRITICAL",True,True,"0.32.6","Heap buffer overflow in libwebp — CISA KEV — CVSS 10.0")],
   "before":'"sharp": "0.32.0"',"after":'"sharp": "0.33.2"',
   "faqs":[("Is CVE-2023-4863 the same as the Chrome zero-day?","Yes — libwebp is the underlying C library used by Chrome, Firefox, and sharp. The same heap buffer overflow allows code execution via a crafted WebP image across all three."),("Do I need to process WebP images to be vulnerable?","You need to process a malicious WebP image. If your application processes user-uploaded images without validating format first, you're at risk. Validate that uploaded files are what they claim to be before processing.")],
   "related":[{"url":"/kev/CVE-2023-4863","title":"CVE-2023-4863 Detail","desc":"CISA KEV — CVSS 10.0"},{"url":"/npm","title":"npm Security","desc":"All npm guides"}]},

  {"slug":"fix/npm/passport","pkg":"passport","eco":"npm","eco_label":"npm","safe_ver":"0.6.0","install":"npm install","weekly":"2M+",
   "desc":"passport is the most widely-used Node.js authentication middleware. Its CVEs are session-related — fixation and state management issues that can lead to authentication bypass.",
   "cves":[("CVE-2022-25896",2022,"HIGH",False,True,"0.6.0","Session fixation in multi-strategy authentication"),
           ("CVE-2023-18414",2023,"HIGH",False,True,"0.6.0","Authentication bypass via state parameter manipulation")],
   "before":'"passport": "0.5.2"',"after":'"passport": "0.6.0"',
   "faqs":[("What is session fixation?","Session fixation is an attack where an attacker sets the session ID before a user authenticates, then reuses that session after login. Passport 0.6.0 regenerates the session ID on successful authentication, preventing this."),("Are passport strategies also vulnerable?","The vulnerabilities are in the core passport session handling, not in individual strategies. Updating passport to 0.6.0 is sufficient — you don't need to update each strategy separately.")],
   "related":[{"url":"/fix/npm/jsonwebtoken","title":"Fix jsonwebtoken","desc":"JWT auth CVEs"},{"url":"/npm","title":"npm Security","desc":"All npm guides"}]},

  {"slug":"fix/npm/socket.io","pkg":"socket.io","eco":"npm","eco_label":"npm","safe_ver":"4.6.2","install":"npm install","weekly":"5M+",
   "desc":"socket.io is the most widely-used WebSocket library for Node.js. Its main CVE is a ReDoS vulnerability in socket ID parsing.",
   "cves":[("CVE-2020-28469",2020,"HIGH",False,True,"2.4.0","ReDoS via crafted socket ID"),
           ("CVE-2023-32695",2023,"HIGH",False,True,"4.6.2","ReDoS via specially crafted socket.id")],
   "before":'"socket.io": "4.6.0"',"after":'"socket.io": "4.6.2"',
   "faqs":[("Is socket.io ReDoS exploitable?","Yes — a malicious client can send a crafted socket ID that causes the server to hang during regex processing. In Node.js's single-threaded event loop, this can block all other connections."),("Does this affect socket.io-client?","No — the ReDoS is server-side. The socket.io-client package is not affected.")],
   "related":[{"url":"/fix/npm/ws","title":"Fix ws","desc":"Lower-level WebSocket CVEs"},{"url":"/npm","title":"npm Security","desc":"All npm guides"}]},

  # ── PyPI ───────────────────────────────────────────────────────────────────
  {"slug":"fix/pypi/flask","pkg":"Flask","eco":"pypi","eco_label":"PyPI","safe_ver":"3.0.3","install":"pip install -r requirements.txt","weekly":"100M+",
   "desc":"Flask is Python's most popular microframework. CVEs in Flask itself are rare — most Flask-related vulnerabilities come through Werkzeug or Jinja2. The main direct CVE is a cookie bypass.",
   "cves":[("CVE-2018-1000656",2018,"HIGH",False,True,"0.12.3","DoS via large cookie value"),
           ("CVE-2023-30861",2023,"HIGH",False,True,"2.3.2","Secure cookie bypass via response manipulation")],
   "before":'"Flask==2.0.0"',"after":'"Flask==3.0.3"',
   "faqs":[("Does Flask have many CVEs?","Flask itself has very few direct CVEs — most Flask security issues come through its dependencies Werkzeug (routing, request handling) and Jinja2 (templates). Keep the entire Flask stack updated together."),("What changed in CVE-2023-30861?","A response could be crafted to cause Flask to set cookies without the Secure flag even when configured to require it. Update to 2.3.2 or later.")],
   "related":[{"url":"/fix/pypi/werkzeug","title":"Fix Werkzeug","desc":"Flask's WSGI library"},{"url":"/fix/pypi/jinja2","title":"Fix Jinja2","desc":"Flask's template engine"},{"url":"/python","title":"PyPI Security","desc":"All Python guides"}]},

  {"slug":"fix/pypi/werkzeug","pkg":"Werkzeug","eco":"pypi","eco_label":"PyPI","safe_ver":"3.0.3","install":"pip install -r requirements.txt","weekly":"100M+",
   "desc":"Werkzeug is Flask's WSGI toolkit. CVEs here affect all Flask applications since Werkzeug handles request parsing, routing, and debugging. The debugger CVE (2023) is particularly serious.",
   "cves":[("CVE-2023-25577",2023,"HIGH",False,True,"2.2.3","DoS via crafted multipart request with many headers"),
           ("CVE-2023-46136",2023,"HIGH",False,True,"3.0.1","DoS via multipart form parsing with many fields"),
           ("CVE-2024-34069",2024,"CRITICAL",False,True,"3.0.3","RCE via debugger PIN bypass in development mode")],
   "before":'"Werkzeug==2.0.0"',"after":'"Werkzeug==3.0.3"',
   "faqs":[("Is CVE-2024-34069 critical for production apps?","It only affects apps running with WERKZEUG_DEBUG_PIN or debug=True — which should never happen in production. The fix is to never run Werkzeug's debug mode in production AND update to 3.0.3."),("Does updating Flask update Werkzeug?","Not automatically. Specify Werkzeug explicitly in your requirements.txt. Flask has a loose Werkzeug version constraint.")],
   "related":[{"url":"/fix/pypi/flask","title":"Fix Flask","desc":"Werkzeug's main consumer"},{"url":"/python","title":"PyPI Security","desc":"All Python guides"}]},

  {"slug":"fix/pypi/pillow","pkg":"Pillow","eco":"pypi","eco_label":"PyPI","safe_ver":"10.3.0","install":"pip install -r requirements.txt","weekly":"50M+",
   "desc":"Pillow is Python's image processing library — almost every Python web app that handles image uploads uses it. Image parsing is notoriously attack-surface-heavy, and Pillow has had many CVEs.",
   "cves":[("CVE-2021-25287",2021,"CRITICAL",False,True,"8.2.0","Out-of-bounds read via crafted PDF"),
           ("CVE-2021-27923",2021,"HIGH",False,True,"8.1.1","Buffer overflow via TIFF parsing"),
           ("CVE-2022-22815",2022,"HIGH",False,True,"9.0.0","Memory corruption via crafted image file"),
           ("CVE-2022-22816",2022,"HIGH",False,True,"9.0.0","Buffer overflow in ImagePath.getbbox"),
           ("CVE-2023-44271",2023,"HIGH",False,True,"10.0.1","DoS via uncontrolled resource in ImageFont")],
   "before":'"Pillow==8.0.0"',"after":'"Pillow==10.3.0"',
   "faqs":[("Why does Pillow have so many CVEs?","Image file parsing requires handling dozens of complex binary formats (JPEG, PNG, TIFF, BMP, WebP, etc.), each with their own quirks. C extensions handle the low-level parsing, which means memory safety issues in the underlying C code surface as CVEs."),("Should I validate image uploads before passing to Pillow?","Yes — always validate that uploaded files are valid images of the expected format. Use Pillow's verify() method or check the file header before processing. Reject unexpected formats entirely.")],
   "related":[{"url":"/python","title":"PyPI Security","desc":"All Python guides"},{"url":"/glossary/dependency-scanning","title":"Dependency Scanning","desc":"Staying on top of CVEs"}]},

  {"slug":"fix/pypi/urllib3","pkg":"urllib3","eco":"pypi","eco_label":"PyPI","safe_ver":"2.2.2","install":"pip install -r requirements.txt","weekly":"300M+",
   "desc":"urllib3 is the HTTP client underlying Python's requests library. It's one of the most downloaded packages on PyPI. CVEs here affect every application using requests transitively.",
   "cves":[("CVE-2019-11324",2019,"HIGH",False,True,"1.24.2","Certificate verification bypass via crafted hostname"),
           ("CVE-2021-33503",2021,"HIGH",False,True,"1.26.5","ReDoS via crafted HTTP response"),
           ("CVE-2023-43804",2023,"MEDIUM",False,True,"2.0.6","Cookie header not stripped on redirect"),
           ("CVE-2023-45803",2023,"MEDIUM",False,True,"2.0.7","Request body not stripped after redirect")],
   "before":'"urllib3==1.25.11"',"after":'"urllib3==2.2.2"',
   "faqs":[("Is there a breaking change between urllib3 1.x and 2.x?","Yes — urllib3 2.x requires Python 3.8+, drops Python 2 support, and has API changes. requests pins to urllib3<3 so it works with both. If you use urllib3 directly, check the migration guide."),("Does updating requests update urllib3?","Not to a specific version. requests accepts a range. Pin urllib3 explicitly in your requirements.txt if you need to force a specific safe version.")],
   "related":[{"url":"/fix/pypi/requests","title":"Fix requests","desc":"urllib3 consumer"},{"url":"/python","title":"PyPI Security","desc":"All Python guides"}]},

  {"slug":"fix/pypi/paramiko","pkg":"paramiko","eco":"pypi","eco_label":"PyPI","safe_ver":"3.4.0","install":"pip install -r requirements.txt","weekly":"20M+",
   "desc":"paramiko is Python's SSH library. CVEs here are serious because SSH handles authentication and key material. The Terrapin attack (2023) affected virtually all SSH implementations.",
   "cves":[("CVE-2018-1000805",2018,"CRITICAL",False,True,"2.4.2","Authentication bypass in SSH client"),
           ("CVE-2022-24302",2022,"MEDIUM",False,True,"2.10.1","Race condition in private key file creation"),
           ("CVE-2023-48795",2023,"HIGH",False,True,"3.4.0","Terrapin — SSH prefix truncation attack")],
   "before":'"paramiko==2.12.0"',"after":'"paramiko==3.4.0"',
   "faqs":[("What is the Terrapin attack?","Terrapin (CVE-2023-48795) is a prefix truncation attack against the SSH protocol's handshake. An attacker in a man-in-the-middle position can silently remove certain extension negotiation messages, downgrading security properties of the connection."),("Does CVE-2023-48795 require a MitM position?","Yes — the attacker must be able to intercept and modify traffic between client and server. This limits exploitability in practice, but the vulnerability is worth patching.")],
   "related":[{"url":"/python","title":"PyPI Security","desc":"All Python guides"},{"url":"/glossary/dependency-scanning","title":"Dependency Scanning","desc":"How to catch these"}]},

  {"slug":"fix/pypi/aiohttp","pkg":"aiohttp","eco":"pypi","eco_label":"PyPI","safe_ver":"3.9.3","install":"pip install -r requirements.txt","weekly":"50M+",
   "desc":"aiohttp is an async HTTP client and server framework for Python. CVEs here affect both client and server use cases. The directory traversal CVE (2024) is particularly serious.",
   "cves":[("CVE-2023-37276",2023,"HIGH",False,True,"3.8.5","HTTP request smuggling via chunk parsing"),
           ("CVE-2023-47641",2023,"MEDIUM",False,True,"3.9.0","URL redirect via HTTPS to HTTP downgrade"),
           ("CVE-2024-23334",2024,"HIGH",False,True,"3.9.2","Directory traversal in static file serving")],
   "before":'"aiohttp==3.8.6"',"after":'"aiohttp==3.9.3"',
   "faqs":[("Who is affected by the aiohttp directory traversal?","Any application using aiohttp's built-in static file serving with follow_symlinks=True. This is not the default but is a common configuration for serving static files in development. In production, use a reverse proxy for static files."),("Does the aiohttp HTTP smuggling affect API servers?","Yes — CVE-2023-37276 affects any aiohttp server handling chunked transfer encoding, which is most deployments. Update to 3.8.5 or later.")],
   "related":[{"url":"/python","title":"PyPI Security","desc":"All Python guides"}]},

  {"slug":"fix/pypi/sqlalchemy","pkg":"SQLAlchemy","eco":"pypi","eco_label":"PyPI","safe_ver":"2.0.28","install":"pip install -r requirements.txt","weekly":"30M+",
   "desc":"SQLAlchemy is Python's most popular ORM. CVEs here are rare — the team is security-conscious. The main risk is SQL injection via raw query methods, which are discouraged in the documentation.",
   "cves":[("CVE-2019-7164",2019,"HIGH",False,True,"1.3.0","SQL injection via order_by in certain backends"),
           ("CVE-2019-7548",2019,"HIGH",False,True,"1.3.0","SQL injection via group_by in certain backends"),
           ("CVE-2023-30534",2023,"HIGH",False,True,"2.0.28","SQL injection via crafted filter parameters in raw queries")],
   "before":'"SQLAlchemy==1.4.46"',"after":'"SQLAlchemy==2.0.28"',
   "faqs":[("Is SQLAlchemy's ORM safe from SQL injection?","The ORM query interface is safe — SQLAlchemy parameterises queries automatically. The risk is with raw SQL via text() or execute() with string formatting. Never use f-strings or % formatting in SQL queries — always use bindparams."),("Should I migrate from SQLAlchemy 1.4 to 2.0?","SQLAlchemy 1.4 EOL is approaching. 2.0 has significant API changes but also better async support and performance. The migration guide is comprehensive — worth the investment for long-lived projects.")],
   "related":[{"url":"/python","title":"PyPI Security","desc":"All Python guides"}]},

  {"slug":"fix/pypi/gunicorn","pkg":"gunicorn","eco":"pypi","eco_label":"PyPI","safe_ver":"22.0.0","install":"pip install -r requirements.txt","weekly":"30M+",
   "desc":"gunicorn is the most widely-used Python WSGI HTTP server. Its main CVE is HTTP request smuggling — a server-side vulnerability that can affect all applications running behind a reverse proxy.",
   "cves":[("CVE-2018-1000164",2018,"HIGH",False,True,"19.10.0","HTTP request smuggling via header manipulation"),
           ("CVE-2024-1135",2024,"HIGH",False,True,"22.0.0","HTTP request smuggling via invalid Transfer-Encoding")],
   "before":'"gunicorn==20.1.0"',"after":'"gunicorn==22.0.0"',
   "faqs":[("What is HTTP request smuggling?","HTTP request smuggling exploits ambiguity in how front-end proxies and back-end servers parse HTTP requests. An attacker can prefix a malicious request to the next user's request, potentially bypassing access controls or poisoning the request queue."),("Does gunicorn 22.0.0 have breaking changes?","Gunicorn 22 drops Python 3.6 and 3.7 support. For Python 3.8+, the upgrade is straightforward.")],
   "related":[{"url":"/python","title":"PyPI Security","desc":"All Python guides"}]},

  {"slug":"fix/pypi/pyyaml","pkg":"PyYAML","eco":"pypi","eco_label":"PyPI","safe_ver":"6.0.1","install":"pip install -r requirements.txt","weekly":"100M+",
   "desc":"PyYAML is Python's YAML parser. The most critical CVE is CVE-2020-14343 — remote code execution via yaml.load() without a Loader argument. This is on the CISA KEV list.",
   "cves":[("CVE-2017-18342",2017,"CRITICAL",False,True,"5.1","RCE via yaml.load() without Loader"),
           ("CVE-2020-1747",2020,"CRITICAL",False,True,"5.3.1","RCE via crafted YAML in FullLoader"),
           ("CVE-2020-14343",2020,"CRITICAL",True, True,"5.4","RCE via yaml.load() — CISA KEV")],
   "before":'"PyYAML==5.4.1"',"after":'"PyYAML==6.0.1"',
   "faqs":[("How do I fix PyYAML's RCE vulnerability?","Replace yaml.load(data) with yaml.safe_load(data) everywhere in your codebase. safe_load() uses SafeLoader which doesn't allow arbitrary Python object creation. Then update to PyYAML 6.0.1."),("Is yaml.safe_load() completely safe?","safe_load() prevents arbitrary code execution — it only loads basic Python types (strings, numbers, lists, dicts). It's safe for loading configuration files from trusted or untrusted sources.")],
   "related":[{"url":"/kev/CVE-2020-14343","title":"KEV: CVE-2020-14343","desc":"CISA KEV page"},{"url":"/python","title":"PyPI Security","desc":"All Python guides"}]},

  {"slug":"fix/pypi/celery","pkg":"Celery","eco":"pypi","eco_label":"PyPI","safe_ver":"5.3.6","install":"pip install -r requirements.txt","weekly":"10M+",
   "desc":"Celery is Python's distributed task queue. CVEs here affect task result handling and authentication. Keep it updated especially if your Celery broker or backend is accessible from untrusted networks.",
   "cves":[("CVE-2021-23727",2021,"HIGH",False,True,"5.2.2","Privilege escalation via task result backend"),
           ("CVE-2021-27928",2021,"MEDIUM",False,True,"5.0.5","Unsafe deserialization via Pickle backend")],
   "before":'"celery==5.2.7"',"after":'"celery==5.3.6"',
   "faqs":[("Is using Pickle as the Celery result backend safe?","No — Pickle allows arbitrary Python object deserialisation and should never be used with untrusted task results. Use JSON as the task serialiser: task_serializer='json', result_serializer='json', accept_content=['json']."),("Does Celery expose a network endpoint?","Celery workers connect to a broker (RabbitMQ, Redis) and listen for tasks. The broker should never be exposed to untrusted networks. Access control on your broker is as important as keeping Celery updated.")],
   "related":[{"url":"/python","title":"PyPI Security","desc":"All Python guides"}]},

  # ── Ruby ───────────────────────────────────────────────────────────────────
  {"slug":"fix/ruby/puma","pkg":"Puma","eco":"ruby","eco_label":"Ruby","safe_ver":"6.4.2","install":"bundle install","weekly":"5M+",
   "desc":"Puma is Ruby's most widely-used multi-threaded web server. HTTP request smuggling and DoS are its main vulnerability classes — server-level issues that affect all applications regardless of framework.",
   "cves":[("CVE-2019-16770",2019,"HIGH",False,True,"3.12.2","DoS via thread exhaustion"),
           ("CVE-2020-11076",2020,"HIGH",False,True,"4.3.5","HTTP request smuggling via chunked transfer"),
           ("CVE-2021-29509",2021,"HIGH",False,True,"4.3.8","DoS via connection queue exhaustion"),
           ("CVE-2022-24790",2022,"HIGH",False,True,"5.6.4","HTTP request smuggling via chunked encoding")],
   "before": "gem 'puma', '4.3.0'", "after": "gem 'puma', '6.4.2'",
   "faqs":[("What is the impact of Puma's HTTP request smuggling CVEs?","HTTP request smuggling can allow an attacker to bypass access controls, poison shared response caches, and hijack credentials. In a reverse-proxy setup (Nginx → Puma), smuggling exploits the gap between how each server parses the same request."),("Does Rails update Puma automatically?","No — Puma is a separate gem. Specify it explicitly in your Gemfile and update regularly.")],
   "related":[{"url":"/fix/ruby/rack","title":"Fix Rack","desc":"Related server-level CVEs"},{"url":"/ruby","title":"Ruby Security","desc":"All Ruby guides"}]},

  {"slug":"fix/ruby/rack","pkg":"Rack","eco":"ruby","eco_label":"Ruby","safe_ver":"3.0.11","install":"bundle install","weekly":"8M+",
   "desc":"Rack is the Ruby web server interface — the foundation that Rails, Sinatra, and every Ruby web app runs on. CVEs here affect all Ruby web applications.",
   "cves":[("CVE-2018-16471",2018,"MEDIUM",False,True,"1.6.11","XSS via PATH_INFO in Rack::Directory"),
           ("CVE-2020-8161",2020,"HIGH",False,True,"2.1.3","Directory traversal in Rack::Directory"),
           ("CVE-2022-30122",2022,"HIGH",False,True,"2.2.3","DoS via crafted multipart body"),
           ("CVE-2022-30123",2022,"CRITICAL",False,True,"2.2.3","Shell command injection via newline in PATH_INFO"),
           ("CVE-2023-27530",2023,"HIGH",True, True,"3.0.4","DoS via multipart body parsing — CISA KEV")],
   "before": "gem 'rack', '2.2.2'", "after": "gem 'rack', '3.0.11'",
   "faqs":[("Does updating Rails update Rack?","Rails depends on Rack but with a loose version constraint. Specify rack explicitly in your Gemfile to pin to a safe version, or update Rails to a version that requires a safe Rack."),("Is CVE-2022-30123 (shell injection) easy to exploit?","It requires the ability to inject a newline into PATH_INFO — possible if your routing doesn't validate URL paths. Update to 2.2.3+ immediately.")],
   "related":[{"url":"/kev/CVE-2023-27530","title":"KEV: CVE-2023-27530","desc":"CISA KEV page"},{"url":"/fix/ruby/rails","title":"Fix Rails","desc":"Main Rack consumer"},{"url":"/ruby","title":"Ruby Security","desc":"All Ruby guides"}]},

  {"slug":"fix/ruby/devise","pkg":"Devise","eco":"ruby","eco_label":"Ruby","safe_ver":"4.9.4","install":"bundle install","weekly":"2M+",
   "desc":"Devise is Ruby's most widely-used authentication solution for Rails. CVEs here are authentication bypasses and open redirects — serious for any application that handles user authentication.",
   "cves":[("CVE-2019-5421",2019,"CRITICAL",False,True,"4.6.2","Authentication bypass via bypass_sign_in"),
           ("CVE-2021-28125",2021,"HIGH",False,True,"4.8.0","Open redirect in OAuth callback"),
           ("CVE-2021-32797",2021,"HIGH",False,True,"4.8.0","Improper cookie handling in remember_me")],
   "before": "gem 'devise', '4.7.3'", "after": "gem 'devise', '4.9.4'",
   "faqs":[("Is the Devise authentication bypass CVE serious?","CVE-2019-5421 allowed bypass_sign_in to be called without verification in certain configurations. It affects applications using Devise's admin impersonation features. Update to 4.6.2+."),("Does Devise handle 2FA?","Devise itself doesn't — use devise-two-factor or Authy for 2FA. Keep both gems updated.")],
   "related":[{"url":"/fix/ruby/rails","title":"Fix Rails","desc":"Devise's framework"},{"url":"/ruby","title":"Ruby Security","desc":"All Ruby guides"}]},

  {"slug":"fix/ruby/omniauth","pkg":"OmniAuth","eco":"ruby","eco_label":"Ruby","safe_ver":"2.1.2","install":"bundle install","weekly":"2M+",
   "desc":"OmniAuth handles OAuth authentication for Rails apps. CVE-2015-9284 is a critical CSRF vulnerability that is still being exploited — it's on the CISA KEV list despite being a 2015 CVE.",
   "cves":[("CVE-2015-9284",2015,"HIGH",True, True,"2.0.0","CSRF in OAuth callback via GET request — CISA KEV"),
           ("CVE-2019-3891",2019,"HIGH",False,True,"1.9.2","Authentication bypass via manipulated OAuth state")],
   "before": "gem 'omniauth', '1.9.1'", "after": "gem 'omniauth', '2.1.2'",
   "faqs":[("Why is a 2015 CVE still on CISA KEV?","CVE-2015-9284 wasn't fully addressed in the original fix. OmniAuth 2.0 (released 2021) was the proper fix — requiring POST-only OAuth callbacks. Many applications are still on OmniAuth 1.x making this an active attack surface."),("What changed in OmniAuth 2.0?","OmniAuth 2.0 requires POST requests for OAuth callbacks by default, eliminating the CSRF vector. It's a breaking change — you need to add the omniauth-rails_csrf_protection gem or configure your OAuth provider for POST callbacks.")],
   "related":[{"url":"/kev/CVE-2015-9284","title":"CVE-2015-9284 Detail","desc":"CISA KEV page"},{"url":"/fix/ruby/devise","title":"Fix Devise","desc":"Related auth gem"},{"url":"/ruby","title":"Ruby Security","desc":"All Ruby guides"}]},

  {"slug":"fix/ruby/sidekiq","pkg":"Sidekiq","eco":"ruby","eco_label":"Ruby","safe_ver":"7.2.4","install":"bundle install","weekly":"2M+",
   "desc":"Sidekiq is Ruby's most popular background job processor. CVEs here are mostly DoS via crafted job payloads. Keep it updated especially if your Redis instance is accessible externally.",
   "cves":[("CVE-2022-23837",2022,"HIGH",False,True,"5.2.10","DoS via malformed job JSON parsing"),
           ("CVE-2023-26141",2023,"MEDIUM",False,True,"6.5.12","XSS in Sidekiq web UI")],
   "before": "gem 'sidekiq', '6.5.0'", "after": "gem 'sidekiq', '7.2.4'",
   "faqs":[("Should the Sidekiq web UI be publicly accessible?","No — Sidekiq's web UI should be protected with authentication and only accessible to admins. CVE-2023-26141 (XSS in the web UI) is less critical if the UI is properly access-controlled."),("Does Sidekiq 7 have breaking changes from 6?","Yes — Sidekiq 7 requires Ruby 2.7+ and Redis 6.2+. Job format is backwards-compatible. Check the upgrade notes.")],
   "related":[{"url":"/ruby","title":"Ruby Security","desc":"All Ruby guides"}]},

  # ── PHP ────────────────────────────────────────────────────────────────────
  {"slug":"fix/php/laravel","pkg":"Laravel Framework","eco":"php","eco_label":"PHP","safe_ver":"^11.0","install":"composer install","weekly":"5M+",
   "desc":"Laravel is PHP's most popular framework. The security team is active and releases patches regularly. Subscribe to the Laravel security mailing list and review releases before upgrading.",
   "cves":[("CVE-2018-15133",2018,"CRITICAL",False,True,"5.6.30","RCE via unserialize in remember_me cookie"),
           ("CVE-2021-3129", 2021,"CRITICAL",False,True,"8.4.3", "RCE via Ignition debug mode — widely exploited"),
           ("CVE-2021-43503",2021,"HIGH",    False,True,"8.75",  "Mass assignment via model fillable bypass")],
   "before":'"laravel/framework": "^8.0"',"after":'"laravel/framework": "^11.0"',
   "faqs":[("Is CVE-2021-3129 still being exploited?","Yes — Ignition's debug mode RCE is still found in production deployments running old Laravel versions. Never run APP_DEBUG=true in production. Update to 8.4.3+ immediately if you're affected."),("Does Laravel auto-update minor versions?","Composer installs the latest matching version when you run composer update. Pin major versions in composer.json (^8.0) to avoid unintended breaking changes while still getting security patches.")],
   "related":[{"url":"/fix/php/symfony","title":"Fix Symfony","desc":"Related PHP framework"},{"url":"/php","title":"PHP Security","desc":"All PHP guides"}]},

  {"slug":"fix/php/symfony","pkg":"Symfony","eco":"php","eco_label":"PHP","safe_ver":"^7.0","install":"composer install","weekly":"10M+",
   "desc":"Symfony is PHP's most widely-used enterprise framework. It has an excellent security process — patches for supported versions are released simultaneously. Track symfony.com/blog/security.",
   "cves":[("CVE-2019-10909",2019,"MEDIUM",False,True,"4.2.7","XSS via Twig templates without escaping"),
           ("CVE-2021-41268",2021,"HIGH",  False,True,"5.3.12","Authentication bypass via remember-me cookie"),
           ("CVE-2022-24894",2022,"HIGH",  False,True,"6.0.19","Incorrect cache-control headers on private responses"),
           ("CVE-2024-50340",2024,"HIGH",  False,True,"7.0.9", "Authentication bypass via malformed token")],
   "before":'"symfony/http-foundation": "^5.0"',"after":'"symfony/http-foundation": "^7.0"',
   "faqs":[("How does Symfony handle security releases?","Symfony backports security fixes to all currently supported branches simultaneously. When a CVE is disclosed, patches are available for Symfony 5.4, 6.4, and 7.x at the same time."),("Does the Symfony cache-control CVE affect production?","CVE-2022-24894 can cause private responses to be cached and served to other users by intermediate caches. If you use Symfony's HttpCache or an external reverse proxy, this is serious.")],
   "related":[{"url":"/fix/php/laravel","title":"Fix Laravel","desc":"Related PHP framework"},{"url":"/php","title":"PHP Security","desc":"All PHP guides"}]},

  {"slug":"fix/php/guzzle","pkg":"Guzzle HTTP","eco":"php","eco_label":"PHP","safe_ver":"^7.9","install":"composer install","weekly":"50M+",
   "desc":"Guzzle is PHP's most popular HTTP client — used by Laravel, Symfony, AWS SDK, and hundreds of other packages. CVEs here affect any application making HTTP requests through Guzzle.",
   "cves":[("CVE-2016-5385",2016,"HIGH",False,True,"6.2.1","HTTP_PROXY environment variable injection"),
           ("CVE-2022-29248",2022,"HIGH",False,True,"7.4.5","Cookie header not cleared on redirect to different domain"),
           ("CVE-2022-31090",2022,"HIGH",False,True,"7.4.5","CURLOPT_HTTPAUTH credential leak on host change"),
           ("CVE-2022-31091",2022,"HIGH",False,True,"7.4.5","CURLOPT_HTTPAUTH header exposure on redirect")],
   "before":'"guzzlehttp/guzzle": "^7.0"',"after":'"guzzlehttp/guzzle": "^7.9"',
   "faqs":[("Why does Guzzle have credential exposure CVEs?","HTTP clients that follow redirects must decide what to do with authentication headers when the redirect goes to a different host. Guzzle historically was too permissive, sending auth headers across host boundaries. The fixes add strict host checking before forwarding credentials."),("Do Laravel and Symfony use Guzzle?","Yes — Laravel's HTTP client wraps Guzzle, and many Symfony packages use it. Updating the underlying guzzlehttp/guzzle package directly is the safest approach.")],
   "related":[{"url":"/fix/php/laravel","title":"Fix Laravel","desc":"Main Guzzle consumer"},{"url":"/php","title":"PHP Security","desc":"All PHP guides"}]},

  {"slug":"fix/php/flysystem","pkg":"Flysystem","eco":"php","eco_label":"PHP","safe_ver":"^3.28","install":"composer install","weekly":"10M+",
   "desc":"Flysystem is PHP's filesystem abstraction library used by Laravel for all file storage. CVE-2021-32708 is critical — path traversal allowing arbitrary file read. It's on the CISA KEV list.",
   "cves":[("CVE-2021-32708",2021,"CRITICAL",True,True,"1.1.4","Path traversal allowing arbitrary file read — CISA KEV")],
   "before":'"league/flysystem": "^1.1"',"after":'"league/flysystem": "^3.28"',
   "faqs":[("What does CVE-2021-32708 allow an attacker to do?","Read arbitrary files on the server via a crafted path containing ../ sequences. If your application uses Flysystem to serve or process user-specified file paths, an attacker can read /etc/passwd, .env files, or any other readable file."),("Does Laravel use Flysystem?","Yes — Laravel's Storage facade is built on Flysystem. All Laravel apps using Storage::get() or similar methods that accept user input are potentially vulnerable if on a pre-1.1.4 version."),("Is migrating from Flysystem 1.x to 3.x a big change?","Yes — Flysystem 3.x has significant API changes. Laravel 9+ uses Flysystem 3.x. If you're on Laravel 8 with Flysystem 1.x, plan your upgrade path.")],
   "related":[{"url":"/kev/CVE-2021-32708","title":"KEV: CVE-2021-32708","desc":"CISA KEV page"},{"url":"/fix/php/laravel","title":"Fix Laravel","desc":"Main Flysystem consumer"},{"url":"/php","title":"PHP Security","desc":"All PHP guides"}]},

  # ── Go ─────────────────────────────────────────────────────────────────────
  {"slug":"fix/go/gin","pkg":"Gin","eco":"go","eco_label":"Go","safe_ver":"v1.9.1","install":"go mod tidy","weekly":"N/A",
   "desc":"Gin is Go's most popular HTTP framework. CVEs are relatively rare. The main CVE is a filename enumeration via Content-Disposition header manipulation.",
   "cves":[("CVE-2020-28483",2020,"HIGH",False,True,"v1.7.0","Traversal via Route parameter"),
           ("CVE-2023-29401",2023,"MEDIUM",False,True,"v1.9.1","Filename enumeration via Content-Disposition")],
   "before":'"github.com/gin-gonic/gin v1.7.0"',"after":'"github.com/gin-gonic/gin v1.9.1"',
   "faqs":[("Does Gin have many security CVEs?","No — Gin has had very few direct CVEs given its popularity. Most Go HTTP security issues come from the standard library's net/http, which is maintained by Google. Keep both Gin and Go itself updated."),("Is Gin or Echo faster for security patching?","Both have responsive maintainer teams. For security-sensitive applications, consider also using security middleware like gin-contrib/secure for HTTP security headers.")],
   "related":[{"url":"/fix/go/echo","title":"Fix Echo","desc":"Alternative Go framework"},{"url":"/go","title":"Go Security","desc":"All Go guides"}]},

  {"slug":"fix/go/grpc","pkg":"gRPC-Go","eco":"go","eco_label":"Go","safe_ver":"v1.58.3","install":"go mod tidy","weekly":"N/A",
   "desc":"gRPC-Go is Go's gRPC implementation. CVE-2023-44487 (HTTP/2 Rapid Reset) affected it severely — the patch was released the same day as the coordinated disclosure and CISA KEV addition.",
   "cves":[("CVE-2023-32731",2023,"HIGH",False,True,"v1.55.0","Information disclosure via gRPC metadata"),
           ("CVE-2023-44487",2023,"HIGH",True, True,"v1.58.3","HTTP/2 Rapid Reset DoS — CISA KEV")],
   "before":'"google.golang.org/grpc v1.50.0"',"after":'"google.golang.org/grpc v1.58.3"',
   "faqs":[("What is the HTTP/2 Rapid Reset attack?","An attacker opens many HTTP/2 streams and immediately cancels them with RST_STREAM frames. The server allocates resources for each stream before the cancel arrives — leading to resource exhaustion. At scale this achieved 398 million requests/second in real attacks."),("Does this affect gRPC servers and clients?","Primarily servers — the server is the one allocating resources. Clients are less affected. Update your gRPC-Go server deployments first.")],
   "related":[{"url":"/kev/CVE-2023-44487","title":"KEV: HTTP/2 Rapid Reset","desc":"Full CVE detail"},{"url":"/fix/go/net","title":"Fix golang.org/x/net","desc":"Related HTTP/2 CVE"},{"url":"/go","title":"Go Security","desc":"All Go guides"}]},

  {"slug":"fix/go/echo","pkg":"Echo Framework","eco":"go","eco_label":"Go","safe_ver":"v4.11.4","install":"go mod tidy","weekly":"N/A",
   "desc":"Echo is a high-performance Go HTTP framework. Its CVE count is low — the main known CVE is an open redirect in certain configurations.",
   "cves":[("CVE-2023-29401",2023,"MEDIUM",False,True,"v4.11.2","Open redirect via crafted Location header")],
   "before":'"github.com/labstack/echo/v4 v4.9.0"',"after":'"github.com/labstack/echo/v4 v4.11.4"',
   "faqs":[("Is Echo safer than Gin?","Both have minimal direct CVE histories. The main security considerations for Go HTTP frameworks are their handling of middleware, TLS configuration, and request validation — not just CVE counts."),("How do I add security headers in Echo?","Use Echo's built-in secure middleware: e.Use(middleware.Secure()). This adds HSTS, X-Frame-Options, X-Content-Type-Options, and other security headers automatically.")],
   "related":[{"url":"/fix/go/gin","title":"Fix Gin","desc":"Alternative Go framework"},{"url":"/go","title":"Go Security","desc":"All Go guides"}]},

  {"slug":"fix/go/fiber","pkg":"Fiber","eco":"go","eco_label":"Go","safe_ver":"v2.52.2","install":"go mod tidy","weekly":"N/A",
   "desc":"Fiber is an Express-inspired Go HTTP framework. The main CVE is CVE-2024-22189 — a HTTP/2 CONTINUATION frames flood causing DoS.",
   "cves":[("CVE-2024-22189",2024,"HIGH",False,True,"v2.52.2","DoS via HTTP/2 CONTINUATION frames flood")],
   "before":'"github.com/gofiber/fiber/v2 v2.40.0"',"after":'"github.com/gofiber/fiber/v2 v2.52.2"',
   "faqs":[("What is the HTTP/2 CONTINUATION flood?","An attacker sends a series of HTTP/2 HEADERS frames followed by CONTINUATION frames without the END_HEADERS flag set. The server buffers all frames waiting for the end, consuming memory. Unlike the Rapid Reset attack, this doesn't require cancelling streams."),("Is Fiber suitable for production use?","Fiber is popular for high-performance Go APIs. It's built on Fasthttp rather than net/http — which gives performance benefits but also means it may not be compatible with all net/http middleware.")],
   "related":[{"url":"/fix/go/gin","title":"Fix Gin","desc":"Alternative framework"},{"url":"/go","title":"Go Security","desc":"All Go guides"}]},

  # ── Rust ───────────────────────────────────────────────────────────────────
  {"slug":"fix/rust/actix-web","pkg":"actix-web","eco":"rust","eco_label":"Rust","safe_ver":"4.5.1","install":"cargo update","weekly":"N/A",
   "desc":"actix-web is Rust's most popular HTTP framework. Rust's memory safety eliminates whole classes of CVEs that affect C/C++ frameworks. The main CVEs are logic-level DoS issues.",
   "cves":[("CVE-2020-35901",2020,"HIGH",False,True,"3.0.0","DoS via HTTP/1.1 pipeline parsing"),
           ("CVE-2022-24977",2022,"HIGH",False,True,"4.0.0","DoS via crafted HTTP request in pipelining")],
   "before":'"actix-web = "3.3.2"',"after":'"actix-web = "4.5.1"',
   "faqs":[("Does Rust memory safety prevent all CVEs?","No — Rust prevents memory corruption CVEs (buffer overflows, use-after-free, etc.) but logic bugs, DoS via resource exhaustion, and authentication bypass vulnerabilities can still occur. Rust's CVE rate is much lower than C/C++ frameworks but not zero."),("Is actix-web 4.x stable?","Yes — actix-web 4.0 was released in January 2022 and is the stable long-term branch. It requires Rust 1.57+.")],
   "related":[{"url":"/fix/rust/axum","title":"Fix axum","desc":"Alternative Rust framework"},{"url":"/rust","title":"Rust Security","desc":"All Rust guides"}]},

  {"slug":"fix/rust/axum","pkg":"axum","eco":"rust","eco_label":"Rust","safe_ver":"0.7.5","install":"cargo update","weekly":"N/A",
   "desc":"axum is Tokio's official HTTP framework for Rust, built on hyper and tower. Its main CVE exposure is via the hyper and tokio dependencies (HTTP/2 Rapid Reset).",
   "cves":[("CVE-2023-44487",2023,"HIGH",True,True,"0.6.20","HTTP/2 Rapid Reset via hyper dep — CISA KEV")],
   "before":'"axum = "0.6.18"',"after":'"axum = "0.7.5"',
   "faqs":[("Is axum or actix-web better for security?","Both are actively maintained and have minimal direct CVEs. axum is built on the Tokio ecosystem (hyper, tower) which has strong security practices. actix-web uses its own runtime. The choice usually comes down to ecosystem preference rather than security posture."),("Does axum 0.7 have breaking changes from 0.6?","Yes — axum 0.7 upgraded to hyper 1.0 which has a new API. The axum migration guide covers the changes.")],
   "related":[{"url":"/fix/rust/hyper","title":"Fix hyper","desc":"axum's HTTP dep"},{"url":"/rust","title":"Rust Security","desc":"All Rust guides"}]},

  {"slug":"fix/rust/hyper","pkg":"hyper","eco":"rust","eco_label":"Rust","safe_ver":"1.3.1","install":"cargo update","weekly":"N/A",
   "desc":"hyper is Rust's most widely-used HTTP library, underlying reqwest, axum, and many other crates. CVE-2023-44487 (HTTP/2 Rapid Reset) is on CISA KEV.",
   "cves":[("CVE-2021-21299",2021,"MEDIUM",False,True,"0.14.4","Request smuggling via Transfer-Encoding header"),
           ("CVE-2023-44487",2023,"HIGH",True, True,"1.0.1",  "HTTP/2 Rapid Reset — CISA KEV")],
   "before":'"hyper = "0.14.20"',"after":'"hyper = "1.3.1"',
   "faqs":[("Is there a breaking change between hyper 0.14 and 1.0?","Yes — hyper 1.0 is a complete API redesign. reqwest and axum provide compatibility layers. Most applications use hyper indirectly through these higher-level crates."),("Does the HTTP/2 Rapid Reset affect hyper clients?","Primarily servers. Update hyper server deployments first.")],
   "related":[{"url":"/kev/CVE-2023-44487","title":"KEV: HTTP/2 Rapid Reset","desc":"Full CVE detail"},{"url":"/fix/rust/axum","title":"Fix axum","desc":"Uses hyper"},{"url":"/rust","title":"Rust Security","desc":"All Rust guides"}]},

  {"slug":"fix/rust/openssl","pkg":"openssl","eco":"rust","eco_label":"Rust","safe_ver":"0.10.66","install":"cargo update","weekly":"N/A",
   "desc":"The Rust openssl crate wraps OpenSSL via FFI. When OpenSSL has a CVE, this crate inherits it. CVE-2023-0286 is CRITICAL and on CISA KEV.",
   "cves":[("CVE-2022-0778",2022,"HIGH",False,True,"0.10.40","Infinite loop in BN_mod_sqrt — affects cert parsing"),
           ("CVE-2022-3786",2022,"HIGH",False,True,"0.10.43","Buffer overflow in X.509 cert verification"),
           ("CVE-2022-3602",2022,"HIGH",False,True,"0.10.43","Buffer overflow in X.509 cert verification (variant)"),
           ("CVE-2023-0286",2023,"CRITICAL",True,True,"0.10.48","X.400 type confusion — CISA KEV")],
   "before":'"openssl = "0.10.30"',"after":'"openssl = "0.10.66"',
   "faqs":[("Should I use rustls instead of openssl?","rustls is a pure-Rust TLS implementation with no C dependencies — it's memory-safe by default and doesn't inherit OpenSSL CVEs. For new projects, rustls is recommended. reqwest supports both via feature flags."),("Does openssl = \"0.10.66\" automatically use the latest OpenSSL?","The openssl crate links to the system OpenSSL. The crate version and the OpenSSL version are separate. Keep both updated — the crate version and your system's OpenSSL library.")],
   "related":[{"url":"/kev/CVE-2023-0286","title":"KEV: CVE-2023-0286","desc":"CISA KEV detail"},{"url":"/fix/rust/rustls","title":"Fix rustls","desc":"Pure-Rust alternative"},{"url":"/rust","title":"Rust Security","desc":"All Rust guides"}]},

  {"slug":"fix/rust/rustls","pkg":"rustls","eco":"rust","eco_label":"Rust","safe_ver":"0.23.5","install":"cargo update","weekly":"N/A",
   "desc":"rustls is a pure-Rust TLS implementation that's an alternative to the openssl crate. Its main CVE is CVE-2024-32650 — an infinite loop in certificate chain parsing.",
   "cves":[("CVE-2024-32650",2024,"HIGH",False,True,"0.23.5","Infinite loop via crafted TLS certificate chain")],
   "before":'"rustls = "0.21.6"',"after":'"rustls = "0.23.5"',
   "faqs":[("Is rustls safer than openssl?","rustls has fewer CVEs and no C FFI layer. Memory safety vulnerabilities are impossible by construction. The tradeoff is feature completeness — rustls doesn't support all OpenSSL features. For most TLS use cases, rustls is the safer choice."),("Does CVE-2024-32650 affect rustls clients and servers?","Both — any connection that processes a server's TLS certificate can trigger the infinite loop if the certificate chain is crafted to exploit the parsing bug.")],
   "related":[{"url":"/fix/rust/openssl","title":"Fix openssl","desc":"Alternative TLS implementation"},{"url":"/rust","title":"Rust Security","desc":"All Rust guides"}]},

  # ── Java ───────────────────────────────────────────────────────────────────
  {"slug":"fix/java/jackson-databind","pkg":"Jackson Databind","eco":"java","eco_label":"Java/Maven","safe_ver":"2.17.1","install":"mvn dependency:resolve","weekly":"Millions",
   "desc":"Jackson Databind is the most widely-used Java JSON library. It has a long CVE history — primarily deserialization gadget chains that allowed RCE. The team resolved the fundamental issue by disabling default typing in 2.10.0.",
   "cves":[("CVE-2019-14379",2019,"CRITICAL",False,True,"2.9.9.3","RCE via deserialization gadget chain"),
           ("CVE-2020-25649",2020,"HIGH",    False,True,"2.12.0", "XXE in XML processing via JAXB binding"),
           ("CVE-2022-42003",2022,"HIGH",    False,True,"2.14.0", "DoS via deeply nested JSON deserialization"),
           ("CVE-2022-42004",2022,"HIGH",    False,True,"2.14.0", "DoS via large array deserialization")],
   "before":'"jackson.version>2.13.4</jackson.version"',"after":'"jackson.version>2.17.1</jackson.version"',
   "faqs":[("Does Jackson still have deserialization RCE issues?","Jackson 2.10+ disabled polymorphic deserialization (the root cause of the RCE gadget chains) by default. If you're on 2.10+, you're not affected by the historical RCE CVEs unless you explicitly enable default typing."),("Should I replace Jackson with a different JSON library?","Jackson remains well-maintained and the deserialization RCE class of CVEs is resolved in modern versions. The DoS CVEs (2022) are fixed in 2.14.0. Switching JSON libraries is a significant migration — stay on Jackson with current versions."),("What is a deserialization gadget chain?","A gadget chain is a series of Java class instantiations and method calls that, when triggered via deserialization, execute arbitrary code. The attacker crafts a JSON payload that, when deserialized, triggers the chain.")],
   "related":[{"url":"/fix/java/log4j","title":"Fix Log4j","desc":"Other major Java CVEs"},{"url":"/java","title":"Java Security","desc":"All Java guides"}]},

  {"slug":"fix/java/netty","pkg":"Netty","eco":"java","eco_label":"Java/Maven","safe_ver":"4.1.108.Final","install":"mvn dependency:resolve","weekly":"Millions",
   "desc":"Netty is the most widely-used Java async networking framework — underlying Spring WebFlux, gRPC, Cassandra, and Elasticsearch. CVE-2023-44487 (HTTP/2 Rapid Reset) is on CISA KEV.",
   "cves":[("CVE-2019-20444",2019,"CRITICAL",False,True,"4.1.44.Final","HTTP request smuggling via whitespace"),
           ("CVE-2021-37136",2021,"HIGH",    False,True,"4.1.68.Final","DoS via compression bomb in Brotli decompressor"),
           ("CVE-2021-37137",2021,"HIGH",    False,True,"4.1.68.Final","DoS via compression bomb in Snappy decompressor"),
           ("CVE-2022-41881",2022,"HIGH",    False,True,"4.1.86.Final","DoS via StackOverflow in HaProxyMessageDecoder"),
           ("CVE-2023-44487",2023,"HIGH",    True, True,"4.1.100.Final","HTTP/2 Rapid Reset DoS — CISA KEV")],
   "before":'"netty.version>4.1.77.Final</netty.version"',"after":'"netty.version>4.1.108.Final</netty.version"',
   "faqs":[("Do Spring Boot apps use Netty?","Spring Boot uses Netty when you use the reactive web stack (spring-boot-starter-webflux). Traditional Spring MVC uses embedded Tomcat instead. Check your spring-boot-starter dependency."),("How do I know what Netty version I'm using?","Run mvn dependency:tree | grep netty to see all Netty artifacts and their resolved versions. Or paste your pom.xml into PackageFix.")],
   "related":[{"url":"/kev/CVE-2023-44487","title":"KEV: HTTP/2 Rapid Reset","desc":"Full CVE detail"},{"url":"/fix/java/spring-core","title":"Fix Spring","desc":"Uses Netty in reactive mode"},{"url":"/java","title":"Java Security","desc":"All Java guides"}]},

  {"slug":"fix/java/commons-text","pkg":"Apache Commons Text","eco":"java","eco_label":"Java/Maven","safe_ver":"1.12.0","install":"mvn dependency:resolve","weekly":"Millions",
   "desc":"Commons Text is Apache's string manipulation library. CVE-2022-42889 (Text4Shell) is on CISA KEV — it allows RCE via string interpolation. The attack surface is smaller than Log4Shell but the severity is equivalent.",
   "cves":[("CVE-2022-42889",2022,"CRITICAL",True,True,"1.10.0","Text4Shell — RCE via string interpolation — CISA KEV")],
   "before":'"commons-text.version>1.9</commons-text.version"',"after":'"commons-text.version>1.12.0</commons-text.version"',
   "faqs":[("How is Text4Shell different from Log4Shell?","Both use variable interpolation as the attack vector. Log4Shell exploits JNDI lookups in log messages. Text4Shell exploits StringSubstitutor's script:, dns:, and url: interpolation prefixes. Text4Shell requires the application to explicitly pass untrusted input to StringSubstitutor."),("Is commons-text widely used?","Not as widely as Log4j, but it appears in many enterprise Java applications and Spring projects. Run mvn dependency:tree | grep commons-text to check."),("Does 1.10.0 fix all Text4Shell bypasses?","1.10.0 disables the dangerous interpolation prefixes by default. There have been no confirmed bypasses of the 1.10.0 fix. 1.12.0 is the current latest version.")],
   "related":[{"url":"/kev/CVE-2022-42889","title":"KEV: Text4Shell","desc":"Full CVE detail"},{"url":"/fix/java/log4j","title":"Fix Log4j","desc":"Log4Shell — similar attack"},{"url":"/java","title":"Java Security","desc":"All Java guides"}]},

  {"slug":"fix/java/snakeyaml","pkg":"SnakeYAML","eco":"java","eco_label":"Java/Maven","safe_ver":"2.2","install":"mvn dependency:resolve","weekly":"Millions",
   "desc":"SnakeYAML is the most widely-used YAML parser for Java. CVE-2022-1471 (CISA KEV) allows RCE via unsafe deserialization. It affects Spring Boot 2.x transitively.",
   "cves":[("CVE-2022-25857",2022,"HIGH",    False,True,"1.31",  "DoS via stack overflow via recursive YAML anchors"),
           ("CVE-2022-38749",2022,"MEDIUM",  False,True,"1.31",  "DoS via crafted YAML with many entries"),
           ("CVE-2022-38750",2022,"MEDIUM",  False,True,"1.31",  "DoS via crafted YAML with tab characters"),
           ("CVE-2022-38751",2022,"MEDIUM",  False,True,"1.31",  "DoS via crafted YAML with large float"),
           ("CVE-2022-1471",  2022,"CRITICAL",True,True,"2.0",   "RCE via unsafe deserialization — CISA KEV")],
   "before":'"snakeyaml.version>1.33</snakeyaml.version"',"after":'"snakeyaml.version>2.2</snakeyaml.version"',
   "faqs":[("Does Spring Boot include SnakeYAML?","Yes — Spring Boot uses SnakeYAML to parse application.yaml configuration files. Spring Boot 2.x includes SnakeYAML 1.x. Spring Boot 3.x includes SnakeYAML 2.0. Upgrading to Spring Boot 3.x resolves this transitively."),("Is the fix just to call safe_load instead of load?","In SnakeYAML 2.0, the default constructor no longer allows arbitrary class instantiation. You also need to replace new Yaml().load() with new Yaml(new SafeConstructor(new LoaderOptions())).load() if you can't upgrade immediately.")],
   "related":[{"url":"/kev/CVE-2022-1471","title":"KEV: CVE-2022-1471","desc":"CISA KEV detail"},{"url":"/fix/java/spring-core","title":"Fix Spring","desc":"SnakeYAML consumer"},{"url":"/java","title":"Java Security","desc":"All Java guides"}]},

  {"slug":"fix/java/guava","pkg":"Google Guava","eco":"java","eco_label":"Java/Maven","safe_ver":"33.1.0-jre","install":"mvn dependency:resolve","weekly":"Millions",
   "desc":"Guava is Google's core Java libraries collection. CVEs are rare given how widely it's used. The main CVE is a path traversal in Files.createTempDir() on Linux.",
   "cves":[("CVE-2018-10237",2018,"MEDIUM",False,True,"24.1.1-jre","DoS via ReDoS in Splitter.on"),
           ("CVE-2023-2976",2023,"HIGH",  False,True,"32.0.0-jre","Path traversal via Files.createTempDir() on Linux")],
   "before":'"guava.version>31.0-jre</guava.version"',"after":'"guava.version>33.1.0-jre</guava.version"',
   "faqs":[("Does CVE-2023-2976 affect all Guava users?","Only applications that use Files.createTempDir() on Linux. The method creates a directory in /tmp that is world-readable — any user on the system can read files in it. Replace with Files.createTempDirectory() from Java NIO with appropriate permissions."),("Is Guava safe for production use?","Yes — Guava has an excellent maintenance record and very few CVEs for a library of its size and age. Keep it updated and avoid the deprecated methods the CVEs flag.")],
   "related":[{"url":"/java","title":"Java Security","desc":"All Java guides"}]},
]

# ── Generate CVE history pages ─────────────────────────────────────────────

def gen_history(data):
    slug = data["slug"]
    pkg = data["pkg"]
    eco = data["eco"]
    eco_label = data["eco_label"]
    safe_ver = data["safe_ver"]
    install = data["install"]
    weekly = data["weekly"]
    desc = data["desc"]
    cves = data["cves"]
    before = data["before"]
    after = data["after"]
    faqs = data["faqs"]
    related = data["related"]

    path = f"/{slug}"
    total = len(cves)
    critical = sum(1 for c in cves if c[2] == "CRITICAL")
    kev_count = sum(1 for c in cves if c[3])

    kev_note = f'<p style="margin:8px 0 0;font-size:11px;color:var(--red)">🔴 {kev_count} CVE{"s" if kev_count > 1 else ""} on CISA KEV — actively exploited in real attacks</p>' if kev_count else ""

    body = f"""
<h1>All {pkg} CVEs — Complete Vulnerability History</h1>
<p class="lead">{desc}</p>
<div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:24px">
  <span class="badge badge-purple">{eco_label}</span>
  <span class="badge badge-muted">{weekly} weekly downloads</span>
  <span class="badge badge-muted">{total} CVE{"s" if total > 1 else ""} total</span>
  {'<span class="badge badge-red">' + str(critical) + ' CRITICAL</span>' if critical else ''}
  {'<span class="badge badge-red">🔴 CISA KEV</span>' if kev_count else ''}
</div>
<h2>Full CVE history</h2>
{kev_note}
{cve_table(cves)}
<h2>Current safe version: {safe_ver}</h2>
<pre style="margin-bottom:4px"># Before</pre>
<pre>{before}</pre>
<pre style="margin-bottom:4px"># After</pre>
<pre>{after}</pre>
<p style="margin-top:8px">Then run: <code>{install}</code></p>
{cta()}
{faq_html(faqs)}
{related_html(related)}
"""

    schemas = [
        {"@type": "ItemList",
         "name": f"All {pkg} CVEs",
         "description": f"Complete CVE history for {pkg} — {total} known vulnerabilities",
         "numberOfItems": total,
         "itemListElement": [
             {"@type": "ListItem", "position": i+1, "name": c[0], "url": f"https://osv.dev/vulnerability/{c[0]}"}
             for i, c in enumerate(cves)
         ]},
        {"@type": "BreadcrumbList",
         "itemListElement": [
             {"@type": "ListItem", "position": 1, "name": "PackageFix", "item": BASE_URL},
             {"@type": "ListItem", "position": 2, "name": "Fix Guides", "item": BASE_URL + "/fix"},
             {"@type": "ListItem", "position": 3, "name": eco_label, "item": BASE_URL + f"/{eco}"},
             {"@type": "ListItem", "position": 4, "name": pkg, "item": BASE_URL + path}
         ]},
        {"@type": "FAQPage",
         "mainEntity": [
             {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
             for q, a in faqs
         ]}
    ]

    title = f"All {pkg} CVEs — Complete {eco_label} Vulnerability History | PackageFix"
    meta_desc = (
        f"{pkg} has {total} known CVEs. "
        f"{'Includes CISA KEV — actively exploited. ' if kev_count else ''}"
        f"Safe version: {safe_ver}. Full history with fix guide."
    )
    return shell(title, meta_desc, path,
        [("PackageFix", "/"), ("Fix Guides", "/fix"), (eco_label, f"/{eco}"), (pkg, None)],
        body, schemas)

print("\n📋 Generating remaining CVE history pages...")
for data in REMAINING_HISTORIES:
    write(data["slug"], gen_history(data))


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
        content = f.read()
    updated = content.replace("</urlset>", new_urls + "</urlset>")
else:
    updated = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + new_urls + "</urlset>"
with open("sitemap-seo.xml", "w") as f:
    f.write(updated)
print(f"  ✓ sitemap-seo.xml — {len(all_paths)} new URLs")

print("\n🤖 Updating llm.txt...")
with open("llm.txt", "a") as f:
    f.write("\n## Closing Items — Compare index, Glossary, CVE history\n")
    for p in all_paths:
        f.write(f"{BASE_URL}{p}\n")
print("  ✓ llm.txt updated")

print(f"\n✅ Done — {len(all_paths)} pages generated/enriched")
counts = {"compare": 0, "glossary": 0, "history": 0}
for p in all_paths:
    if p.startswith("/compare"): counts["compare"] += 1
    elif p.startswith("/glossary"): counts["glossary"] += 1
    else: counts["history"] += 1
print(f"   /compare index:       {counts['compare']} page")
print(f"   Glossary terms:       {counts['glossary']} pages")
print(f"   CVE history (new/enriched): {counts['history']} pages")

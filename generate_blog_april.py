#!/usr/bin/env python3
"""
PackageFix Blog Posts - April 2026 Batch
1. Weekly CVE Digest #3 (April 1, 2026)
2. Transitive Package Vulnerability Guide
3. multer 1.4.5-lts.1 Deep Dive
4. Ruby on Rails Security Releases 2024
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
h2{font-size:14px;font-weight:600;margin:36px 0 12px}
h3{font-size:13px;font-weight:600;margin:24px 0 8px}
p{color:var(--muted);margin-bottom:12px;font-size:12px;line-height:1.7}
.lead{color:var(--text);font-size:13px;margin-bottom:24px;line-height:1.7}
.meta{font-size:11px;color:var(--muted);margin-bottom:32px}
.kev-banner{background:rgba(239,68,68,.12);border:1px solid var(--red);border-radius:10px;padding:16px 20px;margin:24px 0}
.kev-banner .label{font-size:10px;font-weight:700;color:var(--red);text-transform:uppercase;letter-spacing:.1em;margin-bottom:6px}
.kev-banner p{color:var(--red);margin:0;font-size:12px}
.warning-box{background:rgba(249,115,22,.08);border:1px solid rgba(249,115,22,.3);border-left:3px solid var(--orange);border-radius:8px;padding:16px 20px;margin:20px 0}
.warning-box .label{font-size:10px;font-weight:700;color:var(--orange);text-transform:uppercase;letter-spacing:.1em;margin-bottom:8px}
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
.digest-item{border-bottom:1px solid var(--border);padding:24px 0}
.digest-item:last-child{border-bottom:none}
.digest-item h3{font-size:13px;font-weight:600;margin:0 0 8px;color:var(--text)}
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

def page(title, desc, path, date, body, schemas):
    canonical = BASE_URL + path
    sj = json.dumps({"@context": "https://schema.org", "@graph": schemas}, indent=2)
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
        '<div class="breadcrumb">'
        '<a href="/">PackageFix</a> <span style="color:var(--border)">/</span> '
        '<a href="/blog">Blog</a> <span style="color:var(--border)">/</span> '
        '<span style="color:var(--text)">' + title.split('|')[0].strip() + '</span>'
        '</div>'
        + body +
        '</main>'
        '<footer class="site-footer">'
        '<p>PackageFix &middot; <a href="/">packagefix.dev</a> &middot; MIT Licensed &middot; Open Source</p>'
        '<p style="margin-top:6px">Part of the MetricLogic network &middot; '
        '<a href="https://configclarity.dev">ConfigClarity</a> &middot; '
        '<a href="https://domainpreflight.dev">DomainPreflight</a></p>'
        '</footer></body></html>'
    )

def cta():
    return (
        '<div class="cta-box">'
        '<p>Paste your manifest &mdash; PackageFix scans every dependency against OSV and CISA KEV instantly.</p>'
        '<a href="/" class="cta-btn">Scan with PackageFix &rarr;</a>'
        '<p style="margin-top:12px;font-size:11px;color:var(--muted)">Free &middot; No signup &middot; No CLI &middot; Runs in your browser</p>'
        '</div>'
    )

def related(pages):
    cards = ''.join(
        '<div class="related-card"><a href="' + p['url'] + '">' + p['title'] + '</a><p>' + p['desc'] + '</p></div>'
        for p in pages
    )
    return '<div style="margin:40px 0"><h2>Related</h2><div class="related-grid">' + cards + '</div></div>'

def faq(items):
    html = '<div class="faq"><h2>Common questions</h2>'
    for q, a in items:
        html += '<div class="faq-item"><div class="faq-q">' + q + '</div><div class="faq-a">' + a + '</div></div>'
    return html + '</div>'

all_paths = []

def write(slug, html):
    p = os.path.join("seo", slug, "index.html")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(html)
    all_paths.append("/" + slug)
    print("  OK /" + slug)


# =========================================================================
# POST 1 - Weekly CVE Digest #3 - April 1, 2026
# =========================================================================
print("\nGenerating weekly CVE digest #3...")

DIGEST3 = [
    ("CVE-2024-29041", "express", "npm", "MEDIUM", "4.17.x", "4.19.2",
     "Open redirect via res.redirect() with user-controlled URLs. Any Express app passing user input to res.redirect() is affected. Common in OAuth callback handlers. Fix: update to 4.19.2.",
     "/fix/npm/express"),
    ("CVE-2024-21508", "mysql2", "npm", "CRITICAL", "below 3.9.7", "3.9.7",
     "Remote code execution via SQL injection in prepared statement handling. CRITICAL - update immediately if your app uses mysql2 with any user-controlled input in queries.",
     "/fix/npm/mysql2"),
    ("CVE-2024-34069", "Werkzeug", "PyPI", "CRITICAL", "below 3.0.3", "3.0.3",
     "RCE via Werkzeug debugger PIN bypass. Only affects apps running with debug=True. Never run debug mode in production. Update to 3.0.3 and verify APP_DEBUG=False.",
     "/fix/pypi/werkzeug"),
    ("CVE-2024-22189", "fiber", "Go", "HIGH", "below v2.52.2", "v2.52.2",
     "DoS via HTTP/2 CONTINUATION frames flood. Any Fiber server accepting HTTP/2 connections is affected. Part of the broader 2024 HTTP/2 vulnerability class.",
     "/fix/go/fiber"),
    ("CVE-2024-32650", "rustls", "Rust", "HIGH", "below 0.23.5", "0.23.5",
     "Infinite loop via crafted TLS certificate chain. Any Rust server using rustls that processes TLS connections from untrusted clients is affected.",
     "/fix/rust/rustls"),
    ("CVE-2024-1135", "gunicorn", "PyPI", "HIGH", "below 22.0.0", "22.0.0",
     "HTTP request smuggling via invalid Transfer-Encoding header. Affects all gunicorn deployments behind a reverse proxy. Update to 22.0.0.",
     "/fix/pypi/gunicorn"),
]

d3_items = ""
for cve, pkg, eco, sev, vuln, safe, desc, fix_url in DIGEST3:
    sc = "badge-red" if sev == "CRITICAL" else "badge-orange" if sev == "HIGH" else "badge-purple"
    d3_items += (
        '<div class="digest-item">'
        '<h3><a href="https://osv.dev/vulnerability/' + cve + '" target="_blank" rel="noopener">' + cve + '</a>'
        ' &mdash; ' + pkg + ' <span class="badge ' + sc + '">' + sev + '</span></h3>'
        '<p><strong>Ecosystem:</strong> ' + eco + ' &nbsp;&nbsp; '
        '<strong>Affected:</strong> ' + vuln + ' &nbsp;&nbsp; '
        '<strong>Fix:</strong> ' + safe + '</p>'
        '<p>' + desc + '</p>'
        '<p><a href="' + fix_url + '">Full fix guide &rarr;</a></p>'
        '</div>'
    )

digest3_body = (
    '<h1>Weekly CVE Digest &mdash; April 1, 2026</h1>'
    '<p class="meta">April 1, 2026 &middot; PackageFix &middot; 6 CVEs this week across npm, PyPI, Go, Rust</p>'
    '<p class="lead">Two CRITICAL CVEs this week: mysql2 RCE and Werkzeug debugger bypass. '
    'Six total across npm, PyPI, Go, and Rust. '
    'Paste your manifest into PackageFix to check if you are affected.</p>'
    + d3_items
    + cta()
    + related([
        {"url": "/blog/weekly-cve-march-29-2026", "title": "Last Week", "desc": "March 29 digest"},
        {"url": "/blog/weekly-cve-march-2026", "title": "March 22 digest", "desc": "7 CVEs"},
        {"url": "/cisa-kev", "title": "CISA KEV", "desc": "All actively exploited packages"},
        {"url": "/fix/npm/mysql2", "title": "Fix mysql2", "desc": "CRITICAL RCE"},
    ])
)

write("blog/weekly-cve-april-1-2026", page(
    "Weekly CVE Digest - April 1, 2026 | PackageFix",
    "6 CVEs this week: mysql2 RCE (CRITICAL), Werkzeug debugger RCE (CRITICAL), gunicorn HTTP smuggling, rustls infinite loop, express open redirect, fiber HTTP/2 DoS.",
    "/blog/weekly-cve-april-1-2026",
    "2026-04-01",
    digest3_body,
    [
        {"@type": "Article",
         "headline": "Weekly CVE Digest - April 1, 2026",
         "description": "6 CVEs this week including 2 CRITICAL: mysql2 RCE and Werkzeug debugger bypass.",
         "datePublished": "2026-04-01", "dateModified": "2026-04-01",
         "author": {"@type": "Organization", "name": "PackageFix", "url": BASE_URL}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "PackageFix", "item": BASE_URL},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": BASE_URL + "/blog"},
            {"@type": "ListItem", "position": 3, "name": "Weekly CVE Digest April 1 2026", "item": BASE_URL + "/blog/weekly-cve-april-1-2026"}
        ]}
    ]
))


# =========================================================================
# POST 2 - Transitive Package Vulnerability Guide
# =========================================================================
print("\nGenerating transitive vulnerability guide...")

transitive_faqs = [
    ("How do I find transitive vulnerabilities?",
     "npm audit and pip audit show transitive vulnerabilities but don't always make it clear which direct dependency is pulling in the vulnerable package. PackageFix shows the full dependency path: Your App -> express -> qs -> [vulnerable version]. You can also run npm ls [package-name] to see which packages pull in a specific dependency."),
    ("Can npm audit fix transitive vulnerabilities automatically?",
     "npm audit fix --force can sometimes resolve transitive vulnerabilities by upgrading the parent package. But if the parent package hasn't released a version that uses the safe transitive version, npm audit fix won't help. That's when npm overrides are the solution."),
    ("What is an npm override and when should I use it?",
     "An npm override forces a specific version of a package regardless of what parent packages request. Use it when a transitive dependency has a CVE but the parent package hasn't released a fix yet. Add it to your package.json overrides field. PackageFix generates the exact overrides block you need."),
    ("Are transitive vulnerabilities actually exploitable?",
     "It depends on whether the vulnerable code path is reachable from your application - this is called reachability analysis. A CVE in a package your app never calls is technically present but may not be practically exploitable. CISA KEV entries are confirmed exploited in real attacks regardless of reachability."),
    ("How many levels deep can transitive dependencies go?",
     "In large Node.js projects, dependency trees commonly go 10-15 levels deep. A vulnerability at any level can affect your application. The minimist CVE (CVE-2021-44906) affected thousands of packages because minimist was a transitive dependency 5-8 levels deep in many common tools.")
]

transitive_body = (
    '<h1>What is a Transitive Package Vulnerability? Real Examples and How to Fix Them</h1>'
    '<p class="meta">April 1, 2026 &middot; PackageFix &middot; 8 min read</p>'
    '<p class="lead">Transitive vulnerabilities are CVEs in packages your app does not directly depend on - '
    'but pulls in indirectly through another package. They are harder to find, harder to fix, '
    'and account for the majority of CVEs in most production applications.</p>'

    '<h2>Direct vs transitive dependencies</h2>'
    '<p>Your package.json lists your direct dependencies - the packages you chose to install. '
    'Each of those packages has its own dependencies, which have their own dependencies, and so on. '
    'The full tree can contain hundreds of packages from a handful of direct dependencies.</p>'
    '<p>A direct dependency vulnerability is straightforward: update the package in your package.json. '
    'A transitive vulnerability is more complex: you do not control that package directly - '
    'it is managed by one of your direct dependencies.</p>'

    '<pre>'
    'Your app\n'
    '  express 4.17.1   (direct)\n'
    '    qs 6.5.2       (transitive - CVE-2022-24999)\n'
    '      ---> VULNERABLE\n'
    '</pre>'

    '<h2>Real example: qs via Express</h2>'
    '<p>CVE-2022-24999 is a prototype pollution vulnerability in the qs query string library. '
    'Most developers who had this vulnerability had never heard of qs - '
    'it was pulled in automatically by Express to parse HTTP query strings.</p>'
    '<p>npm audit flagged it. But updating qs directly in package.json did nothing - '
    'Express controlled which version of qs it used. The fix required either updating Express '
    'to 4.18.0+ (which bundled a safe qs) or using an npm override.</p>'

    '<div class="fix-box">'
    '<div class="label">The fix - npm overrides</div>'
    '<pre>'
    '// package.json\n'
    '{\n'
    '  "dependencies": {\n'
    '    "express": "4.17.1"\n'
    '  },\n'
    '  "overrides": {\n'
    '    "qs": "6.11.0"\n'
    '  }\n'
    '}'
    '</pre>'
    '</div>'

    '<h2>Real example: minimist - the CVE that was everywhere</h2>'
    '<p>CVE-2021-44906 (CVSS 9.8, CISA KEV) is a prototype pollution in minimist - '
    'a tiny argument parser. minimist itself is almost never a direct dependency. '
    'But it was a transitive dependency of npm, webpack, mocha, eslint, and thousands of other tools.</p>'
    '<p>Running npm ls minimist on a typical Node.js project in 2022 would show '
    'minimist appearing 20-30 times, pulled in from different parent packages at different levels. '
    'The only practical fix was an npm override forcing the safe version across the entire tree.</p>'

    '<pre>'
    '// package.json\n'
    '{\n'
    '  "overrides": {\n'
    '    "minimist": "1.2.6"\n'
    '  }\n'
    '}'
    '</pre>'

    '<h2>Real example: Log4Shell - the transitive CVE that broke the internet</h2>'
    '<p>CVE-2021-44228 (Log4Shell, CVSS 10.0) is the most severe transitive vulnerability ever discovered. '
    'Log4j was a logging library - most Java applications that had it did not know they had it. '
    'It was a transitive dependency of thousands of enterprise Java frameworks.</p>'
    '<p>Organizations that did not know their full dependency tree had no idea they were vulnerable. '
    'This incident more than any other drove adoption of SBOMs and dependency scanning tools.</p>'

    '<h2>How PackageFix handles transitive vulnerabilities</h2>'
    '<p>Paste your manifest and lockfile into PackageFix. The lockfile contains the full resolved '
    'dependency tree including all transitive packages. PackageFix scans every package in the tree '
    'against OSV and CISA KEV, shows the dependency path for each vulnerability, '
    'and generates the npm overrides block to fix transitive CVEs where no parent update is available.</p>'

    + cta()
    + faq(transitive_faqs)
    + related([
        {"url": "/glossary/transitive-dependency", "title": "What is a Transitive Dependency", "desc": "Plain-English definition"},
        {"url": "/glossary/prototype-pollution", "title": "Prototype Pollution", "desc": "Most common transitive CVE class"},
        {"url": "/fix/npm/qs", "title": "Fix qs", "desc": "The Express transitive CVE"},
        {"url": "/fix/npm/minimist", "title": "Fix minimist", "desc": "CISA KEV transitive CVE"},
        {"url": "/kev/CVE-2021-44228", "title": "Log4Shell", "desc": "The most severe transitive CVE"},
        {"url": "/guides/github-actions", "title": "Automate in CI", "desc": "Catch transitive CVEs before they ship"},
    ])
)

write("blog/transitive-package-vulnerability-fix", page(
    "Transitive Package Vulnerability - What It Is and How to Fix It | PackageFix",
    "Transitive vulnerabilities are CVEs in packages you did not install directly. Real examples: qs via Express, minimist, Log4Shell. How to fix with npm overrides.",
    "/blog/transitive-package-vulnerability-fix",
    "2026-04-01",
    transitive_body,
    [
        {"@type": "Article",
         "headline": "What is a Transitive Package Vulnerability? Real Examples and How to Fix Them",
         "description": "Transitive vulnerabilities are CVEs in packages pulled in indirectly. Real examples with npm overrides fix instructions.",
         "datePublished": "2026-04-01", "dateModified": "2026-04-01",
         "author": {"@type": "Organization", "name": "PackageFix", "url": BASE_URL}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "PackageFix", "item": BASE_URL},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": BASE_URL + "/blog"},
            {"@type": "ListItem", "position": 3, "name": "Transitive Package Vulnerability Guide", "item": BASE_URL + "/blog/transitive-package-vulnerability-fix"}
        ]},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in transitive_faqs
        ]}
    ]
))


# =========================================================================
# POST 3 - multer 1.4.5-lts.1 Deep Dive
# =========================================================================
print("\nGenerating multer deep dive...")

multer_faqs = [
    ("Why is the version 1.4.5-lts.1 and not just 1.4.5?",
     "multer 1.4.4 had a CRITICAL prototype pollution vulnerability (CVE-2022-24434). The maintainers released a patched version as 1.4.5-lts.1 rather than 1.4.5 to signal it was a long-term support security patch, not a feature release. The -lts.1 suffix is unconventional for npm but common in some ecosystems. It is a valid semver pre-release identifier."),
    ("Does npm update to 1.4.5-lts.1 automatically?",
     'No - npm does not automatically install pre-release versions. If your package.json has "multer": "^1.4.4", npm will not upgrade to 1.4.5-lts.1 because pre-release versions are excluded from semver range matching by default. You must explicitly update: npm install multer@1.4.5-lts.1.'),
    ("Is multer 2.x available?",
     "multer 2.x is in development but has not been officially released as of early 2026. The current safe version is 1.4.5-lts.1. Check the multer GitHub repo for the latest status before deciding whether to wait for v2 or pin to 1.4.5-lts.1."),
    ("What is CVE-2022-24434?",
     "CVE-2022-24434 is a denial of service vulnerability in multer's multipart form parsing. A crafted multipart request can cause multer to hang indefinitely, blocking the Node.js event loop and taking down the server. In Node.js's single-threaded model, a single malicious request can affect all concurrent users."),
    ("Does multer 1.4.5-lts.1 have any breaking changes from 1.4.4?",
     "No - 1.4.5-lts.1 is a security patch only. The API is identical to 1.4.4. Updating requires no code changes - just the version number in package.json and a npm install.")
]

multer_body = (
    '<h1>multer 1.4.5-lts.1 &mdash; What Changed, Why the Version String is Weird, and How to Update</h1>'
    '<p class="meta">April 1, 2026 &middot; PackageFix &middot; 5 min read</p>'
    '<p class="lead">multer 1.4.5-lts.1 is confusing a lot of developers. The version string looks wrong. '
    'npm does not auto-update to it. Here is what happened, why the version is named this way, '
    'and the exact commands to update.</p>'

    '<h2>What happened with multer</h2>'
    '<p>multer 1.4.4 and below have CVE-2022-24434 &mdash; a denial of service vulnerability '
    'in multipart form parsing. A crafted HTTP request can cause multer to hang the Node.js event loop, '
    'effectively taking down your server.</p>'
    '<p>The fix was released as version <strong>1.4.5-lts.1</strong>. '
    'Not 1.4.5. Not 2.0.0. The unusual version string is causing confusion &mdash; '
    'developers see it and think it is not a real release, or their version managers skip it.</p>'

    '<h2>Why the version is called 1.4.5-lts.1</h2>'
    '<p>In semver, anything after a hyphen is a pre-release identifier. '
    'So 1.4.5-lts.1 is technically a pre-release of 1.4.5. '
    'This means <code>npm install multer</code> and <code>npm update multer</code> '
    'will NOT install it unless you ask explicitly &mdash; '
    'npm skips pre-release versions by default.</p>'
    '<p>The maintainers used this naming to signal it was a security-focused LTS patch '
    'rather than a standard feature release. The intention was good '
    'but the side effect is that millions of projects are still running vulnerable versions '
    'because their package managers quietly skipped the update.</p>'

    '<div class="warning-box">'
    '<div class="label">Why npm audit fix does not always work</div>'
    '<p style="margin:0">If you run <code>npm audit fix</code> on a project with vulnerable multer, '
    'it may report "0 vulnerabilities fixed" even though the vulnerability exists. '
    'This is because npm treats 1.4.5-lts.1 as a pre-release and will not upgrade to it '
    'automatically via audit fix. You must update manually.</p>'
    '</div>'

    '<h2>How to update - exact commands</h2>'
    '<pre>'
    '# Check your current version\n'
    'npm list multer\n\n'
    '# Update to the safe version\n'
    'npm install multer@1.4.5-lts.1\n\n'
    '# Verify the update\n'
    'npm list multer\n'
    '# Should show: multer@1.4.5-lts.1\n\n'
    '# Commit the lockfile\n'
    'git add package.json package-lock.json\n'
    'git commit -m "fix: update multer to 1.4.5-lts.1 (CVE-2022-24434)"'
    '</pre>'

    '<h2>If multer is a transitive dependency</h2>'
    '<p>Some projects pull in multer indirectly through another package. '
    'If <code>npm list multer</code> shows it under another package (not directly under your project), '
    'you need an npm override:</p>'
    '<pre>'
    '// package.json\n'
    '{\n'
    '  "overrides": {\n'
    '    "multer": "1.4.5-lts.1"\n'
    '  }\n'
    '}'
    '</pre>'

    '<h2>Is multer 2.x coming?</h2>'
    '<p>multer 2.x is in development as of early 2026 but has not been officially released. '
    'For now, 1.4.5-lts.1 is the safe version to use. '
    'There are no known CVEs in 1.4.5-lts.1.</p>'

    + cta()
    + faq(multer_faqs)
    + related([
        {"url": "/fix/npm/multer", "title": "multer CVE History", "desc": "All known vulnerabilities"},
        {"url": "/blog/transitive-package-vulnerability-fix", "title": "Transitive Vulnerabilities", "desc": "When multer is indirect"},
        {"url": "/glossary/remediation", "title": "Remediation Guide", "desc": "Fix strategies"},
        {"url": "/fix/npm/express", "title": "Fix Express", "desc": "Related npm security"},
    ])
)

write("blog/multer-1-4-5-lts-1-update-guide", page(
    "multer 1.4.5-lts.1 - Why npm Skips It and How to Update | PackageFix",
    "multer 1.4.5-lts.1 fixes CVE-2022-24434 but npm audit fix skips it because it is a pre-release version. Exact commands to update manually and fix transitive multer vulnerabilities.",
    "/blog/multer-1-4-5-lts-1-update-guide",
    "2026-04-01",
    multer_body,
    [
        {"@type": "Article",
         "headline": "multer 1.4.5-lts.1 - What Changed and How to Update",
         "description": "multer 1.4.5-lts.1 fixes CVE-2022-24434 but npm skips it automatically. Here is why and how to update manually.",
         "datePublished": "2026-04-01", "dateModified": "2026-04-01",
         "author": {"@type": "Organization", "name": "PackageFix", "url": BASE_URL}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "PackageFix", "item": BASE_URL},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": BASE_URL + "/blog"},
            {"@type": "ListItem", "position": 3, "name": "multer 1.4.5-lts.1 Guide", "item": BASE_URL + "/blog/multer-1-4-5-lts-1-update-guide"}
        ]},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in multer_faqs
        ]}
    ]
))


# =========================================================================
# POST 4 - Ruby on Rails Security Releases 2024
# =========================================================================
print("\nGenerating Rails security releases post...")

RAILS_2024 = [
    ("CVE-2024-26143", "Feb 2024", "HIGH",    "7.1.3.1 / 7.0.8.1 / 6.1.7.7", "XSS via Action Text content"),
    ("CVE-2024-26142", "Feb 2024", "HIGH",    "7.1.3.1 / 7.0.8.1 / 6.1.7.7", "ReDoS via header parsing"),
    ("CVE-2024-28103", "Jun 2024", "MEDIUM",  "7.1.3.4 / 7.0.8.4 / 6.1.7.8", "Possible header injection in CORS headers"),
    ("CVE-2024-41128", "Oct 2024", "HIGH",    "7.2.1.1 / 7.1.4.1 / 7.0.8.5", "ReDoS in query parameter parsing"),
    ("CVE-2024-47887", "Oct 2024", "HIGH",    "7.2.1.1 / 7.1.4.1 / 7.0.8.5", "DoS via large multipart form"),
    ("CVE-2024-47888", "Oct 2024", "MEDIUM",  "7.2.1.1 / 7.1.4.1 / 7.0.8.5", "DoS via crafted Accept header"),
    ("CVE-2024-47889", "Oct 2024", "MEDIUM",  "7.2.1.1 / 7.1.4.1 / 7.0.8.5", "DoS via crafted Content-Type header"),
    ("CVE-2024-54133", "Dec 2024", "HIGH",    "7.2.2.1 / 7.1.5.1",            "Action Pack host authorization bypass"),
]

rails_rows = ""
for cve, date, sev, fix_ver, desc in RAILS_2024:
    sc = "badge-red" if sev == "CRITICAL" else "badge-orange" if sev == "HIGH" else "badge-purple"
    rails_rows += (
        '<tr>'
        '<td><a href="https://osv.dev/vulnerability/' + cve + '" target="_blank" rel="noopener">' + cve + '</a></td>'
        '<td>' + date + '</td>'
        '<td><span class="badge ' + sc + '">' + sev + '</span></td>'
        '<td style="color:var(--muted)">' + desc + '</td>'
        '<td style="color:var(--green);font-size:11px">' + fix_ver + '</td>'
        '</tr>'
    )

rails_faqs = [
    ("How do I update Rails to the latest security release?",
     "Update your Gemfile: gem 'rails', '~> 7.1.0'. Then run bundle update rails. Always run your full test suite after updating Rails. Check the Rails security mailing list at groups.google.com/g/rubyonrails-security for announcements."),
    ("Does Rails backport security fixes to older versions?",
     "Yes - Rails backports security fixes to all currently supported branches. When a CVE is released, patches are available for the two most recent major versions simultaneously. Rails 6.1 reached end of life in June 2024 - upgrade to 7.0 or 7.1 to continue receiving security patches."),
    ("How do I know which Rails security releases affect my version?",
     "Each CVE announcement lists the affected version ranges and patched versions. The Rails blog at rubyonrails.org/blog and the rubyonrails-security Google Group publish all security releases. PackageFix checks your Gemfile against the OSV database which includes all Rails CVEs."),
    ("What is the current supported Rails version in 2026?",
     "As of early 2026, Rails 7.1 and 7.2 are the actively maintained branches. Rails 7.0 is in security-only maintenance. Rails 6.1 and below are end of life. For new projects, use Rails 7.2.")
]

rails_body = (
    '<h1>Ruby on Rails Security Releases 2024 &mdash; Complete CVE List</h1>'
    '<p class="meta">April 1, 2026 &middot; PackageFix &middot; 6 min read</p>'
    '<p class="lead">Rails had 8 security releases in 2024 spanning CVEs in Action Pack, Action Text, '
    'and the query parser. Four of them were released together in October 2024 &mdash; '
    'the largest single security release batch in recent Rails history. '
    'Here is every CVE, the affected versions, and the exact patch version to update to.</p>'

    '<h2>All Rails CVEs in 2024</h2>'
    '<table style="width:100%;border-collapse:collapse;font-size:12px;margin:16px 0">'
    '<thead><tr style="border-bottom:2px solid var(--border)">'
    '<th style="text-align:left;padding:10px 12px;color:var(--muted);font-size:10px;text-transform:uppercase">CVE</th>'
    '<th style="text-align:left;padding:10px 12px;color:var(--muted);font-size:10px;text-transform:uppercase">Date</th>'
    '<th style="text-align:left;padding:10px 12px;color:var(--muted);font-size:10px;text-transform:uppercase">Severity</th>'
    '<th style="text-align:left;padding:10px 12px;color:var(--muted);font-size:10px;text-transform:uppercase">Description</th>'
    '<th style="text-align:left;padding:10px 12px;color:var(--muted);font-size:10px;text-transform:uppercase">Fix version</th>'
    '</tr></thead>'
    '<tbody>' + rails_rows + '</tbody>'
    '</table>'

    '<h2>The October 2024 batch</h2>'
    '<p>On October 15, 2024, the Rails team released patches for four CVEs simultaneously across '
    'Rails 7.2, 7.1, and 7.0. This is the standard Rails security release process &mdash; '
    'vulnerabilities are held until all supported versions are patched, then released together.</p>'
    '<p>CVE-2024-41128 (ReDoS in query parsing) is the most serious of the four. '
    'An attacker sending a crafted query string can cause the Rails router to hang, '
    'blocking the request thread. In multi-threaded Puma deployments, enough of these '
    'requests can exhaust the thread pool.</p>'

    '<h2>CVE-2024-54133 - December host authorization bypass</h2>'
    '<p>The final 2024 Rails CVE was CVE-2024-54133 in December &mdash; '
    'a host authorization bypass in Action Pack. '
    'Applications using ActionDispatch::HostAuthorization middleware '
    'with certain configurations could be bypassed by a crafted Host header. '
    'This affects applications restricting access by hostname. '
    'Fix version: 7.2.2.1 or 7.1.5.1.</p>'

    '<h2>How to stay current with Rails security releases</h2>'
    '<p>The Rails security mailing list publishes all CVEs as they are released. '
    'Subscribe at groups.google.com/g/rubyonrails-security. '
    'The rubyonrails.org/blog also publishes all security releases. '
    'Use PackageFix to check your current Gemfile against all known CVEs instantly.</p>'

    '<div class="fix-box">'
    '<div class="label">Update Rails</div>'
    '<pre>'
    '# Update to latest security release\n'
    'bundle update rails\n\n'
    '# Or pin to specific version in Gemfile\n'
    "gem 'rails', '~> 7.1.5'\n\n"
    '# Verify\n'
    'bundle exec rails --version'
    '</pre>'
    '</div>'

    + cta()
    + faq(rails_faqs)
    + related([
        {"url": "/fix/ruby/rails", "title": "Rails CVE History", "desc": "All Rails CVEs"},
        {"url": "/fix/ruby/actionpack", "title": "Fix actionpack", "desc": "Rails component CVEs"},
        {"url": "/fix/ruby/rack", "title": "Fix Rack", "desc": "Rails server interface"},
        {"url": "/ruby", "title": "Ruby Security", "desc": "All Ruby CVE guides"},
    ])
)

write("blog/ruby-on-rails-security-releases-2024", page(
    "Ruby on Rails Security Releases 2024 - Complete CVE List | PackageFix",
    "All 8 Ruby on Rails security CVEs in 2024 including the October batch (CVE-2024-41128, CVE-2024-47887) and December host authorization bypass. Affected versions and fix versions for Rails 7.0, 7.1, 7.2.",
    "/blog/ruby-on-rails-security-releases-2024",
    "2026-04-01",
    rails_body,
    [
        {"@type": "Article",
         "headline": "Ruby on Rails Security Releases 2024 - Complete CVE List",
         "description": "All 8 Rails security CVEs in 2024. October batch plus December host authorization bypass. Fix versions for Rails 7.0, 7.1, 7.2.",
         "datePublished": "2026-04-01", "dateModified": "2026-04-01",
         "author": {"@type": "Organization", "name": "PackageFix", "url": BASE_URL}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "PackageFix", "item": BASE_URL},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": BASE_URL + "/blog"},
            {"@type": "ListItem", "position": 3, "name": "Rails Security Releases 2024", "item": BASE_URL + "/blog/ruby-on-rails-security-releases-2024"}
        ]},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in rails_faqs
        ]}
    ]
))


# =========================================================================
# UPDATE SITEMAP + VERCEL
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
    new_urls += "  <url>\n    <loc>" + BASE_URL + p + "</loc>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>\n"

if os.path.exists("sitemap-seo.xml"):
    with open("sitemap-seo.xml") as f:
        content = f.read()
    updated = content.replace("</urlset>", new_urls + "</urlset>")
else:
    updated = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + new_urls + "</urlset>"
with open("sitemap-seo.xml", "w") as f:
    f.write(updated)

print("\nUpdating llm.txt...")
with open("llm.txt", "a") as f:
    f.write("\n## Blog Posts - April 2026\n")
    for p in all_paths:
        f.write(BASE_URL + p + "\n")

print("\nDone - " + str(len(all_paths)) + " posts generated:")
for p in all_paths:
    print("  " + p)

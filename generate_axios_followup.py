#!/usr/bin/env python3
"""
axios attack follow-up content:
1. Blog post: How the axios attack used plain-crypto-js as a transitive dependency
2. Updated /blog index with all 8 posts
3. /cisa-kev breaking news banner for axios attack
"""
import os, json, re

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
.critical-banner{background:rgba(239,68,68,.15);border:2px solid var(--red);border-radius:10px;padding:20px 24px;margin:0 0 32px}
.critical-banner .label{font-size:11px;font-weight:700;color:var(--red);text-transform:uppercase;letter-spacing:.1em;margin-bottom:10px}
.critical-banner p{color:var(--text);margin:0;font-size:13px;line-height:1.7}
.fix-box{background:rgba(34,197,94,.08);border:1px solid rgba(34,197,94,.3);border-left:3px solid var(--green);border-radius:8px;padding:16px 20px;margin:20px 0}
.fix-box .label{font-size:10px;font-weight:700;color:var(--green);text-transform:uppercase;letter-spacing:.1em;margin-bottom:8px}
.warning-box{background:rgba(249,115,22,.08);border:1px solid rgba(249,115,22,.3);border-left:3px solid var(--orange);border-radius:8px;padding:16px 20px;margin:20px 0}
.warning-box .label{font-size:10px;font-weight:700;color:var(--orange);text-transform:uppercase;letter-spacing:.1em;margin-bottom:8px}
pre{background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:14px 16px;overflow-x:auto;font-size:11px;line-height:1.6;margin:8px 0;white-space:pre-wrap}
code{background:var(--surface);border:1px solid var(--border);border-radius:3px;padding:1px 5px;font-size:11px}
.cta-box{background:var(--surface);border:1px solid var(--purple);border-radius:10px;padding:24px;margin:32px 0;text-align:center}
.cta-box p{color:var(--text);font-size:13px;margin-bottom:16px}
.cta-btn{display:inline-block;background:var(--purple);color:#fff;font-family:'JetBrains Mono',monospace;font-size:13px;font-weight:600;padding:12px 28px;border-radius:7px;text-decoration:none}
.blog-grid{display:grid;gap:16px;margin-top:16px}
.blog-card{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:20px 24px}
.blog-card .date{font-size:10px;color:var(--muted);margin-bottom:8px;text-transform:uppercase;letter-spacing:.08em}
.blog-card h2{font-size:13px;font-weight:600;margin:0 0 8px}
.blog-card h2 a{color:var(--text)}
.blog-card h2 a:hover{color:var(--purple)}
.blog-card p{font-size:11px;color:var(--muted);margin:0;line-height:1.6}
.blog-card .tag{display:inline-block;font-size:9px;font-weight:700;padding:2px 6px;border-radius:3px;text-transform:uppercase;letter-spacing:.05em;margin-bottom:8px}
.tag-breaking{background:rgba(239,68,68,.2);color:var(--red);border:1px solid var(--red)}
.tag-guide{background:rgba(108,99,255,.2);color:var(--purple);border:1px solid var(--purple)}
.tag-digest{background:rgba(34,197,94,.2);color:var(--green);border:1px solid var(--green)}
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

def shell(title, desc, path, crumb_extra, body, schemas):
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
        + crumb_extra +
        '</div>'
        + body +
        '</main>'
        '<footer class="site-footer">'
        '<p>PackageFix &middot; <a href="/">packagefix.dev</a> &middot; MIT Licensed</p>'
        '<p style="margin-top:6px">Vulnerability data: '
        '<a href="https://osv.dev">OSV</a> &middot; '
        '<a href="https://www.cisa.gov/known-exploited-vulnerabilities-catalog">CISA KEV</a></p>'
        '</footer></body></html>'
    )

def cta():
    return (
        '<div class="cta-box">'
        '<p>Check your lockfile for plain-crypto-js or compromised axios versions now.</p>'
        '<a href="/" class="cta-btn">Scan with PackageFix &rarr;</a>'
        '<p style="margin-top:12px;font-size:11px;color:var(--muted)">Free &middot; No signup &middot; Paste your package-lock.json</p>'
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

all_paths = []

def write(slug, html):
    p = os.path.join("seo", slug, "index.html")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(html)
    all_paths.append("/" + slug)
    print("  OK /" + slug)


# =========================================================================
# POST: How the axios attack used plain-crypto-js as a transitive dependency
# =========================================================================
print("\nGenerating axios transitive dep deep-dive...")

FAQS = [
    ("Why did npm install plain-crypto-js automatically?",
     "npm installs all dependencies listed in a package's package.json, including transitive ones. When you run npm install axios@1.14.1, npm reads axios's package.json, sees plain-crypto-js@4.2.1 listed as a dependency, and installs it automatically. You never asked for it, you never knew it was there, but npm ran its postinstall script anyway."),
    ("Would a lockfile have protected me?",
     "A lockfile protects you from unexpected version changes on re-installs. But if you ran npm install axios@1.14.1 for the first time during the attack window, the lockfile would have been generated with plain-crypto-js@4.2.1 already in it. The lockfile records what was installed, it does not prevent malicious new packages from being installed the first time."),
    ("Could npm audit have caught this before installation?",
     "No. npm audit checks against known CVE databases. plain-crypto-js@4.2.1 was a brand new malicious package published specifically for this attack. No CVE existed yet. This is why real-time package reputation monitoring matters beyond CVE scanning."),
    ("What is the difference between this and a normal transitive CVE?",
     "A normal transitive CVE is a vulnerability in a legitimate package that your dependency uses. The axios attack is different: the malicious transitive dependency was injected by an attacker into what appeared to be a legitimate package release. The attack vector was the same (transitive dependency) but the mechanism was supply chain compromise rather than a vulnerability in existing code."),
    ("How do I prevent this class of attack in the future?",
     "Use npm ci instead of npm install in CI/CD pipelines - it respects the lockfile exactly. Pin all dependencies to exact versions in production. Use package integrity checks. Consider tools that monitor for new transitive dependencies being added to packages you depend on. Require provenance attestations for critical packages.")
]

body = (
    '<h1>How the axios Attack Used plain-crypto-js as a Transitive Dependency</h1>'
    '<p class="meta">March 31, 2026 &middot; PackageFix &middot; 6 min read</p>'

    '<div class="critical-banner">'
    '<div class="label">&#x1F6A8; Related to breaking axios attack</div>'
    '<p>This post explains the technical mechanism of the March 31, 2026 axios supply chain attack. '
    'If you ran npm install today, <a href="/blog/axios-supply-chain-attack-march-2026">check the main incident report first</a>.</p>'
    '</div>'

    '<p class="lead">The axios attack on March 31, 2026 succeeded because of how npm handles transitive dependencies. '
    'The attacker did not need to modify axios source code. '
    'They just added one line to axios\'s package.json. '
    'npm did the rest.</p>'

    '<h2>What is a transitive dependency?</h2>'
    '<p>When you install a package, you install everything it depends on too &mdash; '
    'and everything those packages depend on, and so on. '
    'These indirect dependencies are called transitive dependencies. '
    'In a typical Node.js project, your package.json might list 30 direct dependencies, '
    'but your node_modules folder contains 300-500 packages. '
    'The other 470 are transitive.</p>'
    '<pre>'
    'Your package.json:\n'
    '  "axios": "1.14.1"    <- you asked for this\n\n'
    'npm also installs:\n'
    '  follow-redirects     <- axios needs this (legitimate)\n'
    '  form-data            <- axios needs this (legitimate)\n'
    '  proxy-from-env       <- axios needs this (legitimate)\n'
    '  plain-crypto-js      <- axios needs this (MALICIOUS - injected by attacker)\n'
    '</pre>'

    '<h2>The attack mechanism - step by step</h2>'

    '<h3>Step 1: Attacker pre-stages a "clean" package</h3>'
    '<p>On March 30 at 05:57 UTC, the attacker published plain-crypto-js@4.2.0 to npm. '
    'This version was completely clean &mdash; no malicious code. '
    'Its purpose was to establish a brief package history and avoid '
    '"brand-new package" security alerts that some tools trigger for packages with no history.</p>'

    '<h3>Step 2: Attacker publishes the malicious version</h3>'
    '<p>23 hours later, plain-crypto-js@4.2.1 was published with the RAT payload. '
    'The package looked identical to a legitimate crypto library. '
    'Its package.json mimicked the real crypto-js library. '
    'The only difference: a postinstall script in the scripts field that executed setup.js.</p>'
    '<pre>'
    '// plain-crypto-js@4.2.1 package.json (malicious)\n'
    '{\n'
    '  "name": "plain-crypto-js",\n'
    '  "version": "4.2.1",\n'
    '  "scripts": {\n'
    '    "postinstall": "node setup.js"  // <-- the dropper\n'
    '  }\n'
    '}'
    '</pre>'

    '<h3>Step 3: Attacker compromises the axios maintainer account</h3>'
    '<p>Using credentials from the compromised jasonsaayman npm account, '
    'the attacker published axios@1.14.1 with one change from the legitimate 1.14.0: '
    'plain-crypto-js@4.2.1 was added as a runtime dependency.</p>'
    '<pre>'
    '// axios@1.14.1 package.json (malicious - showing only the change)\n'
    '{\n'
    '  "dependencies": {\n'
    '    "follow-redirects": "^1.15.4",  // legitimate\n'
    '    "form-data": "^4.0.0",          // legitimate\n'
    '    "proxy-from-env": "^1.1.0",     // legitimate\n'
    '    "plain-crypto-js": "^4.2.1"     // INJECTED - RAT dropper\n'
    '  }\n'
    '}'
    '</pre>'

    '<h3>Step 4: npm does exactly what it is designed to do</h3>'
    '<p>When any developer or CI/CD pipeline runs <code>npm install axios@1.14.1</code>, '
    'npm resolves the full dependency tree, finds plain-crypto-js@4.2.1 in axios\'s dependencies, '
    'downloads it, and runs its postinstall script. '
    'The RAT dropper executes in approximately 15 seconds. '
    'It contacts the C2 server, downloads platform-specific second-stage payloads, '
    'then deletes itself and replaces its package.json with a clean decoy.</p>'

    '<div class="warning-box">'
    '<div class="label">The key insight</div>'
    '<p style="margin:0">npm postinstall scripts run automatically with full system permissions '
    'of whoever ran npm install. In CI/CD pipelines, that is often a service account '
    'with access to secrets, cloud credentials, and source code repositories. '
    'This is why supply chain attacks via npm are so effective &mdash; '
    'the execution happens silently during a routine operation every developer performs hundreds of times.</p>'
    '</div>'

    '<h2>Why transitive dependencies are the attack surface</h2>'
    '<p>The attacker chose the transitive dependency route deliberately. '
    'A direct modification to axios source code would have been noticed immediately &mdash; '
    'the axios repository is watched by thousands of developers and security researchers. '
    'But a new dependency added to package.json is much less visible. '
    'Most developers never read the full dependency tree of packages they install.</p>'
    '<p>This is the same attack surface exploited in the event-stream attack (2018), '
    'the ua-parser-js attack (2021), and the node-ipc attack (2022). '
    'In each case, the attacker gained access to a legitimate package and used it '
    'as a vector to deliver malicious code via the transitive dependency mechanism.</p>'

    '<h2>How to detect this class of attack</h2>'
    '<pre>'
    '# Check if plain-crypto-js is in your lockfile\n'
    'grep "plain-crypto-js" package-lock.json\n\n'
    '# See ALL transitive dependencies of axios\n'
    'npm ls axios\n\n'
    '# Check when a package was added to your lockfile\n'
    'git log -p package-lock.json | grep "plain-crypto-js"\n\n'
    '# Verify axios has only its legitimate 3 deps\n'
    'npm ls --depth=1 axios'
    '</pre>'

    '<div class="fix-box">'
    '<div class="label">The legitimate axios deps (3 only)</div>'
    '<p style="margin:0">axios@1.14.0 (safe) has exactly 3 dependencies: '
    '<code>follow-redirects</code>, <code>form-data</code>, <code>proxy-from-env</code>. '
    'Any additional dependency in an axios release is a red flag. '
    'The presence of plain-crypto-js confirms the malicious version.</p>'
    '</div>'

    + cta()
    + faq_html(FAQS)
    + related_html([
        {"url": "/blog/axios-supply-chain-attack-march-2026", "title": "axios Incident Report", "desc": "IOCs, timeline, remediation"},
        {"url": "/glossary/transitive-dependency", "title": "What is a Transitive Dependency", "desc": "Plain-English definition"},
        {"url": "/blog/transitive-package-vulnerability-fix", "title": "Transitive Vulnerability Guide", "desc": "How to fix them"},
        {"url": "/glossary/supply-chain-attack", "title": "Supply Chain Attack", "desc": "The attack category"},
        {"url": "/fix/npm/axios", "title": "axios CVE History", "desc": "All axios vulnerabilities"},
        {"url": "/glossary/glassworm", "title": "Glassworm", "desc": "Invisible script attacks"},
    ])
)

write("blog/axios-plain-crypto-js-transitive-attack-explained", shell(
    "How the axios Attack Used plain-crypto-js as a Transitive Dependency | PackageFix",
    "The March 2026 axios supply chain attack succeeded because npm automatically installs transitive dependencies. Step-by-step technical breakdown of how plain-crypto-js was injected.",
    "/blog/axios-plain-crypto-js-transitive-attack-explained",
    '<a href="/blog">Blog</a> <span style="color:var(--border)">/</span> <span style="color:var(--text)">axios Transitive Attack Explained</span>',
    body,
    [
        {"@type": "Article",
         "headline": "How the axios Attack Used plain-crypto-js as a Transitive Dependency",
         "description": "Technical breakdown of how the March 2026 axios supply chain attack exploited npm transitive dependency installation.",
         "datePublished": "2026-03-31", "dateModified": "2026-03-31",
         "author": {"@type": "Organization", "name": "PackageFix", "url": BASE_URL}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "PackageFix", "item": BASE_URL},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": BASE_URL + "/blog"},
            {"@type": "ListItem", "position": 3, "name": "axios Transitive Attack Explained", "item": BASE_URL + "/blog/axios-plain-crypto-js-transitive-attack-explained"}
        ]},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in FAQS
        ]}
    ]
))


# =========================================================================
# UPDATE: /blog index - all 8 posts
# =========================================================================
print("\nUpdating /blog index...")

ALL_POSTS = [
    {
        "url": "/blog/axios-plain-crypto-js-transitive-attack-explained",
        "date": "March 31, 2026",
        "tag": "breaking",
        "tag_label": "Breaking",
        "title": "How the axios Attack Used plain-crypto-js as a Transitive Dependency",
        "desc": "Technical breakdown of how the March 2026 supply chain attack exploited npm's transitive dependency mechanism. Step-by-step with detection commands."
    },
    {
        "url": "/blog/axios-supply-chain-attack-march-2026",
        "date": "March 31, 2026",
        "tag": "breaking",
        "tag_label": "Breaking",
        "title": "axios npm Supply Chain Attack — March 31, 2026",
        "desc": "axios@1.14.1 and axios@0.30.4 contain a RAT via plain-crypto-js@4.2.1. IOCs, full timeline, and remediation steps."
    },
    {
        "url": "/blog/weekly-cve-april-1-2026",
        "date": "April 1, 2026",
        "tag": "digest",
        "tag_label": "Weekly Digest",
        "title": "Weekly CVE Digest — April 1, 2026",
        "desc": "6 CVEs this week: mysql2 RCE (CRITICAL), Werkzeug debugger RCE (CRITICAL), gunicorn HTTP smuggling, rustls, express, fiber."
    },
    {
        "url": "/blog/ruby-on-rails-security-releases-2024",
        "date": "April 1, 2026",
        "tag": "guide",
        "tag_label": "Guide",
        "title": "Ruby on Rails Security Releases 2024 — Complete CVE List",
        "desc": "All 8 Rails CVEs in 2024 including the October batch and December host authorization bypass. Fix versions for Rails 7.0, 7.1, 7.2."
    },
    {
        "url": "/blog/multer-1-4-5-lts-1-update-guide",
        "date": "April 1, 2026",
        "tag": "guide",
        "tag_label": "Guide",
        "title": "multer 1.4.5-lts.1 — Why npm Skips It and How to Update",
        "desc": "multer 1.4.5-lts.1 fixes CVE-2022-24434 but npm audit fix skips pre-release versions. Exact commands to update manually."
    },
    {
        "url": "/blog/transitive-package-vulnerability-fix",
        "date": "April 1, 2026",
        "tag": "guide",
        "tag_label": "Guide",
        "title": "Transitive Package Vulnerability — What It Is and How to Fix It",
        "desc": "CVEs in packages you did not install directly. Real examples: qs via Express, minimist, Log4Shell. Fix with npm overrides."
    },
    {
        "url": "/blog/weekly-cve-march-29-2026",
        "date": "March 29, 2026",
        "tag": "digest",
        "tag_label": "Weekly Digest",
        "title": "Weekly CVE Digest — March 29, 2026",
        "desc": "6 CVEs: mysql2 RCE, Werkzeug debugger RCE, gunicorn HTTP smuggling, rustls infinite loop, express open redirect, fiber."
    },
    {
        "url": "/blog/weekly-cve-march-2026",
        "date": "March 22, 2026",
        "tag": "digest",
        "tag_label": "Weekly Digest",
        "title": "Weekly CVE Digest — March 22, 2026",
        "desc": "7 CVEs including Log4Shell, Spring4Shell, SnakeYAML RCE, HTTP/2 Rapid Reset. Fix guides for all ecosystems."
    },
    {
        "url": "/blog/supply-chain-attacks-package-json",
        "date": "March 2026",
        "tag": "guide",
        "tag_label": "Guide",
        "title": "5 Supply Chain Attacks That npm audit Would Have Missed",
        "desc": "Typosquatting, dependency confusion, zombie packages, Glassworm Unicode attacks, and build script injection. How each works and how to detect them."
    },
]

tag_class = {"breaking": "tag-breaking", "guide": "tag-guide", "digest": "tag-digest"}

cards = ""
for post in ALL_POSTS:
    tc = tag_class.get(post["tag"], "tag-guide")
    cards += (
        '<div class="blog-card">'
        '<div class="date">' + post["date"] + '</div>'
        '<span class="tag ' + tc + '">' + post["tag_label"] + '</span>'
        '<h2><a href="' + post["url"] + '">' + post["title"] + '</a></h2>'
        '<p>' + post["desc"] + '</p>'
        '</div>'
    )

blog_body = (
    '<h1>PackageFix Blog</h1>'
    '<p class="lead">CVE digests, supply chain attack breakdowns, and fix guides for npm, PyPI, Ruby, PHP, Go, Rust, and Java.</p>'
    '<div class="blog-grid">' + cards + '</div>'
)

blog_schemas = [
    {"@type": "Blog",
     "name": "PackageFix Blog",
     "description": "CVE digests, supply chain attack analysis, and dependency security fix guides.",
     "url": BASE_URL + "/blog",
     "blogPost": [
         {"@type": "BlogPosting",
          "headline": p["title"],
          "url": BASE_URL + p["url"],
          "datePublished": "2026-03-31"}
         for p in ALL_POSTS
     ]},
    {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "PackageFix", "item": BASE_URL},
        {"@type": "ListItem", "position": 2, "name": "Blog", "item": BASE_URL + "/blog"}
    ]}
]

write("blog", shell(
    "PackageFix Blog — CVE Digests & Supply Chain Attack Guides",
    "CVE digests, supply chain attack breakdowns, and fix guides. axios supply chain attack, multer 1.4.5-lts.1, transitive vulnerabilities, Rails 2024 CVEs.",
    "/blog",
    '<span style="color:var(--text)">Blog</span>',
    blog_body,
    blog_schemas
))


# =========================================================================
# UPDATE: /cisa-kev - add axios breaking news banner
# =========================================================================
print("\nUpdating /cisa-kev with axios banner...")

cisa_path = "seo/cisa-kev/index.html"
if os.path.exists(cisa_path):
    with open(cisa_path) as f:
        content = f.read()

    banner = (
        '<div class="critical-banner" style="background:rgba(239,68,68,.15);border:2px solid #EF4444;'
        'border-radius:10px;padding:20px 24px;margin:0 0 32px">'
        '<div style="font-size:11px;font-weight:700;color:#EF4444;text-transform:uppercase;'
        'letter-spacing:.1em;margin-bottom:10px">&#x1F6A8; Breaking &mdash; March 31, 2026</div>'
        '<p style="color:var(--text);margin:0;font-size:13px;line-height:1.7">'
        '<strong>axios supply chain attack:</strong> '
        'axios@1.14.1 and axios@0.30.4 backdoored via compromised maintainer account. '
        'Hidden dependency plain-crypto-js@4.2.1 installs a cross-platform RAT. '
        'Safe versions: axios@1.14.0 or axios@0.30.3. '
        'CVE pending: GHSA-fw8c-xr5c-95f9. '
        '<a href="/blog/axios-supply-chain-attack-march-2026" style="color:#EF4444;font-weight:600">'
        'Full incident report &rarr;</a></p>'
        '</div>'
    )

    if 'axios-supply-chain-attack' not in content:
        content = content.replace('<h1>', banner + '<h1>', 1)
        with open(cisa_path, 'w') as f:
            f.write(content)
        print("  OK - banner added to /cisa-kev")
    else:
        print("  Banner already exists on /cisa-kev")
else:
    print("  /cisa-kev not found")


# =========================================================================
# UPDATE vercel.json + sitemap
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
print("  vercel.json - " + str(added) + " new rewrites (blog/ already had rewrites)")

print("\nUpdating sitemap-seo.xml...")
new_urls = (
    "  <url>\n    <loc>" + BASE_URL + "/blog/axios-plain-crypto-js-transitive-attack-explained</loc>\n"
    "    <changefreq>daily</changefreq>\n    <priority>0.9</priority>\n  </url>\n"
)
if os.path.exists("sitemap-seo.xml"):
    with open("sitemap-seo.xml") as f:
        content = f.read()
    if "/blog/axios-plain-crypto-js" not in content:
        updated = content.replace("</urlset>", new_urls + "</urlset>")
        with open("sitemap-seo.xml", "w") as f:
            f.write(updated)
        print("  sitemap updated")

print("\nUpdating llm.txt...")
with open("llm.txt", "a") as f:
    f.write(BASE_URL + "/blog/axios-plain-crypto-js-transitive-attack-explained\n")

print("\nDone:")
for p in all_paths:
    print("  " + p)
print("  /cisa-kev - axios banner added")

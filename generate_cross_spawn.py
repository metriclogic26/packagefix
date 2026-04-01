#!/usr/bin/env python3
"""
cross-spawn CVE-2024-21538 fix page
148M weekly downloads, almost entirely transitive
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
h3{font-size:13px;font-weight:600;margin:20px 0 8px}
p{color:var(--muted);margin-bottom:12px;font-size:12px;line-height:1.7}
.lead{color:var(--text);font-size:13px;margin-bottom:24px;line-height:1.7}
.meta{font-size:11px;color:var(--muted);margin-bottom:24px}
.warning-box{background:rgba(249,115,22,.08);border:1px solid rgba(249,115,22,.3);border-left:3px solid var(--orange);border-radius:8px;padding:16px 20px;margin:20px 0}
.warning-box .label{font-size:10px;font-weight:700;color:var(--orange);text-transform:uppercase;letter-spacing:.1em;margin-bottom:8px}
.fix-box{background:rgba(34,197,94,.08);border:1px solid rgba(34,197,94,.3);border-left:3px solid var(--green);border-radius:8px;padding:16px 20px;margin:20px 0}
.fix-box .label{font-size:10px;font-weight:700;color:var(--green);text-transform:uppercase;letter-spacing:.1em;margin-bottom:8px}
pre{background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:14px 16px;overflow-x:auto;font-size:11px;line-height:1.6;margin:8px 0;white-space:pre-wrap}
code{background:var(--surface);border:1px solid var(--border);border-radius:3px;padding:1px 5px;font-size:11px}
.badge{display:inline-block;font-size:10px;font-weight:700;padding:2px 8px;border-radius:4px;text-transform:uppercase;letter-spacing:.05em}
.badge-orange{background:rgba(249,115,22,.2);color:var(--orange);border:1px solid var(--orange)}
.badge-green{background:rgba(34,197,94,.2);color:var(--green);border:1px solid var(--green)}
.badge-purple{background:rgba(108,99,255,.2);color:var(--purple);border:1px solid var(--purple)}
.badge-muted{background:rgba(107,114,128,.15);color:var(--muted);border:1px solid var(--border)}
.cve-table{width:100%;border-collapse:collapse;margin:16px 0;font-size:12px}
.cve-table th{text-align:left;padding:10px 12px;border-bottom:2px solid var(--border);color:var(--muted);font-size:10px;text-transform:uppercase;letter-spacing:.08em}
.cve-table td{padding:10px 12px;border-bottom:1px solid var(--border);vertical-align:top}
.cve-table tr:last-child td{border-bottom:none}
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

FAQS = [
    ("How do I fix cross-spawn if it is not in my package.json?",
     "cross-spawn is almost always a transitive dependency — you did not install it directly. Use npm overrides to force the safe version: add {\"overrides\": {\"cross-spawn\": \"7.0.5\"}} to your package.json. Then run npm install. PackageFix generates this overrides block automatically when it detects a vulnerable cross-spawn."),
    ("Which packages pull in cross-spawn?",
     "cross-spawn is a dependency of jest, eslint, webpack, create-react-app, vite, npm itself, and thousands of other tools. Most Node.js projects have it several times over at various depths in their dependency tree. Run npm ls cross-spawn to see all the paths."),
    ("Is the cross-spawn ReDoS exploitable in production?",
     "It depends on whether user-controlled input reaches the cross-spawn argument() function. In most applications cross-spawn is used for running build tools and CLI commands — not for processing user input. The risk is lower for production web apps and higher for CLI tools or build systems that process user-supplied arguments. Updating is still the right call."),
    ("Does npm audit fix update cross-spawn automatically?",
     "Sometimes. If the parent package has released a version using cross-spawn 7.0.5+, npm audit fix will update it. If the parent has not updated yet, npm audit fix will report 'no fix available' — that is when you need the npm overrides approach."),
    ("What is the difference between cross-spawn and child_process.spawn?",
     "Node.js has a built-in child_process.spawn but it has inconsistent behavior on Windows. cross-spawn wraps it to provide consistent cross-platform behavior. That is why it appears in so many tools — anything that runs CLI commands on both Linux/Mac and Windows tends to use it.")
]

body = (
    '<h1>Fix cross-spawn CVE-2024-21538 &mdash; ReDoS Vulnerability | PackageFix</h1>'
    '<p class="meta">Updated April 1, 2026 &middot; <span class="badge badge-orange">HIGH</span> &middot; CVSS 7.5 &middot; Safe version: 7.0.5</p>'
    '<p class="lead">cross-spawn has a high-severity ReDoS vulnerability (CVE-2024-21538) affecting all versions below 7.0.5. '
    'With 148 million weekly downloads, it is almost always a transitive dependency &mdash; '
    'you probably have it without knowing. Fix: npm overrides forcing 7.0.5.</p>'

    '<h2>CVE-2024-21538 Details</h2>'
    '<table class="cve-table">'
    '<thead><tr><th>Field</th><th>Value</th></tr></thead>'
    '<tbody>'
    '<tr><td>CVE ID</td><td><a href="https://osv.dev/vulnerability/CVE-2024-21538" target="_blank" rel="noopener">CVE-2024-21538</a></td></tr>'
    '<tr><td>Severity</td><td><span class="badge badge-orange">HIGH</span> CVSS 7.5</td></tr>'
    '<tr><td>Type</td><td>ReDoS &mdash; Regular Expression Denial of Service</td></tr>'
    '<tr><td>Affected</td><td>cross-spawn &lt; 6.0.6 and cross-spawn 7.0.0&ndash;7.0.4</td></tr>'
    '<tr><td>Safe versions</td><td>6.0.6+ or 7.0.5+</td></tr>'
    '<tr><td>Disclosed</td><td>November 8, 2024</td></tr>'
    '<tr><td>CISA KEV</td><td>No</td></tr>'
    '</tbody></table>'

    '<h2>What is the vulnerability?</h2>'
    '<p>cross-spawn uses a regular expression to escape arguments when spawning child processes. '
    'The regex has catastrophic backtracking behavior &mdash; a crafted string with many backslashes '
    'followed by a specific Unicode character causes the CPU to spike to 100% and the process to hang indefinitely. '
    'This is a classic ReDoS pattern.</p>'
    '<p>The vulnerable code is in <code>cross-spawn/lib/util/escape.js</code> in the <code>argument()</code> function. '
    'The fix in 7.0.5 disables regexp backtracking entirely for this case.</p>'

    '<h2>Am I affected?</h2>'
    '<pre>'
    '# Check if cross-spawn is in your tree\n'
    'npm ls cross-spawn\n\n'
    '# Check the version specifically\n'
    'npm ls cross-spawn | grep cross-spawn\n\n'
    '# If you see any version below 7.0.5, you are affected'
    '</pre>'

    '<div class="warning-box">'
    '<div class="label">Typical output showing the problem</div>'
    '<pre style="margin:0;background:transparent;border:none;padding:0">'
    'my-app@1.0.0\n'
    '&#x251C;&#x2500;&#x2500; jest@29.7.0\n'
    '&#x2502;   &#x2514;&#x2500;&#x2500; cross-spawn@7.0.3  &lt;-- VULNERABLE\n'
    '&#x2514;&#x2500;&#x2500; eslint@8.57.0\n'
    '    &#x2514;&#x2500;&#x2500; cross-spawn@7.0.3  &lt;-- VULNERABLE'
    '</pre>'
    '</div>'

    '<h2>Fix: npm overrides</h2>'
    '<p>cross-spawn is almost always a transitive dependency. '
    'The fix is to add an npm override that forces all packages to use the safe version.</p>'

    '<div class="fix-box">'
    '<div class="label">Fix</div>'
    '<pre style="margin:0;background:transparent;border:none;padding:0">'
    '// package.json\n'
    '{\n'
    '  "dependencies": {\n'
    '    "jest": "^29.7.0",\n'
    '    "eslint": "^8.57.0"\n'
    '  },\n'
    '  "overrides": {\n'
    '    "cross-spawn": "7.0.5"\n'
    '  }\n'
    '}'
    '</pre>'
    '</div>'

    '<pre>'
    '# After adding the override, reinstall\n'
    'npm install\n\n'
    '# Verify the fix\n'
    'npm ls cross-spawn\n'
    '# All instances should now show 7.0.5\n\n'
    '# Confirm npm audit is clean\n'
    'npm audit'
    '</pre>'

    '<h2>Why cross-spawn is everywhere</h2>'
    '<p>cross-spawn solves a real problem: Node.js\'s built-in '
    '<code>child_process.spawn</code> has inconsistent behavior on Windows. '
    'Argument escaping works differently, paths with spaces break, '
    'and certain characters cause issues. cross-spawn wraps the built-in '
    'to provide consistent cross-platform behavior.</p>'
    '<p>This is why virtually every tool that runs CLI commands uses it &mdash; '
    'jest, eslint, webpack, vite, create-react-app, npm itself. '
    'Most Node.js projects have it 5-15 times over at various depths. '
    'The 148 million weekly downloads are almost entirely transitive.</p>'

    '<div class="fix-box">'
    '<div class="label">PackageFix detects this automatically</div>'
    '<p style="margin:0;font-size:12px;color:var(--text)">Paste your package-lock.json into PackageFix. '
    'It scans the full lockfile including transitive packages, '
    'flags cross-spawn below 7.0.5, and generates the exact overrides block above.</p>'
    '</div>'

    '<div class="cta-box">'
    '<p>Paste your lockfile &mdash; PackageFix finds cross-spawn vulnerabilities in your full dependency tree.</p>'
    '<a href="/" class="cta-btn">Scan with PackageFix &rarr;</a>'
    '<p style="margin-top:12px;font-size:11px;color:var(--muted)">Free &middot; No signup &middot; Paste package-lock.json for transitive scan</p>'
    '</div>'

    '<div class="faq"><h2>Common questions</h2>'
    + ''.join(
        '<div class="faq-item"><div class="faq-q">' + q + '</div>'
        '<div class="faq-a">' + a + '</div></div>'
        for q, a in FAQS
    )
    + '</div>'

    '<div style="margin:40px 0"><h2>Related</h2><div class="related-grid">'
    '<div class="related-card"><a href="/glossary/transitive-dependency">Transitive Dependencies</a><p>Why cross-spawn shows up without being installed</p></div>'
    '<div class="related-card"><a href="/glossary/redos">ReDoS Explained</a><p>How regex denial of service works</p></div>'
    '<div class="related-card"><a href="/fix/npm/semver">Fix semver</a><p>Another ReDoS CVE in a transitive dep</p></div>'
    '<div class="related-card"><a href="/fix/npm/minimist">Fix minimist</a><p>Another heavily-transitive CVE</p></div>'
    '<div class="related-card"><a href="/npm">npm Security</a><p>All npm CVE guides</p></div>'
    '</div></div>'
)

schemas = [
    {"@type": "TechArticle",
     "headline": "Fix cross-spawn CVE-2024-21538 - ReDoS Vulnerability",
     "description": "cross-spawn CVE-2024-21538 ReDoS affects all versions below 7.0.5. 148M weekly downloads. Fix with npm overrides.",
     "datePublished": "2026-04-01", "dateModified": "2026-04-01",
     "author": {"@type": "Organization", "name": "PackageFix", "url": BASE_URL}},
    {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "PackageFix", "item": BASE_URL},
        {"@type": "ListItem", "position": 2, "name": "Fix Guides", "item": BASE_URL + "/fix"},
        {"@type": "ListItem", "position": 3, "name": "npm", "item": BASE_URL + "/npm"},
        {"@type": "ListItem", "position": 4, "name": "cross-spawn", "item": BASE_URL + "/fix/npm/cross-spawn"}
    ]},
    {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in FAQS
    ]},
    {"@type": "SoftwareSourceCode",
     "codeSampleType": "full solution",
     "programmingLanguage": "javascript",
     "text": '{"overrides": {"cross-spawn": "7.0.5"}}'}
]

html = (
    '<!DOCTYPE html><html lang="en"><head>'
    '<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">'
    '<title>Fix cross-spawn CVE-2024-21538 ReDoS - npm Vulnerability | PackageFix</title>'
    '<meta name="description" content="cross-spawn CVE-2024-21538 (HIGH, CVSS 7.5) ReDoS affects all versions below 7.0.5. 148M weekly downloads - almost always transitive. Fix with npm overrides in 2 minutes.">'
    '<link rel="canonical" href="' + BASE_URL + '/fix/npm/cross-spawn">'
    '<meta property="og:title" content="Fix cross-spawn CVE-2024-21538 ReDoS | PackageFix">'
    '<meta property="og:description" content="cross-spawn below 7.0.5 is vulnerable to ReDoS. Fix with npm overrides. 148M weekly downloads - likely in your tree.">'
    '<meta property="og:url" content="' + BASE_URL + '/fix/npm/cross-spawn">'
    '<meta property="og:type" content="article">'
    '<meta name="twitter:card" content="summary">'
    '<link rel="icon" type="image/svg+xml" href="/icon.svg">'
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&display=swap" rel="stylesheet">'
    '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": schemas}, indent=2) + '</script>'
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
    '<a href="/fix">Fix Guides</a> <span style="color:var(--border)">/</span> '
    '<a href="/npm">npm</a> <span style="color:var(--border)">/</span> '
    '<span style="color:var(--text)">cross-spawn</span>'
    '</div>'
    + body +
    '</main>'
    '<footer class="site-footer">'
    '<p>PackageFix &middot; <a href="/">packagefix.dev</a> &middot; MIT Licensed</p>'
    '<p style="margin-top:6px">Vulnerability data: <a href="https://osv.dev">OSV</a> &middot; '
    '<a href="https://www.cisa.gov/known-exploited-vulnerabilities-catalog">CISA KEV</a></p>'
    '</footer></body></html>'
)

# Write page
path = "seo/fix/npm/cross-spawn/index.html"
os.makedirs(os.path.dirname(path), exist_ok=True)
with open(path, "w", encoding="utf-8") as f:
    f.write(html)
print("OK /fix/npm/cross-spawn")

# Update vercel.json
import json as jsonlib
with open("vercel.json") as f:
    config = jsonlib.load(f)

existing = config.get("rewrites", [])
existing_sources = {r["source"] for r in existing}
new_rewrites = [
    {"source": "/fix/npm/cross-spawn", "destination": "/seo/fix/npm/cross-spawn/index.html"},
    {"source": "/fix/npm/cross-spawn/", "destination": "/seo/fix/npm/cross-spawn/index.html"},
]
added = 0
for r in new_rewrites:
    if r["source"] not in existing_sources:
        existing.append(r)
        added += 1
config["rewrites"] = existing
with open("vercel.json", "w") as f:
    jsonlib.dump(config, f, indent=2)
print(f"vercel.json - {added} new rewrites")

# Update sitemap
new_url = "  <url>\n    <loc>" + BASE_URL + "/fix/npm/cross-spawn</loc>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n"
with open("sitemap-seo.xml") as f:
    content = f.read()
if "/fix/npm/cross-spawn" not in content:
    content = content.replace("</urlset>", new_url + "</urlset>")
    with open("sitemap-seo.xml", "w") as f:
        f.write(content)
    print("sitemap updated")

# Update llm.txt
with open("llm.txt", "a") as f:
    f.write(BASE_URL + "/fix/npm/cross-spawn\n")

print("\nDone. Deploy:")
print("  git add -A && git commit -m 'feat: cross-spawn CVE-2024-21538 fix page' && git push")

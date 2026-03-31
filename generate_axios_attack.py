#!/usr/bin/env python3
"""
BREAKING: axios npm supply chain attack - March 31, 2026
Build immediately - breaking news, zero competition right now
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
.badge{display:inline-block;font-size:10px;font-weight:700;padding:2px 8px;border-radius:4px;text-transform:uppercase;letter-spacing:.05em}
.badge-red{background:rgba(239,68,68,.2);color:var(--red);border:1px solid var(--red)}
.badge-green{background:rgba(34,197,94,.2);color:var(--green);border:1px solid var(--green)}
.timeline{margin:16px 0}
.timeline-item{display:flex;gap:16px;padding:10px 0;border-bottom:1px solid var(--border)}
.timeline-item:last-child{border-bottom:none}
.timeline-time{color:var(--muted);font-size:11px;min-width:140px}
.timeline-event{font-size:12px;color:var(--text)}
.ioc-table{width:100%;border-collapse:collapse;margin:16px 0;font-size:12px}
.ioc-table th{text-align:left;padding:10px 12px;border-bottom:2px solid var(--border);color:var(--muted);font-size:10px;text-transform:uppercase;letter-spacing:.08em}
.ioc-table td{padding:10px 12px;border-bottom:1px solid var(--border);vertical-align:top}
.ioc-table tr:last-child td{border-bottom:none}
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
@media(max-width:640px){.nav-links{display:none}.related-grid{grid-template-columns:1fr}.timeline-item{flex-direction:column;gap:4px}}
"""

def shell(title, desc, path, body, schemas):
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
        '<span style="color:var(--text)">axios Supply Chain Attack</span>'
        '</div>'
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
        '<p>Check your lockfile for plain-crypto-js or axios@1.14.1 right now.</p>'
        '<a href="/" class="cta-btn">Scan with PackageFix &rarr;</a>'
        '<p style="margin-top:12px;font-size:11px;color:var(--muted)">Free &middot; No signup &middot; Paste your package-lock.json &middot; Instant results</p>'
        '</div>'
    )

def faq_html(items):
    html = '<div class="faq"><h2>Common questions</h2>'
    for q, a in items:
        html += '<div class="faq-item"><div class="faq-q">' + q + '</div><div class="faq-a">' + a + '</div></div>'
    return html + '</div>'

def related_html(pages):
    cards = ''.join(
        '<div class="related-card"><a href="' + p['url'] + '">' + p['title'] + '</a><p>' + p['desc'] + '</p></div>'
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
# PAGE 1: axios Supply Chain Attack - Breaking News
# =========================================================================

FAQS = [
    ("Am I affected if I did not install axios today?",
     "You are only affected if you ran npm install (or a CI/CD pipeline ran it) between approximately 00:21 UTC and 03:30 UTC on March 31, 2026, AND the resolved axios version was 1.14.1 or 0.30.4. If your package-lock.json shows axios@1.14.0 or earlier, you are not affected from this incident."),
    ("How do I check if plain-crypto-js was installed?",
     "Run: grep -r plain-crypto-js node_modules/ package-lock.json. If you find it, your system was exposed. The malicious package was designed to self-delete after execution, so absence in node_modules does not guarantee safety if it ran during installation."),
    ("What should I do if I installed the malicious version?",
     "Treat the machine as fully compromised. Isolate it from the network. Re-image or restore from a clean backup taken before March 30, 2026. Rotate all credentials that were accessible from the machine: API keys, GitHub tokens, AWS/cloud credentials, database passwords, SSH keys. Review CI/CD pipeline logs for unauthorized activity."),
    ("Are axios@1.14.0 and axios@0.30.3 safe?",
     "Yes. These are the safe versions. axios@1.14.0 is the last clean 1.x release. axios@0.30.3 is the last clean 0.x release. If you are on any other version of axios, check whether it predates the malicious releases - versions below 1.14.1 and below 0.30.4 are not affected by this specific attack."),
    ("How did the attacker compromise the axios maintainer account?",
     "The exact compromise vector has not been publicly confirmed. The attacker changed the registered email on the jasonsaayman npm account to an anonymous ProtonMail address to lock out the legitimate owner. The attack was pre-staged 18 hours in advance with a clean decoy package (plain-crypto-js@4.2.0) published before the malicious version."),
    ("Will axios@1.14.1 appear as a vulnerability in PackageFix?",
     "Yes - PackageFix checks against the OSV database which has assigned GHSA-fw8c-xr5c-95f9 to this incident. Paste your package-lock.json and PackageFix will flag axios@1.14.1 and axios@0.30.4 as malicious with a link to the full incident report."),
    ("What is plain-crypto-js@4.2.1?",
     "plain-crypto-js@4.2.1 is a purpose-built malicious package created specifically for this attack. It was designed to look like a legitimate crypto library. Its package.json mimics the real crypto-js library. It has no legitimate functionality - its only purpose is to execute the postinstall dropper script that installs the RAT."),
]

TIMELINE = [
    ("Mar 30, 05:57 UTC", "plain-crypto-js@4.2.0 published (clean decoy to establish history)"),
    ("Mar 30, 23:59 UTC", "plain-crypto-js@4.2.1 published with RAT payload"),
    ("Mar 31, 00:21 UTC", "axios@1.14.1 published via compromised jasonsaayman account"),
    ("Mar 31, 01:00 UTC", "axios@0.30.4 published via same compromised account"),
    ("Mar 31, ~03:30 UTC", "Malicious versions removed from npm by registry"),
    ("Mar 31, 04:30 UTC", "StepSecurity publishes full technical analysis"),
    ("Mar 31, ongoing", "CVE assignment in progress: GHSA-fw8c-xr5c-95f9 / MAL-2026-2306"),
]

tl_html = '<div class="timeline">' + ''.join(
    '<div class="timeline-item">'
    '<span class="timeline-time">' + t + '</span>'
    '<span class="timeline-event">' + e + '</span>'
    '</div>'
    for t, e in TIMELINE
) + '</div>'

body = (
    '<h1>axios npm Supply Chain Attack &mdash; March 31, 2026</h1>'
    '<p class="meta">March 31, 2026 &middot; PackageFix &middot; Breaking &middot; Updated as new information emerges</p>'

    '<div class="critical-banner">'
    '<div class="label">&#x1F6A8; Critical &mdash; Active Supply Chain Attack</div>'
    '<p><strong>axios@1.14.1 and axios@0.30.4 are malicious.</strong> '
    'A compromised maintainer account was used to publish backdoored releases containing a cross-platform Remote Access Trojan. '
    'Safe versions: <strong>axios@1.14.0</strong> (1.x) or <strong>axios@0.30.3</strong> (0.x). '
    'If you ran npm install between 00:21&ndash;03:30 UTC on March 31, 2026 and resolved either malicious version, '
    'treat your system as compromised.</p>'
    '</div>'

    '<h2>What happened</h2>'
    '<p>On March 31, 2026, an attacker compromised the npm account of the primary axios maintainer '
    'and published two malicious versions of axios &mdash; one of the most widely-used JavaScript libraries '
    'with approximately 100 million weekly downloads.</p>'
    '<p>The malicious versions did not modify axios source code directly. '
    'Instead, they added a hidden dependency &mdash; plain-crypto-js@4.2.1 &mdash; '
    'to the package.json. When npm installed axios@1.14.1, it automatically pulled in plain-crypto-js@4.2.1 '
    'and executed its postinstall hook. That script was a RAT dropper targeting macOS, Windows, and Linux.</p>'

    '<div class="fix-box">'
    '<div class="label">Immediate action</div>'
    '<pre>'
    '# Check your current axios version\n'
    'npm list axios\n\n'
    '# Check if plain-crypto-js is present\n'
    'grep -r "plain-crypto-js" package-lock.json\n\n'
    '# If affected - downgrade immediately\n'
    'npm install axios@1.14.0\n\n'
    '# For 0.x users\n'
    'npm install axios@0.30.3\n\n'
    '# Commit the fix\n'
    'git add package.json package-lock.json\n'
    'git commit -m "security: downgrade axios - supply chain attack (GHSA-fw8c-xr5c-95f9)"'
    '</pre>'
    '</div>'

    '<h2>How the attack worked</h2>'
    '<p>The attack was pre-staged 18 hours in advance. '
    'plain-crypto-js@4.2.0 was published on March 30 as a clean decoy to establish a brief package history '
    'and avoid "brand-new package" alarms from security scanners. '
    'plain-crypto-js@4.2.1 containing the payload was then published just before the malicious axios releases.</p>'
    '<p>The dropper used two layers of obfuscation: reversed Base64 encoding with padding substitution, '
    'and XOR cipher with a hardcoded key. After execution, it deleted itself and replaced its package.json '
    'with a clean decoy &mdash; leaving no obvious trace in node_modules for a developer inspecting after the fact.</p>'

    '<h2>Attack timeline</h2>'
    + tl_html +

    '<h2>Indicators of Compromise (IOCs)</h2>'
    '<table class="ioc-table">'
    '<thead><tr><th>Type</th><th>Indicator</th><th>Description</th></tr></thead>'
    '<tbody>'
    '<tr><td>npm package</td><td><code>axios@1.14.1</code></td><td>Malicious axios release</td></tr>'
    '<tr><td>npm package</td><td><code>axios@0.30.4</code></td><td>Malicious axios release (0.x branch)</td></tr>'
    '<tr><td>npm package</td><td><code>plain-crypto-js@4.2.1</code></td><td>RAT dropper package</td></tr>'
    '<tr><td>C2 domain</td><td><code>sfrclak.com</code></td><td>Command and control server</td></tr>'
    '<tr><td>C2 endpoint</td><td><code>sfrclak.com:8000</code></td><td>RAT beacon address</td></tr>'
    '<tr><td>File</td><td><code>setup.js</code> in plain-crypto-js</td><td>Dropper script</td></tr>'
    '<tr><td>npm account</td><td><code>jasonsaayman</code></td><td>Compromised maintainer account</td></tr>'
    '</tbody></table>'

    '<div class="warning-box">'
    '<div class="label">If plain-crypto-js ran on your machine</div>'
    '<p style="margin:0">The malware self-deletes after execution. Absence from node_modules does not mean it did not run. '
    'If your build logs show npm install ran during 00:21&ndash;03:30 UTC March 31 and resolved axios@1.14.1 or axios@0.30.4, '
    'assume credential exfiltration occurred. Rotate everything: API keys, tokens, SSH keys, database passwords.</p>'
    '</div>'

    '<h2>Why axios was targeted</h2>'
    '<p>axios is present in approximately 80% of cloud and code environments. '
    'It is a direct or transitive dependency in millions of applications. '
    'The attacker targeted the 1.x and 0.x branches simultaneously to maximize exposure across both modern '
    'and legacy codebases. The attack appears to be espionage or APT activity &mdash; '
    'no cryptocurrency mining or ransomware components were found, suggesting credential harvesting '
    'and intelligence gathering rather than immediate financial gain.</p>'

    '<h2>How PackageFix helps</h2>'
    '<p>Paste your package-lock.json into PackageFix. '
    'If your lockfile resolves axios@1.14.1 or axios@0.30.4, '
    'PackageFix will flag it as malicious and show the safe downgrade version. '
    'It also detects plain-crypto-js@4.2.1 as a known malicious package via the OSV database.</p>'

    + cta()
    + faq_html(FAQS)
    + related_html([
        {"url": "/fix/npm/axios", "title": "axios CVE History", "desc": "All axios vulnerabilities"},
        {"url": "/glossary/supply-chain-attack", "title": "Supply Chain Attack", "desc": "How these attacks work"},
        {"url": "/glossary/zombie-package", "title": "Zombie Packages", "desc": "Related threat vector"},
        {"url": "/cisa-kev", "title": "CISA KEV", "desc": "All actively exploited packages"},
        {"url": "/blog/transitive-package-vulnerability-fix", "title": "Transitive Vulnerabilities", "desc": "How indirect deps spread attacks"},
        {"url": "/guides/github-actions", "title": "Secure your CI", "desc": "Detect supply chain attacks in CI"},
    ])
)

schemas = [
    {"@type": "Article",
     "headline": "axios npm Supply Chain Attack - March 31, 2026",
     "description": "axios@1.14.1 and axios@0.30.4 were backdoored with a RAT via a compromised maintainer account. Safe versions, IOCs, and remediation steps.",
     "datePublished": "2026-03-31",
     "dateModified": "2026-03-31",
     "author": {"@type": "Organization", "name": "PackageFix", "url": BASE_URL},
     "about": {"@type": "SoftwareApplication", "name": "axios", "applicationCategory": "DeveloperApplication"}},
    {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "PackageFix", "item": BASE_URL},
        {"@type": "ListItem", "position": 2, "name": "Blog", "item": BASE_URL + "/blog"},
        {"@type": "ListItem", "position": 3, "name": "axios Supply Chain Attack March 2026", "item": BASE_URL + "/blog/axios-supply-chain-attack-march-2026"}
    ]},
    {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in FAQS
    ]}
]

write("blog/axios-supply-chain-attack-march-2026", shell(
    "axios npm Supply Chain Attack (March 31, 2026) - IOCs, Safe Versions & Remediation | PackageFix",
    "axios@1.14.1 and axios@0.30.4 contain a RAT via plain-crypto-js@4.2.1. Safe versions: axios@1.14.0 or axios@0.30.3. IOCs, timeline, and full remediation steps.",
    "/blog/axios-supply-chain-attack-march-2026",
    body, schemas
))

# Also update the /fix/npm/axios page to add a prominent banner
print("\nUpdating /fix/npm/axios with attack banner...")
axios_fix_path = "seo/fix/npm/axios/index.html"
if os.path.exists(axios_fix_path):
    with open(axios_fix_path) as f:
        content = f.read()

    banner = (
        '<div class="critical-banner" style="background:rgba(239,68,68,.15);border:2px solid #EF4444;'
        'border-radius:10px;padding:20px 24px;margin:0 0 32px">'
        '<div style="font-size:11px;font-weight:700;color:#EF4444;text-transform:uppercase;'
        'letter-spacing:.1em;margin-bottom:10px">&#x1F6A8; Breaking &mdash; March 31, 2026</div>'
        '<p style="color:var(--text);margin:0;font-size:13px">'
        '<strong>axios@1.14.1 and axios@0.30.4 are malicious.</strong> '
        'Supply chain attack via compromised maintainer account. '
        'Safe versions: <strong>axios@1.14.0</strong> or <strong>axios@0.30.3</strong>. '
        '<a href="/blog/axios-supply-chain-attack-march-2026">Full incident report &rarr;</a></p>'
        '</div>'
    )

    if '<h1>' in content and 'axios-supply-chain-attack' not in content:
        content = content.replace('<h1>', banner + '<h1>', 1)
        with open(axios_fix_path, 'w') as f:
            f.write(content)
        print("  OK - banner added to /fix/npm/axios")
else:
    print("  /fix/npm/axios not found - skipping banner")


# Update vercel.json and sitemap
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
new_urls = (
    "  <url>\n"
    "    <loc>" + BASE_URL + "/blog/axios-supply-chain-attack-march-2026</loc>\n"
    "    <changefreq>daily</changefreq>\n"
    "    <priority>1.0</priority>\n"
    "  </url>\n"
)
if os.path.exists("sitemap-seo.xml"):
    with open("sitemap-seo.xml") as f:
        content = f.read()
    updated = content.replace("</urlset>", new_urls + "</urlset>")
    with open("sitemap-seo.xml", "w") as f:
        f.write(updated)

print("\nUpdating llm.txt...")
with open("llm.txt", "a") as f:
    f.write("\n## Breaking - axios Supply Chain Attack\n")
    f.write(BASE_URL + "/blog/axios-supply-chain-attack-march-2026\n")

print("\nDone. Pages generated:")
for p in all_paths:
    print("  " + p)
print("\nALSO UPDATED: /fix/npm/axios - attack banner added")

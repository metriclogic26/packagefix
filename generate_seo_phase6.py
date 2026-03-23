#!/usr/bin/env python3
"""
PackageFix — Phase 6 SEO
15 more KEV/CVE pages + /terminal page + /guides/github-actions + /guides/pre-commit
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
.fix-box{background:rgba(34,197,94,.08);border:1px solid rgba(34,197,94,.3);border-left:3px solid var(--green);border-radius:8px;padding:16px 20px;margin:20px 0}
.fix-box .label{font-size:10px;font-weight:700;color:var(--green);text-transform:uppercase;letter-spacing:.1em;margin-bottom:8px}
.info-box{background:rgba(108,99,255,.08);border:1px solid rgba(108,99,255,.3);border-left:3px solid var(--purple);border-radius:8px;padding:16px 20px;margin:20px 0}
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
.terminal-box{background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:20px;margin:20px 0;font-family:'JetBrains Mono',monospace}
.terminal-box .prompt{color:var(--green);font-size:11px}
.terminal-box .cmd{color:var(--text);font-size:12px}
.step-list{counter-reset:steps;padding:0;list-style:none;margin:16px 0}
.step-list li{counter-increment:steps;display:flex;gap:16px;margin-bottom:20px;font-size:12px;color:var(--muted)}
.step-list li::before{content:counter(steps);display:flex;align-items:center;justify-content:center;min-width:28px;height:28px;background:var(--purple);color:#fff;border-radius:50%;font-weight:700;font-size:11px;flex-shrink:0;margin-top:2px}
.site-footer{border-top:1px solid var(--border);padding:24px;text-align:center;font-size:11px;color:var(--muted);margin-top:60px}
.site-footer a{color:var(--muted)}
@media(max-width:640px){.nav-links{display:none}.related-grid{grid-template-columns:1fr}}
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
    items = "".join(
        f'<div class="faq-item"><div class="faq-q">{q}</div><div class="faq-a">{a}</div></div>'
        for q,a in faqs
    )
    return f'<div class="faq"><h2>Frequently Asked Questions</h2>{items}</div>'

def related_html(pages):
    cards = "".join(
        f'<div class="related-card"><a href="{p["url"]}">{p["title"]}</a><p>{p["desc"]}</p></div>'
        for p in pages
    )
    return f'<div style="margin:40px 0"><h2>Related</h2><div class="related-grid">{cards}</div></div>'


def build_schemas(howto_name, howto_desc, steps, breadcrumbs_list, faqs):
    return [
        {"@type":"HowTo","name":howto_name,"description":howto_desc,
         "estimatedCost":{"@type":"MonetaryAmount","currency":"USD","value":"0"},
         "step":[{"@type":"HowToStep","name":s["name"],"text":s["text"]} for s in steps]},
        {"@type":"BreadcrumbList","itemListElement":[
            {"@type":"ListItem","position":i+1,"name":n,"item":BASE_URL+u}
            for i,(n,u) in enumerate(breadcrumbs_list)
        ]},
        {"@type":"FAQPage","mainEntity":[
            {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}}
            for q,a in faqs
        ]}
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
# KEV PAGES — SIMPLE TEMPLATE (15 CVEs)
# ══════════════════════════════════════════════════════════════════════════════

KEV_DATA = [
    # (cve_id, name, cvss, ecosystem, package, vuln_ver, safe_ver, fix_page,
    #  short_desc, long_desc, fix_steps, faqs)
    ("CVE-2020-8203","Lodash Prototype Pollution",7.4,
     "npm","lodash","< 4.17.21","4.17.21","/fix/npm/lodash",
     "Prototype pollution via zipper merge in lodash",
     "Lodash's zipObjectDeep, merge, and mergeWith functions allow an attacker to modify Object.prototype by passing a crafted payload. Any application that passes user-controlled data to these functions is vulnerable. Widely exploited — lodash appears on CISA KEV.",
     ["Update lodash to 4.17.21 in package.json","Run npm install","Verify with: node -e \"const _ = require('lodash'); console.log(_.version)\""],
     [("What functions in lodash are affected by CVE-2020-8203?","zipObjectDeep, merge, mergeWith, and defaultsDeep are the primary affected functions. Any code that passes user-controlled object keys to these functions is vulnerable."),
      ("Is lodash being replaced by native JavaScript?","Yes — many lodash functions have native equivalents in modern JavaScript. However, migration takes time. Updating to 4.17.21 is the immediate fix."),
      ("Why is lodash on the CISA KEV list?","CISA added lodash because CVE-2020-8203 was confirmed being exploited in attacks against production applications. The wide deployment of lodash makes it a high-value target.")]),

    ("CVE-2021-23337","Lodash Command Injection",7.2,
     "npm","lodash","< 4.17.21","4.17.21","/fix/npm/lodash",
     "Command injection via template function in lodash",
     "Lodash's template function passes user-controlled strings to Function() constructor without sanitization, enabling arbitrary JavaScript execution. If you use _.template() with untrusted input, you are vulnerable.",
     ["Update lodash to 4.17.21","Run npm install","Avoid passing user-controlled data to _.template()"],
     [("How is CVE-2021-23337 different from CVE-2020-8203?","CVE-2020-8203 is prototype pollution. CVE-2021-23337 is command injection via the template function. Both are fixed in lodash 4.17.21."),
      ("Do I need to stop using _.template()?","Not necessarily — the fix in 4.17.21 patches the unsafe behavior. However, passing untrusted user input to template functions is inherently risky and should be avoided where possible."),
      ("Does lodash 4.17.21 fix both CVEs?","Yes — lodash 4.17.21 addresses both CVE-2020-8203 and CVE-2021-23337.")]),

    ("CVE-2022-24999","qs Prototype Pollution",7.5,
     "npm","qs","< 6.11.0","6.11.0","/fix/npm/qs",
     "Prototype pollution via query string parsing in qs",
     "The qs query string parser allows prototype pollution via crafted query strings containing __proto__ or constructor keys. Any application that parses user-controlled query strings with qs is potentially vulnerable. qs is widely used as an Express.js dependency.",
     ["Update qs to 6.11.0 or later","If qs is a transitive dep, add npm overrides: {\"overrides\": {\"qs\": \"6.11.0\"}}","Run npm install"],
     [("What is prototype pollution?","Prototype pollution allows an attacker to modify Object.prototype by injecting properties via crafted input. This can enable property injection, DoS, or in some cases RCE depending on how the polluted properties are used downstream."),
      ("Is qs a direct or transitive dependency?","qs is bundled as a transitive dependency of Express.js and many other packages. Even if you don't use qs directly, you may be affected. PackageFix checks transitive deps when you drop your package-lock.json."),
      ("Why is qs on CISA KEV?","CISA confirmed active exploitation of CVE-2022-24999 in production systems. The combination of wide deployment (qs is installed billions of times per week) and prototype pollution impact made it a priority target.")]),

    ("CVE-2021-44906","minimist Prototype Pollution",9.8,
     "npm","minimist","< 1.2.6","1.2.6","/fix/npm/minimist",
     "Prototype pollution in command-line argument parsing",
     "minimist parses command-line arguments and is vulnerable to prototype pollution via __proto__ and constructor.prototype keys. Despite minimist being a small utility package, it is a transitive dependency of thousands of packages — making this a widespread vulnerability.",
     ["Update minimist to 1.2.6","For transitive: {\"overrides\": {\"minimist\": \"1.2.6\"}}","Run npm install"],
     [("Why is minimist CRITICAL?","minimist has a CVSS of 9.8 because prototype pollution can be exploited remotely in applications that parse user-controlled arguments or query strings with minimist."),
      ("Is minimist a common transitive dependency?","Yes — minimist is one of the most downloaded npm packages and appears as a transitive dependency in thousands of projects including webpack, mocha, and many CLI tools."),
      ("How do I fix minimist if it's not in my package.json?","Use npm overrides: add {\"overrides\": {\"minimist\": \"1.2.6\"}} to your package.json. PackageFix generates this override block automatically when it detects a transitive minimist vulnerability.")]),

    ("CVE-2023-26136","tough-cookie Prototype Pollution",9.8,
     "npm","tough-cookie","< 4.1.3","4.1.3","/fix/npm/tough-cookie",
     "Prototype pollution via cookie parsing in tough-cookie",
     "tough-cookie, used for HTTP cookie handling in Node.js, is vulnerable to prototype pollution via specially crafted cookie values. tough-cookie is a transitive dependency of many packages including request and axios.",
     ["Update tough-cookie to 4.1.3","For transitive: {\"overrides\": {\"tough-cookie\": \"4.1.3\"}}","Run npm install"],
     [("What is tough-cookie used for?","tough-cookie handles HTTP cookies in Node.js — parsing, storing, and serializing cookies for HTTP clients. It is a transitive dependency of many popular packages including request, got, and superagent."),
      ("Is tough-cookie on CISA KEV?","Check the live CISA KEV catalog at packagefix.dev — the catalog updates daily."),
      ("How do I update tough-cookie if it's a transitive dependency?","Use npm overrides in package.json: {\"overrides\": {\"tough-cookie\": \"4.1.3\"}}. PackageFix generates this snippet automatically.")]),

    ("CVE-2023-45857","Axios SSRF",8.8,
     "npm","axios","< 1.6.0","1.7.4","/fix/npm/axios",
     "Server-side request forgery via protocol-relative URL",
     "Axios incorrectly follows protocol-relative URLs (//example.com) when XSRF tokens are present, potentially leaking sensitive data to attacker-controlled servers. Applications that use axios with XSRF protection and allow user-controlled redirect targets are vulnerable.",
     ["Update axios to 1.6.0 or later (1.7.4 recommended)","Run npm install","Review any code that passes user-controlled URLs to axios"],
     [("What is SSRF?","Server-Side Request Forgery allows an attacker to cause the server to make HTTP requests to attacker-controlled destinations, potentially exposing internal services or credentials."),
      ("Does this affect all axios users?","The vulnerability requires XSRF tokens to be in use and a protocol-relative URL to be followed. If you use axios with XSRF protection, update immediately."),
      ("What version of axios should I use?","1.7.4 is the current safe version as of March 2026.")]),

    ("CVE-2022-23540","jsonwebtoken Algorithm Confusion",9.8,
     "npm","jsonwebtoken","< 9.0.0","9.0.0","/fix/npm/jsonwebtoken",
     "Algorithm confusion allowing arbitrary JWT signing",
     "jsonwebtoken before 9.0.0 allows attackers to forge tokens by exploiting algorithm confusion — when the verifier accepts multiple algorithms, an attacker can switch to a weaker algorithm or the 'none' algorithm to bypass verification entirely.",
     ["Update jsonwebtoken to 9.0.0","Run npm install","Always pass algorithms explicitly: jwt.verify(token, secret, {algorithms: ['HS256']})"],
     [("What is algorithm confusion in JWT?","Algorithm confusion occurs when a JWT library accepts tokens signed with unexpected algorithms. An attacker can forge a token signed with 'none' (no signature) or switch to a weaker algorithm the attacker can compute."),
      ("Is this on CISA KEV?","Yes — CVE-2022-23540 is on the CISA Known Exploited Vulnerabilities catalog. Authentication bypass via JWT forgery is being actively exploited."),
      ("How do I make my JWT verification safe?","Always pass an explicit algorithms array to jwt.verify(). Never pass the algorithm from the token header itself — always use your own hardcoded list.")]),

    ("CVE-2023-29017","vm2 Sandbox Escape",10.0,
     "npm","vm2","< 3.9.19","3.9.19","/fix/npm/vm2",
     "Sandbox escape allowing remote code execution",
     "vm2 is a popular Node.js sandbox library used to execute untrusted code safely. CVE-2023-29017 allows a complete sandbox escape — code running inside vm2 can break out and execute arbitrary code on the host system. CVSS 10.0.",
     ["Update vm2 to 3.9.19","Run npm install","Consider migrating to isolated-vm or a container-based sandbox for stronger isolation"],
     [("Is vm2 still safe to use?","vm2 has had multiple critical sandbox escapes. The maintainers recommend considering isolated-vm or vm2's own successor packages for production sandbox use."),
      ("What can an attacker do with this vulnerability?","A complete sandbox escape — code inside the vm2 sandbox can read the host filesystem, execute system commands, exfiltrate environment variables, and establish network connections."),
      ("What's the CVSS score for CVE-2023-29017?","CVSS 10.0 — the maximum possible score. This is one of the most severe npm vulnerabilities ever discovered. Fix immediately.")]),

    ("CVE-2023-4863","libwebp Heap Buffer Overflow",10.0,
     "npm","sharp","< 0.32.6","0.33.2","/fix/npm/sharp",
     "Heap buffer overflow in WebP image processing",
     "A heap buffer overflow in Google's libwebp library allows remote code execution via a crafted WebP image. The sharp npm package bundles libwebp. Any application that processes WebP images from untrusted sources using sharp is vulnerable. Also affects Chrome, Firefox, and Electron apps.",
     ["Update sharp to 0.32.6 or later (0.33.2 recommended)","Run npm install","If you process user-uploaded images, validate image format before processing"],
     [("Is this the same vulnerability as the Chrome zero-day?","Yes — CVE-2023-4863 affects both browsers and any software bundling libwebp, including sharp. Google, Mozilla, and Apple all released emergency patches for this."),
      ("Does this affect all WebP image processing?","Any application using a vulnerable version of libwebp to process WebP images is affected. This includes sharp, Electron apps, and browser-based image processing."),
      ("Why is sharp CVSS 10.0?","The heap buffer overflow in libwebp allows arbitrary code execution with no authentication. Processing a single malicious WebP image is enough to trigger it.")]),

    ("CVE-2022-25883","semver ReDoS",7.5,
     "npm","semver","< 7.5.2","7.5.4","/fix/npm/semver",
     "ReDoS via inefficient regex in coerce function",
     "The semver package's coerce() function uses a regular expression vulnerable to catastrophic backtracking. An attacker can send a crafted version string that causes the regex engine to spin for seconds or minutes, creating a denial-of-service condition in any application that calls semver.coerce() with user input.",
     ["Update semver to 7.5.2 or later (7.5.4 recommended)","Run npm install","Avoid calling semver.coerce() with untrusted input"],
     [("What is ReDoS?","Regular Expression Denial of Service — a crafted input string causes a regex to backtrack exponentially, consuming CPU and hanging the process. Even a single crafted request can take down a Node.js server."),
      ("Is semver a transitive dependency?","Yes — semver is one of the most widely installed npm packages. It is a transitive dependency of npm itself, webpack, and thousands of other packages. Use npm overrides to force the safe version transitively."),
      ("How do I fix semver if it's transitive?","Add to package.json: {\"overrides\": {\"semver\": \"7.5.4\"}}. PackageFix generates this automatically when it detects a transitive semver vulnerability.")]),

    ("CVE-2023-32681","requests Proxy Credential Leak",6.1,
     "pypi","requests","< 2.31.0","2.31.0","/fix/pypi/requests",
     "Proxy credentials leaked via HTTP redirect in Python requests",
     "The Python requests library leaks Proxy-Authorization headers when following HTTP redirects from HTTPS to HTTP. Any application using requests with proxy authentication and following redirects could expose proxy credentials to the redirect destination.",
     ["Update requests to 2.31.0","Run pip install -r requirements.txt","Review any code that uses proxies with requests and follows redirects"],
     [("Who is affected by CVE-2023-32681?","Applications using requests with proxy authentication (Proxy-Authorization header) that also follow HTTP redirects. If you don't use proxy authentication, you are not affected."),
      ("Is requests widely used?","requests is one of the most downloaded Python packages — over 300 million downloads per month. Even a MEDIUM severity CVE affects a massive surface area."),
      ("What's the fix?","Update to requests 2.31.0. The fix strips Proxy-Authorization headers on redirect to different hosts.")]),

    ("CVE-2024-27351","Django ReDoS",7.5,
     "pypi","Django","< 4.2.13","4.2.13","/fix/pypi/django",
     "ReDoS in strip_tags HTML sanitizer",
     "Django's strip_tags() utility function is vulnerable to ReDoS via specially crafted HTML input. Applications that call strip_tags() on untrusted user input can be brought down by a single malicious string. strip_tags() is commonly used for sanitizing user-submitted content.",
     ["Update Django to 4.2.13 or 5.0.3","Run pip install -r requirements.txt","Avoid calling strip_tags() on very large or deeply nested HTML strings from untrusted sources"],
     [("What is strip_tags() used for?","strip_tags() removes HTML tags from a string, typically used to sanitize user-submitted content before display. It's commonly used in Django views and template tags."),
      ("Does this affect all Django versions?","Django 3.2, 4.1, 4.2, and 5.0 are all affected. 4.2.13 and 5.0.3 include the fix. Django 3.2 is end-of-life — upgrade to a supported branch."),
      ("Can this take down my Django app?","Yes — a single malicious HTTP request containing a crafted HTML string can cause strip_tags() to spin indefinitely, hanging the worker process.")]),

    ("CVE-2024-34064","Jinja2 XSS",5.4,
     "pypi","Jinja2","< 3.1.4","3.1.4","/fix/pypi/jinja2",
     "XSS via xmlattr filter with keys containing spaces",
     "Jinja2's xmlattr filter does not properly sanitize keys containing spaces. An attacker can inject additional HTML attributes into the rendered output, leading to XSS. Applications using the xmlattr filter with user-controlled dictionary keys are vulnerable.",
     ["Update Jinja2 to 3.1.4","Run pip install -r requirements.txt","Review any templates using the xmlattr filter with user-controlled input"],
     [("What is the xmlattr filter?","The xmlattr filter in Jinja2 renders a dictionary as HTML attributes. For example: <div {{ {'class': 'foo'} | xmlattr }}>. If dictionary keys come from user input, the XSS is possible."),
      ("Does this affect Flask apps?","Yes — Flask uses Jinja2 as its template engine. Any Flask application using the xmlattr filter with user input is affected."),
      ("What's the CVSS for CVE-2024-34064?","5.4 (MEDIUM) — XSS severity varies by context. In admin interfaces or authenticated areas, the impact can be higher.")]),

    ("CVE-2022-24836","Nokogiri ReDoS",7.5,
     "ruby","nokogiri","< 1.13.4","1.16.5","/fix/ruby/nokogiri",
     "ReDoS in CSS selector parsing in Nokogiri",
     "Nokogiri's CSS selector parser is vulnerable to catastrophic regex backtracking via crafted CSS selector strings. Any Ruby application that accepts user-controlled CSS selectors and passes them to Nokogiri is vulnerable to denial of service.",
     ["Update nokogiri to 1.13.4 or later (1.16.5 recommended)","Run bundle install","Avoid accepting user-controlled CSS selectors"],
     [("What is Nokogiri used for?","Nokogiri is a Ruby gem for parsing HTML and XML. It's widely used in Rails applications for HTML sanitization, web scraping, and document processing."),
      ("Does this affect rails-html-sanitizer?","Yes — rails-html-sanitizer depends on Nokogiri. Rails applications using html_sanitize with user input are indirectly affected. Update Nokogiri."),
      ("How do I check my Nokogiri version?","Run bundle exec nokogiri --version, or paste your Gemfile into PackageFix to get the current version and CVE status.")]),

    ("CVE-2023-27530","Rack DoS",7.5,
     "ruby","rack","< 3.0.4","3.0.11","/fix/ruby/rack",
     "Denial of service via multipart parsing in Rack",
     "Rack's multipart parser does not limit the number of parameters it processes, allowing an attacker to send a crafted multipart request with a huge number of parts and exhaust server memory or CPU. Any Rack-based application (Rails, Sinatra) that accepts file uploads or form submissions is vulnerable.",
     ["Update rack to 3.0.4 or later (3.0.11 recommended)","Run bundle install","Consider adding request size limits in your web server config"],
     [("Does this affect all Rails applications?","Yes — Rails runs on Rack. Any Rails app accepting multipart form submissions or file uploads is vulnerable to CVE-2023-27530 if running rack < 3.0.4."),
      ("Is rack on CISA KEV?","Yes — CISA added rack to the Known Exploited Vulnerabilities catalog. The multipart DoS is being actively used against Rails applications."),
      ("What's the temporary mitigation?","Set a request body size limit in your nginx or Apache config while you update. In nginx: client_max_body_size 10m;. Update rack as soon as possible.")]),
]

def generate_kev_page(data):
    (cve_id, name, cvss, eco, pkg, vuln_ver, safe_ver, fix_page,
     short_desc, long_desc, fix_steps, faqs) = data

    path = f"/kev/{cve_id}"
    sev = "CRITICAL" if cvss >= 9.0 else "HIGH" if cvss >= 7.0 else "MEDIUM"
    sev_class = "badge-red" if sev == "CRITICAL" else "badge-orange" if sev == "HIGH" else "badge-purple"
    eco_badge = {"npm":"badge-green","pypi":"badge-purple","ruby":"badge-red"}.get(eco,"badge-purple")

    steps_html = "".join(
        f'<li style="margin-bottom:8px;color:var(--muted);font-size:12px">{s}</li>'
        for s in fix_steps
    )

    body = f"""
<h1>{cve_id} — {name} <span class="badge {sev_class}">{sev}</span></h1>
<div style="margin-bottom:20px">
  <span class="badge badge-red" style="margin-right:6px">🔴 CISA KEV</span>
  <span class="badge {eco_badge}" style="margin-right:6px">{eco}</span>
  <span style="font-size:11px;color:var(--muted)">CVSS {cvss} · {pkg} {vuln_ver} → {safe_ver}</span>
</div>
<p class="lead">{long_desc}</p>

<div class="kev-banner">
  <div class="label">🔴 Actively Exploited</div>
  <p>{cve_id} is on the CISA Known Exploited Vulnerabilities catalog. This is not a theoretical risk — it is being used in real attacks right now. Fix immediately.</p>
</div>

<h2>What's affected</h2>
<table class="cve-table">
  <thead><tr><th>Package</th><th>Ecosystem</th><th>Vulnerable</th><th>Safe version</th><th>Fix guide</th></tr></thead>
  <tbody>
    <tr>
      <td><strong>{pkg}</strong></td>
      <td><span class="badge {eco_badge}">{eco}</span></td>
      <td>{vuln_ver}</td>
      <td>{safe_ver}</td>
      <td><a href="{fix_page}">Full fix guide →</a></td>
    </tr>
  </tbody>
</table>

<h2>How to fix {cve_id}</h2>
<ol style="padding-left:20px;margin:12px 0 20px">{steps_html}</ol>

<div class="fix-box">
  <div class="label">✓ Verify with PackageFix</div>
  <p style="margin:0">Paste your manifest into PackageFix to confirm the fix was applied. If {cve_id} no longer appears in the CVE table, you're clean.</p>
</div>

{cta()}
{faq_html(faqs)}
{related_html([
    {"url":"/cisa-kev","title":"All CISA KEV Packages","desc":"Full actively exploited list"},
    {"url":fix_page,"title":f"Fix {pkg} — Full Guide","desc":f"{eco} fix with config examples"},
    {"url":"/blog/supply-chain-attacks-package-json","title":"Supply Chain Attack Guide","desc":"5 attacks npm audit misses"},
    {"url":"/blog/weekly-cve-march-2026","title":"Weekly CVE Digest","desc":"This week's critical CVEs"},
])}"""

    breadcrumbs_data = [
        ("PackageFix","/"),("CISA KEV","/cisa-kev"),(cve_id,None)
    ]
    schemas = [
        {"@type":"TechArticle",
         "headline":f"{cve_id} — {name}",
         "description":short_desc,
         "datePublished":"2026-03-22","dateModified":"2026-03-22",
         "author":{"@type":"Organization","name":"PackageFix","url":BASE_URL}},
        {"@type":"BreadcrumbList","itemListElement":[
            {"@type":"ListItem","position":i+1,"name":n,"item":BASE_URL+(u or path)}
            for i,(n,u) in enumerate(breadcrumbs_data)
        ]},
        {"@type":"FAQPage","mainEntity":[
            {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}}
            for q,a in faqs
        ]}
    ]
    return shell(
        f"{cve_id} ({name}) — Fix Guide | PackageFix",
        f"Fix {cve_id}: {short_desc}. CVSS {cvss}. Affected: {pkg} {vuln_ver}. Safe version: {safe_ver}. Step-by-step fix for {eco}.",
        path, breadcrumbs_data, body, schemas
    )

# ══════════════════════════════════════════════════════════════════════════════
# TERMINAL PAGE
# ══════════════════════════════════════════════════════════════════════════════

def generate_terminal_page():
    faqs = [
        ("Does my manifest file get sent to a server?","No. The base64-encoded manifest is decoded entirely in your browser using JavaScript's atob() function. No data is sent to any server — the URL parameter is processed client-side only."),
        ("What if my manifest is too large for a URL?","For very large manifests (>10,000 dependencies), the URL may exceed browser limits. In that case, use the drag-and-drop upload on the main page instead."),
        ("Does this work with all 7 ecosystems?","Yes. PackageFix auto-detects the ecosystem from the file content. The same base64 technique works for package.json, requirements.txt, Gemfile, composer.json, go.mod, Cargo.toml, and pom.xml."),
        ("Can I add this to a Makefile or npm script?","Yes. Add it as a script: {\"scripts\": {\"audit-browser\": \"B64=$(base64 -i package.json) && open \\\"https://packagefix.dev/?file=$B64\\\"\"}}, then run npm run audit-browser."),
        ("Why doesn't curl packagefix.dev/api work?","PackageFix is intentionally client-side only — no backend, no API. The browser is the runtime. The terminal one-liner opens a browser window rather than making a CLI call.")
    ]

    body = f"""
<h1>Use PackageFix from the Terminal</h1>
<p class="lead">Pipe any manifest directly into PackageFix from your terminal. The file is encoded as base64 and decoded in your browser — nothing is sent to a server.</p>

<h2>The one-liner</h2>

<div class="terminal-box">
  <div class="prompt">$ npm</div>
  <div class="cmd">B64=$(base64 -i package.json) && open "https://packagefix.dev/?file=$B64"</div>
</div>

<div class="terminal-box">
  <div class="prompt">$ pypi</div>
  <div class="cmd">B64=$(base64 -i requirements.txt) && open "https://packagefix.dev/?file=$B64"</div>
</div>

<div class="terminal-box">
  <div class="prompt">$ ruby</div>
  <div class="cmd">B64=$(base64 -i Gemfile) && open "https://packagefix.dev/?file=$B64"</div>
</div>

<div class="terminal-box">
  <div class="prompt">$ php</div>
  <div class="cmd">B64=$(base64 -i composer.json) && open "https://packagefix.dev/?file=$B64"</div>
</div>

<div class="terminal-box">
  <div class="prompt">$ go</div>
  <div class="cmd">B64=$(base64 -i go.mod) && open "https://packagefix.dev/?file=$B64"</div>
</div>

<div class="terminal-box">
  <div class="prompt">$ rust</div>
  <div class="cmd">B64=$(base64 -i Cargo.toml) && open "https://packagefix.dev/?file=$B64"</div>
</div>

<div class="terminal-box">
  <div class="prompt">$ java</div>
  <div class="cmd">B64=$(base64 -i pom.xml) && open "https://packagefix.dev/?file=$B64"</div>
</div>

<h2>Linux (replace open with xdg-open)</h2>
<div class="terminal-box">
  <div class="cmd">B64=$(base64 -w0 -i package.json) && xdg-open "https://packagefix.dev/?file=$B64"</div>
</div>

<h2>Add it as an npm script</h2>
<pre>{{
  "scripts": {{
    "audit-browser": "B64=$(base64 -i package.json) && open \\"https://packagefix.dev/?file=$B64\\""
  }}
}}</pre>
<p>Then run: <code>npm run audit-browser</code></p>

<h2>Add it as a Makefile target</h2>
<pre>audit:
	B64=$$(base64 -i package.json) && open "https://packagefix.dev/?file=$$B64"</pre>

<h2>How it works</h2>
<ul style="padding-left:20px;margin:12px 0 20px;color:var(--muted);font-size:12px;line-height:2">
  <li>base64 encodes your manifest file into a URL-safe string</li>
  <li>The encoded string is passed as a <code>?file=</code> query parameter</li>
  <li>PackageFix decodes it in your browser using <code>atob()</code></li>
  <li>Ecosystem is auto-detected from the file content</li>
  <li>The file is pre-loaded in the scan interface — click Scan to run</li>
  <li>Nothing is sent to any server at any point</li>
</ul>

{cta()}
{faq_html(faqs)}
{related_html([
    {"url":"/npm","title":"npm Security Guide","desc":"All npm vulnerability guides"},
    {"url":"/guides/github-actions","title":"GitHub Actions Integration","desc":"Scan on every push"},
    {"url":"/guides/pre-commit","title":"Pre-commit Hook Guide","desc":"Scan before every commit"},
    {"url":"/cisa-kev","title":"CISA KEV Packages","desc":"Actively exploited right now"},
])}"""

    schemas = build_schemas("Use PackageFix from the terminal",
        "Pipe any manifest directly into PackageFix using base64 URL encoding",
        [{"@type":"HowToStep","name":"Encode manifest","text":"Run: B64=$(base64 -i package.json)"},
         {"@type":"HowToStep","name":"Open PackageFix","text":"Run: open https://packagefix.dev/?file=$B64"},
         {"@type":"HowToStep","name":"Scan","text":"Click Scan Dependencies in the browser"}],
        [("PackageFix","/"),("Terminal Usage","/terminal")], faqs)
    return shell(
        "Use PackageFix from the Terminal — pipe manifest via base64 URL",
        "Scan npm, PyPI, Ruby, PHP, Go, Rust, or Java dependencies directly from your terminal. One command opens PackageFix with your manifest pre-loaded. Nothing sent to a server.",
        "/terminal",
        [("PackageFix","/"),("Terminal Usage",None)],
        body, schemas
    )

# ══════════════════════════════════════════════════════════════════════════════
# GITHUB ACTIONS GUIDE
# ══════════════════════════════════════════════════════════════════════════════

def generate_github_actions_page():
    faqs = [
        ("Does PackageFix have a GitHub Actions integration?","PackageFix is a browser tool for manual scans. For automated CI scanning, use OSV Scanner (Google's open-source CLI) or the ecosystem audit tools (npm audit, pip-audit). PackageFix generates the GitHub Actions workflow YAML you can copy directly from the results page."),
        ("How do I block a deploy if critical CVEs are found?","Use --audit-level=critical in npm audit or --fail-on=critical in pip-audit. The GitHub Actions job will fail and block the deploy. See the workflows below."),
        ("Can I use PackageFix in CI without a browser?","PackageFix requires a browser. For headless CI scanning, use OSV Scanner: google/osv-scanner-action@v2. It uses the same OSV database as PackageFix."),
        ("How do I get a fixed manifest automatically in CI?","Use Renovate or Dependabot — they open PRs with fixed versions automatically. PackageFix is for manual one-off scans. Use both: PackageFix for immediate checks, Renovate for automated maintenance."),
    ]

    body = f"""
<h1>Dependency Security Scanning in GitHub Actions</h1>
<p class="lead">Add automatic CVE scanning to your GitHub Actions pipeline. Catch vulnerable dependencies on every push before they reach production.</p>

<h2>Option 1 — OSV Scanner (recommended)</h2>
<p>Google's OSV Scanner uses the same database as PackageFix. Works for all 7 ecosystems.</p>
<pre>name: Dependency Security Scan
on: [push, pull_request]

jobs:
  osv-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: google/osv-scanner-action@v2
        with:
          scan-args: |-
            --lockfile=package-lock.json</pre>

<h2>Option 2 — npm audit (npm projects)</h2>
<pre>name: npm Security Scan
on: [push, pull_request]

jobs:
  npm-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npm audit --audit-level=high</pre>

<h2>Option 3 — pip-audit (Python projects)</h2>
<pre>name: Python Security Scan
on: [push, pull_request]

jobs:
  pip-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install pip-audit
      - run: pip-audit -r requirements.txt --fail-on critical</pre>

<h2>Option 4 — bundle-audit (Ruby projects)</h2>
<pre>name: Ruby Security Scan
on: [push, pull_request]

jobs:
  bundle-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.3'
          bundler-cache: true
      - run: gem install bundler-audit
      - run: bundle audit check --update</pre>

<div class="info-box">
  <p style="margin:0"><strong>Get this YAML from PackageFix:</strong> After scanning your manifest, the "Add to CI/CD" action card generates the exact workflow for your detected ecosystem. Copy it directly.</p>
</div>

{cta()}
{faq_html(faqs)}
{related_html([
    {"url":"/terminal","title":"Terminal One-Liner","desc":"Pipe manifest from command line"},
    {"url":"/guides/pre-commit","title":"Pre-commit Hook","desc":"Scan before every commit"},
    {"url":"/cisa-kev","title":"CISA KEV Packages","desc":"Actively exploited right now"},
    {"url":"/npm","title":"npm Security Guide","desc":"All npm vulnerability guides"},
])}"""

    schemas = [
        {"@type":"HowTo","name":"Add dependency security scanning to GitHub Actions",
         "description":"Automate CVE scanning in your CI/CD pipeline with GitHub Actions",
         "estimatedCost":{"@type":"MonetaryAmount","currency":"USD","value":"0"},
         "step":[
             {"@type":"HowToStep","name":"Add workflow file","text":"Create .github/workflows/security.yml"},
             {"@type":"HowToStep","name":"Choose scanner","text":"Use OSV Scanner for all ecosystems or ecosystem-specific tools"},
             {"@type":"HowToStep","name":"Set fail threshold","text":"Use --audit-level=high or --fail-on=critical to block deploys"}
         ]},
        {"@type":"BreadcrumbList","itemListElement":[
            {"@type":"ListItem","position":1,"name":"PackageFix","item":BASE_URL},
            {"@type":"ListItem","position":2,"name":"Guides","item":BASE_URL+"/guides"},
            {"@type":"ListItem","position":3,"name":"GitHub Actions","item":BASE_URL+"/guides/github-actions"}
        ]},
        {"@type":"FAQPage","mainEntity":[
            {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}}
            for q,a in faqs
        ]}
    ]
    return shell(
        "Dependency Security Scanning in GitHub Actions | PackageFix",
        "Add CVE scanning to GitHub Actions. OSV Scanner, npm audit, pip-audit, and bundle-audit workflows — copy-paste ready. Block deploys on critical vulnerabilities.",
        "/guides/github-actions",
        [("PackageFix","/"),("Guides","/guides"),("GitHub Actions",None)],
        body, schemas
    )

# ══════════════════════════════════════════════════════════════════════════════
# PRE-COMMIT GUIDE
# ══════════════════════════════════════════════════════════════════════════════

def generate_precommit_page():
    faqs = [
        ("Should I block commits on HIGH severity CVEs?","It depends on your team. Blocking on CRITICAL is usually the right threshold — HIGH CVEs should be flagged but not necessarily block the commit. Too many blocks leads to developers bypassing the hook."),
        ("How do I skip the pre-commit hook in an emergency?","Run git commit --no-verify to bypass all pre-commit hooks. Use sparingly — the point of the hook is to catch vulnerabilities before they ship."),
        ("Does the PackageFix terminal one-liner work as a pre-commit hook?","The terminal one-liner opens a browser window — that's not suitable for a pre-commit hook. Use npm audit or OSV Scanner in the hook, then PackageFix manually for detailed analysis and fix downloads."),
        ("How do I install pre-commit?","Run pip install pre-commit, then pre-commit install in your repo root. It will run automatically on every git commit from that point."),
    ]

    body = f"""
<h1>Dependency Security Scanning with Pre-commit Hooks</h1>
<p class="lead">Catch vulnerable dependencies before they even enter your git history. Pre-commit hooks run automatically on every commit — no CI required.</p>

<h2>Quick setup — npm projects</h2>
<p>Add to your package.json scripts and use Husky:</p>
<pre># Install husky
npm install --save-dev husky
npx husky init

# Add to .husky/pre-commit:
#!/bin/sh
npm audit --audit-level=critical
if [ $? -ne 0 ]; then
  echo "Critical CVEs found. Fix before committing."
  echo "Run: npm audit fix or paste package.json into packagefix.dev"
  exit 1
fi</pre>

<h2>Using pre-commit framework (all ecosystems)</h2>
<p>Create <code>.pre-commit-config.yaml</code> in your repo root:</p>
<pre>repos:
  # OSV Scanner — works for all 7 ecosystems
  - repo: https://github.com/google/osv-scanner
    rev: v1.7.0
    hooks:
      - id: osv-scanner
        args: ['--fail-on-vuln']

  # npm audit (npm projects only)
  - repo: local
    hooks:
      - id: npm-audit
        name: npm audit
        entry: npm audit --audit-level=high
        language: system
        files: package\.json$
        pass_filenames: false</pre>

<p>Install the hooks:</p>
<pre>pip install pre-commit
pre-commit install</pre>

<h2>Python projects — pip-audit hook</h2>
<pre>repos:
  - repo: local
    hooks:
      - id: pip-audit
        name: pip-audit
        entry: pip-audit -r requirements.txt --fail-on critical
        language: system
        files: requirements\.txt$
        pass_filenames: false</pre>

<h2>Ruby projects — bundle-audit hook</h2>
<pre>repos:
  - repo: local
    hooks:
      - id: bundle-audit
        name: bundle audit
        entry: bundle audit check --update
        language: system
        files: Gemfile\.lock$
        pass_filenames: false</pre>

<div class="info-box">
  <p style="margin:0"><strong>When a hook fails:</strong> Open PackageFix, paste your manifest, and download the fixed version. The pre-commit hook tells you there's a problem — PackageFix gives you the fixed file.</p>
</div>

{cta()}
{faq_html(faqs)}
{related_html([
    {"url":"/guides/github-actions","title":"GitHub Actions Integration","desc":"Scan on every push"},
    {"url":"/terminal","title":"Terminal One-Liner","desc":"Pipe manifest from command line"},
    {"url":"/cisa-kev","title":"CISA KEV Packages","desc":"Actively exploited right now"},
    {"url":"/npm","title":"npm Security Guide","desc":"All npm vulnerability guides"},
])}"""

    schemas = [
        {"@type":"HowTo","name":"Add dependency security scanning to pre-commit hooks",
         "description":"Run CVE scanning automatically on every git commit",
         "estimatedCost":{"@type":"MonetaryAmount","currency":"USD","value":"0"},
         "step":[
             {"@type":"HowToStep","name":"Install pre-commit","text":"pip install pre-commit"},
             {"@type":"HowToStep","name":"Create config","text":"Create .pre-commit-config.yaml with OSV Scanner or ecosystem tool"},
             {"@type":"HowToStep","name":"Install hooks","text":"Run pre-commit install in your repo root"}
         ]},
        {"@type":"BreadcrumbList","itemListElement":[
            {"@type":"ListItem","position":1,"name":"PackageFix","item":BASE_URL},
            {"@type":"ListItem","position":2,"name":"Guides","item":BASE_URL+"/guides"},
            {"@type":"ListItem","position":3,"name":"Pre-commit","item":BASE_URL+"/guides/pre-commit"}
        ]},
        {"@type":"FAQPage","mainEntity":[
            {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}}
            for q,a in faqs
        ]}
    ]
    return shell(
        "Dependency Security Pre-commit Hooks | PackageFix",
        "Catch vulnerable dependencies before they enter git history. Pre-commit hooks with OSV Scanner, npm audit, pip-audit, and bundle-audit — copy-paste ready config.",
        "/guides/pre-commit",
        [("PackageFix","/"),("Guides","/guides"),("Pre-commit Hooks",None)],
        body, schemas
    )

# ══════════════════════════════════════════════════════════════════════════════
# WRITE ALL PAGES
# ══════════════════════════════════════════════════════════════════════════════

print("\n🔴 Generating KEV pages...")
for data in KEV_DATA:
    write(f"kev/{data[0]}", generate_kev_page(data))

print("\n💻 Generating terminal page...")
write("terminal", generate_terminal_page())

print("\n⚙ Generating guides...")
write("guides/github-actions", generate_github_actions_page())
write("guides/pre-commit", generate_precommit_page())

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
    priority = "0.9" if p.startswith("/kev/") else "0.8"
    freq = "monthly"
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
print(f"  ✓ sitemap-seo.xml — {len(all_paths)} new URLs")

print("\n🤖 Updating llm.txt...")
with open("llm.txt", "a") as f:
    f.write("\n## Phase 6 — KEV Pages + Terminal + Guides\n")
    for p in all_paths:
        f.write(f"{BASE_URL}{p}\n")
print("  ✓ llm.txt updated")

print(f"\n✅ Done — {len(all_paths)} Phase 6 pages")
for p in all_paths:
    print(f"   {p}")

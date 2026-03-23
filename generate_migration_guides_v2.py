#!/usr/bin/env python3
"""
PackageFix - Migration Guides v2
Avoids f-string/triple-quote conflicts by building content with string concatenation
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
h3{font-size:13px;font-weight:600;margin:24px 0 8px;color:var(--text)}
p{color:var(--muted);margin-bottom:12px;font-size:12px;line-height:1.7}
.lead{color:var(--text);font-size:13px;margin-bottom:24px;line-height:1.7}
.warning-box{background:rgba(249,115,22,.08);border:1px solid rgba(249,115,22,.3);border-left:3px solid var(--orange);border-radius:8px;padding:16px 20px;margin:20px 0}
.warning-box .label{font-size:10px;font-weight:700;color:var(--orange);text-transform:uppercase;letter-spacing:.1em;margin-bottom:8px}
.fix-box{background:rgba(34,197,94,.08);border:1px solid rgba(34,197,94,.3);border-left:3px solid var(--green);border-radius:8px;padding:16px 20px;margin:20px 0}
pre{background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:14px 16px;overflow-x:auto;font-size:11px;line-height:1.6;margin:8px 0;white-space:pre-wrap}
code{background:var(--surface);border:1px solid var(--border);border-radius:3px;padding:1px 5px;font-size:11px}
.cta-box{background:var(--surface);border:1px solid var(--purple);border-radius:10px;padding:24px;margin:32px 0;text-align:center}
.cta-box p{color:var(--text);font-size:13px;margin-bottom:16px}
.cta-btn{display:inline-block;background:var(--purple);color:#fff;font-family:'JetBrains Mono',monospace;font-size:13px;font-weight:600;padding:12px 28px;border-radius:7px;text-decoration:none}
.badge-orange{background:rgba(249,115,22,.2);color:var(--orange);border:1px solid var(--orange);display:inline-block;font-size:10px;font-weight:700;padding:2px 8px;border-radius:4px;text-transform:uppercase}
.option-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px;margin:16px 0}
.option-card{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:18px}
.option-card h3{font-size:13px;font-weight:600;margin:0 0 8px;color:var(--text)}
.option-card .tag{font-size:10px;color:var(--purple);text-transform:uppercase;letter-spacing:.08em;margin-bottom:8px;display:block}
.option-card p{font-size:11px;margin:0;line-height:1.6}
.diff-row{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:12px 0}
.col-label{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;margin-bottom:4px;padding:4px 8px;border-radius:4px}
.col-label.before{background:rgba(239,68,68,.15);color:#EF4444}
.col-label.after{background:rgba(34,197,94,.15);color:#22C55E}
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
@media(max-width:640px){.nav-links{display:none}.related-grid,.option-grid{grid-template-columns:1fr}.diff-row{grid-template-columns:1fr}}
"""

def page(title, desc, canonical_path, breadcrumbs, body, schemas):
    canonical = BASE_URL + canonical_path
    sj = json.dumps({"@context": "https://schema.org", "@graph": schemas}, indent=2)
    crumb = " <span style='color:var(--border)'>/</span> ".join(
        ('<a href="' + u + '">' + n + '</a>') if u else ('<span style="color:var(--text)">' + n + '</span>')
        for n, u in breadcrumbs)
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
        '<div class="breadcrumb">' + crumb + '</div>'
        + body +
        '</main>'
        '<footer class="site-footer">'
        '<p>PackageFix &middot; <a href="/">packagefix.dev</a> &middot; MIT Licensed &middot; Open Source</p>'
        '<p style="margin-top:6px">Vulnerability data: <a href="https://osv.dev">OSV</a> &middot; '
        '<a href="https://www.cisa.gov/known-exploited-vulnerabilities-catalog">CISA KEV</a></p>'
        '</footer></body></html>'
    )

def cta():
    return (
        '<div class="cta-box">'
        '<p>Check your current dependencies for CVEs before migrating.</p>'
        '<a href="/" class="cta-btn">Scan with PackageFix &rarr;</a>'
        '<p style="margin-top:12px;font-size:11px;color:var(--muted)">Free &middot; No signup &middot; No CLI &middot; Runs in your browser</p>'
        '</div>'
    )

def faqs(items):
    html = '<div class="faq"><h2>Common questions</h2>'
    for q, a in items:
        html += '<div class="faq-item"><div class="faq-q">' + q + '</div><div class="faq-a">' + a + '</div></div>'
    return html + '</div>'

def related(pages):
    html = '<div style="margin:40px 0"><h2>Related</h2><div class="related-grid">'
    for p in pages:
        html += '<div class="related-card"><a href="' + p["url"] + '">' + p["title"] + '</a><p>' + p["desc"] + '</p></div>'
    return html + '</div></div>'

def diff(before_label, before_code, after_label, after_code):
    return (
        '<div class="diff-row">'
        '<div><div class="col-label before">' + before_label + '</div>'
        '<pre>' + before_code + '</pre></div>'
        '<div><div class="col-label after">' + after_label + '</div>'
        '<pre>' + after_code + '</pre></div>'
        '</div>'
    )

def option_card(tag, title, desc, install):
    return (
        '<div class="option-card">'
        '<span class="tag">' + tag + '</span>'
        '<h3>' + title + '</h3>'
        '<p>' + desc + '</p>'
        '<p style="margin-top:8px"><code>' + install + '</code></p>'
        '</div>'
    )

all_paths = []

def write(slug, html):
    p = os.path.join("seo", slug, "index.html")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(html)
    all_paths.append("/" + slug)
    print("  OK /" + slug)

def bc(items):
    return [{"@type": "ListItem", "position": i+1, "name": n, "item": BASE_URL + (u or "")}
            for i, (n, u) in enumerate(items)]


# =============================================================================
# MOMENT.JS MIGRATION GUIDE
# =============================================================================
print("\nGenerating moment.js migration guide...")

# All code blocks as plain variables - no f-strings
moment_basic_before = (
    "// Parse\n"
    "moment('2024-01-15')\n"
    "moment('2024-01-15', 'YYYY-MM-DD')\n\n"
    "// Format\n"
    "moment().format('YYYY-MM-DD')\n"
    "moment().format('MMMM Do YYYY')\n\n"
    "// Manipulate\n"
    "moment().add(7, 'days')\n"
    "moment().subtract(1, 'month')\n\n"
    "// Compare\n"
    "moment('2024-01-15').isBefore('2024-06-01')\n"
    "moment('2024-01-15').isAfter(moment())\n\n"
    "// Display\n"
    "moment().fromNow()\n"
    "moment().toDate()"
)

moment_basic_after = (
    "// Parse\n"
    "dayjs('2024-01-15')\n"
    "dayjs('2024-01-15', 'YYYY-MM-DD')  // needs customParseFormat plugin\n\n"
    "// Format\n"
    "dayjs().format('YYYY-MM-DD')\n"
    "dayjs().format('MMMM Do YYYY')     // needs advancedFormat plugin\n\n"
    "// Manipulate\n"
    "dayjs().add(7, 'day')\n"
    "dayjs().subtract(1, 'month')\n\n"
    "// Compare\n"
    "dayjs('2024-01-15').isBefore('2024-06-01')\n"
    "dayjs('2024-01-15').isAfter(dayjs())\n\n"
    "// Display\n"
    "dayjs().fromNow()  // needs relativeTime plugin\n"
    "dayjs().toDate()"
)

moment_tz_before = (
    "import moment from 'moment-timezone'\n\n"
    "moment.tz('2024-01-15 12:00', 'America/New_York')\n"
    "moment().tz('Europe/London').format()"
)

moment_tz_after = (
    "import dayjs from 'dayjs'\n"
    "import utc from 'dayjs/plugin/utc'\n"
    "import timezone from 'dayjs/plugin/timezone'\n"
    "dayjs.extend(utc)\n"
    "dayjs.extend(timezone)\n\n"
    "dayjs.tz('2024-01-15 12:00', 'America/New_York')\n"
    "dayjs().tz('Europe/London').format()"
)

moment_datefns_before = (
    "import moment from 'moment'\n\n"
    "// Format\n"
    "moment().format('yyyy-MM-dd')\n\n"
    "// Add days\n"
    "moment().add(7, 'days').toDate()\n\n"
    "// Check if before\n"
    "moment('2024-01-15').isBefore('2024-06-01')\n\n"
    "// From now\n"
    "moment().fromNow()"
)

moment_datefns_after = (
    "import { format, addDays, isBefore, formatDistanceToNow } from 'date-fns'\n\n"
    "// Format\n"
    "format(new Date(), 'yyyy-MM-dd')\n\n"
    "// Add days\n"
    "addDays(new Date(), 7)\n\n"
    "// Check if before\n"
    "isBefore(new Date('2024-01-15'), new Date('2024-06-01'))\n\n"
    "// From now\n"
    "formatDistanceToNow(new Date(), { addSuffix: true })"
)

moment_plugins_code = (
    "import dayjs from 'dayjs'\n"
    "import relativeTime from 'dayjs/plugin/relativeTime'\n"
    "import advancedFormat from 'dayjs/plugin/advancedFormat'\n"
    "import customParseFormat from 'dayjs/plugin/customParseFormat'\n"
    "import timezone from 'dayjs/plugin/timezone'\n"
    "import utc from 'dayjs/plugin/utc'\n"
    "import duration from 'dayjs/plugin/duration'\n\n"
    "dayjs.extend(relativeTime)\n"
    "dayjs.extend(advancedFormat)\n"
    "dayjs.extend(customParseFormat)\n"
    "dayjs.extend(utc)\n"
    "dayjs.extend(timezone)"
)

moment_faqs_data = [
    ("Is moment.js broken?",
     "Not broken - moment.js 2.29.4 works and has no unpatched CVEs. The issue is maintenance-only mode. "
     "The team will not add features or fix non-security bugs. Future CVEs may not get patches. "
     "For long-lived projects, migrating before you have to is easier than migrating under pressure."),
    ("Which replacement is easiest to migrate to?",
     "dayjs has an almost identical API to moment.js. Most moment.js code works with dayjs after changing "
     "the import. date-fns uses a completely different functional API and requires rewriting your date logic."),
    ("Can I run moment.js and dayjs side by side?",
     "Yes - both can be installed simultaneously. Migrate file by file, testing as you go. "
     "Remove moment.js when the last import is gone."),
    ("Does dayjs support all moment.js plugins?",
     "dayjs has its own plugin ecosystem covering most moment.js plugin functionality. "
     "Check the dayjs plugin docs before migrating - duration, timezone, and relative time all have equivalents."),
    ("Is date-fns tree-shakeable?",
     "Yes - this is one of date-fns's main advantages over moment.js. Only the functions you import "
     "get bundled. Typical date-fns usage adds 5-10KB vs moment's 67KB minimum.")
]

moment_body = (
    '<h1>Migrating from moment.js - Complete Guide</h1>'
    '<p class="lead">moment.js is in maintenance mode. It still works and 2.29.4 has no unpatched CVEs, '
    'but new features will not be added and future security fixes are not guaranteed. '
    'This guide covers migrating to dayjs (near drop-in) or date-fns (more modern, tree-shakeable).</p>'

    '<div class="warning-box"><div class="label">moment.js Status</div>'
    '<p>moment.js has been in maintenance-only mode since September 2020. No new features, '
    'no non-security bug fixes. It has 4 known CVEs - all fixed in 2.29.4. '
    'Future CVEs may not receive patches.</p></div>'

    '<h2>Choose your replacement</h2>'
    '<div class="option-grid">'
    + option_card("Easiest migration", "dayjs",
        "Near-identical API to moment.js. 2KB gzipped vs moment 67KB. "
        "Most moment.js code works after changing the import.",
        "npm install dayjs")
    + option_card("Most modern", "date-fns",
        "Functional API - completely different from moment. "
        "Tree-shakeable, TypeScript-first. Better for new code than migration.",
        "npm install date-fns")
    + option_card("Full featured", "Luxon",
        "Built by a moment.js author. Wraps the native Intl API. "
        "Immutable by default. Best for serious timezone and locale support.",
        "npm install luxon")
    + option_card("No dependency (Node 18+)", "Temporal API",
        "Upcoming native JavaScript date API. Currently a TC39 proposal "
        "with polyfill available.",
        "npm install @js-temporal/polyfill")
    + '</div>'

    '<h2>Option A - Migrate to dayjs (recommended for existing codebases)</h2>'

    '<h3>Step 1 - Install dayjs and remove moment</h3>'
    '<pre>npm install dayjs\nnpm uninstall moment</pre>'

    '<h3>Step 2 - Replace imports</h3>'
    + diff("moment.js", "import moment from 'moment';",
           "dayjs", "import dayjs from 'dayjs';")

    + '<h3>Step 3 - Basic usage</h3>'
    + diff("moment.js", moment_basic_before, "dayjs", moment_basic_after)

    + '<h3>Step 4 - Enable plugins you need</h3>'
    + '<pre>' + moment_plugins_code + '</pre>'

    + '<h3>Step 5 - Timezone handling</h3>'
    + diff("moment-timezone", moment_tz_before, "dayjs timezone", moment_tz_after)

    + '<h3>Key differences to watch for</h3>'
    '<ul style="padding-left:20px;margin:12px 0;color:var(--muted);font-size:12px;line-height:2">'
    '<li>dayjs objects are <strong>immutable</strong> - manipulations return new objects</li>'
    "<li>add() uses singular units: 'day' not 'days'</li>"
    '<li>moment.duration() requires dayjs/plugin/duration</li>'
    '<li>moment.utc() requires dayjs/plugin/utc</li>'
    '<li>fromNow() requires dayjs/plugin/relativeTime</li>'
    '</ul>'

    '<h2>Option B - Migrate to date-fns</h2>'
    '<p>date-fns uses a functional API - every operation is a standalone function. '
    'Better for greenfield code than migration.</p>'
    + diff("moment.js", moment_datefns_before, "date-fns", moment_datefns_after)

    + '<h2>Check your CVE status first</h2>'
    '<p>If you are on moment.js 2.29.4 you have no unpatched CVEs. '
    'The migration is about future-proofing, not an emergency.</p>'
    + cta()
    + faqs(moment_faqs_data)
    + related([
        {"url": "/fix/npm/moment", "title": "moment.js CVE History", "desc": "All 4 known CVEs"},
        {"url": "/npm", "title": "npm Security Overview", "desc": "All npm CVE guides"},
        {"url": "/glossary/remediation", "title": "Remediation", "desc": "Fix strategies"},
        {"url": "/fix/npm/request/migrate", "title": "request Migration Guide", "desc": "Another deprecated package"},
    ])
)

moment_schemas = [
    {"@type": "HowTo", "name": "Migrate from moment.js to dayjs",
     "description": "Step-by-step guide to replace moment.js with dayjs or date-fns",
     "estimatedCost": {"@type": "MonetaryAmount", "currency": "USD", "value": "0"},
     "step": [
         {"@type": "HowToStep", "name": "Install dayjs", "text": "Run: npm install dayjs && npm uninstall moment"},
         {"@type": "HowToStep", "name": "Replace imports", "text": "Change import moment to import dayjs"},
         {"@type": "HowToStep", "name": "Enable plugins", "text": "Add relativeTime, timezone, duration plugins"},
         {"@type": "HowToStep", "name": "Test", "text": "Run your test suite"}
     ]},
    {"@type": "BreadcrumbList", "itemListElement": bc([
        ("PackageFix", "/"), ("Fix Guides", "/fix"), ("npm", "/npm"),
        ("moment.js", "/fix/npm/moment"), ("Migration Guide", None)
    ])},
    {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in moment_faqs_data
    ]}
]

write("fix/npm/moment/migrate", page(
    "Migrating from moment.js to dayjs or date-fns - Complete Guide | PackageFix",
    "moment.js is in maintenance mode. Migrate to dayjs (near drop-in) or date-fns (modern). Side-by-side code examples for every common operation.",
    "/fix/npm/moment/migrate",
    [("PackageFix", "/"), ("Fix Guides", "/fix"), ("npm", "/npm"),
     ("moment.js", "/fix/npm/moment"), ("Migration Guide", None)],
    moment_body, moment_schemas
))


# =============================================================================
# REQUEST DEPRECATION GUIDE
# =============================================================================
print("\nGenerating request deprecation guide...")

req_get_before = (
    "const request = require('request')\n\n"
    "// Callback style\n"
    "request('https://api.example.com/data', (err, res, body) => {\n"
    "  if (err) throw err\n"
    "  const data = JSON.parse(body)\n"
    "  console.log(data)\n"
    "})\n\n"
    "// With request-promise\n"
    "const rp = require('request-promise')\n"
    "const data = await rp.get({\n"
    "  uri: 'https://api.example.com/data',\n"
    "  json: true\n"
    "})"
)

req_get_after = (
    "const axios = require('axios')\n"
    "// or: import axios from 'axios'\n\n"
    "// Automatic JSON parsing\n"
    "const { data } = await axios.get('https://api.example.com/data')\n"
    "console.log(data)\n\n"
    "// With options\n"
    "const { data } = await axios.get('https://api.example.com/data', {\n"
    "  params: { page: 1 },\n"
    "  headers: { Authorization: 'Bearer token' }\n"
    "})"
)

req_post_before = (
    "request.post({\n"
    "  url: 'https://api.example.com/users',\n"
    "  json: true,\n"
    "  body: { name: 'Alice', email: 'alice@example.com' }\n"
    "}, (err, res, body) => {\n"
    "  console.log(body)\n"
    "})"
)

req_post_after = (
    "const { data } = await axios.post('https://api.example.com/users', {\n"
    "  name: 'Alice',\n"
    "  email: 'alice@example.com'\n"
    "})\n"
    "console.log(data)"
)

req_error_before = (
    "request('https://api.example.com', (err, res, body) => {\n"
    "  if (err) {\n"
    "    console.error('Network error:', err)\n"
    "    return\n"
    "  }\n"
    "  if (res.statusCode !== 200) {\n"
    "    console.error('HTTP error:', res.statusCode)\n"
    "    return\n"
    "  }\n"
    "  console.log(JSON.parse(body))\n"
    "})"
)

req_error_after = (
    "try {\n"
    "  const { data } = await axios.get('https://api.example.com')\n"
    "  console.log(data)\n"
    "} catch (err) {\n"
    "  if (err.response) {\n"
    "    // non-200 response\n"
    "    console.error('HTTP error:', err.response.status)\n"
    "  } else {\n"
    "    // network failure\n"
    "    console.error('Network error:', err.message)\n"
    "  }\n"
    "}"
)

req_headers_before = (
    "request({\n"
    "  url: 'https://api.example.com/data',\n"
    "  headers: {\n"
    "    'Authorization': 'Bearer mytoken',\n"
    "    'X-Custom-Header': 'value'\n"
    "  },\n"
    "  auth: { user: 'username', pass: 'password' }\n"
    "}, callback)"
)

req_headers_after = (
    "// Per-request headers\n"
    "await axios.get('https://api.example.com/data', {\n"
    "  headers: {\n"
    "    'Authorization': 'Bearer mytoken',\n"
    "    'X-Custom-Header': 'value'\n"
    "  },\n"
    "  auth: { username: 'username', password: 'password' }\n"
    "})\n\n"
    "// Global defaults\n"
    "axios.defaults.headers.common['Authorization'] = 'Bearer mytoken'"
)

req_got_before = (
    "const request = require('request')\n\n"
    "request.get({\n"
    "  url: 'https://api.example.com/data',\n"
    "  json: true\n"
    "}, (err, res, body) => {\n"
    "  console.log(body)\n"
    "})"
)

req_got_after = (
    "const got = require('got')\n\n"
    "const body = await got('https://api.example.com/data').json()\n"
    "console.log(body)\n\n"
    "// With options\n"
    "const body = await got('https://api.example.com/data', {\n"
    "  searchParams: { page: 1 },\n"
    "  headers: { Authorization: 'Bearer token' }\n"
    "}).json()"
)

req_fetch_before = (
    "request('https://api.example.com/data', (err, res, body) => {\n"
    "  const data = JSON.parse(body)\n"
    "  console.log(data)\n"
    "})"
)

req_fetch_after = (
    "// Built into Node.js 18+\n"
    "const res = await fetch('https://api.example.com/data')\n"
    "if (!res.ok) throw new Error('HTTP error: ' + res.status)\n"
    "const data = await res.json()\n"
    "console.log(data)\n\n"
    "// POST\n"
    "const res = await fetch('https://api.example.com/users', {\n"
    "  method: 'POST',\n"
    "  headers: { 'Content-Type': 'application/json' },\n"
    "  body: JSON.stringify({ name: 'Alice' })\n"
    "})\n"
    "const data = await res.json()"
)

request_faqs_data = [
    ("Is request still safe to use?",
     "request has been deprecated since February 2020 - no security patches, no updates. "
     "Any new CVE will never be fixed. You should migrate."),
    ("Which replacement is easiest to migrate from request?",
     "got has an API most similar to request and was designed as a modern replacement. "
     "axios is the most popular choice overall. For Node.js 18+, native fetch works for simple use cases."),
    ("Does request support async/await?",
     "request uses callbacks natively. The request-promise wrapper is also deprecated. "
     "Modern alternatives support async/await natively."),
    ("Is axios safe to use in 2026?",
     "axios 1.7.4 has no unpatched CVEs. It is actively maintained and the most widely used "
     "JavaScript HTTP client for both Node.js and browser environments."),
    ("Should I use native fetch instead of a library?",
     "For Node.js 18+, the built-in fetch handles most HTTP use cases with zero dependencies. "
     "For retries, interceptors, or streaming, a library like got or axios is worth the dependency.")
]

request_body = (
    '<h1>Migrating away from request - Complete Guide</h1>'
    '<p class="lead">The request npm package has been deprecated since February 2020 and receives '
    'no security patches. With 15M+ weekly downloads it is still in millions of production applications. '
    'This guide covers migrating to axios, got, or native fetch.</p>'

    '<div class="warning-box"><div class="label">request is deprecated</div>'
    '<p>request has been officially deprecated since February 11, 2020. No security patches, '
    'no bug fixes, no updates. Any CVE discovered in request will never be fixed. '
    'The maintainers explicitly recommend migration.</p></div>'

    '<h2>Choose your replacement</h2>'
    '<div class="option-grid">'
    + option_card("Most popular", "axios",
        "The most widely-used Node.js HTTP client. Works in Node.js and the browser. "
        "Promise-based, supports interceptors, automatic JSON parsing.",
        "npm install axios")
    + option_card("Easiest migration from request", "got",
        "Designed as a modern replacement for request. Supports retries, pagination, HTTP/2. "
        "ESM-only in v12+.",
        "npm install got")
    + option_card("No dependency (Node 18+)", "Native fetch",
        "Built into Node.js 18+. No install needed. "
        "Covers basic GET and POST with no dependencies.",
        "Built-in - no install")
    + option_card("Lightweight", "node-fetch",
        "Polyfills the browser fetch API for Node.js. "
        "ESM-only in v3, CJS in v2.",
        "npm install node-fetch")
    + '</div>'

    '<h2>Option A - Migrate to axios (recommended)</h2>'
    '<h3>Install</h3>'
    '<pre>npm install axios\nnpm uninstall request request-promise</pre>'

    '<h3>GET requests</h3>'
    + diff("request", req_get_before, "axios", req_get_after)

    + '<h3>POST requests</h3>'
    + diff("request", req_post_before, "axios", req_post_after)

    + '<h3>Error handling</h3>'
    + diff("request", req_error_before, "axios", req_error_after)

    + '<h3>Headers and auth</h3>'
    + diff("request", req_headers_before, "axios", req_headers_after)

    + '<h2>Option B - Migrate to got</h2>'
    '<p>got is ESM-only from v12. If you are on CommonJS (require()), use got v11 or switch to axios.</p>'
    '<pre>npm install got@11   # CommonJS compatible\nnpm install got      # ESM only (v12+)</pre>'
    + diff("request", req_got_before, "got v11", req_got_after)

    + '<h2>Option C - Native fetch (Node.js 18+)</h2>'
    '<p>No install required. Best for simple requests where you do not need retries or interceptors.</p>'
    + diff("request", req_fetch_before, "native fetch", req_fetch_after)

    + '<h2>Check your CVE exposure first</h2>'
    '<p>Paste your package.json into PackageFix to see which request-related CVEs you are currently exposed to.</p>'
    + cta()
    + faqs(request_faqs_data)
    + related([
        {"url": "/fix/npm/axios", "title": "axios CVE History", "desc": "All axios vulnerabilities"},
        {"url": "/fix/npm/node-fetch", "title": "node-fetch CVE History", "desc": "node-fetch vulnerabilities"},
        {"url": "/fix/npm/moment/migrate", "title": "moment.js Migration", "desc": "Another deprecated package"},
        {"url": "/npm", "title": "npm Security Overview", "desc": "All npm CVE guides"},
    ])
)

request_schemas = [
    {"@type": "HowTo", "name": "Migrate from request npm package to axios or got",
     "description": "Step-by-step guide to replace the deprecated request package",
     "estimatedCost": {"@type": "MonetaryAmount", "currency": "USD", "value": "0"},
     "step": [
         {"@type": "HowToStep", "name": "Choose replacement", "text": "axios for most projects, got for request-like API"},
         {"@type": "HowToStep", "name": "Install", "text": "npm install axios && npm uninstall request request-promise"},
         {"@type": "HowToStep", "name": "Replace callbacks", "text": "axios and got are promise-based - use async/await"},
         {"@type": "HowToStep", "name": "Update error handling", "text": "axios throws on non-200 responses - update error handling"}
     ]},
    {"@type": "BreadcrumbList", "itemListElement": bc([
        ("PackageFix", "/"), ("Fix Guides", "/fix"), ("npm", "/npm"),
        ("request", "/fix/npm/request"), ("Migration Guide", None)
    ])},
    {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in request_faqs_data
    ]}
]

write("fix/npm/request/migrate", page(
    "Migrating from request (deprecated) to axios, got, or fetch - Complete Guide | PackageFix",
    "request has been deprecated since 2020 with no security patches. Migrate to axios, got, or native fetch. Side-by-side code for GET, POST, error handling, and auth.",
    "/fix/npm/request/migrate",
    [("PackageFix", "/"), ("Fix Guides", "/fix"), ("npm", "/npm"),
     ("request", "/fix/npm/request"), ("Migration Guide", None)],
    request_body, request_schemas
))


# =============================================================================
# UPDATE CONFIG FILES
# =============================================================================
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
print("  vercel.json - " + str(len(existing)) + " rewrites (" + str(added) + " new)")

print("Updating sitemap-seo.xml...")
new_urls = ""
for p in all_paths:
    new_urls += "  <url>\n    <loc>" + BASE_URL + p + "</loc>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n"

if os.path.exists("sitemap-seo.xml"):
    with open("sitemap-seo.xml") as f:
        content = f.read()
    updated = content.replace("</urlset>", new_urls + "</urlset>")
else:
    updated = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + new_urls + "</urlset>"
with open("sitemap-seo.xml", "w") as f:
    f.write(updated)
print("  sitemap-seo.xml - " + str(len(all_paths)) + " new URLs")

print("Updating llm.txt...")
with open("llm.txt", "a") as f:
    f.write("\n## Migration Guides\n")
    for p in all_paths:
        f.write(BASE_URL + p + "\n")
print("  llm.txt updated")

print("\nDone - " + str(len(all_paths)) + " pages generated")
for p in all_paths:
    print("  " + p)

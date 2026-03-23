#!/usr/bin/env python3
"""
PackageFix — Migration Guides
1. /fix/npm/moment/migrate — moment.js → date-fns / dayjs
2. /fix/npm/request/migrate — request → axios / node-fetch / got
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
.fix-box .label{font-size:10px;font-weight:700;color:var(--green);text-transform:uppercase;letter-spacing:.1em;margin-bottom:8px}
.option-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px;margin:16px 0}
.option-card{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:18px}
.option-card h3{font-size:13px;font-weight:600;margin:0 0 8px;color:var(--text)}
.option-card .tag{font-size:10px;color:var(--purple);text-transform:uppercase;letter-spacing:.08em;margin-bottom:8px;display:block}
.option-card p{font-size:11px;margin:0;line-height:1.6}
pre{background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:14px 16px;overflow-x:auto;font-size:11px;line-height:1.6;margin:8px 0;white-space:pre-wrap}
code{background:var(--surface);border:1px solid var(--border);border-radius:3px;padding:1px 5px;font-size:11px}
.cta-box{background:var(--surface);border:1px solid var(--purple);border-radius:10px;padding:24px;margin:32px 0;text-align:center}
.cta-box p{color:var(--text);font-size:13px;margin-bottom:16px}
.cta-btn{display:inline-block;background:var(--purple);color:#fff;font-family:'JetBrains Mono',monospace;font-size:13px;font-weight:600;padding:12px 28px;border-radius:7px;text-decoration:none}
.badge{display:inline-block;font-size:10px;font-weight:700;padding:2px 8px;border-radius:4px;text-transform:uppercase;letter-spacing:.05em}
.badge-orange{background:rgba(249,115,22,.2);color:var(--orange);border:1px solid var(--orange)}
.badge-green{background:rgba(34,197,94,.2);color:var(--green);border:1px solid var(--green)}
.badge-purple{background:rgba(108,99,255,.2);color:var(--purple);border:1px solid var(--purple)}
.faq{margin:40px 0}.faq-item{border-bottom:1px solid var(--border);padding:16px 0}
.faq-item:last-child{border-bottom:none}
.faq-q{font-size:12px;font-weight:600;color:var(--text);margin-bottom:8px}
.faq-a{font-size:12px;color:var(--muted);line-height:1.7}
.related-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px;margin-top:12px}
.related-card{background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:14px}
.related-card a{color:var(--text);font-size:12px;font-weight:500}
.related-card p{font-size:11px;color:var(--muted);margin:4px 0 0}
.diff-row{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:12px 0}
.diff-row .col-label{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;margin-bottom:4px;padding:4px 8px;border-radius:4px}
.col-label.before{background:rgba(239,68,68,.15);color:var(--red)}
.col-label.after{background:rgba(34,197,94,.15);color:var(--green)}
.site-footer{border-top:1px solid var(--border);padding:24px;text-align:center;font-size:11px;color:var(--muted);margin-top:60px}
.site-footer a{color:var(--muted)}
@media(max-width:640px){.nav-links{display:none}.related-grid{grid-template-columns:1fr}.option-grid{grid-template-columns:1fr}.diff-row{grid-template-columns:1fr}}
"""

def shell(title, desc, path, breadcrumbs, body, schemas):
    canonical = BASE_URL + path
    sj = json.dumps({"@context":"https://schema.org","@graph":schemas}, indent=2)
    crumb = " <span style='color:var(--border)'>/</span> ".join(
        f'<a href="{u}">{n}</a>' if u else f'<span style="color:var(--text)">{n}</span>'
        for n,u in breadcrumbs)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="article">
<meta name="twitter:card" content="summary">
<link rel="icon" type="image/svg+xml" href="/icon.svg">
<link rel="icon" type="image/png" sizes="512x512" href="/icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<script type="application/ld+json">{sj}</script>
<style>{TOKENS}</style>
</head>
<body>
<header class="site-header">
  <a href="/" class="logo">Package<span>Fix</span></a>
  <nav class="nav-links">
    <a href="/">Tool</a>
    <a href="/glossary">Glossary</a>
    <a href="/cisa-kev">CISA KEV</a>
    <a href="/blog">Blog</a>
    <a href="https://github.com/metriclogic26/packagefix">GitHub</a>
  </nav>
</header>
<main class="container">
  <div class="breadcrumb">{crumb}</div>
  {body}
</main>
<footer class="site-footer">
  <p>PackageFix · <a href="/">packagefix.dev</a> · MIT Licensed · Open Source</p>
  <p style="margin-top:6px">Vulnerability data: <a href="https://osv.dev">OSV</a> · <a href="https://www.cisa.gov/known-exploited-vulnerabilities-catalog">CISA KEV</a></p>
  <p style="margin-top:6px">Always test in staging before deploying to production.</p>
</footer>
</body></html>"""

def cta():
    return """<div class="cta-box">
  <p>Check your current dependencies for CVEs before migrating.</p>
  <a href="/" class="cta-btn">Scan with PackageFix →</a>
  <p style="margin-top:12px;font-size:11px;color:var(--muted)">Free · No signup · No CLI · Runs in your browser</p>
</div>"""

def faq_html(faqs):
    items = "".join(f'<div class="faq-item"><div class="faq-q">{q}</div><div class="faq-a">{a}</div></div>' for q,a in faqs)
    return f'<div class="faq"><h2>Common questions</h2>{items}</div>'

def related_html(pages):
    cards = "".join(f'<div class="related-card"><a href="{p["url"]}">{p["title"]}</a><p>{p["desc"]}</p></div>' for p in pages)
    return f'<div style="margin:40px 0"><h2>Related</h2><div class="related-grid">{cards}</div></div>'

all_paths = []

def write(slug, html):
    p = os.path.join("seo", slug, "index.html")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(html)
    all_paths.append("/" + slug)
    print(f"  ✓ /{slug}")

def diff(before_label, before_code, after_label, after_code):
    return f"""<div class="diff-row">
  <div>
    <div class="col-label before">{before_label}</div>
    <pre>{before_code}</pre>
  </div>
  <div>
    <div class="col-label after">{after_label}</div>
    <pre>{after_code}</pre>
  </div>
</div>"""

# ══════════════════════════════════════════════════════════════════════════════
# 1. MOMENT.JS MIGRATION GUIDE
# ══════════════════════════════════════════════════════════════════════════════

print("\n📅 Generating moment.js migration guide...")

moment_faqs = [
    ("Is moment.js broken?","Not broken — moment.js 2.29.4 works fine and has no unpatched CVEs. The issue is that it's in maintenance mode. The team won't add features or fix non-security bugs. Future CVEs may not get patches. For long-lived projects, migrating before you have to is easier than migrating under pressure."),
    ("Which replacement is the easiest migration from moment?","dayjs has an almost identical API to moment.js. Most moment.js code works with dayjs after changing the import — you don't need to relearn anything. date-fns is more comprehensive but uses a completely different functional API that requires rewriting your date logic."),
    ("Can I run moment.js and dayjs side by side during migration?","Yes — both can be installed simultaneously. Migrate file by file, testing as you go. Remove moment.js from package.json when the last import is gone."),
    ("Does dayjs support all moment.js plugins?","dayjs has its own plugin ecosystem that covers most moment.js plugin functionality. Check the dayjs plugin docs before migrating — plugins like duration, timezone, and relative time all have dayjs equivalents."),
    ("What about moment-timezone?","dayjs has dayjs/plugin/timezone which uses the native Intl.DateTimeFormat API. It's smaller and doesn't require a timezone database bundle. The API is slightly different — check the dayjs timezone plugin docs."),
    ("Is date-fns tree-shakeable?","Yes — this is one of date-fns's main advantages over moment.js. Only the functions you import get bundled. A typical date-fns usage might add 5-10KB to your bundle vs moment.js's 67KB minimum.")
]

moment_body = f"""
<h1>Migrating from moment.js — Complete Guide</h1>
<p class="lead">moment.js is in maintenance mode. It still works and 2.29.4 has no unpatched CVEs, but new features won't be added and future security fixes aren't guaranteed. This guide covers migrating to dayjs (near drop-in) or date-fns (more modern, tree-shakeable).</p>

<div class="warning-box">
  <div class="label">⚠ moment.js Status</div>
  <p>moment.js is officially in maintenance-only mode as of September 2020. The team recommends using Luxon, date-fns, or dayjs for new projects. The package has <strong>4 known CVEs</strong> — all fixed in 2.29.4. Future CVEs may not receive patches.</p>
</div>

<h2>Choose your replacement</h2>
<div class="option-grid">
  <div class="option-card">
    <span class="tag">Easiest migration</span>
    <h3>dayjs</h3>
    <p>Near-identical API to moment.js. 2KB gzipped vs moment's 67KB. Most moment.js code works after changing the import. Plugin ecosystem covers timezone, duration, relative time.</p>
    <p style="margin-top:8px"><code>npm install dayjs</code></p>
  </div>
  <div class="option-card">
    <span class="tag">Most modern</span>
    <h3>date-fns</h3>
    <p>Functional API — completely different from moment. Tree-shakeable, TypeScript-first. Better for new code than migration. 200+ utility functions, each imported separately.</p>
    <p style="margin-top:8px"><code>npm install date-fns</code></p>
  </div>
  <div class="option-card">
    <span class="tag">Full featured</span>
    <h3>Luxon</h3>
    <p>Built by one of the moment.js authors. Wraps the native Intl API. Immutable by default. Best if you need serious timezone and locale support.</p>
    <p style="margin-top:8px"><code>npm install luxon</code></p>
  </div>
  <div class="option-card">
    <span class="tag">Native (no library)</span>
    <h3>Temporal API</h3>
    <p>The upcoming native JavaScript date API — better than Date, similar concepts to moment. Currently a TC39 proposal with polyfill available. Best choice for new projects targeting modern environments.</p>
    <p style="margin-top:8px"><code>npm install @js-temporal/polyfill</code></p>
  </div>
</div>

<h2>Option A — Migrate to dayjs (recommended for existing codebases)</h2>

<h3>Step 1 — Install dayjs and remove moment</h3>
<pre>npm install dayjs
npm uninstall moment</pre>

<h3>Step 2 — Replace imports</h3>
{diff("moment.js", "import moment from 'moment';", "dayjs", "import dayjs from 'dayjs';")}

<h3>Step 3 — Basic usage — almost identical</h3>
{diff("moment.js",
"""// Parse
moment('2024-01-15')
moment('2024-01-15', 'YYYY-MM-DD')

// Format
moment().format('YYYY-MM-DD')
moment().format('MMMM Do YYYY')

// Manipulate
moment().add(7, 'days')
moment().subtract(1, 'month')

// Compare
moment('2024-01-15').isBefore('2024-06-01')
moment('2024-01-15').isAfter(moment())

// Display
moment().fromNow()
moment().toDate()""",
"dayjs",
"""// Parse
dayjs('2024-01-15')
dayjs('2024-01-15', 'YYYY-MM-DD')  // requires customParseFormat plugin

// Format
dayjs().format('YYYY-MM-DD')
dayjs().format('MMMM Do YYYY')     // requires advancedFormat plugin

// Manipulate
dayjs().add(7, 'day')
dayjs().subtract(1, 'month')

// Compare
dayjs('2024-01-15').isBefore('2024-06-01')
dayjs('2024-01-15').isAfter(dayjs())

// Display
dayjs().fromNow()                  // requires relativeTime plugin
dayjs().toDate()""")}

<h3>Step 4 — Enable plugins you need</h3>
<pre>import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import advancedFormat from 'dayjs/plugin/advancedFormat'
import customParseFormat from 'dayjs/plugin/customParseFormat'
import timezone from 'dayjs/plugin/timezone'
import utc from 'dayjs/plugin/utc'
import duration from 'dayjs/plugin/duration'

dayjs.extend(relativeTime)
dayjs.extend(advancedFormat)
dayjs.extend(customParseFormat)
dayjs.extend(utc)
dayjs.extend(timezone)</pre>

<h3>Step 5 — Timezone handling</h3>
{diff("moment-timezone",
"""import moment from 'moment-timezone'

moment.tz('2024-01-15 12:00', 'America/New_York')
moment().tz('Europe/London').format()""",
"dayjs timezone",
"""import dayjs from 'dayjs'
import utc from 'dayjs/plugin/utc'
import timezone from 'dayjs/plugin/timezone'
dayjs.extend(utc)
dayjs.extend(timezone)

dayjs.tz('2024-01-15 12:00', 'America/New_York')
dayjs().tz('Europe/London').format()""")}

<h3>Key differences to watch for</h3>
<ul style="padding-left:20px;margin:12px 0;color:var(--muted);font-size:12px;line-height:2">
  <li>dayjs objects are <strong>immutable</strong> — manipulations return new objects (moment mutates by default)</li>
  <li><code>add()</code> uses singular units: <code>'day'</code> not <code>'days'</code> (both work in dayjs but singular is canonical)</li>
  <li><code>moment.duration()</code> → requires <code>dayjs/plugin/duration</code></li>
  <li><code>moment.utc()</code> → requires <code>dayjs/plugin/utc</code></li>
  <li><code>fromNow()</code> → requires <code>dayjs/plugin/relativeTime</code></li>
</ul>

<h2>Option B — Migrate to date-fns (recommended for new code)</h2>

<p>date-fns uses a functional API — every operation is a standalone function. It's more verbose but also more explicit and tree-shakeable. Better for greenfield code than migration.</p>

{diff("moment.js",
"""import moment from 'moment'

// Format
moment().format('yyyy-MM-dd')

// Add days
moment().add(7, 'days').toDate()

// Check if before
moment('2024-01-15').isBefore('2024-06-01')

// From now
moment().fromNow()""",
"date-fns",
"""import { format, addDays, isBefore, formatDistanceToNow } from 'date-fns'

// Format
format(new Date(), 'yyyy-MM-dd')

// Add days
addDays(new Date(), 7)

// Check if before
isBefore(new Date('2024-01-15'), new Date('2024-06-01'))

// From now
formatDistanceToNow(new Date(), { addSuffix: true })""")}

<h2>Before migrating — check your CVE status</h2>
<p>If you're on moment.js 2.29.4, you have no unpatched CVEs. The migration is about future-proofing, not an emergency. Paste your package.json into PackageFix to confirm your current CVE exposure before starting the migration.</p>

{cta()}

{faq_html(moment_faqs)}

{related_html([
    {"url":"/fix/npm/moment","title":"moment.js CVE History","desc":"All 4 known CVEs"},
    {"url":"/npm","title":"npm Security Overview","desc":"All npm CVE guides"},
    {"url":"/glossary/remediation","title":"Remediation","desc":"Fix strategies"},
    {"url":"/fix/npm/semver","title":"Fix semver","desc":"Another ReDoS CVE"},
])}
"""


moment_schemas = [
    {"@type":"HowTo","name":"Migrate from moment.js to dayjs",
     "description":"Step-by-step guide to replace moment.js with dayjs or date-fns",
     "estimatedCost":{"@type":"MonetaryAmount","currency":"USD","value":"0"},
     "supply":{"@type":"HowToSupply","name":"package.json with moment.js"},
     "tool":{"@type":"HowToTool","name":"npm"},
     "step":[
         {"@type":"HowToStep","name":"Install dayjs","text":"Run: npm install dayjs && npm uninstall moment"},
         {"@type":"HowToStep","name":"Replace imports","text":"Change import moment from 'moment' to import dayjs from 'dayjs'"},
         {"@type":"HowToStep","name":"Enable plugins","text":"Add relativeTime, timezone, duration plugins as needed"},
         {"@type":"HowToStep","name":"Test","text":"Run your test suite — most moment.js code works with minimal changes"}
     ]},
    {"@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"PackageFix","item":BASE_URL},
        {"@type":"ListItem","position":2,"name":"Fix Guides","item":BASE_URL+"/fix"},
        {"@type":"ListItem","position":3,"name":"npm","item":BASE_URL+"/npm"},
        {"@type":"ListItem","position":4,"name":"moment.js","item":BASE_URL+"/fix/npm/moment"},
        {"@type":"ListItem","position":5,"name":"Migration Guide","item":BASE_URL+"/fix/npm/moment/migrate"}
    ]},
    {"@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}}
        for q,a in moment_faqs
    ]}
]

write("fix/npm/moment/migrate", shell(
    "Migrating from moment.js to dayjs or date-fns — Complete Guide | PackageFix",
    "moment.js is in maintenance mode. This guide covers migrating to dayjs (near drop-in replacement) or date-fns (modern functional API). Includes side-by-side code examples for every common operation.",
    "/fix/npm/moment/migrate",
    [("PackageFix","/"),("Fix Guides","/fix"),("npm","/npm"),("moment.js","/fix/npm/moment"),("Migration Guide",None)],
    moment_body, moment_schemas
))


# ══════════════════════════════════════════════════════════════════════════════
# 2. REQUEST DEPRECATION GUIDE
# ══════════════════════════════════════════════════════════════════════════════

print("\n🌐 Generating request deprecation guide...")

request_faqs = [
    ("Is request still safe to use?","request has been deprecated since February 2020 — no security patches, no updates. It has several unpatched vulnerabilities and will never receive fixes. Any new CVE discovered in request will not be patched. You should migrate."),
    ("Which request replacement is the easiest migration?","got has an API most similar to request and was explicitly designed as a modern replacement. axios is the most popular choice for new code. For Node.js 18+, the built-in fetch API works for simple use cases with no dependencies."),
    ("Does request support async/await?","request uses callbacks natively. There are wrapper packages (request-promise, request-promise-native) but these are also deprecated. Modern alternatives support async/await natively."),
    ("What about request-promise?","request-promise is also deprecated — it wraps request. Migrating from request-promise to got is straightforward since got returns promises natively."),
    ("Is axios safe to use in 2026?","axios 1.7.4 has no unpatched CVEs. It's actively maintained. It's the most widely used HTTP client for JavaScript and a solid choice for both Node.js and browser environments."),
    ("Should I use the native fetch API instead of a library?","For Node.js 18+, the built-in fetch API handles most HTTP use cases with zero dependencies. For complex needs (retries, interceptors, streaming), a library like got or axios is worth the dependency.")
]

request_body = f"""
<h1>Migrating away from request — Complete Guide</h1>
<p class="lead">The request npm package has been deprecated since February 2020 and receives no security patches. With 15M+ weekly downloads, it's still in millions of production applications. This guide covers migrating to axios, got, or native fetch.</p>

<div class="warning-box">
  <div class="label">⚠ request is deprecated</div>
  <p>request has been officially deprecated since February 11, 2020. No security patches, no bug fixes, no updates. Any CVE discovered in request will never be fixed. The maintainers explicitly recommend migration to alternatives.</p>
</div>

<h2>Choose your replacement</h2>
<div class="option-grid">
  <div class="option-card">
    <span class="tag">Most popular</span>
    <h3>axios</h3>
    <p>The most widely-used Node.js HTTP client. Works in both Node.js and the browser. Promise-based, supports interceptors, automatic JSON parsing, request/response transformation.</p>
    <p style="margin-top:8px"><code>npm install axios</code></p>
  </div>
  <div class="option-card">
    <span class="tag">Easiest migration from request</span>
    <h3>got</h3>
    <p>Designed as a modern replacement for request. Supports retries, pagination, HTTP/2, streams. ESM-only in v12+. Most request patterns translate directly.</p>
    <p style="margin-top:8px"><code>npm install got</code></p>
  </div>
  <div class="option-card">
    <span class="tag">No dependency (Node 18+)</span>
    <h3>Native fetch</h3>
    <p>Built into Node.js 18+. No install needed. Covers basic GET/POST use cases. Lacks retries, interceptors, and some convenience features of libraries.</p>
    <p style="margin-top:8px">Built-in — no install</p>
  </div>
  <div class="option-card">
    <span class="tag">Lightweight</span>
    <h3>node-fetch</h3>
    <p>Polyfills the browser fetch API for Node.js. Familiar if you use fetch in the browser. ESM-only in v3, CJS in v2. Simpler than axios or got.</p>
    <p style="margin-top:8px"><code>npm install node-fetch</code></p>
  </div>
</div>

<h2>Option A — Migrate to axios (recommended)</h2>

<h3>Install</h3>
<pre>npm install axios
npm uninstall request request-promise</pre>

<h3>GET requests</h3>
{diff("request",
"""const request = require('request')

// Callback style
request('https://api.example.com/data', (err, res, body) => {
  if (err) throw err
  const data = JSON.parse(body)
  console.log(data)
})

// With request-promise
const rp = require('request-promise')
const data = await rp.get({
  uri: 'https://api.example.com/data',
  json: true
})""",
"axios",
"""const axios = require('axios')
// or: import axios from 'axios'

// Promise style — automatic JSON parsing
const { data } = await axios.get('https://api.example.com/data')
console.log(data)

// With options
const { data } = await axios.get('https://api.example.com/data', {
  params: { page: 1 },
  headers: { Authorization: 'Bearer token' }
})""")}

<h3>POST requests</h3>
{diff("request",
"""request.post({
  url: 'https://api.example.com/users',
  json: true,
  body: { name: 'Alice', email: 'alice@example.com' }
}, (err, res, body) => {
  console.log(body)
})""",
"axios",
"""const { data } = await axios.post('https://api.example.com/users', {
  name: 'Alice',
  email: 'alice@example.com'
})
console.log(data)""")}

<h3>Error handling</h3>
{diff("request",
"""request('https://api.example.com', (err, res, body) => {
  if (err) {
    console.error('Network error:', err)
    return
  }
  if (res.statusCode !== 200) {
    console.error('HTTP error:', res.statusCode)
    return
  }
  console.log(JSON.parse(body))
})""",
"axios",
"""try {
  const { data } = await axios.get('https://api.example.com')
  console.log(data)
} catch (err) {
  if (err.response) {
    // HTTP error (4xx, 5xx)
    console.error('HTTP error:', err.response.status)
  } else {
    // Network error
    console.error('Network error:', err.message)
  }
}""")}

<h3>Custom headers and auth</h3>
{diff("request",
"""request({
  url: 'https://api.example.com/data',
  headers: {
    'Authorization': 'Bearer mytoken',
    'X-Custom-Header': 'value'
  },
  auth: { user: 'username', pass: 'password' }
}, callback)""",
"axios",
"""// Per-request headers
await axios.get('https://api.example.com/data', {
  headers: {
    'Authorization': 'Bearer mytoken',
    'X-Custom-Header': 'value'
  },
  auth: { username: 'username', password: 'password' }
})

// Global defaults (set once)
axios.defaults.headers.common['Authorization'] = 'Bearer mytoken'""")}

<h2>Option B — Migrate to got</h2>

<p>got is ESM-only from v12. If you're on CommonJS (<code>require()</code>), use got v11 or switch to axios.</p>

<pre># got v11 (CommonJS compatible)
npm install got@11

# got v12+ (ESM only)
npm install got</pre>

{diff("request",
"""const request = require('request')

request.get({
  url: 'https://api.example.com/data',
  json: true
}, (err, res, body) => {
  console.log(body)
})""",
"got v11",
"""const got = require('got')

const body = await got('https://api.example.com/data').json()
console.log(body)

// With options
const body = await got('https://api.example.com/data', {
  searchParams: { page: 1 },
  headers: { Authorization: 'Bearer token' }
}).json()""")}

<h2>Option C — Native fetch (Node.js 18+)</h2>

<p>No install required. Best for simple requests where you don't need retries or interceptors.</p>

{diff("request",
"""request('https://api.example.com/data', (err, res, body) => {
  const data = JSON.parse(body)
  console.log(data)
})""",
"native fetch",
"""// Built into Node.js 18+
const res = await fetch('https://api.example.com/data')
if (!res.ok) throw new Error(`HTTP error: ${res.status}`)
const data = await res.json()
console.log(data)

// POST
const res = await fetch('https://api.example.com/users', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ name: 'Alice' })
})
const data = await res.json()""")}

<h2>Check your current CVE exposure first</h2>
<p>Before migrating, paste your package.json into PackageFix to see which request-related CVEs you're currently exposed to. This gives you a clear picture of urgency.</p>

{cta()}

{faq_html(request_faqs)}

{related_html([
    {"url":"/fix/npm/axios","title":"axios CVE History","desc":"All axios vulnerabilities"},
    {"url":"/fix/npm/node-fetch","title":"node-fetch CVE History","desc":"node-fetch vulnerabilities"},
    {"url":"/fix/npm/moment/migrate","title":"moment.js Migration","desc":"Another deprecated package"},
    {"url":"/npm","title":"npm Security Overview","desc":"All npm CVE guides"},
])}
"""

request_schemas = [
    {"@type":"HowTo","name":"Migrate from request npm package to axios or got",
     "description":"Step-by-step guide to replace the deprecated request package with axios, got, or native fetch",
     "estimatedCost":{"@type":"MonetaryAmount","currency":"USD","value":"0"},
     "supply":{"@type":"HowToSupply","name":"package.json using request or request-promise"},
     "tool":{"@type":"HowToTool","name":"npm"},
     "step":[
         {"@type":"HowToStep","name":"Choose replacement","text":"axios for most projects, got for request-like API, native fetch for Node.js 18+ simple use cases"},
         {"@type":"HowToStep","name":"Install","text":"npm install axios && npm uninstall request request-promise"},
         {"@type":"HowToStep","name":"Replace callbacks with async/await","text":"axios and got are promise-based — replace request callbacks with async/await"},
         {"@type":"HowToStep","name":"Update error handling","text":"axios throws on non-2xx responses, request does not — update error handling logic"}
     ]},
    {"@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"PackageFix","item":BASE_URL},
        {"@type":"ListItem","position":2,"name":"Fix Guides","item":BASE_URL+"/fix"},
        {"@type":"ListItem","position":3,"name":"npm","item":BASE_URL+"/npm"},
        {"@type":"ListItem","position":4,"name":"request","item":BASE_URL+"/fix/npm/request"},
        {"@type":"ListItem","position":5,"name":"Migration Guide","item":BASE_URL+"/fix/npm/request/migrate"}
    ]},
    {"@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}}
        for q,a in request_faqs
    ]}
]

write("fix/npm/request/migrate", shell(
    "Migrating from request (deprecated) to axios, got, or fetch — Complete Guide | PackageFix",
    "request has been deprecated since 2020 with no security patches. This guide covers migrating to axios, got, or native fetch — with side-by-side code examples for GET, POST, error handling, and auth.",
    "/fix/npm/request/migrate",
    [("PackageFix","/"),("Fix Guides","/fix"),("npm","/npm"),("request","/fix/npm/request"),("Migration Guide",None)],
    request_body, request_schemas
))


# ══════════════════════════════════════════════════════════════════════════════
# UPDATE CONFIG FILES
# ══════════════════════════════════════════════════════════════════════════════

print("\n📝 Updating vercel.json...")
rewrites = [{"source":p,"destination":f"/seo{p}/index.html"} for p in all_paths] + \
           [{"source":p+"/","destination":f"/seo{p}/index.html"} for p in all_paths]

vercel_config = {}
if os.path.exists("vercel.json"):
    with open("vercel.json") as f:
        vercel_config = json.load(f)

existing = vercel_config.get("rewrites",[])
existing_sources = {r["source"] for r in existing}
added = 0
for r in rewrites:
    if r["source"] not in existing_sources:
        existing.append(r)
        existing_sources.add(r["source"])
        added += 1

vercel_config["rewrites"] = existing
with open("vercel.json","w") as f:
    json.dump(vercel_config, f, indent=2)
print(f"  ✓ vercel.json — {len(existing)} total rewrites ({added} new)")

print("\n🗺 Updating sitemap-seo.xml...")
new_urls = "".join(
    f"  <url>\n    <loc>{BASE_URL}{p}</loc>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n"
    for p in all_paths)
if os.path.exists("sitemap-seo.xml"):
    with open("sitemap-seo.xml") as f:
        content = f.read()
    updated = content.replace("</urlset>", new_urls + "</urlset>")
else:
    updated = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + new_urls + "</urlset>"
with open("sitemap-seo.xml","w") as f:
    f.write(updated)
print(f"  ✓ sitemap-seo.xml — {len(all_paths)} new URLs")

print("\n🤖 Updating llm.txt...")
with open("llm.txt","a") as f:
    f.write("\n## Migration Guides\n")
    for p in all_paths:
        f.write(f"{BASE_URL}{p}\n")
print("  ✓ llm.txt updated")

print(f"\n✅ Done — {len(all_paths)} migration guides generated")
for p in all_paths:
    print(f"   {p}")

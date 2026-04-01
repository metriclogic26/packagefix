#!/usr/bin/env python3
"""
Critical updates:
1. multer - 1.4.5-lts.1 is NOW VULNERABLE (CVE-2025-47944). Safe: 2.1.1
2. Rails - update to March 2026 security releases (7.2.3.1, 8.0.4.1, 8.1.2.1)
"""
import os, re

# =========================================================================
# 1. MULTER - CRITICAL UPDATE
# CVE-2025-47944 affects >=1.4.4-lts.1 <2.0.0
# Safe version: multer@2.1.1
# =========================================================================
print("Updating multer page - CRITICAL...")

multer_path = "seo/fix/npm/multer/index.html"
if os.path.exists(multer_path):
    with open(multer_path) as f:
        content = f.read()

    # 1. Update title
    content = content.replace(
        'multer 1.4.5-lts.1 \u2014 Fix CVE-2022-24434 | PackageFix',
        'Fix multer CVE-2025-47944 \u2014 Upgrade to 2.1.1 (1.4.5-lts.1 is Vulnerable) | PackageFix'
    )

    # 2. Update meta description
    content = content.replace(
        'multer 1.4.5-lts.1 fixes CVE-2022-24434 (HIGH) \u2014 denial of service via crafted multipart request. Paste your package.json, get a fixed version instantly. No CLI, no signup.',
        'multer 1.4.5-lts.1 is now vulnerable to CVE-2025-47944 (HIGH). Safe version: multer@2.1.1. Upgrade guide from 1.x to 2.x with breaking changes and migration steps.'
    )

    # 3. Update og:description
    content = re.sub(
        r'<meta property="og:description" content="multer 1\.4\.5-lts\.1 fixes[^"]*">',
        '<meta property="og:description" content="multer 1.4.5-lts.1 is now vulnerable to CVE-2025-47944 (HIGH). Safe version: multer@2.1.1. Upgrade guide from 1.x to 2.x.">',
        content
    )

    # 4. Update h1
    content = content.replace(
        'multer 1.4.5-lts.1 \u2014 Fix CVE-2022-24434 <span class="badge badge-orange">HIGH</span>',
        'Fix multer \u2014 CVE-2025-47944 <span class="badge badge-red">HIGH</span> <span class="badge badge-orange" style="font-size:9px;margin-left:4px">1.4.5-lts.1 VULNERABLE</span>'
    )

    # 5. Replace the version table with updated one showing 1.4.5-lts.1 as VULNERABLE
    OLD_TABLE_START = '<div id="version-status-table">'
    OLD_TABLE_END = '</div><h1>'

    NEW_TABLE = '''<div id="version-status-table">
<div style="background:rgba(239,68,68,.15);border:2px solid #EF4444;border-radius:10px;padding:20px 24px;margin:0 0 24px">
<div style="font-size:11px;font-weight:700;color:#EF4444;text-transform:uppercase;letter-spacing:.1em;margin-bottom:10px">&#x26A0; Critical Update &mdash; April 2026</div>
<p style="color:var(--text);margin:0;font-size:13px;line-height:1.7"><strong>multer 1.4.5-lts.1 is now vulnerable.</strong> CVE-2025-47944 (HIGH, CVSS 7.5) affects all multer versions &gt;=1.4.4-lts.1 and &lt;2.0.0. The only fix is upgrading to <strong>multer@2.1.1</strong>. No workarounds exist.</p>
</div>

<h2>multer Version Security Status</h2>
<p style="color:var(--muted);font-size:12px;margin-bottom:12px">Last updated April 1, 2026. Check your version: <code>npm list multer</code></p>
<table style="width:100%;border-collapse:collapse;font-size:12px">
<thead>
<tr style="border-bottom:2px solid var(--border)">
<th style="text-align:left;padding:10px 12px;color:var(--muted);font-size:10px;text-transform:uppercase;letter-spacing:.08em">Version</th>
<th style="text-align:left;padding:10px 12px;color:var(--muted);font-size:10px;text-transform:uppercase;letter-spacing:.08em">Status</th>
<th style="text-align:left;padding:10px 12px;color:var(--muted);font-size:10px;text-transform:uppercase;letter-spacing:.08em">CVEs</th>
<th style="text-align:left;padding:10px 12px;color:var(--muted);font-size:10px;text-transform:uppercase;letter-spacing:.08em">Notes</th>
</tr>
</thead>
<tbody>
<tr style="border-bottom:1px solid var(--border);background:rgba(34,197,94,.05)">
<td style="padding:10px 12px;font-weight:700;color:var(--text)">2.1.1+</td>
<td style="padding:10px 12px"><span style="background:rgba(34,197,94,.2);color:#22C55E;border:1px solid #22C55E;font-size:10px;font-weight:700;padding:2px 8px;border-radius:4px;text-transform:uppercase">SAFE</span></td>
<td style="padding:10px 12px;color:var(--muted)">None</td>
<td style="padding:10px 12px;color:var(--muted)">Current safe version. Requires Node.js 10.16+. Has breaking changes from 1.x.</td>
</tr>
<tr style="border-bottom:1px solid var(--border)">
<td style="padding:10px 12px;font-weight:700;color:var(--text)">1.4.5-lts.1</td>
<td style="padding:10px 12px"><span style="background:rgba(239,68,68,.2);color:#EF4444;border:1px solid #EF4444;font-size:10px;font-weight:700;padding:2px 8px;border-radius:4px;text-transform:uppercase">VULNERABLE</span></td>
<td style="padding:10px 12px;color:var(--muted)">CVE-2025-47944, CVE-2022-24434</td>
<td style="padding:10px 12px;color:var(--muted)">Previously recommended as safe for CVE-2022-24434 &mdash; now itself vulnerable. Upgrade to 2.1.1.</td>
</tr>
<tr style="border-bottom:1px solid var(--border)">
<td style="padding:10px 12px;font-weight:700;color:var(--text)">1.4.4 and below</td>
<td style="padding:10px 12px"><span style="background:rgba(239,68,68,.2);color:#EF4444;border:1px solid #EF4444;font-size:10px;font-weight:700;padding:2px 8px;border-radius:4px;text-transform:uppercase">VULNERABLE</span></td>
<td style="padding:10px 12px;color:var(--muted)">CVE-2022-24434 + more</td>
<td style="padding:10px 12px;color:var(--muted)">Multiple CVEs. Upgrade to 2.1.1 immediately.</td>
</tr>
</tbody>
</table>

<h2>How to upgrade: 1.x &rarr; 2.x</h2>
<div style="background:rgba(34,197,94,.08);border:1px solid rgba(34,197,94,.3);border-left:3px solid #22C55E;border-radius:8px;padding:16px 20px;margin:12px 0">
<div style="font-size:10px;font-weight:700;color:#22C55E;text-transform:uppercase;letter-spacing:.1em;margin-bottom:8px">Fix</div>
<pre style="margin:0;background:transparent;border:none;padding:0">npm install multer@2.1.1</pre>
</div>

<div style="background:rgba(249,115,22,.08);border:1px solid rgba(249,115,22,.3);border-left:3px solid #F97316;border-radius:8px;padding:16px 20px;margin:12px 0">
<div style="font-size:10px;font-weight:700;color:#F97316;text-transform:uppercase;letter-spacing:.1em;margin-bottom:8px">Breaking changes in multer 2.x</div>
<ul style="margin:0;padding-left:18px;color:var(--muted);font-size:12px;line-height:2">
<li>Requires Node.js 10.16.0 or later</li>
<li><code>fileFilter</code> callback signature changed &mdash; check the multer 2.x docs</li>
<li>Some multer plugins (multer-gridfs-storage, multer-s3) may need updates to support 2.x &mdash; check their GitHub for 2.x compatibility</li>
<li>Error handling changed &mdash; test your upload error paths</li>
</ul>
</div>
</div>'''

    if OLD_TABLE_START in content and OLD_TABLE_END in content:
        start_idx = content.index(OLD_TABLE_START)
        end_idx = content.index(OLD_TABLE_END) + len(OLD_TABLE_END)
        content = content[:start_idx] + NEW_TABLE + '\n</div><h1>' + content[end_idx:]
        print("  OK - multer version table replaced with updated version")
    else:
        # Just prepend the warning banner before h1
        warning = '<div style="background:rgba(239,68,68,.15);border:2px solid #EF4444;border-radius:10px;padding:20px 24px;margin:0 0 24px"><div style="font-size:11px;font-weight:700;color:#EF4444;text-transform:uppercase;letter-spacing:.1em;margin-bottom:10px">&#x26A0; Critical Update</div><p style="color:var(--text);margin:0;font-size:13px">multer 1.4.5-lts.1 is now vulnerable (CVE-2025-47944). Upgrade to multer@2.1.1.</p></div>'
        content = content.replace('<h1>', warning + '<h1>', 1)
        print("  OK - multer warning banner added (table not found)")

    with open(multer_path, 'w') as f:
        f.write(content)
    print("  multer page updated")
else:
    print("  multer page not found")


# =========================================================================
# 2. RAILS - UPDATE TO MARCH 2026 RELEASES
# New: 7.2.3.1, 8.0.4.1, 8.1.2.1 (March 23, 2026) - 10 CVEs
# Rails 7.0 and 7.1 are EOL
# =========================================================================
print("\nUpdating Rails page...")

rails_path = "seo/fix/ruby/rails/index.html"
if os.path.exists(rails_path):
    with open(rails_path) as f:
        content = f.read()

    # Update the freshness box with new versions
    OLD_FRESHNESS = 'Rails 7.2 &rarr; <strong>7.2.2.1</strong> &nbsp;&middot;&nbsp; Rails 7.1 LTS &rarr; <strong>7.1.5.1</strong> &nbsp;&middot;&nbsp; Rails 7.0 &rarr; <strong>7.0.8.5</strong>'
    NEW_FRESHNESS = 'Rails 8.1 &rarr; <strong>8.1.2.1</strong> &nbsp;&middot;&nbsp; Rails 8.0 &rarr; <strong>8.0.4.1</strong> &nbsp;&middot;&nbsp; Rails 7.2 &rarr; <strong>7.2.3.1</strong> &nbsp;&middot;&nbsp; <span style="color:var(--red)">Rails 7.1 &amp; 7.0: EOL &mdash; no more patches</span>'

    if OLD_FRESHNESS in content:
        content = content.replace(OLD_FRESHNESS, NEW_FRESHNESS)
        print("  OK - Rails freshness box updated to March 2026 versions")

    # Update the date stamp
    content = content.replace(
        'as of March 31, 2026',
        'as of April 1, 2026'
    )

    # Add March 2026 security release section if not already there
    MARCH_2026_SECTION = '''
<h2>March 2026 Security Release &mdash; 10 CVEs</h2>
<p>On March 23, 2026, Rails released security patches across all supported versions (7.2.3.1, 8.0.4.1, 8.1.2.1) addressing 10 security issues including path traversal in Active Storage, XSS in Action Pack debug exceptions, and DoS via Active Storage proxy mode. Rails 7.0 and 7.1 received no patches &mdash; they are end of life.</p>
<table style="width:100%;border-collapse:collapse;font-size:12px;margin:16px 0">
<thead><tr style="border-bottom:2px solid var(--border)">
<th style="text-align:left;padding:8px 12px;color:var(--muted);font-size:10px;text-transform:uppercase">CVE</th>
<th style="text-align:left;padding:8px 12px;color:var(--muted);font-size:10px;text-transform:uppercase">Component</th>
<th style="text-align:left;padding:8px 12px;color:var(--muted);font-size:10px;text-transform:uppercase">Description</th>
</tr></thead>
<tbody>
<tr style="border-bottom:1px solid var(--border)"><td style="padding:8px 12px;color:var(--purple)">CVE-2026-33195</td><td style="padding:8px 12px;color:var(--muted)">Active Storage</td><td style="padding:8px 12px;color:var(--muted)">Path traversal in DiskService</td></tr>
<tr style="border-bottom:1px solid var(--border)"><td style="padding:8px 12px;color:var(--purple)">CVE-2026-33167</td><td style="padding:8px 12px;color:var(--muted)">Action Pack</td><td style="padding:8px 12px;color:var(--muted)">XSS in debug exceptions (dev mode)</td></tr>
<tr style="border-bottom:1px solid var(--border)"><td style="padding:8px 12px;color:var(--purple)">CVE-2026-33168</td><td style="padding:8px 12px;color:var(--muted)">Action View</td><td style="padding:8px 12px;color:var(--muted)">XSS in tag helpers</td></tr>
<tr style="border-bottom:1px solid var(--border)"><td style="padding:8px 12px;color:var(--purple)">CVE-2026-33174</td><td style="padding:8px 12px;color:var(--muted)">Active Storage</td><td style="padding:8px 12px;color:var(--muted)">DoS via Range requests in proxy mode</td></tr>
<tr style="border-bottom:1px solid var(--border)"><td style="padding:8px 12px;color:var(--purple)">CVE-2026-33202</td><td style="padding:8px 12px;color:var(--muted)">Active Storage</td><td style="padding:8px 12px;color:var(--muted)">Glob injection in DiskService</td></tr>
<tr style="border-bottom:1px solid var(--border)"><td style="padding:8px 12px;color:var(--purple)">CVE-2026-33169</td><td style="padding:8px 12px;color:var(--muted)">Active Support</td><td style="padding:8px 12px;color:var(--muted)">ReDoS in number_to_delimited</td></tr>
<tr><td style="padding:8px 12px;color:var(--purple)">+4 more</td><td style="padding:8px 12px;color:var(--muted)">Various</td><td style="padding:8px 12px;color:var(--muted)">XSS, DoS, metadata filtering</td></tr>
</tbody>
</table>
<div style="background:rgba(34,197,94,.08);border:1px solid rgba(34,197,94,.3);border-left:3px solid #22C55E;border-radius:8px;padding:14px 18px;margin:12px 0">
<pre style="margin:0;background:transparent;border:none;padding:0"># Update to March 2026 security release
bundle update rails

# Target specific version
gem 'rails', '~> 8.1.2'  # Rails 8.1
gem 'rails', '~> 8.0.4'  # Rails 8.0
gem 'rails', '~> 7.2.3'  # Rails 7.2 (last supported minor)</pre>
</div>

<div style="background:rgba(239,68,68,.08);border:1px solid rgba(239,68,68,.3);border-left:3px solid #EF4444;border-radius:8px;padding:14px 18px;margin:12px 0">
<div style="font-size:10px;font-weight:700;color:#EF4444;text-transform:uppercase;letter-spacing:.1em;margin-bottom:6px">Rails 7.0 and 7.1 are End of Life</div>
<p style="margin:0;font-size:12px;color:var(--muted)">Rails 7.0 reached EOL April 2025. Rails 7.1 reached EOL October 2025. Neither received patches for the March 2026 CVEs. If you are on 7.0 or 7.1, upgrade to 7.2 or 8.x immediately &mdash; your application has unpatched path traversal and XSS vulnerabilities.</p>
</div>
'''

    if 'March 2026 Security Release' not in content:
        # Insert before the first h2
        content = content.replace('<h2>', MARCH_2026_SECTION + '<h2>', 1)
        print("  OK - March 2026 section added to Rails page")

    with open(rails_path, 'w') as f:
        f.write(content)
    print("  Rails page updated")
else:
    print("  Rails page not found")


# =========================================================================
# 3. UPDATE /fix/ruby/rails/cve-2024 title to mention 2026
# =========================================================================
print("\nUpdating rails/cve-2024 page title...")

rails_2024_path = "seo/fix/ruby/rails/cve-2024/index.html"
if os.path.exists(rails_2024_path):
    with open(rails_2024_path) as f:
        content = f.read()

    content = content.replace(
        'Ruby on Rails CVEs 2024 \u2014 All Security Releases | PackageFix',
        'Ruby on Rails CVEs 2024\u20132026 \u2014 All Security Releases | PackageFix'
    )
    content = content.replace(
        '<h1>Ruby on Rails CVEs 2024 \u2014 All Security Releases</h1>',
        '<h1>Ruby on Rails CVEs 2024\u20132026 \u2014 All Security Releases</h1>'
    )

    with open(rails_2024_path, 'w') as f:
        f.write(content)
    print("  OK - cve-2024 title updated to 2024-2026")
else:
    print("  cve-2024 page not found")

print("\nAll critical updates done.")
print("Pages updated:")
print("  seo/fix/npm/multer/index.html")
print("  seo/fix/ruby/rails/index.html")
print("  seo/fix/ruby/rails/cve-2024/index.html")

#!/usr/bin/env python3
"""
Quick wins based on GSC data:
1. multer version history table
2. JWT transitive dependency box
3. Snyk meta description update
"""
import os, json, re

# =========================================================================
# 1. MULTER VERSION HISTORY TABLE
# =========================================================================
print("Adding multer version history table...")

MULTER_VERSION_TABLE = """
<div style="margin:0 0 32px">
<h2>multer Version Security Status</h2>
<p style="color:var(--muted);font-size:12px;margin-bottom:12px">Last updated March 31, 2026. Check your version: <code>npm list multer</code></p>
<table style="width:100%;border-collapse:collapse;font-size:12px">
<thead>
<tr style="border-bottom:2px solid var(--border)">
<th style="text-align:left;padding:10px 12px;color:var(--muted);font-size:10px;text-transform:uppercase;letter-spacing:.08em">Version</th>
<th style="text-align:left;padding:10px 12px;color:var(--muted);font-size:10px;text-transform:uppercase;letter-spacing:.08em">Status</th>
<th style="text-align:left;padding:10px 12px;color:var(--muted);font-size:10px;text-transform:uppercase;letter-spacing:.08em">CVE</th>
<th style="text-align:left;padding:10px 12px;color:var(--muted);font-size:10px;text-transform:uppercase;letter-spacing:.08em">Notes</th>
</tr>
</thead>
<tbody>
<tr style="border-bottom:1px solid var(--border);background:rgba(34,197,94,.05)">
<td style="padding:10px 12px;font-weight:700;color:var(--text)">1.4.5-lts.1</td>
<td style="padding:10px 12px"><span style="background:rgba(34,197,94,.2);color:#22C55E;border:1px solid #22C55E;font-size:10px;font-weight:700;padding:2px 8px;border-radius:4px;text-transform:uppercase">SAFE</span></td>
<td style="padding:10px 12px;color:var(--muted)">None</td>
<td style="padding:10px 12px;color:var(--muted)">Current safe version. Update to this.</td>
</tr>
<tr style="border-bottom:1px solid var(--border)">
<td style="padding:10px 12px;font-weight:700;color:var(--text)">1.4.4</td>
<td style="padding:10px 12px"><span style="background:rgba(239,68,68,.2);color:#EF4444;border:1px solid #EF4444;font-size:10px;font-weight:700;padding:2px 8px;border-radius:4px;text-transform:uppercase">VULNERABLE</span></td>
<td style="padding:10px 12px"><a href="https://osv.dev/vulnerability/CVE-2022-24434" target="_blank" rel="noopener" style="color:var(--purple)">CVE-2022-24434</a></td>
<td style="padding:10px 12px;color:var(--muted)">DoS via crafted multipart request. Do not use.</td>
</tr>
<tr style="border-bottom:1px solid var(--border)">
<td style="padding:10px 12px;font-weight:700;color:var(--text)">1.4.3</td>
<td style="padding:10px 12px"><span style="background:rgba(239,68,68,.2);color:#EF4444;border:1px solid #EF4444;font-size:10px;font-weight:700;padding:2px 8px;border-radius:4px;text-transform:uppercase">VULNERABLE</span></td>
<td style="padding:10px 12px"><a href="https://osv.dev/vulnerability/CVE-2022-24434" target="_blank" rel="noopener" style="color:var(--purple)">CVE-2022-24434</a></td>
<td style="padding:10px 12px;color:var(--muted)">Affected. Update to 1.4.5-lts.1.</td>
</tr>
<tr style="border-bottom:1px solid var(--border)">
<td style="padding:10px 12px;font-weight:700;color:var(--text)">1.4.2</td>
<td style="padding:10px 12px"><span style="background:rgba(239,68,68,.2);color:#EF4444;border:1px solid #EF4444;font-size:10px;font-weight:700;padding:2px 8px;border-radius:4px;text-transform:uppercase">VULNERABLE</span></td>
<td style="padding:10px 12px"><a href="https://osv.dev/vulnerability/CVE-2022-24434" target="_blank" rel="noopener" style="color:var(--purple)">CVE-2022-24434</a></td>
<td style="padding:10px 12px;color:var(--muted)">Affected. Update to 1.4.5-lts.1.</td>
</tr>
<tr style="border-bottom:1px solid var(--border)">
<td style="padding:10px 12px;font-weight:700;color:var(--text)">1.4.1</td>
<td style="padding:10px 12px"><span style="background:rgba(239,68,68,.2);color:#EF4444;border:1px solid #EF4444;font-size:10px;font-weight:700;padding:2px 8px;border-radius:4px;text-transform:uppercase">VULNERABLE</span></td>
<td style="padding:10px 12px"><a href="https://osv.dev/vulnerability/CVE-2022-24434" target="_blank" rel="noopener" style="color:var(--purple)">CVE-2022-24434</a></td>
<td style="padding:10px 12px;color:var(--muted)">Affected. Update to 1.4.5-lts.1.</td>
</tr>
<tr>
<td style="padding:10px 12px;font-weight:700;color:var(--text)">1.4.0 and below</td>
<td style="padding:10px 12px"><span style="background:rgba(239,68,68,.2);color:#EF4444;border:1px solid #EF4444;font-size:10px;font-weight:700;padding:2px 8px;border-radius:4px;text-transform:uppercase">VULNERABLE</span></td>
<td style="padding:10px 12px"><a href="https://osv.dev/vulnerability/CVE-2022-24434" target="_blank" rel="noopener" style="color:var(--purple)">CVE-2022-24434</a></td>
<td style="padding:10px 12px;color:var(--muted)">All versions below 1.4.5-lts.1 are affected.</td>
</tr>
</tbody>
</table>
<div style="margin-top:12px;background:rgba(34,197,94,.08);border:1px solid rgba(34,197,94,.3);border-left:3px solid #22C55E;border-radius:8px;padding:12px 16px">
<p style="margin:0;font-size:12px;color:var(--text)"><strong>Fix:</strong> <code>npm install multer@1.4.5-lts.1</code> &mdash; Note: npm update will NOT auto-upgrade to this version because the -lts.1 suffix makes it a pre-release. You must update manually.</p>
</div>
</div>
"""

multer_path = "seo/fix/npm/multer/index.html"
if os.path.exists(multer_path):
    with open(multer_path) as f:
        content = f.read()

    # Insert table before the h1
    if 'version-status-table' not in content:
        content = content.replace(
            '<h1>',
            '<div id="version-status-table">' + MULTER_VERSION_TABLE + '</div><h1>',
            1
        )
        with open(multer_path, 'w') as f:
            f.write(content)
        print("  OK - multer version table added")
    else:
        print("  Already has version table")
else:
    print("  multer page not found")


# =========================================================================
# 2. JWT TRANSITIVE DEPENDENCY BOX
# =========================================================================
print("\nAdding JWT transitive dependency box...")

JWT_BOX = """<div style="background:rgba(108,99,255,.08);border:1px solid rgba(108,99,255,.3);border-left:3px solid #6C63FF;border-radius:8px;padding:16px 20px;margin:24px 0">
<div style="font-size:10px;font-weight:700;color:#6C63FF;text-transform:uppercase;letter-spacing:.1em;margin-bottom:8px">Did you know?</div>
<p style="margin:0 0 8px;font-size:12px;color:var(--text)"><strong>ruby-jwt is often a transitive dependency.</strong> You may have it without knowing.</p>
<p style="margin:0;font-size:12px;color:var(--muted)">Auth0, Devise-JWT, and several API authentication gems pull in ruby-jwt automatically. If you use any of these, a vulnerable ruby-jwt version may be in your lockfile even if it is not in your Gemfile directly. This is called a <a href="/glossary/transitive-dependency" style="color:#6C63FF">transitive dependency</a>.</p>
<pre style="margin:12px 0 0;background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:10px 12px;font-size:11px"># Check if ruby-jwt is pulled in transitively
bundle list | grep jwt

# If it appears, check the version
bundle exec gem list jwt</pre>
</div>"""

jwt_path = "seo/fix/ruby/jwt/index.html"
if os.path.exists(jwt_path):
    with open(jwt_path) as f:
        content = f.read()

    if 'transitive-dependency' not in content or 'Did you know' not in content:
        # Insert after the h1
        content = content.replace('</h1>', '</h1>' + JWT_BOX, 1)
        with open(jwt_path, 'w') as f:
            f.write(content)
        print("  OK - JWT transitive box added")
    else:
        print("  Already has transitive box")
else:
    print("  JWT page not found")


# =========================================================================
# 3. SNYK META DESCRIPTION UPDATE
# =========================================================================
print("\nUpdating snyk-vs-dependabot meta description...")

snyk_path = "seo/compare/snyk-vs-dependabot/index.html"
if os.path.exists(snyk_path):
    with open(snyk_path) as f:
        content = f.read()

    old_meta = 'Snyk vs Dependabot (2026): both require GitHub access and neither downloads a fixed manifest. PackageFix is the browser alternative \u2014 no account, no GitHub, fixed file in one click.'
    new_meta = 'Snyk vs Dependabot in 2026: neither caught the axios supply chain attack or the multer transitive vulnerability without GitHub access. PackageFix is the browser alternative that needs no account and downloads the fixed manifest.'

    if old_meta in content:
        content = content.replace(old_meta, new_meta)
        with open(snyk_path, 'w') as f:
            f.write(content)
        print("  OK - snyk meta description updated")
    else:
        # Try updating whatever meta description is there
        content = re.sub(
            r'<meta name="description" content="[^"]*Snyk vs Dependabot[^"]*">',
            '<meta name="description" content="' + new_meta + '">',
            content
        )
        # Also update og:description
        content = re.sub(
            r'<meta property="og:description" content="[^"]*Snyk vs Dependabot[^"]*">',
            '<meta property="og:description" content="' + new_meta + '">',
            content
        )
        with open(snyk_path, 'w') as f:
            f.write(content)
        print("  OK - snyk meta updated via regex")
else:
    print("  snyk page not found")


# =========================================================================
# 4. BONUS: Add "Current safe version" timestamp to rails page
# =========================================================================
print("\nAdding freshness timestamp to rails page...")

rails_path = "seo/fix/ruby/rails/index.html"
if os.path.exists(rails_path):
    with open(rails_path) as f:
        content = f.read()

    freshness_box = (
        '<div style="background:rgba(34,197,94,.08);border:1px solid rgba(34,197,94,.3);'
        'border-radius:8px;padding:14px 18px;margin:0 0 24px;display:flex;'
        'align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px">'
        '<div>'
        '<div style="font-size:10px;font-weight:700;color:#22C55E;text-transform:uppercase;'
        'letter-spacing:.1em;margin-bottom:4px">Current Safe Versions (as of March 31, 2026)</div>'
        '<p style="margin:0;font-size:12px;color:var(--text)">'
        'Rails 7.2 &rarr; <strong>7.2.2.1</strong> &nbsp;&middot;&nbsp; '
        'Rails 7.1 LTS &rarr; <strong>7.1.5.1</strong> &nbsp;&middot;&nbsp; '
        'Rails 7.0 &rarr; <strong>7.0.8.5</strong>'
        '</p>'
        '</div>'
        '<a href="/blog/ruby-on-rails-security-releases-2024" '
        'style="color:#6C63FF;font-size:11px;white-space:nowrap">'
        'Full 2024 release history &rarr;</a>'
        '</div>'
    )

    if 'Current Safe Versions' not in content:
        content = content.replace('<h1>', freshness_box + '<h1>', 1)
        with open(rails_path, 'w') as f:
            f.write(content)
        print("  OK - rails freshness box added")
    else:
        print("  Already has freshness box")
else:
    print("  Rails page not found")

print("\nAll updates done.")

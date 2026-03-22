#!/usr/bin/env python3
"""
PackageFix — Programmatic SEO Page Generator — Phase 3
PHP + Go + Rust + Java package pages + comparison pairs = ~80 pages
Run: python3 generate_seo_phase3.py
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
h1{font-size:clamp(18px,3vw,26px);font-weight:700;margin-bottom:12px;line-height:1.3}
h2{font-size:14px;font-weight:600;margin:32px 0 12px}
p{color:var(--muted);margin-bottom:12px;font-size:12px;line-height:1.7}
.lead{color:var(--text);font-size:13px;margin-bottom:24px;line-height:1.7}
.problem-box{background:rgba(239,68,68,.08);border:1px solid rgba(239,68,68,.3);border-left:3px solid var(--red);border-radius:8px;padding:16px 20px;margin:20px 0}
.problem-box .label{font-size:10px;font-weight:700;color:var(--red);text-transform:uppercase;letter-spacing:.1em;margin-bottom:8px}
.fix-box{background:rgba(34,197,94,.08);border:1px solid rgba(34,197,94,.3);border-left:3px solid var(--green);border-radius:8px;padding:16px 20px;margin:20px 0}
.fix-box .label{font-size:10px;font-weight:700;color:var(--green);text-transform:uppercase;letter-spacing:.1em;margin-bottom:8px}
.kev-box{background:rgba(239,68,68,.12);border:1px solid var(--red);border-radius:8px;padding:12px 16px;margin:16px 0;font-size:11px;color:var(--red)}
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
.faq{margin:40px 0}
.faq-item{border-bottom:1px solid var(--border);padding:16px 0}
.faq-item:last-child{border-bottom:none}
.faq-q{font-size:12px;font-weight:600;color:var(--text);margin-bottom:8px}
.faq-a{font-size:12px;color:var(--muted);line-height:1.7}
.related-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px;margin-top:12px}
.related-card{background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:14px}
.related-card a{color:var(--text);font-size:12px;font-weight:500}
.related-card p{font-size:11px;color:var(--muted);margin:4px 0 0}
.cve-table{width:100%;border-collapse:collapse;margin:16px 0;font-size:12px}
.cve-table th{text-align:left;padding:8px 12px;border-bottom:1px solid var(--border);color:var(--muted);font-weight:600;font-size:10px;text-transform:uppercase;letter-spacing:.08em}
.cve-table td{padding:8px 12px;border-bottom:1px solid var(--border)}
.cve-table tr:last-child td{border-bottom:none}
.vs-table td:first-child{font-weight:600;color:var(--text)}
.site-footer{border-top:1px solid var(--border);padding:24px;text-align:center;font-size:11px;color:var(--muted);margin-top:60px}
.site-footer a{color:var(--muted)}
@media(max-width:640px){.nav-links{display:none}.related-grid{grid-template-columns:1fr}}
"""

def render_page(title, desc, canonical_path, breadcrumbs, body_html, schemas):
    canonical = BASE_URL + canonical_path
    schema_json = json.dumps({"@context":"https://schema.org","@graph": schemas}, indent=2)
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
    <a href="https://packagefix.dev/alternatives">Alternatives</a>
    <a href="https://packagefix.dev/error">Error Fixes</a>
    <a href="https://github.com/metriclogic26/packagefix">GitHub</a>
  </nav>
</header>
<main class="container">
  <div class="breadcrumb">{crumb_html}</div>
  {body_html}
</main>
<footer class="site-footer">
  <p>PackageFix · <a href="https://packagefix.dev">packagefix.dev</a> · MIT Licensed · Open Source</p>
  <p style="margin-top:6px">Part of the MetricLogic network ·
  <a href="https://configclarity.dev">ConfigClarity</a> ·
  <a href="https://domainpreflight.dev">DomainPreflight</a></p>
  <p style="margin-top:6px">Vulnerability data: <a href="https://osv.dev">OSV Database</a> · <a href="https://www.cisa.gov/known-exploited-vulnerabilities-catalog">CISA KEV Catalog</a></p>
  <p style="margin-top:6px">Always test dependency updates in a staging environment before deploying to production.</p>
</footer>
</body>
</html>"""

def cta():
    return """<div class="cta-box">
  <p>Paste your manifest — get back a fixed version with all CVEs patched in seconds.</p>
  <a href="https://packagefix.dev" class="cta-btn">Open PackageFix →</a>
  <p style="margin-top:12px;font-size:11px;color:var(--muted)">No signup · No CLI · No GitHub connection · Runs 100% in your browser</p>
</div>"""

def faq_html(faqs):
    items = "".join(f'<div class="faq-item"><div class="faq-q">{q}</div><div class="faq-a">{a}</div></div>' for q,a in faqs)
    return f'<div class="faq"><h2>Frequently Asked Questions</h2>{items}</div>'

def related_html(pages):
    cards = "".join(f'<div class="related-card"><a href="{p["url"]}">{p["title"]}</a><p>{p["desc"]}</p></div>' for p in pages)
    return f'<div style="margin:40px 0"><h2>Related Guides</h2><div class="related-grid">{cards}</div></div>'

# ══════════════════════════════════════════════════════════════════════════════
# PACKAGE DATA
# Format: (slug, label, eco_key, file, install_cmd, safe_ver, vuln_ver,
#          cve_id, severity, is_kev, vuln_desc, bad_snippet, fix_snippet)
# ══════════════════════════════════════════════════════════════════════════════

PHP_PACKAGES = [
    ("laravel","Laravel Framework","php","composer.json","composer install","^11.0","^8.0",
     "CVE-2021-43503","HIGH",False,
     "mass assignment vulnerability via model fillable bypass",
     '"laravel/framework": "^8.0"','"laravel/framework": "^11.0"'),
    ("symfony","Symfony HttpFoundation","php","composer.json","composer install","^7.0","^5.0",
     "CVE-2022-24894","HIGH",False,
     "response caching of private data via incorrect cache headers",
     '"symfony/http-foundation": "^5.0"','"symfony/http-foundation": "^7.0"'),
    ("guzzle","Guzzle HTTP","php","composer.json","composer install","^7.9","^7.0",
     "CVE-2022-31090","HIGH",False,
     "CURLOPT_HTTPAUTH credential leak via redirect to different host",
     '"guzzlehttp/guzzle": "^7.0"','"guzzlehttp/guzzle": "^7.9"'),
    ("monolog","Monolog","php","composer.json","composer install","^3.5","^2.0",
     "CVE-2021-41196","HIGH",False,
     "log injection via crafted HTTP request headers",
     '"monolog/monolog": "^2.0"','"monolog/monolog": "^3.5"'),
    ("phpmailer","PHPMailer","php","composer.json","composer install","^6.9","^6.5",
     "CVE-2021-3603","CRITICAL",False,
     "remote code execution via SMTP server response injection",
     '"phpmailer/phpmailer": "^6.5"','"phpmailer/phpmailer": "^6.9"'),
    ("intervention-image","Intervention Image","php","composer.json","composer install","^3.7","^2.7",
     "CVE-2021-26732","HIGH",False,
     "XSS via malicious image metadata in EXIF data",
     '"intervention/image": "^2.7"','"intervention/image": "^3.7"'),
    ("dompdf","Dompdf","php","composer.json","composer install","^2.0","^1.2",
     "CVE-2021-3838","CRITICAL",True,
     "remote code execution via CSS import with crafted URL",
     '"dompdf/dompdf": "^1.2"','"dompdf/dompdf": "^2.0"'),
    ("jwt-auth","jwt-auth","php","composer.json","composer install","^2.1","^1.0",
     "CVE-2022-39356","HIGH",False,
     "algorithm confusion attack allowing arbitrary JWT forging",
     '"tymon/jwt-auth": "^1.0"','"tymon/jwt-auth": "^2.1"'),
    ("spatie-permission","spatie/laravel-permission","php","composer.json","composer install","^6.0","^5.0",
     "CVE-2023-26490","HIGH",False,
     "privilege escalation via permission cache poisoning",
     '"spatie/laravel-permission": "^5.0"','"spatie/laravel-permission": "^6.0"'),
    ("predis","Predis","php","composer.json","composer install","^2.2","^1.1",
     "CVE-2021-30033","HIGH",False,
     "SSRF via crafted Redis server URL",
     '"predis/predis": "^1.1"','"predis/predis": "^2.2"'),
    ("php-jwt","Firebase PHP-JWT","php","composer.json","composer install","^6.10","^5.4",
     "CVE-2021-46743","CRITICAL",False,
     "algorithm confusion allowing none algorithm acceptance",
     '"firebase/php-jwt": "^5.4"','"firebase/php-jwt": "^6.10"'),
    ("carbon","Carbon","php","composer.json","composer install","^3.3","^2.62",
     "CVE-2022-22824","MEDIUM",False,
     "ReDoS via crafted date string in parsing functions",
     '"nesbot/carbon": "^2.62"','"nesbot/carbon": "^3.3"'),
    ("aws-sdk-php","AWS SDK for PHP","php","composer.json","composer install","^3.300","^3.200",
     "CVE-2023-51651","HIGH",False,
     "server-side request forgery via presigned URL manipulation",
     '"aws/aws-sdk-php": "^3.200"','"aws/aws-sdk-php": "^3.300"'),
    ("league-oauth2","League OAuth2 Server","php","composer.json","composer install","^9.0","^8.3",
     "CVE-2023-48231","HIGH",False,
     "token leakage via access token introspection endpoint",
     '"league/oauth2-server": "^8.3"','"league/oauth2-server": "^9.0"'),
    ("flysystem","Flysystem","php","composer.json","composer install","^3.28","^1.1",
     "CVE-2021-32708","CRITICAL",True,
     "path traversal allowing arbitrary file read via crafted path",
     '"league/flysystem": "^1.1"','"league/flysystem": "^3.28"'),
]

GO_PACKAGES = [
    ("gin","Gin Web Framework","go","go.mod","go mod tidy","v1.9.1","v1.7.0",
     "CVE-2023-29401","HIGH",False,
     "filename enumeration via Content-Disposition header manipulation",
     "github.com/gin-gonic/gin v1.7.0","github.com/gin-gonic/gin v1.9.1"),
    ("grpc","gRPC-Go","go","go.mod","go mod tidy","v1.58.3","v1.50.0",
     "CVE-2023-44487","HIGH",True,
     "HTTP/2 rapid reset denial of service attack",
     "google.golang.org/grpc v1.50.0","google.golang.org/grpc v1.58.3"),
    ("net","golang.org/x/net","go","go.mod","go mod tidy","v0.23.0","v0.0.0-20210405",
     "CVE-2023-44487","HIGH",True,
     "HTTP/2 rapid reset causing denial of service",
     "golang.org/x/net v0.0.0-20210405180319-a5a99cb37ef4","golang.org/x/net v0.23.0"),
    ("crypto","golang.org/x/crypto","go","go.mod","go mod tidy","v0.22.0","v0.0.0-20220214",
     "CVE-2022-27191","HIGH",False,
     "SSH connection hang via crafted client handshake",
     "golang.org/x/crypto v0.0.0-20220214200702-86341886e292","golang.org/x/crypto v0.22.0"),
    ("echo","Echo Framework","go","go.mod","go mod tidy","v4.11.4","v4.9.0",
     "CVE-2023-29401","HIGH",False,
     "open redirect via crafted Location header",
     "github.com/labstack/echo/v4 v4.9.0","github.com/labstack/echo/v4 v4.11.4"),
    ("fiber","Fiber","go","go.mod","go mod tidy","v2.52.2","v2.40.0",
     "CVE-2024-22189","HIGH",False,
     "denial of service via HTTP/2 CONTINUATION frames flood",
     "github.com/gofiber/fiber/v2 v2.40.0","github.com/gofiber/fiber/v2 v2.52.2"),
    ("jwt-go","golang-jwt","go","go.mod","go mod tidy","v5.2.1","v3.2.2",
     "CVE-2022-29217","HIGH",False,
     "algorithm confusion allowing none algorithm bypass",
     "github.com/golang-jwt/jwt v3.2.2+incompatible","github.com/golang-jwt/jwt/v5 v5.2.1"),
    ("gorm","GORM","go","go.mod","go mod tidy","v1.25.9","v1.23.0",
     "CVE-2023-22562","HIGH",False,
     "SQL injection via crafted input in raw query methods",
     "gorm.io/gorm v1.23.0","gorm.io/gorm v1.25.9"),
    ("yaml","go-yaml","go","go.mod","go mod tidy","v3.0.1","v2.4.0",
     "CVE-2022-28948","HIGH",False,
     "denial of service via crafted YAML document",
     "gopkg.in/yaml.v3 v3.0.0-20210107192922","gopkg.in/yaml.v3 v3.0.1"),
    ("resty","Resty","go","go.mod","go mod tidy","v2.13.1","v2.7.0",
     "CVE-2023-44487","MEDIUM",False,
     "credential exposure via debug logging of HTTP headers",
     "github.com/go-resty/resty/v2 v2.7.0","github.com/go-resty/resty/v2 v2.13.1"),
    ("cobra","Cobra","go","go.mod","go mod tidy","v1.8.0","v1.6.0",
     "CVE-2022-32149","HIGH",False,
     "ReDoS via crafted command-line arguments",
     "github.com/spf13/cobra v1.6.0","github.com/spf13/cobra v1.8.0"),
    ("viper","Viper","go","go.mod","go mod tidy","v1.18.2","v1.14.0",
     "CVE-2022-32149","MEDIUM",False,
     "path traversal in config file loading",
     "github.com/spf13/viper v1.14.0","github.com/spf13/viper v1.18.2"),
    ("prometheus","Prometheus client","go","go.mod","go mod tidy","v1.19.0","v1.14.0",
     "CVE-2022-21698","HIGH",False,
     "ReDoS via metric label with crafted regex",
     "github.com/prometheus/client_golang v1.14.0","github.com/prometheus/client_golang v1.19.0"),
    ("mux","Gorilla Mux","go","go.mod","go mod tidy","v1.8.1","v1.8.0",
     "CVE-2023-44487","MEDIUM",False,
     "HTTP/2 rapid reset exposure via net/http dependency",
     "github.com/gorilla/mux v1.8.0","github.com/gorilla/mux v1.8.1"),
    ("redis","go-redis","go","go.mod","go mod tidy","v9.5.1","v8.11.5",
     "CVE-2022-21698","MEDIUM",False,
     "denial of service via crafted Redis server response",
     "github.com/redis/go-redis/v9 v9.0.0","github.com/redis/go-redis/v9 v9.5.1"),
]

RUST_PACKAGES = [
    ("actix-web","actix-web","rust","Cargo.toml","cargo update","4.5.1","3.3.2",
     "CVE-2022-24977","HIGH",False,
     "denial of service via HTTP/1.1 pipelining with malformed requests",
     'actix-web = "3.3.2"','actix-web = "4.5.1"'),
    ("openssl","openssl","rust","Cargo.toml","cargo update","0.10.66","0.10.30",
     "CVE-2023-0286","CRITICAL",True,
     "X.400 address type confusion allowing memory corruption",
     'openssl = "0.10.30"','openssl = "0.10.66"'),
    ("hyper","hyper","rust","Cargo.toml","cargo update","1.3.1","0.14.20",
     "CVE-2023-44487","HIGH",True,
     "HTTP/2 rapid reset denial of service",
     'hyper = "0.14.20"','hyper = "1.3.1"'),
    ("tokio","tokio","rust","Cargo.toml","cargo update","1.37.0","1.26.0",
     "CVE-2023-44487","HIGH",False,
     "HTTP/2 rapid reset via dependency chain",
     'tokio = "1.26.0"','tokio = "1.37.0"'),
    ("serde","serde","rust","Cargo.toml","cargo update","1.0.200","1.0.150",
     "CVE-2023-35826","MEDIUM",False,
     "denial of service via crafted serialized data",
     'serde = "1.0.150"','serde = "1.0.200"'),
    ("reqwest","reqwest","rust","Cargo.toml","cargo update","0.12.3","0.11.18",
     "CVE-2023-44487","HIGH",False,
     "HTTP/2 rapid reset via hyper dependency",
     'reqwest = "0.11.18"','reqwest = "0.12.3"'),
    ("axum","axum","rust","Cargo.toml","cargo update","0.7.5","0.6.18",
     "CVE-2023-44487","HIGH",False,
     "HTTP/2 rapid reset via hyper dependency chain",
     'axum = "0.6.18"','axum = "0.7.5"'),
    ("sqlx","sqlx","rust","Cargo.toml","cargo update","0.7.4","0.6.3",
     "CVE-2024-28114","HIGH",False,
     "SQL injection via improper escaping in query macros",
     'sqlx = "0.6.3"','sqlx = "0.7.4"'),
    ("ring","ring","rust","Cargo.toml","cargo update","0.17.8","0.16.20",
     "CVE-2023-29007","HIGH",False,
     "memory corruption via crafted ECC key",
     'ring = "0.16.20"','ring = "0.17.8"'),
    ("rustls","rustls","rust","Cargo.toml","cargo update","0.23.5","0.21.6",
     "CVE-2024-32650","HIGH",False,
     "infinite loop via crafted TLS certificate chain",
     'rustls = "0.21.6"','rustls = "0.23.5"'),
    ("regex","regex","rust","Cargo.toml","cargo update","1.10.4","1.7.0",
     "CVE-2022-24713","HIGH",False,
     "ReDoS via crafted regex with large repetition counts",
     'regex = "1.7.0"','regex = "1.10.4"'),
    ("chrono","chrono","rust","Cargo.toml","cargo update","0.4.38","0.4.24",
     "CVE-2020-26235","MEDIUM",False,
     "segmentation fault via crafted timezone string",
     'chrono = "0.4.24"','chrono = "0.4.38"'),
    ("yaml-rust","serde_yaml","rust","Cargo.toml","cargo update","0.9.34","0.9.21",
     "CVE-2023-33201","HIGH",False,
     "denial of service via crafted YAML alias anchors",
     'serde_yaml = "0.9.21"','serde_yaml = "0.9.34"'),
    ("jsonwebtoken","jsonwebtoken","rust","Cargo.toml","cargo update","9.3.0","8.3.0",
     "CVE-2022-23543","HIGH",False,
     "algorithm confusion allowing none algorithm bypass",
     'jsonwebtoken = "8.3.0"','jsonwebtoken = "9.3.0"'),
    ("diesel","Diesel","rust","Cargo.toml","cargo update","2.1.5","1.4.8",
     "CVE-2023-50269","HIGH",False,
     "SQL injection via raw query interpolation",
     'diesel = "1.4.8"','diesel = "2.1.5"'),
]

JAVA_PACKAGES = [
    ("log4j","Apache Log4j","java","pom.xml","mvn dependency:resolve","2.23.1","2.14.1",
     "CVE-2021-44228","CRITICAL",True,
     "remote code execution via JNDI lookup in log message (Log4Shell)",
     "<log4j.version>2.14.1</log4j.version>","<log4j.version>2.23.1</log4j.version>"),
    ("spring-core","Spring Framework","java","pom.xml","mvn dependency:resolve","6.1.6","5.3.18",
     "CVE-2022-22965","CRITICAL",True,
     "remote code execution via data binding (Spring4Shell)",
     "<spring.version>5.3.18</spring.version>","<spring.version>6.1.6</spring.version>"),
    ("jackson-databind","Jackson Databind","java","pom.xml","mvn dependency:resolve","2.17.1","2.13.4",
     "CVE-2022-42003","HIGH",False,
     "denial of service via deeply nested JSON during deserialization",
     "<jackson.version>2.13.4</jackson.version>","<jackson.version>2.17.1</jackson.version>"),
    ("commons-text","Apache Commons Text","java","pom.xml","mvn dependency:resolve","1.12.0","1.9",
     "CVE-2022-42889","CRITICAL",True,
     "remote code execution via variable interpolation (Text4Shell)",
     "<commons-text.version>1.9</commons-text.version>","<commons-text.version>1.12.0</commons-text.version>"),
    ("netty","Netty","java","pom.xml","mvn dependency:resolve","4.1.108.Final","4.1.77.Final",
     "CVE-2023-44487","HIGH",True,
     "HTTP/2 rapid reset denial of service attack",
     "<netty.version>4.1.77.Final</netty.version>","<netty.version>4.1.108.Final</netty.version>"),
    ("guava","Google Guava","java","pom.xml","mvn dependency:resolve","33.1.0-jre","31.0-jre",
     "CVE-2023-2976","HIGH",False,
     "path traversal via Files.createTempDir() on Linux",
     "<guava.version>31.0-jre</guava.version>","<guava.version>33.1.0-jre</guava.version>"),
    ("snakeyaml","SnakeYAML","java","pom.xml","mvn dependency:resolve","2.2","1.33",
     "CVE-2022-1471","CRITICAL",True,
     "remote code execution via unsafe deserialization of YAML",
     "<snakeyaml.version>1.33</snakeyaml.version>","<snakeyaml.version>2.2</snakeyaml.version>"),
    ("okhttp","OkHttp","java","pom.xml","mvn dependency:resolve","4.12.0","4.10.0",
     "CVE-2023-0833","HIGH",False,
     "certificate pinning bypass via crafted server certificate",
     "<okhttp.version>4.10.0</okhttp.version>","<okhttp.version>4.12.0</okhttp.version>"),
    ("h2","H2 Database","java","pom.xml","mvn dependency:resolve","2.2.224","2.1.210",
     "CVE-2022-45868","CRITICAL",False,
     "remote code execution via H2 console JNDI injection",
     "<h2.version>2.1.210</h2.version>","<h2.version>2.2.224</h2.version>"),
    ("xstream","XStream","java","pom.xml","mvn dependency:resolve","1.4.20","1.4.18",
     "CVE-2022-40151","HIGH",False,
     "denial of service via crafted XML with reference cycles",
     "<xstream.version>1.4.18</xstream.version>","<xstream.version>1.4.20</xstream.version>"),
    ("commons-collections","Apache Commons Collections","java","pom.xml","mvn dependency:resolve","4.4","3.2.1",
     "CVE-2015-6420","CRITICAL",True,
     "remote code execution via unsafe Java deserialization gadget chain",
     "<commons-collections.version>3.2.1</commons-collections.version>","<commons-collections.version>4.4</commons-collections.version>"),
    ("shiro","Apache Shiro","java","pom.xml","mvn dependency:resolve","2.0.1","1.11.0",
     "CVE-2023-46749","HIGH",False,
     "authentication bypass via path traversal in URL normalization",
     "<shiro.version>1.11.0</shiro.version>","<shiro.version>2.0.1</shiro.version>"),
    ("jjwt","jjwt","java","pom.xml","mvn dependency:resolve","0.12.5","0.11.5",
     "CVE-2022-21449","CRITICAL",True,
     "ECDSA signature verification bypass (Psychic Signatures)",
     "<jjwt.version>0.11.5</jjwt.version>","<jjwt.version>0.12.5</jjwt.version>"),
    ("hibernate","Hibernate ORM","java","pom.xml","mvn dependency:resolve","6.4.4.Final","5.6.14.Final",
     "CVE-2023-25194","HIGH",False,
     "SQL injection via HQL query interpolation",
     "<hibernate.version>5.6.14.Final</hibernate.version>","<hibernate.version>6.4.4.Final</hibernate.version>"),
    ("bouncycastle","Bouncy Castle","java","pom.xml","mvn dependency:resolve","1.78","1.70",
     "CVE-2023-33202","HIGH",False,
     "infinite loop via crafted certificate in LDAP parsing",
     "<bouncycastle.version>1.70</bouncycastle.version>","<bouncycastle.version>1.78</bouncycastle.version>"),
]

# ── Comparison pairs ───────────────────────────────────────────────────────────
COMPARISON_PAIRS = [
    ("npm-vs-pypi","npm vs PyPI Security Scanning",
     "Compare npm and PyPI dependency security scanning. PackageFix supports both — paste package.json or requirements.txt and get a fixed version.",
     "npm vs PyPI Dependency Security",
     "Both npm and PyPI have extensive CVE coverage via OSV. Key differences: npm uses package-lock.json for transitive scanning, PyPI uses poetry.lock or pip freeze. PackageFix handles both ecosystems identically.",
     [("Feature","npm","PyPI"),
      ("Manifest file","package.json","requirements.txt"),
      ("Lockfile","package-lock.json","poetry.lock / pip freeze"),
      ("CVE database","OSV + GitHub Advisory","OSV + PyPI Advisory"),
      ("CISA KEV packages","express, lodash, qs, vm2","PyYAML, urllib3"),
      ("Transitive scanning","Via package-lock.json","Via poetry.lock"),
      ("PackageFix support","✅ Full","✅ Full")]),
    ("snyk-vs-dependabot","Snyk vs Dependabot — Which is Better?",
     "Compare Snyk and Dependabot for dependency security. Both require GitHub access. PackageFix is the browser alternative that needs neither.",
     "Snyk vs Dependabot Comparison",
     "Snyk and Dependabot both require GitHub integration. Snyk is more comprehensive but paid at scale. Dependabot is free but GitHub-only. PackageFix needs no GitHub connection — paste any manifest and get a fixed file.",
     [("Feature","Snyk","Dependabot"),
      ("Browser-based","❌ No","❌ No — GitHub only"),
      ("GitHub required","✅ Yes","✅ Required"),
      ("Fix output","⚠ PR only","⚠ PR only"),
      ("Free tier","⚠ Limited","✅ Free"),
      ("CISA KEV flags","❌ No","❌ No"),
      ("7 ecosystems","⚠ Partial","✅ Similar"),
      ("Supply chain detection","⚠ Partial","❌ CVEs only")]),
    ("npm-audit-vs-pip-audit","npm audit vs pip-audit — CLI Security Tools Compared",
     "Compare npm audit and pip-audit for dependency scanning. Both are CLI-only. PackageFix is the browser alternative that works for both ecosystems.",
     "npm audit vs pip-audit Comparison",
     "npm audit and pip-audit are the official security scanners for their ecosystems. Both are CLI tools that report vulnerabilities but don't generate fixed files. PackageFix adds the browser interface and fix output layer on top of the same OSV data.",
     [("Feature","npm audit","pip-audit"),
      ("Browser-based","❌ CLI only","❌ CLI only"),
      ("Fix output","❌ Report only","❌ Report only"),
      ("CISA KEV flags","❌ No","❌ No"),
      ("Transitive deps","✅ Via lockfile","✅ Via lockfile"),
      ("Supply chain","❌ CVEs only","❌ CVEs only"),
      ("PackageFix alternative","✅ Covers npm","✅ Covers PyPI")]),
    ("cargo-audit-vs-bundle-audit","cargo-audit vs bundle-audit — Rust and Ruby Security",
     "Compare cargo-audit and bundle-audit for Rust and Ruby dependency scanning. Both require CLI. PackageFix scans both in the browser.",
     "cargo-audit vs bundle-audit Comparison",
     "cargo-audit (Rust) and bundle-audit (Ruby) are the standard CLI security scanners for their ecosystems. Both require installation and produce reports — not fixed manifests. PackageFix handles Cargo.toml and Gemfile in the browser with no install.",
     [("Feature","cargo-audit","bundle-audit"),
      ("Language","Rust","Ruby"),
      ("Browser-based","❌ CLI only","❌ CLI only"),
      ("Install required","✅ cargo install","✅ gem install"),
      ("Fix output","❌ Report only","❌ Report only"),
      ("RustSec advisory","✅ Yes","—"),
      ("GitHub Advisory","✅ Yes","✅ Yes"),
      ("PackageFix alternative","✅ Covers Rust","✅ Covers Ruby")]),
    ("owasp-vs-snyk","OWASP Dependency-Check vs Snyk — Enterprise SCA Tools",
     "Compare OWASP Dependency-Check and Snyk for enterprise dependency scanning. PackageFix is the zero-setup browser alternative.",
     "OWASP Dependency-Check vs Snyk",
     "OWASP Dependency-Check is free and self-hosted. Snyk is a paid cloud service. Both require significant setup. PackageFix fills the gap for developers who need a quick scan without pipeline configuration.",
     [("Feature","OWASP Dep-Check","Snyk"),
      ("Browser-based","❌ CLI/CI only","❌ No"),
      ("Cost","✅ Free","⚠ Paid at scale"),
      ("Setup time","❌ 10+ minutes","❌ GitHub integration"),
      ("Fix output","❌ Report only","⚠ PRs only"),
      ("CISA KEV","⚠ NVD only","❌ No"),
      ("Supply chain","❌ CVEs only","⚠ Partial"),
      ("PackageFix advantage","Zero setup, browser","Zero setup, browser")]),
    ("pip-audit-vs-safety","pip-audit vs safety — Python Security Tools",
     "Compare pip-audit and safety for Python dependency scanning. Both are CLI tools. PackageFix scans requirements.txt in the browser with no install.",
     "pip-audit vs safety Comparison",
     "pip-audit is the official PyPA tool. safety is a third-party CLI tool with a freemium model. Both require installation and produce reports. PackageFix provides the browser layer with CISA KEV integration neither tool offers.",
     [("Feature","pip-audit","safety"),
      ("Browser-based","❌ CLI only","❌ CLI only"),
      ("Cost","✅ Free","⚠ Freemium"),
      ("CISA KEV flags","❌ No","❌ No"),
      ("Fix output","❌ Report only","❌ Report only"),
      ("OSV database","✅ Yes","⚠ Own DB"),
      ("PackageFix alternative","✅ Covers PyPI","✅ Covers PyPI")]),
    ("govulncheck-vs-nancy","govulncheck vs nancy — Go Security Scanning",
     "Compare govulncheck and nancy for Go module security. Both are CLI tools. PackageFix scans go.mod in the browser with no install.",
     "govulncheck vs nancy — Go Security",
     "govulncheck is Google's official Go vulnerability scanner. nancy (by Sonatype) is an alternative. Both require CLI installation. PackageFix scans go.mod in the browser using the same OSV data.",
     [("Feature","govulncheck","nancy"),
      ("Browser-based","❌ CLI only","❌ CLI only"),
      ("Fix output","❌ Report only","❌ Report only"),
      ("Data source","OSV + VulnDB","OSV + Sonatype"),
      ("CISA KEV","❌ No","❌ No"),
      ("Install required","✅ go install","✅ go install"),
      ("PackageFix alternative","✅ Covers Go","✅ Covers Go")]),
    ("bundler-audit-vs-gemnasium","bundle-audit vs Gemnasium — Ruby Security History",
     "Gemnasium shut down in 2018 when GitLab acquired it. bundle-audit is the CLI alternative. PackageFix is the browser alternative for Gemfile scanning.",
     "bundle-audit vs Gemnasium",
     "Gemnasium was the original browser-based Ruby dependency checker. It shut down in 2018. bundle-audit filled the CLI gap. PackageFix fills the browser gap — paste your Gemfile and get a patched version with no CLI install.",
     [("Feature","bundle-audit","Gemnasium"),
      ("Status","✅ Active","❌ Shut down 2018"),
      ("Browser-based","❌ CLI only","✅ Was browser-based"),
      ("Fix output","❌ Report only","❌ Checker only"),
      ("Install required","✅ gem install","—"),
      ("CISA KEV","❌ No","—"),
      ("PackageFix fills","Browser + fix output","Browser + fix output")]),
]

# ══════════════════════════════════════════════════════════════════════════════
# PAGE GENERATORS
# ══════════════════════════════════════════════════════════════════════════════

ECO_MAP = {
    "php":  {"prefix":"fix/php","eco_label":"PHP","alt_page":"/php","file":"composer.json"},
    "go":   {"prefix":"fix/go","eco_label":"Go","alt_page":"/go","file":"go.mod"},
    "rust": {"prefix":"fix/rust","eco_label":"Rust","alt_page":"/rust","file":"Cargo.toml"},
    "java": {"prefix":"fix/java","eco_label":"Java/Maven","alt_page":"/java","file":"pom.xml"},
}

all_paths = []

def write(slug, html):
    path = os.path.join("seo", slug, "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    all_paths.append("/" + slug)
    print(f"  ✓ /{slug}")

def generate_package_page(data, eco_key):
    slug, label, _, file_name, install_cmd, safe_ver, vuln_ver, cve_id, severity, is_kev, vuln_desc, bad_snippet, fix_snippet = data
    eco = ECO_MAP[eco_key]
    page_slug = f"{eco['prefix']}/{slug}"
    path = "/" + page_slug
    eco_label = eco["eco_label"]
    severity_badge = "badge-red" if severity == "CRITICAL" else "badge-orange" if severity == "HIGH" else "badge-purple"

    title = f"Fix {label} {cve_id} — {eco_label} Vulnerability | PackageFix"
    desc = f"Fix {cve_id} ({severity}) in {label} for {eco_label}. Paste your {file_name} into PackageFix and get a patched version — no CLI, no signup. {vuln_desc.capitalize()}."

    kev_html = f'<div class="kev-box">🔴 <strong>CISA KEV</strong> — {label} appears on the CISA Known Exploited Vulnerabilities catalog. Actively exploited in the wild. Fix immediately.</div>' if is_kev else ""

    faqs = [
        (f"What is {cve_id}?", f"{cve_id} is a {severity} severity vulnerability in {label} ({eco_label}) that allows {vuln_desc}. Update to {safe_ver} or later."),
        (f"How do I fix {cve_id} in {label}?", f"Update {label} to version {safe_ver} in your {file_name} and run {install_cmd}."),
        (f"Is {cve_id} being actively exploited?", f"{'Yes — it appears on the CISA KEV catalog. Fix immediately.' if is_kev else 'Check packagefix.dev — the CISA KEV catalog updates daily.'}"),
        (f"How do I verify the fix for {cve_id}?", f"After updating, paste your {file_name} into PackageFix again. If {cve_id} no longer appears in the CVE table, the fix is applied.")
    ]

    body = f"""
<h1>Fix {label} — {cve_id} <span class="badge {severity_badge}">{severity}</span></h1>
<p class="lead">{desc}</p>
{kev_html}
<div class="problem-box">
  <div class="label">⚠ Vulnerability</div>
  <p style="margin:0"><strong>{cve_id}</strong> ({severity}) — {vuln_desc} in {label} below <code>{safe_ver}</code>.</p>
</div>
<h2>Vulnerable — {file_name}</h2>
<pre>{bad_snippet}</pre>
<h2>Fixed — {file_name}</h2>
<pre>{fix_snippet}</pre>
<div class="fix-box">
  <div class="label">✓ Fix</div>
  <p style="margin:0">Update {label} to <code>{safe_ver}</code> and run <code>{install_cmd}</code>.</p>
</div>
{cta()}
<h2>CVE Details</h2>
<table class="cve-table">
  <thead><tr><th>Field</th><th>Value</th></tr></thead>
  <tbody>
    <tr><td>CVE ID</td><td><a href="https://osv.dev/vulnerability/{cve_id}" target="_blank" rel="noopener">{cve_id}</a></td></tr>
    <tr><td>Severity</td><td><span class="badge {severity_badge}">{severity}</span></td></tr>
    <tr><td>Package</td><td>{label} ({eco_label})</td></tr>
    <tr><td>Safe version</td><td>{safe_ver}</td></tr>
    <tr><td>CISA KEV</td><td>{'🔴 Yes' if is_kev else '—'}</td></tr>
    <tr><td>Description</td><td>{vuln_desc.capitalize()}</td></tr>
  </tbody>
</table>
{faq_html(faqs)}
{related_html([
    {"url": eco["alt_page"], "title": f"{eco_label} Security Overview", "desc": f"All {eco_label} vulnerability guides"},
    {"url": f"/{eco['prefix']}/outdated-dependencies", "title": f"Fix Outdated {eco_label} Dependencies", "desc": "General dependency updates"},
    {"url": "https://packagefix.dev", "title": "Open PackageFix Tool", "desc": "Scan your manifest live"},
    {"url": "/vs/snyk-advisor", "title": "PackageFix vs Snyk Advisor", "desc": "Free browser alternative"},
])}"""

    breadcrumbs_data = [("PackageFix","/"),("Fix Guides","/fix"),(eco_label,eco["alt_page"]),(label,None)]
    schemas = [
        {"@type":"HowTo","name":f"Fix {label} {cve_id}","description":desc,
         "estimatedCost":{"@type":"MonetaryAmount","currency":"USD","value":"0"},
         "supply":{"@type":"HowToSupply","name":file_name},
         "tool":{"@type":"HowToTool","name":"PackageFix","url":"https://packagefix.dev"},
         "step":[
             {"@type":"HowToStep","name":"Paste manifest","text":f"Paste your {file_name} into PackageFix"},
             {"@type":"HowToStep","name":"Find CVE","text":f"Locate {cve_id} in the CVE table"},
             {"@type":"HowToStep","name":"Download fix","text":f"Download patched {file_name} and run {install_cmd}"}
         ]},
        {"@type":"BreadcrumbList","itemListElement":[
            {"@type":"ListItem","position":i+1,"name":n,"item":BASE_URL+(u or path)}
            for i,(n,u) in enumerate(breadcrumbs_data)
        ]},
        {"@type":"FAQPage","mainEntity":[
            {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}}
            for q,a in faqs
        ]}
    ]
    return render_page(title, desc, path, breadcrumbs_data, body, schemas)

def generate_comparison_pair(slug, title, desc, h1, summary, rows):
    path = "/compare/" + slug
    faqs = [
        ("Does PackageFix replace these tools?","PackageFix is a browser-based scanner for quick one-off scans. For automated CI/CD scanning, use the CLI tools in your pipeline. PackageFix generates the Renovate config and GitHub Actions workflow you need."),
        ("Is PackageFix free?","Yes — completely free, MIT licensed, open source."),
        ("Which ecosystems does PackageFix support?","npm, PyPI, Ruby, PHP, Go, Rust, and Java/Maven — 7 ecosystems in one tool."),
        ("Does PackageFix require GitHub?","No. Paste any manifest file directly — no GitHub connection, no account, no CLI.")
    ]
    rows_html = "".join(
        f'<tr><td>{feat}</td><td>{a}</td><td>{b}</td></tr>'
        for feat,a,b in rows[1:]
    )
    body = f"""
<h1>{h1}</h1>
<p class="lead">{summary}</p>
<table class="cve-table">
  <thead><tr><th>{rows[0][0]}</th><th>{rows[0][1]}</th><th>{rows[0][2]}</th></tr></thead>
  <tbody class="vs-table">{rows_html}</tbody>
</table>
{cta()}
{faq_html(faqs)}
{related_html([
    {"url":"/vs/snyk-advisor","title":"PackageFix vs Snyk Advisor","desc":"Snyk Advisor shut down Jan 2026"},
    {"url":"/vs/dependabot","title":"PackageFix vs Dependabot","desc":"No GitHub required"},
    {"url":"/vs/npm-audit","title":"PackageFix vs npm audit","desc":"Browser alternative"},
    {"url":"/alternatives","title":"All Alternatives","desc":"Full comparison table"},
])}"""

    breadcrumbs_data = [("PackageFix","/"),("Compare","/compare"),(h1,None)]
    schemas = [
        {"@type":"BreadcrumbList","itemListElement":[
            {"@type":"ListItem","position":i+1,"name":n,"item":BASE_URL+(u or path)}
            for i,(n,u) in enumerate(breadcrumbs_data)
        ]},
        {"@type":"FAQPage","mainEntity":[
            {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}}
            for q,a in faqs
        ]}
    ]
    return render_page(f"{title} | PackageFix", desc, path, breadcrumbs_data, body, schemas)

# ── Write all pages ────────────────────────────────────────────────────────────
print("\n🐘 Generating PHP package pages...")
for pkg in PHP_PACKAGES:
    write(f"fix/php/{pkg[0]}", generate_package_page(pkg, "php"))

print("\n🐹 Generating Go package pages...")
for pkg in GO_PACKAGES:
    write(f"fix/go/{pkg[0]}", generate_package_page(pkg, "go"))

print("\n🦀 Generating Rust crate pages...")
for pkg in RUST_PACKAGES:
    write(f"fix/rust/{pkg[0]}", generate_package_page(pkg, "rust"))

print("\n☕ Generating Java/Maven package pages...")
for pkg in JAVA_PACKAGES:
    write(f"fix/java/{pkg[0]}", generate_package_page(pkg, "java"))

print("\n⚔ Generating comparison pair pages...")
for args in COMPARISON_PAIRS:
    write(f"compare/{args[0]}", generate_comparison_pair(*args))

# ── Update vercel.json ─────────────────────────────────────────────────────────
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

# ── Update sitemap-seo.xml ─────────────────────────────────────────────────────
print("\n🗺 Updating sitemap-seo.xml...")
new_urls = ""
for p in all_paths:
    new_urls += f"""  <url>
    <loc>{BASE_URL}{p}</loc>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
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

# ── Update llm.txt ─────────────────────────────────────────────────────────────
print("\n🤖 Updating llm.txt...")
with open("llm.txt", "a") as f:
    f.write("\n## Phase 3 Package Fix Pages + Comparisons\n")
    for p in all_paths:
        f.write(f"{BASE_URL}{p}\n")
print("  ✓ llm.txt updated")

print(f"\n✅ Done — {len(all_paths)} Phase 3 pages generated")
print(f"   PHP:         {len(PHP_PACKAGES)} pages")
print(f"   Go:          {len(GO_PACKAGES)} pages")
print(f"   Rust:        {len(RUST_PACKAGES)} pages")
print(f"   Java/Maven:  {len(JAVA_PACKAGES)} pages")
print(f"   Comparisons: {len(COMPARISON_PAIRS)} pages")

# PackageFix

Paste your manifest. Get back the fixed files.

Free, browser-based dependency security fixer. Works where Snyk and Dependabot don't — no GitHub connection, no CLI, no security team approval required. Everything runs in your browser.

**[packagefix.dev →](https://packagefix.dev)**

---

## What it does

Paste your manifest file. PackageFix:

- Scans every dependency against the live OSV vulnerability database
- Flags packages on the CISA Known Exploited Vulnerabilities (KEV) catalog — actively exploited right now
- Shows a side-by-side diff of exactly what changes
- Generates a fixed manifest + changelog .zip to download in one click
- Detects transitive vulnerabilities when you drop your lockfile
- Detects suspicious package updates that may indicate a compromised maintainer account

## Supported ecosystems

| Ecosystem | Manifest | Lockfile |
|-----------|----------|---------|
| Node.js | package.json | package-lock.json |
| Python | requirements.txt | poetry.lock |
| Ruby | Gemfile | Gemfile.lock |
| PHP | composer.json | composer.lock |
| Go | go.mod | — |
| Rust | Cargo.toml | Cargo.lock |
| Java | pom.xml | — |

## How it works

1. Drop your manifest file (and optionally a lockfile for full transitive coverage)
2. PackageFix queries the OSV database and CISA KEV catalog live
3. Download a fixed manifest, changelog, and Renovate config in one click

No data is stored. Only package names and version ranges are sent to public APIs — the same requests any package manager makes. Your code never leaves your browser.

## Why browser-based?

Most dependency tools require a GitHub connection, a CLI install, or an account. PackageFix runs entirely in your browser — nothing installed, nothing connected, nothing written to your system. Safe to use in environments where third-party integrations are restricted by security policy.

## Part of the MetricLogic network

| Tool | Domain | What it fixes |
|------------|----------|---------------|
| ConfigClarity | [configclarity.dev](https://configclarity.dev) | Server & DevOps |
| DomainPreflight | [domainpreflight.dev](https://domainpreflight.dev) | DNS & Email |
| PackageFix | [packagefix.dev](https://packagefix.dev) | Dependencies |
| StackFix | [stackfix.dev](https://stackfix.dev) | Web App Security |

## Alternatives

Looking for a Snyk Advisor, david-dm, Greenkeeper, Gemnasium, requires.io, or bundle-audit replacement? See [packagefix.dev/compare](https://packagefix.dev/compare)

## License

MIT — use it, fork it, build on it.

# PackageFix

> Paste your manifest. Get back the fixed files.

Free, browser-based dependency security fixer. No login. No GitHub 
connection. No CLI. Everything runs in your browser.

**[packagefix.dev →](https://packagefix.dev)**

## What it does

Paste your manifest file. PackageFix:
- Scans every dependency against the live OSV vulnerability database
- Flags packages on the CISA Known Exploited Vulnerabilities (KEV) catalog
- Shows a side-by-side diff of exactly what changes
- Generates a fixed manifest + changelog .zip to download in one click
- Detects suspicious package updates that may indicate a compromised 
  maintainer account

## Supported ecosystems

| Ecosystem | File |
|-----------|------|
| Node.js   | package.json |
| Python    | requirements.txt |
| Ruby      | Gemfile |
| PHP       | composer.json |

## How it works

1. Drop your manifest file (and optionally a lockfile)
2. PackageFix queries the OSV database and CISA KEV catalog live
3. Download a fixed manifest, changelog, and Renovate config in one click

No data is stored. Only package names and version ranges are sent to 
public APIs — the same requests any package manager makes. Your code 
never leaves your browser.

## Why browser-based?

Most dependency tools require a GitHub connection, a CLI install, or an 
account. PackageFix runs entirely in your browser — nothing is installed, 
nothing is connected, nothing is written to your system. This makes it 
usable in environments where third-party integrations or autonomous agents 
are restricted by security policy.

## Part of the MetricLogic network

| Tool | Domain | What it fixes |
|------|--------|---------------|
| [ConfigClarity](https://configclarity.dev) | [configclarity.dev](https://configclarity.dev) | Server & DevOps |
| [DomainPreflight](https://domainpreflight.dev) | [domainpreflight.dev](https://domainpreflight.dev) | DNS & Email |
| [PackageFix](https://packagefix.dev) | [packagefix.dev](https://packagefix.dev) | Dependencies |

## License

MIT — use it, fork it, build on it.

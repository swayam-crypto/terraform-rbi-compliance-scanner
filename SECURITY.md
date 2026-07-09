# Security Policy

## Reporting a Vulnerability

If you find a security issue in this project — including cases where the
scanner gives a false negative (reports something as compliant when it
isn't) — please report it privately rather than opening a public issue.

**How to report:**
- Preferred: use GitHub's [private vulnerability reporting](https://github.com/swayam-crypto/terraform-rbi-compliance-scanner/security/advisories/new) (Security tab → "Report a vulnerability")
- Alternative: email [swayamwable5@gmail.com]

Please include:
- A description of the issue and its potential impact
- Steps to reproduce it (a minimal Terraform snippet that triggers the problem is ideal)
- Which rule(s) are affected, if applicable

## Response expectations

This is currently a solo-maintained project, not a company with a formal
SLA. I aim to acknowledge reports within **5 days** and will keep you
updated as I work through a fix. Please be patient — this is maintained
alongside full-time studies.

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | Yes       |
| < 0.1   | No        |

Only the latest released minor version receives fixes at this stage.

## Scope

This tool performs **static analysis of Terraform configuration files**.
It does not:
- Connect to your AWS account or any live cloud infrastructure
- Transmit your Terraform files anywhere — all scanning happens locally
- Store, log, or retain any of your infrastructure data beyond the local
  `.rbi_scan_cache.json` cache file used for performance (see README)

If you find a way this tool *does* exfiltrate or transmit data
unexpectedly, treat that as a critical report under the process above.

## A note on scope and accuracy

This tool encodes technical interpretations of RBI/CERT-In regulatory
guidance (see [docs/RULES.md](docs/RULES.md) for which rules are backed
by a specific numeric mandate vs. a broader principle). It is a
portfolio/learning project, not a certified compliance product. If you
find a rule that misrepresents or misinterprets a regulation, please
report it the same way — this is taken seriously even though it isn't a
"security vulnerability" in the traditional sense.

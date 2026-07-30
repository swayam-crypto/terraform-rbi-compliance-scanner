# Security Policy

Thank you for helping improve the security and reliability of the **Terraform RBI Compliance Scanner**.

Security reports, rule correctness issues, and false negatives are taken seriously. If you discover a vulnerability or believe the scanner incorrectly reports insecure infrastructure as compliant, please report it privately.

---

# Supported Versions

At this stage of the project, only the latest released minor version receives fixes.

| Version | Supported |
|----------|-----------|
| Latest Release | ✅ Yes |
| Older Releases | ❌ No |

Users are encouraged to upgrade to the latest release before reporting issues.

---

# Reporting a Vulnerability

Please **do not open a public GitHub issue** for security vulnerabilities.

Instead, report vulnerabilities privately using one of the following methods.

## Preferred

Use GitHub's private vulnerability reporting:

**Security → Report a Vulnerability**

or visit:

https://github.com/swayam-crypto/terraform-rbi-compliance-scanner/security/advisories/new

## Alternative

Email:

**swayamwable5@gmail.com**

---

# What to Include

Please include as much information as possible:

- Description of the issue
- Expected behavior
- Actual behavior
- Potential impact
- Steps to reproduce
- Minimal Terraform example (preferred)
- Scanner version
- Python version
- Operating system
- Affected compliance rule(s), if applicable

Providing a small Terraform configuration that reproduces the issue helps significantly reduce investigation time.

---

# Response Timeline

This project is currently maintained by a single developer.

While there is no formal Service Level Agreement (SLA), the goal is:

| Stage | Target |
|--------|--------|
| Initial acknowledgement | Within 5 days |
| Investigation | As soon as possible |
| Security fix | Depends on severity |

You will be kept informed throughout the process whenever practical.

---

# Scope

Terraform RBI Compliance Scanner performs **static analysis** of Terraform configurations.

The scanner **does not**:

- Connect to AWS
- Connect to Azure
- Connect to Google Cloud
- Require cloud credentials
- Modify infrastructure
- Deploy resources
- Execute Terraform code
- Send infrastructure data to external services

All analysis is performed locally.

---

# Privacy

The scanner is designed with privacy as a core principle.

Your Terraform configuration remains on your machine.

The project does **not**:

- Upload Terraform files
- Upload scan results
- Collect analytics
- Collect telemetry
- Track user activity

The only persistent local artifact created by the scanner is:

```
.rbi_scan_cache.json
```

This cache exists solely to improve scan performance.

---

# What Is Considered a Security Issue

Examples include:

- Scanner crashes caused by malformed input
- Arbitrary code execution
- Path traversal
- Denial-of-service vulnerabilities
- Dependency vulnerabilities
- Incorrectly reporting insecure infrastructure as compliant (false negatives)
- Leakage of Terraform configuration data
- Unexpected outbound network communication

Rule correctness issues that could lead users to believe infrastructure is compliant when it is not are considered security-relevant and should be reported privately.

---

# What Is NOT Considered a Security Issue

The following are generally **not** security vulnerabilities:

- False positives
- Missing compliance rules
- Feature requests
- Performance improvements
- Documentation improvements
- UI or formatting issues

These should be reported through GitHub Issues instead.

---

# Responsible Disclosure

Please allow reasonable time for a fix before publicly disclosing any security vulnerability.

Coordinated disclosure helps protect users of the project while a patch is being prepared.

---

# Security Design Principles

The scanner is designed around the following principles:

- Local-first analysis
- Static analysis only
- No cloud credentials required
- No outbound network communication
- Reproducible compliance findings
- Minimal data retention
- Privacy by default

---

# Regulatory Accuracy

This project encodes technical interpretations of:

- Reserve Bank of India (RBI) cybersecurity guidance
- CERT-In Cyber Security Directions
- Digital Personal Data Protection Act (DPDPA)

Although significant effort is made to ensure accuracy, this project is **not** an officially certified compliance product.

If you believe a rule misinterprets regulatory guidance, please report it using the same private disclosure process. Regulatory correctness is considered an important aspect of the project's security and reliability.

---

# Third-Party Dependencies

This project depends on several open-source Python packages.

Security updates for dependencies are applied as part of normal maintenance.

If you discover a vulnerability in one of the project's dependencies that affects this scanner, please report it.

---

# Contact

Security reports:

**swayamwable5@gmail.com**

GitHub Security Advisories are the preferred reporting channel whenever possible.

---

Thank you for helping improve the security, reliability, and regulatory accuracy of Terraform RBI Compliance Scanner.
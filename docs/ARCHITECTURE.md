# Architecture

```
Terraform files (.tf)
        |
        v
   parser/terraform_parser.py
   (HCL -> normalized Python dict)
        |
        v
   engine/scan_engine.py
   (runs every rule against every resource)
        |
        v
   rules/*.py
   (each rule checks one compliance concern)
        |
        v
   reporting/json_reporter.py
   (console output / JSON output)
        |
        v
   cli.py
   (exit code drives CI/CD pass-fail)
```

## Design decisions

**Why a plugin-style rule system?** Each rule is an independent class with
no knowledge of other rules. This means adding RBI-003 later doesn't
require touching the parser, engine, or existing rules just drop in a
new file and register it. This mirrors how Checkov and similar tools are
built, and is a deliberate choice for extensibility.

**Why heuristic tag/name matching for "sensitive data"?** Terraform
doesn't have a first-class field for "this resource holds regulated
data" real infrastructure teams communicate this through naming
conventions and tags. The rule set makes a best-effort judgment based on
that, and is intentionally conservative (skips resources it can't
confirm) to avoid excessive false positives. This is a known limitation,
documented here rather than hidden.

**Why does the CLI exit non-zero on findings?** This is what makes the
tool usable as a CI/CD gate GitHub Actions treats a non-zero exit code
as a failed step, which blocks merges automatically when `--fail-on
critical` finds a critical violation.

# Validation

Checked 4 November 2026.

Local results:

- Python 3.12: 24 tests pass, including a real temporary loopback HTTP server.
- Ruff lint and formatting checks pass.
- ShellCheck passes for the deployment and smoke wrappers.
- Terraform 1.11.2 initialisation, formatting and static validation pass.
- The locked runtime dependency audit reports no known vulnerabilities at the
  time checked. This is not a guarantee against future findings.
- Trivy secret scan completes without findings.
- The Linux-compatible ZIP builds, its checksum matches and the handler imports
  from the ZIP without development site packages.

GitHub Actions passed all four jobs on
[run 41910678271](https://github.com/Pantelovich/serverless-secure-webapp/actions/runs/41910678271),
including dependency and secret checks, Terraform validation and artifact delivery.
Cross-platform provider hashes were added after CI caught a Mac-only lockfile.
AWS deployment, live WAF
behaviour, database TLS trust and rollback have not been verified in this update.
No AWS resources were created or changed.

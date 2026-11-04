# Failure cases

These scenarios are simulated in tests. They are not employment incidents.

## The API returns HTTP 500

Confirm which endpoint, when the issue started, who is affected and recent changes.
Run the endpoint check. An HTTP 500 must fail the check, not print a success summary.
Use request times to locate the corresponding Lambda and API records.

Distinguish secret access failure from database connection failure. For a secret
problem, check IAM access and the private endpoint. For a database problem, check
the hostname, separate port, security groups and database status. A private Lambda
cannot reach a public AWS service endpoint merely because it has an IAM permission.

The handler returns a safe category to clients. It does not return internal
exception details. After the authorised fix, repeat the same request and record
the actual result. Offline tests do not substitute for that live verification.

## A bad release passes its smoke check

The previous shell script printed successful summary lines even when HTTP checks
failed. The replacement validates the status and required response fields and
returns a nonzero exit code on failure. Tests use a temporary local HTTP server
to reproduce HTTP 500 and malformed HTTP 200 responses.

Explain why a release gate must use the process exit code. A green log message
by itself is not evidence that the application is healthy.

## The artifact contains development files

Runtime dependencies are installed into temporary staging. Only the handler is
copied from the application folder. The builder excludes tests, caches and
environment files and records the ZIP checksum. A regression test inspects the ZIP.

The checksum establishes file identity. It is not a claim of artifact signing or
full supply-chain security. Keep the approved previous artifact for recovery.

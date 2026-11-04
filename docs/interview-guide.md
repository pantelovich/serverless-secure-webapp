# Explain this project

"I improved the pipeline for a small Lambda API. It runs Python tests, lint,
dependency and secret checks, and Terraform validation without AWS credentials.
Only a successful run builds the Lambda package. Cloud deployment is a separate
reviewed step."

## What did you actually fix

The smoke test could print success after a failed HTTP request. I replaced it
with a check that returns a failure exit code and tested HTTP 500 against a local
server. I also removed internal exception details from API responses and tested
database connection cleanup.

## What is CI and CD

Continuous integration checks a change automatically. Continuous delivery makes
a tested release artifact available for deployment. Continuous deployment goes
further and automatically deploys it. This project has automatic checks and
artifact delivery, with manual cloud deployment.

## Why no AWS keys in CI

Tests and static validation do not need account access. Deployment credentials
would be unnecessary privilege. A future cloud workflow should use an approved
short-lived identity such as OIDC and an explicit deployment boundary.

## How do you know it works

Explain the tests and show the CI run. A local HTTP server verifies that the
smoke command reacts correctly to success and failure. Terraform validation
checks configuration structure. It does not prove the cloud network works.
Do not claim a live deployment or rollback from these checks.

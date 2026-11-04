# Decision: credential-free CI and separate deployment

Accepted 4 November 2026.

The old workflow attempted an AWS plan for pull requests and an automatic apply
on the main branch. That mixed source checks with credentials and infrastructure
changes. The replacement uses read-only repository permissions and no AWS keys.

Python checks, a runtime dependency audit, a secret scan and Terraform validation
must pass before building a release ZIP. Actions are pinned to verified commits.
Runtime packages have version and hash locks. Tests and caches stay outside the
artifact. A checksum identifies the delivered ZIP.

Cloud deployment remains manual. This keeps infrastructure costs and account
changes outside routine source pushes. It also makes the proof boundary clear:
a successful build is not a successful live deployment or a zero downtime claim.

The original local working tree had unfinished edits. Work was isolated in a new
branch and worktree so those edits remained untouched.

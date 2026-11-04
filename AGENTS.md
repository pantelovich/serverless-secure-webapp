# Serverless API and support CI

Python 3.11, Terraform and GitHub Actions. Work in the isolated branch because
the original working tree has unfinished edits that must remain untouched.
Do not run terraform apply, destroy or any command that creates AWS resources.
Never include credentials, Terraform state, plans or built dependencies in Git.
CI must run without AWS credentials. Runtime and development dependencies stay
separate. Build artifacts must exclude tests, caches and local environment files.
Use plain British English and distinguish static validation from live deployment.
Use Ruflo routing for deliberate delegation. Small changes stay in one session.
This file also contains agents.md routing on case insensitive filesystems.

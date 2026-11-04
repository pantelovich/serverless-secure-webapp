# Context

Existing portfolio API using Lambda, RDS, API Gateway and Terraform.
Implemented credential-free CI, locked dependencies, regression tests and a
separate Linux-compatible build artifact. Fixed the smoke check's failure status
and safe API errors. Static template fixes cover private secret access, host and
port separation, reserved environment variables and explicit API stage creation.
No AWS deployment is authorised as part of this update.
The original working tree is dirty. Its edits are preserved separately.
CI success must not be presented as proof of a working live cloud environment.
Local checks pass. GitHub validation and a review PR are next.

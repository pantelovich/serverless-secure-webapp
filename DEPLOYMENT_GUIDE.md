# Controlled lab deployment

The automated workflow performs CI and artifact delivery. It does not deploy AWS
resources. The revised template has only been statically validated in this update.

## Before deployment

1. Confirm the AWS account, region, budget and permission to create the resources.
2. Review RDS, WAF, Secrets Manager and interface endpoint charges. These are not
   assumed to be free. Review current prices in the AWS calculator.
3. Configure an approved encrypted state backend with suitable access and locking.
   State and saved plans may contain the generated database credentials.
4. Decide the database TLS trust configuration. It is not demonstrated by the
   current offline tests. Do not treat this lab as a production security baseline.
5. If enabling API access logs, first configure the API Gateway CloudWatch role
   for that account and region. This shared setting is not changed by the template.
6. Check MySQL version availability in your region and review backup and deletion
   settings. The app uses PyMySQL and does not support PostgreSQL.

## Prepare and review

Activate the Python environment described in the README.

```bash
python scripts/build_lambda.py
terraform -chdir=infra init
terraform -chdir=infra plan -out=reviewed.tfplan
```

Review the plan before applying it. A missing ZIP stops planning. The deployment
script also requires an explicit APPLY response. Do not run it to test CI.

```bash
./deploy.sh
```

After an authorised deployment, run the endpoint check and inspect Lambda logs.
A failed check means the release has not been verified. Record the actual output.

## Recovery

Keep the previous approved application artifact and infrastructure commit.
Investigate whether the incident is application code, credentials, routing or a
schema change. Review the prior version's compatibility and the rollback plan.
After an approved rollback, rerun the smoke check and verify the original symptom.
No live rollback has been performed as part of this update.

## Cleanup

A lab cleanup deletes infrastructure and may delete the database. Confirm the
backup and retention requirements before reviewing a destroy plan. RDS, stored
secrets and network endpoints may continue to cost money while allocated.

## References

- [Lambda reserved environment variables](https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html)
- [Secrets Manager private endpoints](https://docs.aws.amazon.com/secretsmanager/latest/userguide/vpc-endpoint-overview.html)
- [AWS pricing calculator](https://calculator.aws/)

# 🚀 Deployment Guide

## Quick Start

1. **Prerequisites**
   ```bash
   # Install required tools
   brew install terraform awscli python3
   
   # Configure AWS credentials
   aws configure
   ```

2. **Deploy Infrastructure**
   ```bash
   # Clone and deploy
   git clone <your-repo-url>
   cd serverless-secure-webapp
   ./deploy.sh
   ```

3. **Test the API**
   ```bash
   # Get the API URL from deployment output
   curl https://<api-gateway-url>/prod/time
   ```

## Manual Deployment Steps

### 1. Infrastructure Setup
```bash
cd infra
terraform init
terraform plan
terraform apply
```

### 2. Test Deployment
```bash
cd ..
./test-api.sh <api-gateway-url>
```

### 3. Monitor Resources
- **CloudWatch Logs**: Check `/aws/lambda/serverless-secure-webapp-api`
- **WAF Metrics**: Monitor in CloudWatch under "AWS/WAFV2"
- **RDS Metrics**: Check database performance in RDS console

## Security Features Implemented

✅ **VPC Isolation**: Private subnets for RDS, public subnets for API Gateway  
✅ **WAF Protection**: OWASP Top 10 rules against SQL injection, XSS, etc.  
✅ **Secrets Manager**: Database credentials stored securely  
✅ **Least Privilege IAM**: Lambda role only has necessary permissions  
✅ **Encryption**: RDS encrypted at rest with AWS KMS  
✅ **Network Security**: Security groups restrict access  
✅ **Logging**: Comprehensive CloudWatch logging  

## Cost Optimization

- **RDS**: Uses `db.t3.micro` (free tier eligible)
- **Lambda**: Pay per request (very low cost)
- **API Gateway**: Pay per request
- **WAF**: Pay per request (first 1M requests free)
- **Secrets Manager**: $0.40 per secret per month

## Troubleshooting

### Common Issues

1. **Lambda Timeout**
   - Check VPC configuration
   - Verify security group rules
   - Check CloudWatch logs

2. **Database Connection Failed**
   - Verify RDS is in private subnet
   - Check security group allows Lambda access
   - Verify Secrets Manager permissions

3. **WAF Blocking Requests**
   - Check WAF logs in CloudWatch
   - Review WAF rules configuration
   - Test with different request patterns

### Debug Commands

```bash
# Check Lambda logs
aws logs tail /aws/lambda/serverless-secure-webapp-api --follow

# Check API Gateway logs
aws logs tail /aws/apigateway/serverless-secure-webapp-api --follow

# Test database connectivity
aws rds describe-db-instances --db-instance-identifier serverless-secure-webapp-db

# Check WAF metrics
aws wafv2 get-web-acl --scope REGIONAL --id <web-acl-id>
```

## Cleanup

To destroy all resources:
```bash
cd infra
terraform destroy
```

**⚠️ Warning**: This will permanently delete all resources including the database.

## Next Steps

1. **Add Authentication**: Integrate AWS Cognito
2. **Custom Domain**: Add Route 53 and SSL certificate
3. **CI/CD Pipeline**: Set up GitHub Actions
4. **Monitoring**: Add CloudWatch alarms
5. **API Documentation**: Add OpenAPI/Swagger
6. **Multi-Environment**: Add dev/staging/prod environments

---

**Happy Deploying! 🎉**

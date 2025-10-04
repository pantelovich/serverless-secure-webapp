# API Gateway URL
output "api_gateway_url" {
  description = "URL of the API Gateway"
  value       = "https://${aws_api_gateway_rest_api.main.id}.execute-api.${var.aws_region}.amazonaws.com/prod"
}

# API Gateway ID
output "api_gateway_id" {
  description = "ID of the API Gateway"
  value       = aws_api_gateway_rest_api.main.id
}

# Lambda Function Name
output "lambda_function_name" {
  description = "Name of the Lambda function"
  value       = aws_lambda_function.main.function_name
}

# Lambda Function ARN
output "lambda_function_arn" {
  description = "ARN of the Lambda function"
  value       = aws_lambda_function.main.arn
}

# RDS Endpoint
output "rds_endpoint" {
  description = "RDS instance endpoint"
  value       = aws_db_instance.main.endpoint
  sensitive   = true
}

# RDS Port
output "rds_port" {
  description = "RDS instance port"
  value       = aws_db_instance.main.port
}

# Secrets Manager Secret ARN
output "db_secret_arn" {
  description = "ARN of the database credentials secret"
  value       = aws_secretsmanager_secret.db_credentials.arn
  sensitive   = true
}

# VPC ID
output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

# Private Subnet IDs
output "private_subnet_ids" {
  description = "IDs of the private subnets"
  value       = aws_subnet.private[*].id
}

# Public Subnet IDs
output "public_subnet_ids" {
  description = "IDs of the public subnets"
  value       = aws_subnet.public[*].id
}

# WAF Web ACL ARN
output "waf_web_acl_arn" {
  description = "ARN of the WAF Web ACL"
  value       = aws_wafv2_web_acl.main.arn
}

# CloudWatch Log Groups
output "lambda_log_group" {
  description = "CloudWatch log group for Lambda"
  value       = aws_cloudwatch_log_group.lambda.name
}

output "api_gateway_log_group" {
  description = "CloudWatch log group for API Gateway"
  value       = aws_cloudwatch_log_group.api_gateway.name
}

# Test Command
output "test_command" {
  description = "Command to test the API"
  value       = "curl https://${aws_api_gateway_rest_api.main.id}.execute-api.${var.aws_region}.amazonaws.com/prod/time"
}

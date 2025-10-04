#!/bin/bash

# Serverless Secure Web App Deployment Script
# This script deploys the infrastructure using Terraform

set -e

echo "Starting deployment of Serverless Secure Web App..."

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "ERROR: AWS CLI is not installed. Please install it first."
    exit 1
fi

# Check if Terraform is installed
if ! command -v terraform &> /dev/null; then
    echo "ERROR: Terraform is not installed. Please install it first."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed. Please install it first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "ERROR: pip3 is not installed. Please install it first."
    exit 1
fi

# Check AWS credentials
echo "Checking AWS credentials..."
if ! aws sts get-caller-identity &> /dev/null; then
    echo "ERROR: AWS credentials not configured. Please run 'aws configure' first."
    exit 1
fi

echo "AWS credentials configured"

# Navigate to infrastructure directory
cd infra

# Initialize Terraform
echo "Initializing Terraform..."
terraform init

# Plan deployment
echo "Planning Terraform deployment..."
terraform plan -out=tfplan

# Ask for confirmation
read -p "Do you want to apply this plan? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Deployment cancelled."
    exit 1
fi

# Apply Terraform
echo "Applying Terraform configuration..."
terraform apply tfplan

# Get outputs
echo "Deployment completed! Getting outputs..."
echo ""
echo "API Gateway URL:"
terraform output api_gateway_url

echo ""
echo "Test command:"
terraform output test_command

echo ""
echo "Deployment completed successfully!"
echo ""
echo "Next steps:"
echo "1. Test the API using the test command above"
echo "2. Check CloudWatch logs for monitoring"
echo "3. Review WAF metrics in the AWS Console"
echo ""
echo "To destroy the infrastructure, run:"
echo "   cd infra && terraform destroy"

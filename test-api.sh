#!/bin/bash

# API Testing Script for Serverless Secure Web App
# This script tests the deployed API endpoints

set -e

# Function to print colored output
print_status() {
    echo "[INFO] $1"
}

print_success() {
    echo "[SUCCESS] $1"
}

print_warning() {
    echo "[WARNING] $1"
}

print_error() {
    echo "[ERROR] $1"
}

# Check if API URL is provided
if [ -z "$1" ]; then
    print_error "Please provide the API Gateway URL as the first argument"
    echo "Usage: $0 <api_gateway_url>"
    echo "Example: $0 https://abc123.execute-api.us-east-1.amazonaws.com/prod"
    exit 1
fi

API_URL="$1"
ENDPOINT="$API_URL/time"

print_status "Testing API endpoint: $ENDPOINT"

# Test 1: Basic API call
print_status "Test 1: Basic API call"
response=$(curl -s -w "\n%{http_code}" "$ENDPOINT")
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | head -n -1)

if [ "$http_code" -eq 200 ]; then
    print_success "API responded with HTTP 200"
    echo "Response body:"
    echo "$body" | jq '.' 2>/dev/null || echo "$body"
else
    print_error "API responded with HTTP $http_code"
    echo "Response body:"
    echo "$body"
fi

echo ""

# Test 2: Test with different HTTP methods
print_status "Test 2: Testing unsupported HTTP method (POST)"
response=$(curl -s -w "\n%{http_code}" -X POST "$ENDPOINT")
http_code=$(echo "$response" | tail -n1)

if [ "$http_code" -eq 405 ]; then
    print_success "API correctly rejected POST method (HTTP 405)"
else
    print_warning "API responded with HTTP $http_code for POST method"
fi

echo ""

# Test 3: Test with query parameters
print_status "Test 3: Testing with query parameters"
response=$(curl -s -w "\n%{http_code}" "$ENDPOINT?test=value")
http_code=$(echo "$response" | tail -n1)

if [ "$http_code" -eq 200 ]; then
    print_success "API handled query parameters correctly"
else
    print_warning "API responded with HTTP $http_code for query parameters"
fi

echo ""

# Test 4: Test WAF protection (XSS attempt)
print_status "Test 4: Testing WAF protection (XSS attempt)"
response=$(curl -s -w "\n%{http_code}" "$ENDPOINT?test=<script>alert('xss')</script>")
http_code=$(echo "$response" | tail -n1)

if [ "$http_code" -eq 403 ]; then
    print_success "WAF correctly blocked XSS attempt (HTTP 403)"
elif [ "$http_code" -eq 200 ]; then
    print_warning "WAF did not block XSS attempt - check WAF configuration"
else
    print_warning "API responded with HTTP $http_code for XSS test"
fi

echo ""

# Test 5: Test SQL injection attempt
print_status "Test 5: Testing WAF protection (SQL injection attempt)"
response=$(curl -s -w "\n%{http_code}" "$ENDPOINT?test=' OR '1'='1")
http_code=$(echo "$response" | tail -n1)

if [ "$http_code" -eq 403 ]; then
    print_success "WAF correctly blocked SQL injection attempt (HTTP 403)"
elif [ "$http_code" -eq 200 ]; then
    print_warning "WAF did not block SQL injection attempt - check WAF configuration"
else
    print_warning "API responded with HTTP $http_code for SQL injection test"
fi

echo ""

# Test 6: Performance test
print_status "Test 6: Performance test (5 concurrent requests)"
start_time=$(date +%s.%N)

for i in {1..5}; do
    curl -s "$ENDPOINT" > /dev/null &
done
wait

end_time=$(date +%s.%N)
duration=$(echo "$end_time - $start_time" | bc)

print_success "Completed 5 concurrent requests in ${duration}s"

echo ""
print_status "Testing completed!"

# Summary
echo ""
echo "=========================================="
echo "           TEST SUMMARY"
echo "=========================================="
echo "API Endpoint: $ENDPOINT"
echo "Test Date: $(date)"
echo ""
echo "✅ Basic functionality test"
echo "✅ HTTP method validation"
echo "✅ Query parameter handling"
echo "🛡️  WAF protection tests"
echo "⚡ Performance test"
echo ""
echo "Check the results above for any issues."

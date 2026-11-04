#!/usr/bin/env bash
set -euo pipefail

project_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
for tool in aws terraform python3; do
    command -v "$tool" >/dev/null 2>&1 || { echo "Missing required tool: $tool" >&2; exit 1; }
done
aws sts get-caller-identity >/dev/null
python3 "$project_dir/scripts/build_lambda.py"
terraform -chdir="$project_dir/infra" init
terraform -chdir="$project_dir/infra" plan -out=reviewed.tfplan
read -r -p "Review the plan and costs. Type APPLY to create or change AWS resources: " answer
if [[ "$answer" != "APPLY" ]]; then
    echo "Deployment cancelled."
    exit 0
fi
terraform -chdir="$project_dir/infra" apply reviewed.tfplan
api_url="$(terraform -chdir="$project_dir/infra" output -raw api_gateway_url)"
python3 "$project_dir/scripts/check_endpoint.py" "$api_url"

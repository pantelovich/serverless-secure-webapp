#!/usr/bin/env bash
set -euo pipefail

project_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if [[ $# -ne 1 ]]; then
    echo "Usage: ./test-api.sh API_BASE_URL" >&2
    exit 2
fi
command -v python3 >/dev/null 2>&1 || { echo "Python 3 is required." >&2; exit 1; }
exec python3 "$project_dir/scripts/check_endpoint.py" "$1"

"""Fail a smoke check when the endpoint does not return a valid time response."""

import json
import sys
from datetime import datetime
from urllib.error import URLError
from urllib.parse import urlsplit
from urllib.request import urlopen


def check_endpoint(base_url: str) -> None:
    """Read one authorised endpoint, with a timeout and response checks."""
    parsed = urlsplit(base_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("Provide an HTTP or HTTPS API base URL.")
    if parsed.query or parsed.fragment or parsed.username or parsed.password:
        raise ValueError("Provide a base URL without credentials, query or fragment.")
    with urlopen(f"{base_url.rstrip('/')}/time", timeout=15) as response:
        if response.status != 200:
            raise ValueError(f"Expected HTTP 200, received {response.status}.")
        data = json.load(response)
    if (
        not isinstance(data, dict)
        or not isinstance(data.get("time"), str)
        or not data["time"]
        or not isinstance(data.get("timestamp"), str)
        or not data["timestamp"]
    ):
        raise ValueError("The response has no database time and timestamp.")
    if datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00")).tzinfo is None:
        raise ValueError("The timestamp must include its timezone.")


def main() -> int:
    """Expose a command with meaningful success and failure exit codes."""
    if len(sys.argv) != 2:
        print("Usage: python scripts/check_endpoint.py API_BASE_URL", file=sys.stderr)
        return 2
    try:
        check_endpoint(sys.argv[1])
    except (URLError, ValueError, TypeError, TimeoutError) as error:
        print(f"Endpoint check failed: {type(error).__name__}", file=sys.stderr)
        return 1
    print("Endpoint returned HTTP 200 with a database time and timezone-aware timestamp.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

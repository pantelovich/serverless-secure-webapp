"""Exercise the smoke command against a real local HTTP server and inspect ZIPs."""

import hashlib
import json
import threading
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, HTTPServer
from zipfile import ZipFile

import pytest

from scripts import check_endpoint
from scripts.build_lambda import build_archive


@contextmanager
def serve_response(status, payload):
    """Serve one fixed fictional API response on loopback."""

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(payload).encode())

        def log_message(self, *_args):
            return None

    with HTTPServer(("127.0.0.1", 0), Handler) as server:
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            yield f"http://127.0.0.1:{server.server_port}"
        finally:
            server.shutdown()
            thread.join(timeout=5)


@pytest.mark.parametrize(
    ("status", "payload", "expected"),
    [
        (200, {"time": "2026-11-04 12:00:00", "timestamp": "2026-11-04T12:00:00Z"}, 0),
        (500, {"error": "Simulated database failure"}, 1),
        (200, {"error": "Invalid success body"}, 1),
        (200, {"time": "value", "timestamp": "2026-11-04T12:00:00"}, 1),
    ],
)
def test_smoke_command_exit_code(status, payload, expected, monkeypatch):
    with serve_response(status, payload) as url:
        monkeypatch.setattr("sys.argv", ["check_endpoint.py", url])
        assert check_endpoint.main() == expected


@pytest.mark.parametrize(
    "url",
    [
        "file:///tmp/example",
        "https://user:password@example.test",
        "https://example.test?token=value",
    ],
)
def test_smoke_rejects_non_endpoint_input(url):
    with pytest.raises(ValueError):
        check_endpoint.check_endpoint(url)


def test_build_excludes_tests_caches_and_environment_files(tmp_path):
    staging = tmp_path / "staging"
    staging.mkdir()
    (staging / "app.py").write_text("def handler(event, context): return {}\n")
    (staging / "dependency.py").write_text("VALUE = 1\n")
    (staging / "test_app.py").write_text("fixture")
    (staging / ".env").write_text("fixture")
    (staging / "__pycache__").mkdir()
    (staging / "__pycache__/app.pyc").write_bytes(b"fixture")
    output = tmp_path / "build/lambda.zip"
    digest = build_archive(staging, output)
    with ZipFile(output) as archive:
        assert set(archive.namelist()) == {"app.py", "dependency.py"}
    assert digest == hashlib.sha256(output.read_bytes()).hexdigest()
    assert output.with_suffix(".zip.sha256").read_text() == f"{digest}  lambda.zip\n"


def test_build_requires_the_handler(tmp_path):
    with pytest.raises(ValueError, match="app.py"):
        build_archive(tmp_path, tmp_path / "lambda.zip")

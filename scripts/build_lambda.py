"""Build a Linux-compatible Lambda artifact without modifying source folders."""

import hashlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]


def build_archive(staging: Path, output: Path) -> str:
    """Archive prepared staging and write a SHA256 companion file."""
    if not (staging / "app.py").is_file():
        raise ValueError("The staging directory has no app.py handler.")
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "w", compression=ZIP_DEFLATED) as archive:
        for path in sorted(staging.rglob("*")):
            relative = path.relative_to(staging)
            if not path.is_file() or path.is_symlink():
                continue
            if any(part in {"__pycache__", "tests"} for part in relative.parts):
                continue
            if path.name.startswith(("test_", ".env")) or path.suffix == ".pyc":
                continue
            archive.write(path, relative.as_posix())
    with output.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    output.with_suffix(".zip.sha256").write_text(f"{digest}  {output.name}\n")
    return digest


def main() -> None:
    """Install only pinned runtime wheels into temporary staging, then package."""
    with tempfile.TemporaryDirectory(prefix="lambda-build-") as temporary:
        staging = Path(temporary)
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--require-hashes",
                "--no-compile",
                "--only-binary=:all:",
                "--platform",
                "manylinux2014_x86_64",
                "--python-version",
                "3.12",
                "--implementation",
                "cp",
                "--requirement",
                str(ROOT / "lambda/requirements.txt"),
                "--target",
                str(staging),
            ],
            check=True,
        )
        shutil.copy2(ROOT / "lambda/app.py", staging / "app.py")
        output = ROOT / "build/lambda.zip"
        digest = build_archive(staging, output)
        print(f"Built {output.name}. SHA256: {digest}")


if __name__ == "__main__":
    main()

"""Mirror this repository's model tree to the Hugging Face Hub.

Run from the repo root by .github/workflows/publish-huggingface.yml. Uploads
every file except the git and CI plumbing, keeping the directory layout, so a
consumer only has to swap the base URL:

    https://media.githubusercontent.com/media/<owner>/<repo>/main/<path>
    https://huggingface.co/<hf_repo>/resolve/main/<path>

The repository's LFS budget is exhausted, so `git lfs fetch` is refused and a
checkout yields pointer files. The media host still serves the objects, so the
payload is pulled from there instead. Each pointer carries its object's sha256
and size, which turns it into a manifest: every download is verified against it
before anything is uploaded.

README.md is uploaded with a Hugging Face model card header prepended; the copy
in git is left alone.
"""

import hashlib
import os
import re
import shutil
import sys
import tempfile
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from huggingface_hub import HfApi

MEDIA_BASE = "https://media.githubusercontent.com/media/{repo}/{ref}/{path}"
POINTER_PREFIX = b"version https://git-lfs"
POINTER_MAX_BYTES = 1024
DOWNLOAD_RETRIES = 3

# Hugging Face renders this front matter as the model card header. The body is
# the repository README, appended verbatim.
CARD_HEADER = """---
license: apache-2.0
library_name: onnx
pipeline_tag: image-to-text
tags:
  - ocr
  - paddleocr
  - onnx
  - onnxruntime
  - text-detection
  - text-recognition
---

"""


def read_pointer(path: Path):
    """Return (sha256, size) if this file is an LFS pointer, else None."""
    if path.stat().st_size > POINTER_MAX_BYTES:
        return None
    blob = path.read_bytes()
    if not blob.startswith(POINTER_PREFIX):
        return None
    text = blob.decode("utf-8")
    oid = re.search(r"^oid sha256:([0-9a-f]{64})$", text, re.M)
    size = re.search(r"^size (\d+)$", text, re.M)
    if not oid or not size:
        raise ValueError(f"{path}: malformed LFS pointer")
    return oid.group(1), int(size.group(1))


def fetch(url: str, dest: Path, oid: str, size: int) -> None:
    """Download to dest, verifying sha256 and length. Raises on mismatch."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    last = None
    for attempt in range(1, DOWNLOAD_RETRIES + 1):
        try:
            digest = hashlib.sha256()
            written = 0
            with urllib.request.urlopen(url, timeout=120) as response, dest.open("wb") as out:
                while chunk := response.read(1 << 20):
                    digest.update(chunk)
                    written += len(chunk)
                    out.write(chunk)
            if written != size:
                raise ValueError(f"expected {size} bytes, got {written}")
            if digest.hexdigest() != oid:
                raise ValueError(f"sha256 {digest.hexdigest()} != {oid}")
            return
        except Exception as error:  # noqa: BLE001 - retried, then re-raised
            last = error
            print(f"  retry {attempt}/{DOWNLOAD_RETRIES} {dest.name}: {error}", flush=True)
    raise RuntimeError(f"{dest.name}: {last}")


def stage(root: Path, staging: Path, source_repo: str, ref: str):
    """Copy the tree into staging, replacing pointers with the real objects."""
    pointers = []
    plain = 0

    for path in sorted(root.rglob("*")):
        if not path.is_file() or ".git" in path.parts or ".github" in path.parts:
            continue
        relative = path.relative_to(root)
        target = staging / relative
        pointer = read_pointer(path)
        if pointer:
            oid, size = pointer
            pointers.append((relative, target, oid, size))
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
            plain += 1

    total = sum(size for _, _, _, size in pointers)
    print(f"{plain} plain files, {len(pointers)} LFS objects ({total / 1e6:.1f} MB) to fetch", flush=True)

    def one(item) -> None:
        relative, target, oid, size = item
        fetch(MEDIA_BASE.format(repo=source_repo, ref=ref, path=relative), target, oid, size)
        print(f"  ok {size / 1e6:8.1f} MB  {relative}", flush=True)

    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(one, pointers))

    return plain + len(pointers), total


def main() -> int:
    token = os.environ.get("HF_TOKEN")
    repo_id = os.environ.get("HF_REPO")
    source_repo = os.environ.get("GITHUB_REPOSITORY", "")
    ref = os.environ.get("SOURCE_REF", "main")
    dry_run = os.environ.get("DRY_RUN", "false").lower() == "true"

    if not repo_id:
        print("HF_REPO is not set", file=sys.stderr)
        return 1
    if not source_repo:
        print("GITHUB_REPOSITORY is not set", file=sys.stderr)
        return 1
    if not token and not dry_run:
        print("HF_TOKEN is not set", file=sys.stderr)
        return 1

    root = Path.cwd()
    staging = Path(tempfile.mkdtemp()) / "payload"
    count, fetched = stage(root, staging, source_repo, ref)
    print(f"staged {count} files, {fetched / 1e6:.1f} MB fetched and verified")

    if dry_run:
        return 0

    card = staging / "README.md"
    card.write_text(CARD_HEADER + (root / "README.md").read_text(encoding="utf-8"), encoding="utf-8")

    api = HfApi(token=token)
    api.create_repo(repo_id, repo_type="model", exist_ok=True)
    api.upload_folder(
        folder_path=str(staging),
        repo_id=repo_id,
        repo_type="model",
        commit_message="Mirror model tree from GitHub",
    )

    remote = set(api.list_repo_files(repo_id, repo_type="model"))
    missing = [
        str(p.relative_to(staging))
        for p in staging.rglob("*")
        if p.is_file() and str(p.relative_to(staging)) not in remote
    ]
    if missing:
        print("Files missing on the Hub after upload:", file=sys.stderr)
        for path in missing:
            print(f"  {path}", file=sys.stderr)
        return 1

    print(f"{len(remote)} files on the Hub")
    print(f"https://huggingface.co/{repo_id}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

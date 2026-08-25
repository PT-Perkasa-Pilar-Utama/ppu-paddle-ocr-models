"""Mirror this repository's model tree to the Hugging Face Hub.

Run from the repo root by .github/workflows/publish-huggingface.yml. Uploads
every file except the git and CI plumbing, keeping the directory layout, so a
consumer only has to swap the base URL:

    https://media.githubusercontent.com/media/<owner>/<repo>/main/<path>
    https://huggingface.co/<hf_repo>/resolve/main/<path>

README.md is uploaded with a Hugging Face model card header prepended; the copy
in git is left alone.
"""

import os
import sys
import tempfile
from pathlib import Path

from huggingface_hub import HfApi

IGNORE = [".git*", ".github/*"]

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


def main() -> int:
    token = os.environ.get("HF_TOKEN")
    repo_id = os.environ.get("HF_REPO")
    dry_run = os.environ.get("DRY_RUN", "false").lower() == "true"

    if not repo_id:
        print("HF_REPO is not set", file=sys.stderr)
        return 1
    if not token and not dry_run:
        print("HF_TOKEN is not set", file=sys.stderr)
        return 1

    root = Path.cwd()
    payload = sorted(
        p
        for p in root.rglob("*")
        if p.is_file()
        and ".git" not in p.parts
        and ".github" not in p.parts
    )
    total = sum(p.stat().st_size for p in payload)
    print(f"{len(payload)} files, {total / 1e6:.1f} MB")

    if dry_run:
        for p in payload:
            print(f"  {p.stat().st_size / 1e6:8.1f} MB  {p.relative_to(root)}")

    # An LFS pointer is a ~130 byte text file. If one survived the checkout the
    # upload would silently publish pointers instead of models.
    pointers = [
        p
        for p in payload
        if p.suffix in {".onnx", ".ort"}
        and p.stat().st_size < 1024
        and p.read_bytes().startswith(b"version https://git-lfs")
    ]
    if pointers:
        print("LFS pointers not resolved by the checkout:", file=sys.stderr)
        for p in pointers:
            print(f"  {p.relative_to(root)}", file=sys.stderr)
        return 1

    if dry_run:
        return 0

    card = Path(tempfile.mkdtemp()) / "README.md"
    card.write_text(CARD_HEADER + (root / "README.md").read_text(encoding="utf-8"), encoding="utf-8")

    api = HfApi(token=token)
    api.create_repo(repo_id, repo_type="model", exist_ok=True)
    api.upload_folder(
        folder_path=str(root),
        repo_id=repo_id,
        repo_type="model",
        ignore_patterns=IGNORE + ["README.md"],
        commit_message="Mirror model tree from GitHub",
    )
    api.upload_file(
        path_or_fileobj=str(card),
        path_in_repo="README.md",
        repo_id=repo_id,
        repo_type="model",
        commit_message="Update model card",
    )

    remote = set(api.list_repo_files(repo_id, repo_type="model"))
    missing = [
        str(p.relative_to(root)) for p in payload if str(p.relative_to(root)) not in remote
    ]
    if missing:
        print("Files missing on the Hub after upload:", file=sys.stderr)
        for m in missing:
            print(f"  {m}", file=sys.stderr)
        return 1
    print(f"{len(remote)} files on the Hub")
    print(f"https://huggingface.co/{repo_id}")
    return 0

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlparse


def die(message: str, code: int = 1) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(code)


def parse_github_url(raw: str) -> tuple[str, str | None, str]:
    raw = raw.strip()
    if not raw:
        die("missing GitHub URL")

    parsed = urlparse(raw)
    if parsed.scheme not in {"https", "http"} or parsed.netloc != "github.com":
        die("expected a GitHub HTTPS URL like https://github.com/owner/repo")

    parts = [p for p in parsed.path.split("/") if p]
    if len(parts) < 2:
        die("expected a GitHub repository URL")

    owner, repo = parts[0], parts[1]
    repo = repo.removesuffix(".git")

    branch: str | None = None
    subpath = ""

    if len(parts) >= 4 and parts[2] in {"tree", "blob"}:
        branch = parts[3]
        subpath = "/".join(parts[4:])
        if parts[2] == "blob" and subpath:
            subpath = str(Path(subpath).parent)

    repo_url = f"https://github.com/{owner}/{repo}.git"
    return repo_url, branch, subpath


def find_skill_dir(repo_root: Path, subpath: str) -> Path:
    if subpath:
        candidate = repo_root / subpath
        if (candidate / "SKILL.md").is_file():
            return candidate
        if candidate.name == "SKILL.md" and candidate.parent.is_dir():
            return candidate.parent

    if (repo_root / "SKILL.md").is_file():
        return repo_root

    found = [p.parent for p in repo_root.rglob("SKILL.md")]
    unique: list[Path] = []
    seen: set[str] = set()
    for path in found:
        key = str(path.resolve())
        if key not in seen:
            seen.add(key)
            unique.append(path)

    if not unique:
        die("no SKILL.md found in the repository")
    if len(unique) > 1:
        candidates = "\n".join(f"- {p.relative_to(repo_root)}" for p in unique)
        die(
            "multiple skills found; provide a GitHub tree URL to the exact skill directory\n"
            f"found:\n{candidates}"
        )
    return unique[0]


def read_skill_name(skill_md: Path) -> str:
    text = skill_md.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        die(f"{skill_md} is missing YAML frontmatter")

    frontmatter = match.group(1)
    name_match = re.search(r"^name:\s*([\w-]+)\s*$", frontmatter, re.M)
    if not name_match:
        die(f"{skill_md} is missing a valid name in frontmatter")

    return name_match.group(1)


def main() -> None:
    if len(sys.argv) != 2:
        die("usage: install-skill.py <github-url>")

    repo_url, branch, subpath = parse_github_url(sys.argv[1])

    with tempfile.TemporaryDirectory(prefix="pi-skill-") as tmp:
        clone_dir = Path(tmp) / "repo"
        cmd = ["git", "clone", "--depth", "1"]
        if branch:
            cmd += ["--branch", branch]
        cmd += [repo_url, str(clone_dir)]

        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as exc:
            die(f"git clone failed with exit code {exc.returncode}")

        skill_dir = find_skill_dir(clone_dir, subpath)
        skill_md = skill_dir / "SKILL.md"
        skill_name = read_skill_name(skill_md)

        target_root = Path(__file__).resolve().parents[2]
        target = target_root / skill_name
        target_root.mkdir(parents=True, exist_ok=True)

        if target.exists():
            shutil.rmtree(target)

        shutil.copytree(skill_dir, target)

        print(f"Installed {skill_name} to {target}")


if __name__ == "__main__":
    main()

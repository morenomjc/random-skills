#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
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


def expand(path: str) -> Path:
    return Path(os.path.expanduser(path)).resolve()


def build_targets() -> dict[str, tuple[str, Path]]:
    cwd = Path.cwd().resolve()
    home = Path.home().resolve()
    return {
        "pi-project": ("Pi (project)", cwd / ".pi" / "skills"),
        "pi-global": ("Pi (global)", home / ".pi" / "agent" / "skills"),
        "claude-global": ("Claude Code (global)", home / ".claude" / "skills"),
        "claude-project": ("Claude Code (project)", cwd / ".claude" / "skills"),
        "codex-global": ("OpenAI Codex (global)", home / ".codex" / "skills"),
        "codex-project": ("OpenAI Codex (project)", cwd / ".codex" / "skills"),
        "agents-global": ("Agent Skills generic (global)", home / ".agents" / "skills"),
        "agents-project": ("Agent Skills generic (project)", cwd / ".agents" / "skills"),
    }


def pick_target(target_key: str | None, custom_path: str | None, yes: bool) -> Path:
    if custom_path:
        return expand(custom_path)

    targets = build_targets()

    if target_key:
        if target_key not in targets:
            valid = ", ".join(sorted(targets.keys()))
            die(f"unknown --target '{target_key}'. valid: {valid}")
        return targets[target_key][1]

    if yes:
        return targets["pi-project"][1]

    items = list(targets.items())
    print("Select install target:")
    for i, (_, (label, path)) in enumerate(items, start=1):
        print(f"  {i}. {label}: {path}")
    print(f"  {len(items) + 1}. Custom path")

    raw = input("Enter number [1]: ").strip() or "1"
    if not raw.isdigit():
        die("invalid selection")

    idx = int(raw)
    if idx == len(items) + 1:
        custom = input("Enter absolute or ~ path: ").strip()
        if not custom:
            die("custom path is required")
        return expand(custom)

    if idx < 1 or idx > len(items):
        die("selection out of range")

    return items[idx - 1][1][1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install Agent Skills from GitHub")
    parser.add_argument("github_url", help="GitHub repo/tree/blob URL")
    parser.add_argument(
        "--target",
        help=(
            "Target key (pi-project, pi-global, claude-global, claude-project, "
            "codex-global, codex-project, agents-global, agents-project)"
        ),
    )
    parser.add_argument("--path", help="Custom install directory (overrides --target)")
    parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="Non-interactive mode. If no --target/--path provided, defaults to pi-project.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    repo_url, branch, subpath = parse_github_url(args.github_url)
    target_root = pick_target(args.target, args.path, args.yes)

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

        target = target_root / skill_name
        target_root.mkdir(parents=True, exist_ok=True)

        if target.exists():
            shutil.rmtree(target)

        shutil.copytree(skill_dir, target)

        print(f"Installed {skill_name} to {target}")


if __name__ == "__main__":
    main()

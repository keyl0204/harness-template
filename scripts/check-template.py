#!/usr/bin/env python3
"""Generate representative Copier outputs and verify Harness wiring."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / ".tmp-template-check-source"
OUTPUT_ROOT = ROOT / ".tmp-template-check"
UV_CACHE = ROOT / ".tmp-template-check-uv-cache"
UV_TOOL_DIR = ROOT / ".tmp-template-check-uv-tools"


def run(command: list[str], cwd: Path = ROOT, expect_success: bool = True) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["UV_CACHE_DIR"] = str(UV_CACHE)
    env["UV_TOOL_DIR"] = str(UV_TOOL_DIR)
    result = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    if expect_success and result.returncode != 0:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        raise SystemExit(f"Command failed: {' '.join(command)}")
    if not expect_success and result.returncode == 0:
        raise SystemExit(f"Command unexpectedly succeeded: {' '.join(command)}")
    return result


def clean(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)


def copy_template_source() -> None:
    clean(SOURCE)

    def ignore(_dir: str, names: list[str]) -> set[str]:
        ignored = {".git", "__pycache__", ".pytest_cache", ".ruff_cache"}
        ignored.update(name for name in names if name.startswith(".tmp-"))
        return ignored

    shutil.copytree(ROOT, SOURCE, ignore=ignore)


def copy_case(name: str, values: dict[str, str]) -> Path:
    target = OUTPUT_ROOT / name
    clean(target)
    command = ["uvx", "copier", "copy", "--trust", "--defaults", "--force"]
    for key, value in values.items():
        command.extend(["-d", f"{key}={value}"])
    command.extend([str(SOURCE), str(target)])
    run(command)
    return target


def assert_exists(path: Path) -> None:
    if not path.exists():
        raise SystemExit(f"Expected path to exist: {path}")


def assert_missing(path: Path) -> None:
    if path.exists():
        raise SystemExit(f"Expected path to be absent: {path}")


def harness_check(target: Path) -> None:
    run([sys.executable, "-B", ".harness/scripts/harness-check.py"], cwd=target)


def check_valid_cases() -> None:
    fastapi = copy_case(
        "fastapi-uv",
        {"project_name": "check-fastapi", "project_type": "fastapi", "package_manager": "uv"},
    )
    harness_check(fastapi)
    assert_exists(fastapi / "pyproject.toml")
    assert_exists(fastapi / "src" / "main.py")
    assert_missing(fastapi / "package.json")

    no_switches = copy_case(
        "no-switches",
        {
            "project_name": "check-no-switches",
            "project_type": "fastapi",
            "package_manager": "uv",
            "use_subagents": "false",
            "use_skills": "false",
            "use_security_rules": "false",
        },
    )
    harness_check(no_switches)
    assert_missing(no_switches / ".harness" / "agents")
    assert_missing(no_switches / ".harness" / "skills")
    assert_missing(no_switches / ".harness" / "rules" / "security-rules.md")
    assert_missing(no_switches / ".harness" / "workflows" / "security-fix.md")

    react = copy_case(
        "react-pnpm",
        {
            "project_name": "check-react",
            "project_type": "react",
            "package_manager": "none",
            "frontend_package_manager": "pnpm",
            "use_ci": "true",
            "use_docker": "true",
        },
    )
    harness_check(react)
    assert_exists(react / "package.json")
    assert_exists(react / "src" / "main.tsx")
    assert_exists(react / ".github" / "workflows" / "ci.yml")
    assert_exists(react / "docker" / "Dockerfile")
    assert_missing(react / "pyproject.toml")
    assert_missing(react / "src" / "main.py")
    package_json = json.loads((react / "package.json").read_text(encoding="utf-8"))
    if package_json.get("packageManager") != "pnpm@10.0.0":
        raise SystemExit("React package.json missing expected packageManager")
    ci_text = (react / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    if "actions/setup-python@v5" not in ci_text:
        raise SystemExit("React CI must set up Python for harness-check")


def check_invalid_cases() -> None:
    invalid_backend = [
        "uvx",
        "copier",
        "copy",
        "--trust",
        "--defaults",
        "--force",
        "-d",
        "project_name=invalid-backend",
        "-d",
        "project_type=fastapi",
        "-d",
        "package_manager=none",
        str(SOURCE),
        str(OUTPUT_ROOT / "invalid-backend"),
    ]
    run(invalid_backend, expect_success=False)

    invalid_react = [
        "uvx",
        "copier",
        "copy",
        "--trust",
        "--defaults",
        "--force",
        "-d",
        "project_name=invalid-react",
        "-d",
        "project_type=react",
        "-d",
        "frontend_package_manager=none",
        str(SOURCE),
        str(OUTPUT_ROOT / "invalid-react"),
    ]
    run(invalid_react, expect_success=False)


def main() -> int:
    clean(OUTPUT_ROOT)
    clean(UV_CACHE)
    clean(UV_TOOL_DIR)
    copy_template_source()
    try:
        check_valid_cases()
        check_invalid_cases()
    finally:
        clean(SOURCE)
        clean(OUTPUT_ROOT)
        clean(UV_CACHE)
        clean(UV_TOOL_DIR)
    print("template-check OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())

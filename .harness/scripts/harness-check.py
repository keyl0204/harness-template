#!/usr/bin/env python3
"""Validate generated Harness wiring without third-party dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path.cwd()
HARNESS = ROOT / ".harness"
SOURCE_LIMIT = 800
SOURCE_SUFFIXES = {".py", ".js", ".jsx", ".ts", ".tsx"}


def fail(message: str) -> None:
    print(f"[harness-check] ERROR: {message}")
    raise SystemExit(1)


def warn(message: str) -> None:
    print(f"[harness-check] WARN: {message}")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def frontmatter(path: Path) -> dict[str, str]:
    text = read_text(path)
    if not text.startswith("---\n"):
        fail(f"{path} 缺少 YAML frontmatter")
    end = text.find("\n---", 4)
    if end == -1:
        fail(f"{path} frontmatter 未闭合")

    metadata: dict[str, str] = {}
    for raw_line in text[4:end].splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"').strip("'")
    return metadata


def parse_model_profiles() -> set[str]:
    config = HARNESS / "config" / "models.yml"
    if not config.exists():
        return set()

    profiles: set[str] = set()
    in_profiles = False
    for raw_line in read_text(config).splitlines():
        if raw_line.strip() == "profiles:":
            in_profiles = True
            continue
        if in_profiles and raw_line and not raw_line.startswith(" "):
            break
        match = re.match(r"^  ([A-Za-z0-9_-]+):\s*$", raw_line)
        if in_profiles and match:
            profiles.add(match.group(1))
    return profiles


def check_required_files() -> None:
    required = [
        HARNESS / "rules",
        HARNESS / "workflows",
        HARNESS / "state",
        ROOT / "AGENTS.md",
        ROOT / "Makefile",
    ]
    for path in required:
        if not path.exists():
            fail(f"必需文件或目录不存在: {path}")


def check_agents() -> None:
    agents_dir = HARNESS / "agents"
    if not agents_dir.exists():
        return

    profiles = parse_model_profiles()
    for path in sorted(agents_dir.glob("*.md")):
        metadata = frontmatter(path)
        for key in ("agent_type", "reasoning_effort", "specialization"):
            if not metadata.get(key):
                fail(f"{path} 缺少 agent 元数据: {key}")

        profile = metadata.get("model_profile")
        model = metadata.get("model")
        if not profile and not model:
            fail(f"{path} 必须配置 model_profile 或 model")
        if profile and not profiles:
            fail(f"{path} 使用 model_profile={profile}，但缺少 .harness/config/models.yml")
        if profile and profile not in profiles:
            fail(f"{path} 使用未知 model_profile: {profile}")


def check_skills() -> None:
    skills_dir = HARNESS / "skills"
    if not skills_dir.exists():
        return

    for path in sorted(skills_dir.glob("*/SKILL.md")):
        metadata = frontmatter(path)
        for key in ("name", "description"):
            if not metadata.get(key):
                fail(f"{path} 缺少 skill 元数据: {key}")


def check_feature_state() -> None:
    feature_list = HARNESS / "state" / "feature_list.json"
    if not feature_list.exists():
        return
    try:
        json.loads(read_text(feature_list))
    except json.JSONDecodeError as exc:
        fail(f"{feature_list} 不是合法 JSON: {exc}")


def referenced_harness_paths(text: str) -> set[str]:
    pattern = re.compile(r"`(\.harness/[^`]+)`|(?<![\w./-])(\.harness/[A-Za-z0-9_./*-]+)")
    refs: set[str] = set()
    for match in pattern.finditer(text):
        raw = match.group(1) or match.group(2)
        if "*" in raw:
            continue
        refs.add(raw.rstrip(".,，。；;:：)）"))
    return refs


def check_harness_references() -> None:
    markdown_files = list(HARNESS.rglob("*.md")) + [ROOT / "AGENTS.md"]
    for path in sorted(p for p in markdown_files if p.exists()):
        for ref in referenced_harness_paths(read_text(path)):
            target = ROOT / ref
            if not target.exists():
                fail(f"{path} 引用了不存在的 Harness 路径: {ref}")


def check_source_line_limits() -> None:
    src = ROOT / "src"
    if not src.exists():
        return
    for path in sorted(p for p in src.rglob("*") if p.is_file() and p.suffix in SOURCE_SUFFIXES):
        line_count = len(read_text(path).splitlines())
        if line_count > SOURCE_LIMIT:
            fail(f"{path} 有 {line_count} 行，超过业务源码文件上限 {SOURCE_LIMIT} 行")


def main() -> int:
    if not HARNESS.exists():
        warn("未找到 .harness 目录，跳过 Harness 自检")
        return 0

    check_required_files()
    check_agents()
    check_skills()
    check_feature_state()
    check_harness_references()
    check_source_line_limits()
    print("[harness-check] OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())

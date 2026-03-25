"""uSkills Indexer Module.

This module provides functionality to build skill indexes
from directories of uSkill files, generating markdown documentation
for skill catalogs.
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any

from .validator import load_skill


def _anchor(value: str) -> str:
    """Convert string to markdown anchor.

    Args:
        value: Input string.

    Returns:
        URL-safe anchor string.
    """
    lowered = value.strip().lower()
    chars: list[str] = []
    for char in lowered:
        if char.isalnum() or "\u4e00" <= char <= "\u9fff":
            chars.append(char)
        elif char in {"-", " ", "_"}:
            chars.append("-")
    return "".join(chars).strip("-") or "section"


def _format_skill_entry(skill_data: dict[str, Any]) -> str:
    """Format a single skill entry for markdown table.

    Args:
        skill_data: Skill data dictionary.

    Returns:
        Formatted markdown table row.
    """
    return (
        f"| `{skill_data['skill_id']}` | {skill_data['name']} | "
        f"{skill_data['category']} | {skill_data['domain']} | "
        f"{skill_data['version']} |"
    )


def build_skills_index(skills_dir: str | Path, output_path: str | Path) -> Path:
    """Build markdown skills index from skill directory.

    Scans directory for YAML skill files, groups by source SOP,
    and generates a markdown index file.

    Args:
        skills_dir: Directory containing skill files.
        output_path: Output path for generated index.

    Returns:
        Path to generated index file.
    """
    root = Path(skills_dir)
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    errors: list[str] = []

    for path in sorted(root.rglob("*.yaml")):
        try:
            skill = load_skill(path)
            grouped[skill.source.sop_name].append(
                {
                    "skill_id": skill.skill_id,
                    "name": skill.meta.name,
                    "category": skill.meta.category.value,
                    "domain": skill.meta.domain,
                    "version": skill.meta.version,
                }
            )
        except Exception as e:
            errors.append(f"Error loading {path}: {e}")

    total_groups = len(grouped)
    total_skills = sum(len(items) for items in grouped.values())

    # Build markdown content
    entries: list[str] = [
        "# 技能仓库",
        "",
        f"共收录 **{total_skills}** 个技能，来源于 **{total_groups}** 个 SOP / 技能源。",
        "",
    ]

    # Add error summary if any
    if errors:
        entries.extend(
            [
                '!!! warning "加载警告"',
                "",
                f"    {len(errors)} 个技能文件加载失败，请检查格式。",
                "",
            ]
        )

    # Add category statistics
    category_stats: dict[str, int] = defaultdict(int)
    for items in grouped.values():
        for item in items:
            category_stats[item["category"]] += 1

    entries.extend(["## 分类统计", ""])

    for category, count in sorted(category_stats.items()):
        entries.append(f"- **{category}**: {count} 个技能")

    entries.extend(["", "## 分类导览", ""])

    # Add table of contents
    for source_name, items in sorted(grouped.items()):
        anchor = _anchor(source_name)
        entries.append(f"- [{source_name}](#{anchor}) ({len(items)} 个技能)")

    # Add detailed sections
    for source_name, items in sorted(grouped.items()):
        entries.extend(
            [
                "",
                f"## {source_name}",
                "",
                f"技能数：**{len(items)}**",
                "",
                "| Skill ID | Name | Category | Domain | Version |",
                "| --- | --- | --- | --- | --- |",
            ]
        )
        for item in items:
            entries.append(_format_skill_entry(item))

    # Write output
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    content = "\n".join(entries) + "\n"
    target.write_text(content, encoding="utf-8")

    return target


def get_skill_stats(skills_dir: str | Path) -> dict[str, Any]:
    """Get statistics about skills in directory.

    Args:
        skills_dir: Directory containing skill files.

    Returns:
        Dictionary with skill statistics.
    """
    root = Path(skills_dir)
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for path in sorted(root.rglob("*.yaml")):
        try:
            skill = load_skill(path)
            grouped[skill.source.sop_name].append(
                {
                    "skill_id": skill.skill_id,
                    "category": skill.meta.category.value,
                }
            )
        except Exception:
            continue

    total_skills = sum(len(items) for items in grouped.values())
    category_stats: dict[str, int] = defaultdict(int)
    for items in grouped.values():
        for item in items:
            category_stats[item["category"]] += 1

    return {
        "total_skills": total_skills,
        "total_sources": len(grouped),
        "categories": dict(category_stats),
    }

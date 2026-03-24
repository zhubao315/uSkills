from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any

from .validator import load_skill


def build_skills_index(skills_dir: str | Path, output_path: str | Path) -> Path:
    root = Path(skills_dir)
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for path in sorted(root.rglob("*.yaml")):
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

    total_groups = len(grouped)
    total_skills = sum(len(items) for items in grouped.values())

    entries: list[str] = [
        "# 技能仓库",
        "",
        f"共收录 **{total_skills}** 个技能，来源于 **{total_groups}** 个 SOP / 技能源。",
        "",
        "## 分类导览",
        "",
    ]

    for source_name, items in sorted(grouped.items()):
        anchor = _anchor(source_name)
        entries.append(f"- [{source_name}](#{anchor}) ({len(items)})")

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
            entries.append(
                f"| `{item['skill_id']}` | {item['name']} | {item['category']} | "
                f"{item['domain']} | {item['version']} |"
            )

    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(entries) + "\n", encoding="utf-8")
    return target


def _anchor(value: str) -> str:
    lowered = value.strip().lower()
    chars: list[str] = []
    for char in lowered:
        if char.isalnum() or "\u4e00" <= char <= "\u9fff":
            chars.append(char)
        elif char in {"-", " ", "_"}:
            chars.append("-")
    return "".join(chars).strip("-") or "section"

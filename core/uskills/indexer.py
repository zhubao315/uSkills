from __future__ import annotations

from pathlib import Path

from .validator import load_skill


def build_skills_index(skills_dir: str | Path, output_path: str | Path) -> Path:
    root = Path(skills_dir)
    entries: list[str] = [
        "# Skills Index",
        "",
        "| Skill ID | Name | Category | Domain | Version |",
        "| --- | --- | --- | --- | --- |",
    ]
    for path in sorted(root.rglob("*.yaml")):
        skill = load_skill(path)
        entries.append(
            f"| `{skill.skill_id}` | {skill.meta.name} | {skill.meta.category.value} | "
            f"{skill.meta.domain} | {skill.meta.version} |"
        )

    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(entries) + "\n", encoding="utf-8")
    return target

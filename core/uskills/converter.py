from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

from .schema import (
    ControlConfig,
    ExecuteConfig,
    OutputConfig,
    SkillCategory,
    SkillInput,
    SkillMeta,
    SourceTrace,
    USkill,
)

STEP_PREFIX = re.compile(r"^\s*(?:\d+[.)]|[-*+])\s+")


def _slugify(value: str) -> str:
    lowered = value.strip().lower()
    lowered = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", lowered)
    return lowered.strip("-") or "step"


def extract_steps(text: str) -> list[str]:
    steps: list[str] = []
    for line in text.splitlines():
        cleaned = line.strip()
        if not cleaned:
            continue
        if STEP_PREFIX.match(cleaned):
            steps.append(STEP_PREFIX.sub("", cleaned).strip())
    if steps:
        return steps
    paragraphs = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]
    return paragraphs


def convert_sop_text(text: str, sop_name: str, sop_path: str = "") -> list[USkill]:
    steps = extract_steps(text)
    skills: list[USkill] = []
    sop_slug = _slugify(sop_name)[:32]
    for index, step in enumerate(steps, start=1):
        step_slug = _slugify(step)[:24]
        skill_id = f"uskill-atomic-{sop_slug}-{index:02d}-{step_slug}-v1-0-0"
        skill = USkill(
            skill_id=skill_id,
            meta=SkillMeta(
                name=f"{sop_name} Step {index}",
                version="1.0.0",
                category=SkillCategory.atomic,
                domain="general",
                description=step,
                tags=["converted", "sop", "atomic", sop_slug],
                owner="uSkills",
            ),
            input=SkillInput(
                params=[
                    {
                        "name": "context",
                        "type": "string",
                        "required": False,
                        "description": "Execution context shared across the SOP chain.",
                    }
                ]
            ),
            execute=ExecuteConfig(
                prompt_template=(
                    "You are executing an atomic SOP skill.\n"
                    f"SOP: {sop_name}\n"
                    f"Step objective: {step}\n"
                    "Use {{context}} when provided and produce a structured result."
                ),
                steps=[step],
                temperature=0.1,
                tools=[],
                fallback=["manual-review"],
            ),
            output=OutputConfig(
                format="json",
                params=["status", "result", "notes"],
                validation_rules=[
                    "status must be one of success, partial, failed",
                    "result must summarize the step execution",
                ],
            ),
            control=ControlConfig(
                timeout=30,
                retry=1,
                interrupt=True,
                breakpoint_allowed=True,
                mockable=True,
            ),
            source=SourceTrace(
                sop_name=sop_name,
                sop_path=sop_path,
                step_index=index,
                raw_step=step,
            ),
        )
        skills.append(skill)
    return skills


def convert_sop_file(path: str | Path, output_dir: str | Path | None = None) -> list[Path]:
    source_path = Path(path)
    text = source_path.read_text(encoding="utf-8")
    skills = convert_sop_text(text, source_path.stem, str(source_path))
    output_root = Path(output_dir) if output_dir else source_path.parent / "generated"
    output_root.mkdir(parents=True, exist_ok=True)

    written: list[Path] = []
    for skill in skills:
        target = output_root / f"{skill.skill_id}.yaml"
        target.write_text(
            yaml.safe_dump(
                json.loads(skill.model_dump_json()),
                allow_unicode=True,
                sort_keys=False,
            ),
            encoding="utf-8",
        )
        written.append(target)
    return written

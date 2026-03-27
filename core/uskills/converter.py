"""uSkills Converter Module.

This module provides functionality to convert SOP text files
into standardized uSkill definitions with proper naming conventions
and error handling.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml  # type: ignore

from .schema import (
    ControlConfig,
    ExecuteConfig,
    OutputConfig,
    SkillCategory,
    SkillInputConfig,
    SkillMeta,
    SkillParam,
    SourceTrace,
    USkill,
)

# Step prefix patterns for SOP parsing
STEP_PREFIX = re.compile(r"^\s*(?:\d+[.)]|[-*+])\s+")

# Maximum skill ID component length
MAX_SKILL_ID_COMPONENT_LENGTH = 32

# File encoding constant
DEFAULT_ENCODING = "utf-8"


class ConversionError(Exception):
    """Custom error for SOP conversion failures."""

    def __init__(self, message: str, source_path: str | None = None):
        super().__init__(message)
        self.source_path = source_path


def _slugify(value: str, max_length: int = MAX_SKILL_ID_COMPONENT_LENGTH) -> str:
    """Convert string to URL-safe slug.

    Args:
        value: Input string to slugify.
        max_length: Maximum length of output slug.

    Returns:
        URL-safe slug string.
    """
    lowered = value.strip().lower()
    # Keep alphanumeric, Chinese characters, and hyphens
    lowered = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", lowered)
    slug = lowered.strip("-") or "step"
    return slug[:max_length]


def extract_steps(text: str) -> list[str]:
    """Extract steps from SOP text.

    Parses numbered lists, bullet points, or paragraphs as steps.

    Args:
        text: SOP text content.

    Returns:
        List of extracted step strings.
    """
    if not text or not text.strip():
        return []

    steps: list[str] = []
    for line in text.splitlines():
        cleaned = line.strip()
        if not cleaned:
            continue
        if STEP_PREFIX.match(cleaned):
            step_text = STEP_PREFIX.sub("", cleaned).strip()
            if step_text:
                steps.append(step_text)

    if steps:
        return steps

    # Fallback: split by double newlines (paragraphs)
    paragraphs = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]
    return paragraphs


def _generate_skill_id(sop_slug: str, index: int, step_slug: str) -> str:
    """Generate a standardized skill ID.

    Format: uskill-atomic-{sop_slug}-{index:02d}-{step_slug}-v1-1-0

    Args:
        sop_slug: Slugified SOP name.
        index: Step index (1-based).
        step_slug: Slugified step description.

    Returns:
        Formatted skill ID.
    """
    return f"uskill-atomic-{sop_slug}-{index:02d}-{step_slug}-v1-1-0"


def _build_prompt_template(sop_name: str, step: str) -> str:
    """Build prompt template for a skill.

    Args:
        sop_name: Name of the source SOP.
        step: Step description.

    Returns:
        Formatted prompt template.
    """
    return (
        "You are executing an atomic SOP skill.\n"
        f"SOP: {sop_name}\n"
        f"Step objective: {step}\n"
        "Use {{context}} when provided and produce a structured result."
    )


def convert_sop_text(
    text: str,
    sop_name: str,
    sop_path: str = "",
    domain: str = "general",
    owner: str = "uSkills",
) -> list[USkill]:
    """Convert SOP text to a list of uSkill definitions.

    Args:
        text: SOP text content.
        sop_name: Name of the SOP.
        sop_path: Path to the source SOP file.
        domain: Skill domain category.
        owner: Skill owner name.

    Returns:
        List of USkill instances.

    Raises:
        ConversionError: If no steps can be extracted.
    """
    steps = extract_steps(text)
    if not steps:
        raise ConversionError(
            f"No steps could be extracted from SOP: {sop_name}",
            source_path=sop_path,
        )

    skills: list[USkill] = []
    sop_slug = _slugify(sop_name)

    for index, step in enumerate(steps, start=1):
        step_slug = _slugify(step, max_length=24)
        skill_id = _generate_skill_id(sop_slug, index, step_slug)

        skill = USkill(
            skill_id=skill_id,
            meta=SkillMeta(
                name=f"{sop_name} Step {index}",
                version="1.1.0",
                category=SkillCategory.atomic,
                domain=domain,
                description=step,
                tags=["converted", "sop", "atomic", sop_slug],
                owner=owner,
            ),
            input=SkillInputConfig(
                params=[
                    SkillParam(
                        name="context",
                        type="string",
                        required=False,
                        description="Execution context shared across the SOP chain.",
                    )
                ]
            ),
            execute=ExecuteConfig(
                prompt_template=_build_prompt_template(sop_name, step),
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


def convert_sop_file(
    path: str | Path,
    output_dir: str | Path | None = None,
    domain: str = "general",
    owner: str = "uSkills",
) -> list[Path]:
    """Convert a SOP file to uSkill YAML files.

    Args:
        path: Path to source SOP file.
        output_dir: Output directory for generated skills.
        domain: Skill domain category.
        owner: Skill owner name.

    Returns:
        List of paths to generated skill files.

    Raises:
        FileNotFoundError: If source file does not exist.
        ConversionError: If conversion fails.
    """
    source_path = Path(path)

    try:
        text = source_path.read_text(encoding=DEFAULT_ENCODING)
    except FileNotFoundError as err:
        raise FileNotFoundError(f"SOP file not found: {source_path}") from err
    except UnicodeDecodeError as err:
        raise ConversionError(
            f"Failed to read file with {DEFAULT_ENCODING} encoding: {err}",
            source_path=str(source_path),
        ) from err

    if not text.strip():
        raise ConversionError(
            f"SOP file is empty: {source_path}",
            source_path=str(source_path),
        )

    skills = convert_sop_text(
        text,
        source_path.stem,
        str(source_path),
        domain=domain,
        owner=owner,
    )

    output_root = Path(output_dir) if output_dir else source_path.parent / "generated"
    output_root.mkdir(parents=True, exist_ok=True)

    written: list[Path] = []
    for skill in skills:
        target = output_root / f"{skill.skill_id}.yaml"
        content = yaml.safe_dump(
            json.loads(skill.model_dump_json()),
            allow_unicode=True,
            sort_keys=False,
        )
        target.write_text(content, encoding=DEFAULT_ENCODING)
        written.append(target)

    return written


def convert_sop_to_dict(
    text: str,
    sop_name: str,
    sop_path: str = "",
    domain: str = "general",
    owner: str = "uSkills",
) -> list[dict[str, Any]]:
    """Convert SOP text to list of skill dictionaries.

    Args:
        text: SOP text content.
        sop_name: Name of the SOP.
        sop_path: Path to the source SOP file.
        domain: Skill domain category.
        owner: Skill owner name.

    Returns:
        List of skill dictionaries.
    """
    skills = convert_sop_text(text, sop_name, sop_path, domain, owner)
    return [json.loads(skill.model_dump_json()) for skill in skills]

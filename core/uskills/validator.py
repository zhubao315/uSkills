"""uSkills Validator Module.

This module provides validation utilities for uSkill files,
including schema validation, template variable checking, and
skill ID format verification.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml

from .schema import SKILL_ID_PATTERN, USkill


class ValidationError(Exception):
    """Custom validation error for uSkills."""

    def __init__(self, message: str, path: str | None = None, details: list[str] | None = None):
        super().__init__(message)
        self.path = path
        self.details = details or []


def _read_data(path: Path) -> dict[str, Any]:
    """Read and parse skill file.

    Args:
        path: Path to skill file (YAML or JSON).

    Returns:
        Parsed data dictionary.

    Raises:
        FileNotFoundError: If file does not exist.
        yaml.YAMLError: If YAML parsing fails.
        json.JSONDecodeError: If JSON parsing fails.
    """
    if not path.exists():
        raise FileNotFoundError(f"Skill file not found: {path}")

    raw = path.read_text(encoding="utf-8")

    if path.suffix.lower() == ".json":
        return json.loads(raw)
    return yaml.safe_load(raw)


def load_skill(path: str | Path) -> USkill:
    """Load and validate a skill file.

    Args:
        path: Path to skill file.

    Returns:
        Validated USkill instance.

    Raises:
        FileNotFoundError: If file does not exist.
        pydantic.ValidationError: If validation fails.
    """
    skill_path = Path(path)
    data = _read_data(skill_path)
    return USkill.model_validate(data)


def validate_skill_file(path: str | Path) -> tuple[bool, str]:
    """Validate a skill file and return status.

    Args:
        path: Path to skill file.

    Returns:
        Tuple of (is_valid, message).
    """
    try:
        skill = load_skill(path)
        return True, f"valid: {skill.skill_id}"
    except FileNotFoundError as e:
        return False, f"error: {e}"
    except Exception as e:
        return False, f"error: {e}"


def validate_skill_data(data: dict[str, Any]) -> tuple[bool, str]:
    """Validate skill data dictionary.

    Args:
        data: Skill data dictionary.

    Returns:
        Tuple of (is_valid, message).
    """
    try:
        skill = USkill.model_validate(data)
        return True, f"valid: {skill.skill_id}"
    except Exception as e:
        return False, f"error: {e}"


def validate_skill_id(skill_id: str) -> tuple[bool, str]:
    """Validate skill ID format.

    Args:
        skill_id: Skill ID to validate.

    Returns:
        Tuple of (is_valid, message).
    """
    if SKILL_ID_PATTERN.match(skill_id):
        return True, f"valid: {skill_id}"
    return False, f"invalid format: {skill_id}"


def extract_template_variables(template: str) -> list[str]:
    """Extract variable names from prompt template.

    Args:
        template: Prompt template string with {{variable}} syntax.

    Returns:
        List of variable names found in template.
    """
    pattern = r"\{\{(\w+)\}\}"
    return list(set(re.findall(pattern, template)))


def validate_template_variables(template: str, defined_params: list[str]) -> tuple[bool, list[str]]:
    """Validate template variables against defined parameters.

    Args:
        template: Prompt template string.
        defined_params: List of defined parameter names.

    Returns:
        Tuple of (is_valid, list_of_undefined_variables).
    """
    variables = extract_template_variables(template)
    undefined = [v for v in variables if v not in defined_params]
    return len(undefined) == 0, undefined


def validate_directory(
    skills_dir: str | Path, recursive: bool = True
) -> dict[str, tuple[bool, str]]:
    """Validate all skill files in a directory.

    Args:
        skills_dir: Directory containing skill files.
        recursive: Whether to search subdirectories.

    Returns:
        Dictionary mapping file paths to validation results.
    """
    root = Path(skills_dir)
    results: dict[str, tuple[bool, str]] = {}

    pattern = "*.yaml" if not recursive else "**/*.yaml"
    for path in sorted(root.glob(pattern)):
        results[str(path)] = validate_skill_file(path)

    for path in sorted(root.glob("*.json" if not recursive else "**/*.json")):
        results[str(path)] = validate_skill_file(path)

    return results

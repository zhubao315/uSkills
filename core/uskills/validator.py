"""uSkills Validator Module.

This module provides functionality to validate uSkill YAML/JSON files
against the standard schema and check for template variable consistency.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

import yaml  # type: ignore

from .schema import USkill


class ValidationError(Exception):
    """Custom error for uSkill validation failures."""

    def __init__(self, message: str, file_path: str | None = None):
        super().__init__(message)
        self.file_path = file_path


def load_skill(path: str | Path) -> USkill:
    """Load and validate a uSkill from a YAML or JSON file.

    Args:
        path: Path to the skill file.

    Returns:
        Validated USkill instance.

    Raises:
        FileNotFoundError: If file does not exist.
        ValidationError: If file content is invalid.
    """
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Skill file not found: {file_path}")

    try:
        content = file_path.read_text(encoding="utf-8")
        if file_path.suffix.lower() in (".yaml", ".yml"):
            data = yaml.safe_load(content)
        else:
            data = json.loads(content)

        return USkill(**cast(dict[str, Any], data))
    except Exception as e:
        raise ValidationError(str(e), file_path=str(file_path)) from e


def validate_skill_file(path: str | Path) -> tuple[bool, str]:
    """Validate a skill file and return status.

    Args:
        path: Path to the skill file.

    Returns:
        Tuple of (is_valid, message).
    """
    try:
        skill = load_skill(path)
        return True, f"valid: {skill.skill_id}"
    except Exception as e:
        return False, f"error: {e}"


def validate_skill_data(data: dict[str, Any]) -> tuple[bool, str]:
    """Validate raw skill dictionary.

    Args:
        data: Skill data dictionary.

    Returns:
        Tuple of (is_valid, message).
    """
    try:
        skill = USkill(**data)
        return True, f"valid: {skill.skill_id}"
    except Exception as e:
        return False, f"error: {e}"


def validate_skill_id(skill_id: str) -> tuple[bool, str]:
    """Validate skill ID format.

    Args:
        skill_id: The skill ID string to validate.

    Returns:
        Tuple of (is_valid, message).
    """
    try:
        # We create a dummy USkill to trigger pydantic validation
        # This ensures consistency between CLI and Core
        USkill.validate_skill_id(skill_id)
        return True, "valid"
    except ValueError as e:
        return False, str(e)


def extract_template_variables(template: str) -> list[str]:
    """Extract variable names from prompt template.

    Looks for {{variable_name}} patterns.

    Args:
        template: Prompt template string.

    Returns:
        List of unique variable names.
    """
    import re

    pattern = re.compile(r"\{\{([\w-]+)\}\}")
    return sorted(list(set(pattern.findall(template))))


def validate_template_variables(
    template: str, params: list[str]
) -> tuple[bool, list[str]]:
    """Check if all template variables are defined in input params.

    Args:
        template: Prompt template string.
        params: List of defined parameter names.

    Returns:
        Tuple of (is_all_defined, list_of_undefined_variables).
    """
    variables = extract_template_variables(template)
    undefined = [v for v in variables if v not in params]
    return len(undefined) == 0, undefined


def validate_directory(
    path: str | Path, recursive: bool = True
) -> dict[str, tuple[bool, str]]:
    """Validate all skill files in a directory.

    Args:
        path: Path to directory.
        recursive: Whether to search subdirectories.

    Returns:
        Dictionary mapping file paths to (is_valid, message) tuples.
    """
    root = Path(path)
    results = {}

    patterns = ["*.yaml", "*.yml", "*.json"]
    files: list[Path] = []
    for pattern in patterns:
        if recursive:
            files.extend(root.rglob(pattern))
        else:
            files.extend(root.glob(pattern))

    for file_path in files:
        results[str(file_path)] = validate_skill_file(file_path)

    return results

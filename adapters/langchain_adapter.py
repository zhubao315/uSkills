"""LangChain Adapter for uSkills.

This module provides integration between uSkills and LangChain,
allowing uSkills to be used as LangChain tools.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from core.uskills.schema import USkill
from core.uskills.validator import load_skill


class LangChainAdapter:
    """Adapter for converting uSkills to LangChain specifications."""

    def __init__(self, skill_path: str | Path):
        """Initialize adapter with skill file path.

        Args:
            skill_path: Path to uSkill YAML or JSON file.
        """
        self.skill: USkill = load_skill(skill_path)

    def to_tool_spec(self) -> dict[str, Any]:
        """Convert uSkill to LangChain tool specification.

        Returns:
            Dictionary with LangChain tool specification.
        """
        return {
            "name": self._sanitize_name(self.skill.meta.name),
            "description": self.skill.meta.description,
            "args_schema": self._build_args_schema(),
            "metadata": {
                "skill_id": self.skill.skill_id,
                "category": self.skill.meta.category.value,
                "domain": self.skill.meta.domain,
                "version": self.skill.meta.version,
                "tags": self.skill.meta.tags,
            },
        }

    def to_prompt_template(self) -> str:
        """Get the prompt template for this skill.

        Returns:
            Prompt template string.
        """
        return self.skill.execute.prompt_template

    def to_function_spec(self) -> dict[str, Any]:
        """Convert uSkill to OpenAI function calling specification.

        Returns:
            Dictionary with function specification.
        """
        return {
            "name": self._sanitize_name(self.skill.meta.name),
            "description": self.skill.meta.description,
            "parameters": {
                "type": "object",
                "properties": self._build_properties(),
                "required": self._get_required_params(),
            },
        }

    def _build_args_schema(self) -> dict[str, Any]:
        """Build arguments schema from skill input parameters.

        Returns:
            Dictionary mapping parameter names to their types.
        """
        return {
            param.name: {
                "type": param.type,
                "description": param.description,
                "required": param.required,
                "default": param.default,
            }
            for param in self.skill.input.params
        }

    def _build_properties(self) -> dict[str, Any]:
        """Build JSON Schema properties from skill input.

        Returns:
            Dictionary with JSON Schema properties.
        """
        type_mapping = {
            "string": {"type": "string"},
            "number": {"type": "number"},
            "integer": {"type": "integer"},
            "boolean": {"type": "boolean"},
            "array": {"type": "array"},
            "object": {"type": "object"},
        }

        properties: dict[str, Any] = {}
        for param in self.skill.input.params:
            prop = type_mapping.get(param.type, {"type": "string"})
            prop["description"] = param.description
            properties[param.name] = prop

        return properties

    def _get_required_params(self) -> list[str]:
        """Get list of required parameter names.

        Returns:
            List of required parameter names.
        """
        return [param.name for param in self.skill.input.params if param.required]

    @staticmethod
    def _sanitize_name(name: str) -> str:
        """Sanitize skill name for use as function name.

        Args:
            name: Original skill name.

        Returns:
            Sanitized name suitable for function calls.
        """
        import re

        # Replace spaces and special chars with underscores
        sanitized = re.sub(r"[^a-zA-Z0-9_]", "_", name)
        # Remove consecutive underscores
        sanitized = re.sub(r"_+", "_", sanitized)
        # Remove leading/trailing underscores
        sanitized = sanitized.strip("_").lower()
        return sanitized or "skill"


def as_langchain_spec(path: str | Path) -> dict[str, Any]:
    """Convert a uSkill file to LangChain tool specification.

    This is a convenience function for quick conversion.

    Args:
        path: Path to uSkill file.

    Returns:
        Dictionary with LangChain tool specification.

    Example:
        >>> spec = as_langchain_spec("skills/atomic/text_keyword_extract.yaml")
        >>> print(spec["name"])
        'text_keyword_extract'
    """
    adapter = LangChainAdapter(path)
    return adapter.to_tool_spec()


def as_openai_function(path: str | Path) -> dict[str, Any]:
    """Convert a uSkill file to OpenAI function calling specification.

    Args:
        path: Path to uSkill file.

    Returns:
        Dictionary with OpenAI function specification.

    Example:
        >>> func = as_openai_function("skills/atomic/text_keyword_extract.yaml")
        >>> print(func["name"])
        'text_keyword_extract'
    """
    adapter = LangChainAdapter(path)
    return adapter.to_function_spec()

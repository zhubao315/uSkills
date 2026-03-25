"""uSkills Schema Definitions.

This module defines the core Pydantic models for uSkills, providing
type-safe validation and JSON Schema export capabilities.
"""

from __future__ import annotations

import re
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

# Schema version for compatibility tracking
SCHEMA_VERSION = "1.0.0"

# Skill ID pattern: uskill-{category}-{name}-{version}
SKILL_ID_PATTERN = re.compile(
    r"^uskill-(atomic|composite|domain|governance)-[\w\u4e00-\u9fff-]+-v\d+-\d+-\d+$"
)


class SkillCategory(str, Enum):
    """Skill category enumeration."""

    atomic = "atomic"
    composite = "composite"
    domain = "domain"
    governance = "governance"


class SkillMeta(BaseModel):
    """Skill metadata configuration."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., min_length=1, max_length=200, description="Skill display name")
    version: str = Field(
        default="1.0.0",
        pattern=r"^\d+\.\d+\.\d+$",
        description="Semantic version (e.g., 1.0.0)",
    )
    category: SkillCategory = Field(..., description="Skill category")
    domain: str = Field(default="general", min_length=1, max_length=100, description="Skill domain")
    description: str = Field(..., min_length=1, max_length=2000, description="Skill description")
    tags: list[str] = Field(
        default_factory=list, max_length=20, description="Skill tags for categorization"
    )
    owner: str = Field(default="community", min_length=1, max_length=100, description="Skill owner")

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, v: list[str]) -> list[str]:
        """Validate and clean tags."""
        return [tag.strip().lower() for tag in v if tag.strip()]


class SkillParam(BaseModel):
    """Skill input parameter definition."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., min_length=1, max_length=100, description="Parameter name")
    type: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Parameter type (string, number, boolean, object, array)",
    )
    required: bool = Field(default=True, description="Whether parameter is required")
    description: str = Field(default="", max_length=500, description="Parameter description")
    default: Any | None = Field(default=None, description="Default value if not required")


class SkillInputConfig(BaseModel):
    """Skill input configuration."""

    model_config = ConfigDict(extra="forbid")

    params: list[SkillParam] = Field(
        default_factory=list, max_length=50, description="Input parameters"
    )


class ExecuteConfig(BaseModel):
    """Execution configuration for skill."""

    model_config = ConfigDict(extra="forbid")

    prompt_template: str = Field(
        ..., min_length=1, max_length=10000, description="Prompt template with variables"
    )
    steps: list[str] = Field(default_factory=list, max_length=100, description="Execution steps")
    temperature: float = Field(default=0.1, ge=0.0, le=2.0, description="LLM temperature parameter")
    model: str = Field(
        default="gpt-4o-mini", min_length=1, max_length=100, description="LLM model name"
    )
    tools: list[str] = Field(default_factory=list, max_length=20, description="Required tools")
    fallback: list[str] = Field(
        default_factory=list, max_length=10, description="Fallback strategies"
    )

    @field_validator("prompt_template")
    @classmethod
    def validate_template_variables(cls, v: str) -> str:
        """Validate template variable syntax."""
        # Check for unclosed braces
        open_count = v.count("{")
        close_count = v.count("}")
        if open_count != close_count:
            raise ValueError(
                f"Template has mismatched braces: {open_count} open vs {close_count} close"
            )
        return v


class OutputConfig(BaseModel):
    """Output configuration for skill."""

    model_config = ConfigDict(extra="forbid")

    format: str = Field(
        default="json",
        pattern=r"^(json|yaml|text|markdown)$",
        description="Output format",
    )
    params: list[str] = Field(default_factory=list, max_length=50, description="Output parameters")
    validation_rules: list[str] = Field(
        default_factory=list, max_length=20, description="Output validation rules"
    )


class ControlConfig(BaseModel):
    """Execution control configuration."""

    model_config = ConfigDict(extra="forbid")

    timeout: int = Field(default=30, ge=1, le=3600, description="Execution timeout in seconds")
    retry: int = Field(default=1, ge=0, le=10, description="Retry count on failure")
    interrupt: bool = Field(default=True, description="Allow execution interruption")
    breakpoint_allowed: bool = Field(default=True, description="Allow breakpoints")
    mockable: bool = Field(default=True, description="Allow mock execution")


class SourceTrace(BaseModel):
    """Source traceability information."""

    model_config = ConfigDict(extra="forbid")

    sop_name: str = Field(..., min_length=1, max_length=200, description="Source SOP name")
    sop_path: str = Field(default="", max_length=500, description="Source SOP file path")
    step_index: int = Field(..., ge=0, description="Step index in source SOP")
    raw_step: str = Field(..., min_length=1, max_length=2000, description="Raw step content")


class USkill(BaseModel):
    """Main uSkill model definition."""

    model_config = ConfigDict(extra="forbid")

    skill_id: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Unique skill identifier",
    )
    meta: SkillMeta = Field(..., description="Skill metadata")
    input: SkillInputConfig = Field(..., description="Input configuration")
    execute: ExecuteConfig = Field(..., description="Execution configuration")
    output: OutputConfig = Field(..., description="Output configuration")
    control: ControlConfig = Field(..., description="Control configuration")
    source: SourceTrace = Field(..., description="Source traceability")

    @field_validator("skill_id")
    @classmethod
    def validate_skill_id(cls, v: str) -> str:
        """Validate skill ID format."""
        if not SKILL_ID_PATTERN.match(v):
            raise ValueError(
                f"Invalid skill_id format. Expected: uskill-{{category}}-{{name}}-v{{version}}, "
                f"got: {v}"
            )
        return v


def exported_json_schema() -> dict[str, Any]:
    """Export USkill JSON Schema.

    Returns:
        JSON Schema dictionary for USkill model.
    """
    schema = USkill.model_json_schema()
    schema["$schema"] = "http://json-schema.org/draft-07/schema#"
    schema["$id"] = f"https://zhubao315.github.io/uSkills/schema/v{SCHEMA_VERSION}.json"
    return schema


def get_schema_version() -> str:
    """Get current schema version."""
    return SCHEMA_VERSION

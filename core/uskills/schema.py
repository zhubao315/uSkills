from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class SkillCategory(str, Enum):
    atomic = "atomic"
    composite = "composite"
    domain = "domain"
    governance = "governance"


class SkillMeta(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    version: str = "1.0.0"
    category: SkillCategory
    domain: str
    description: str
    tags: list[str] = Field(default_factory=list)
    owner: str = "community"


class SkillParam(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    type: str
    required: bool = True
    description: str = ""
    default: Any | None = None


class SkillInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    params: list[SkillParam] = Field(default_factory=list)


class ExecuteConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prompt_template: str
    steps: list[str] = Field(default_factory=list)
    temperature: float = 0.1
    model: str = "gpt-5.4-mini"
    tools: list[str] = Field(default_factory=list)
    fallback: list[str] = Field(default_factory=list)


class OutputConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    format: str = "json"
    params: list[str] = Field(default_factory=list)
    validation_rules: list[str] = Field(default_factory=list)


class ControlConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    timeout: int = 30
    retry: int = 1
    interrupt: bool = True
    breakpoint_allowed: bool = True
    mockable: bool = True


class SourceTrace(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sop_name: str
    sop_path: str
    step_index: int
    raw_step: str


class USkill(BaseModel):
    model_config = ConfigDict(extra="forbid")

    skill_id: str
    meta: SkillMeta
    input: SkillInput
    execute: ExecuteConfig
    output: OutputConfig
    control: ControlConfig
    source: SourceTrace


def exported_json_schema() -> dict[str, Any]:
    return USkill.model_json_schema()

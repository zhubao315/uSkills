"""uSkills core package.

This package provides the core functionality for uSkills including:
- Schema definitions and validation
- SOP to Skill conversion
- Skill indexing and cataloging
"""

from .converter import (
    ConversionError,
    convert_sop_file,
    convert_sop_text,
    convert_sop_to_dict,
    extract_steps,
)
from .indexer import build_skills_index, get_skill_stats
from .schema import (
    SCHEMA_VERSION,
    ControlConfig,
    ExecuteConfig,
    OutputConfig,
    SkillCategory,
    SkillInputConfig,
    SkillMeta,
    SkillParam,
    SourceTrace,
    USkill,
    exported_json_schema,
    get_schema_version,
)
from .validator import (
    ValidationError,
    extract_template_variables,
    load_skill,
    validate_directory,
    validate_skill_data,
    validate_skill_file,
    validate_skill_id,
    validate_template_variables,
)

__all__ = [
    # Schema
    "SCHEMA_VERSION",
    "ControlConfig",
    "ExecuteConfig",
    "OutputConfig",
    "SkillCategory",
    "SkillInputConfig",
    "SkillMeta",
    "SkillParam",
    "SourceTrace",
    "USkill",
    "exported_json_schema",
    "get_schema_version",
    # Converter
    "ConversionError",
    "convert_sop_file",
    "convert_sop_text",
    "convert_sop_to_dict",
    "extract_steps",
    # Indexer
    "build_skills_index",
    "get_skill_stats",
    # Validator
    "ValidationError",
    "extract_template_variables",
    "load_skill",
    "validate_directory",
    "validate_skill_data",
    "validate_skill_file",
    "validate_skill_id",
    "validate_template_variables",
]

__version__ = "1.0.0"

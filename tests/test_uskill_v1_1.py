"""Tests for uSkills V1.1.0 new features."""

from core.uskills.schema import SCHEMA_VERSION, USkill


def test_schema_version_v1_1_0():
    """Verify that the schema version is correctly set to 1.1.0."""
    assert SCHEMA_VERSION == "1.1.0"


def test_uskill_instantiation_basic():
    """Verify that a USkill can be instantiated with standard fields."""
    skill_data = {
        "skill_id": "uskill-atomic-test-v1-1-0",
        "meta": {
            "name": "Test Skill",
            "version": "1.1.0",
            "category": "atomic",
            "description": "A test skill for V1.1.0",
        },
        "input": {
            "params": [{"name": "input_val", "type": "string"}]
        },
        "execute": {
            "prompt_template": "Process {{input_val}}",
            "model": "gpt-4o-mini"
        },
        "output": {
            "format": "json"
        },
        "control": {},
        "source": {
            "sop_name": "Test SOP",
            "step_index": 1,
            "raw_step": "Test step"
        }
    }
    skill = USkill(**skill_data)
    assert skill.skill_id == "uskill-atomic-test-v1-1-0"
    assert skill.meta.version == "1.1.0"

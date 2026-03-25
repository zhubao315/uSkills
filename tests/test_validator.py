"""Tests for uSkills Validator module."""

import pytest

from core.uskills.schema import SkillCategory
from core.uskills.validator import (
    extract_template_variables,
    load_skill,
    validate_directory,
    validate_skill_data,
    validate_skill_file,
    validate_skill_id,
    validate_template_variables,
)


class TestLoadSkill:
    """Tests for skill loading."""

    def test_load_existing_skill(self) -> None:
        """Test loading existing skill file."""
        skill = load_skill("skills/atomic/text_keyword_extract.yaml")
        assert skill.meta.category == SkillCategory.atomic
        assert skill.control.interrupt is True

    def test_load_governance_skill(self) -> None:
        """Test loading governance skill."""
        skill = load_skill("skills/governance/execution_guard.yaml")
        assert skill.meta.category == SkillCategory.governance

    def test_load_nonexistent_skill(self) -> None:
        """Test loading nonexistent skill."""
        with pytest.raises(FileNotFoundError):
            load_skill("skills/nonexistent.yaml")


class TestValidateSkillFile:
    """Tests for skill file validation."""

    def test_validate_existing_skill(self) -> None:
        """Test validation of existing skill."""
        ok, message = validate_skill_file("skills/atomic/text_keyword_extract.yaml")
        assert ok is True
        assert "valid:" in message

    def test_validate_nonexistent_skill(self) -> None:
        """Test validation of nonexistent skill."""
        ok, message = validate_skill_file("skills/nonexistent.yaml")
        assert ok is False
        assert "error" in message.lower()


class TestValidateSkillData:
    """Tests for skill data validation."""

    def test_validate_valid_data(self) -> None:
        """Test validation of valid data."""
        data = {
            "skill_id": "uskill-atomic-test-v1-0-0",
            "meta": {
                "name": "Test Skill",
                "version": "1.0.0",
                "category": "atomic",
                "domain": "test",
                "description": "A test skill",
            },
            "input": {"params": []},
            "execute": {
                "prompt_template": "Execute {{task}}",
                "steps": ["step 1"],
            },
            "output": {
                "format": "json",
                "params": ["result"],
            },
            "control": {
                "timeout": 30,
                "retry": 1,
            },
            "source": {
                "sop_name": "Test SOP",
                "step_index": 1,
                "raw_step": "test step",
            },
        }
        ok, message = validate_skill_data(data)
        assert ok is True


class TestValidateSkillId:
    """Tests for skill ID validation."""

    def test_valid_skill_id(self) -> None:
        """Test valid skill ID format."""
        ok, _ = validate_skill_id("uskill-atomic-test-skill-v1-0-0")
        assert ok is True

    def test_invalid_skill_id(self) -> None:
        """Test invalid skill ID format."""
        ok, _ = validate_skill_id("invalid-id")
        assert ok is False

    def test_skill_id_with_chinese(self) -> None:
        """Test skill ID with Chinese characters."""
        ok, _ = validate_skill_id("uskill-atomic-测试技能-v1-0-0")
        assert ok is True


class TestExtractTemplateVariables:
    """Tests for template variable extraction."""

    def test_extract_single_variable(self) -> None:
        """Test single variable extraction."""
        template = "Process {{input}} and return result"
        variables = extract_template_variables(template)
        assert variables == ["input"]

    def test_extract_multiple_variables(self) -> None:
        """Test multiple variable extraction."""
        template = "Process {{input}} with {{config}} and {{context}}"
        variables = extract_template_variables(template)
        assert set(variables) == {"input", "config", "context"}

    def test_extract_no_variables(self) -> None:
        """Test no variables extraction."""
        template = "Process input and return result"
        variables = extract_template_variables(template)
        assert variables == []

    def test_extract_duplicate_variables(self) -> None:
        """Test duplicate variable extraction."""
        template = "{{x}} and {{x}} and {{y}}"
        variables = extract_template_variables(template)
        assert set(variables) == {"x", "y"}


class TestValidateTemplateVariables:
    """Tests for template variable validation."""

    def test_all_defined(self) -> None:
        """Test when all variables are defined."""
        template = "Process {{input}} with {{config}}"
        params = ["input", "config", "context"]
        is_valid, undefined = validate_template_variables(template, params)
        assert is_valid is True
        assert undefined == []

    def test_some_undefined(self) -> None:
        """Test when some variables are undefined."""
        template = "Process {{input}} with {{missing}}"
        params = ["input", "config"]
        is_valid, undefined = validate_template_variables(template, params)
        assert is_valid is False
        assert "missing" in undefined


class TestValidateDirectory:
    """Tests for directory validation."""

    def test_validate_skills_directory(self) -> None:
        """Test validating skills directory."""
        results = validate_directory("skills/atomic")
        assert len(results) > 0
        for _, (ok, message) in results.items():
            assert isinstance(ok, bool)
            assert isinstance(message, str)

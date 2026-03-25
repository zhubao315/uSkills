"""Tests for uSkills Converter module."""

from pathlib import Path

import pytest

from core.uskills.converter import (
    ConversionError,
    _slugify,
    convert_sop_file,
    convert_sop_text,
    extract_steps,
)
from core.uskills.schema import SkillCategory


class TestExtractSteps:
    """Tests for step extraction functionality."""

    def test_extract_from_numbered_list(self) -> None:
        """Test extraction from numbered list."""
        text = "1. first step\n2. second step\n3. third step"
        result = extract_steps(text)
        assert result == ["first step", "second step", "third step"]

    def test_extract_from_bullet_list(self) -> None:
        """Test extraction from bullet list."""
        text = "- first step\n- second step\n- third step"
        result = extract_steps(text)
        assert result == ["first step", "second step", "third step"]

    def test_extract_from_mixed_list(self) -> None:
        """Test extraction from mixed list formats."""
        text = "1. numbered\n* starred\n- dashed\n+ plussed"
        result = extract_steps(text)
        assert len(result) == 4

    def test_extract_from_paragraphs(self) -> None:
        """Test extraction from paragraphs."""
        text = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."
        result = extract_steps(text)
        assert result == ["First paragraph.", "Second paragraph.", "Third paragraph."]

    def test_extract_empty_text(self) -> None:
        """Test extraction from empty text."""
        assert extract_steps("") == []
        assert extract_steps("   ") == []
        assert extract_steps("\n\n\n") == []

    def test_extract_with_empty_lines(self) -> None:
        """Test extraction with empty lines mixed in."""
        text = "1. first\n\n2. second\n\n3. third"
        result = extract_steps(text)
        assert len(result) == 3


class TestSlugify:
    """Tests for slugify functionality."""

    def test_basic_slugify(self) -> None:
        """Test basic slugify."""
        assert _slugify("Hello World") == "hello-world"

    def test_chinese_slugify(self) -> None:
        """Test Chinese character slugify."""
        assert _slugify("设计分析") == "设计分析"

    def test_mixed_slugify(self) -> None:
        """Test mixed language slugify."""
        result = _slugify("Architect 设计分析")
        assert "architect" in result

    def test_max_length(self) -> None:
        """Test max length constraint."""
        long_text = "a" * 100
        result = _slugify(long_text, max_length=10)
        assert len(result) == 10

    def test_empty_slugify(self) -> None:
        """Test empty string slugify."""
        assert _slugify("") == "step"
        assert _slugify("   ") == "step"


class TestConvertSopText:
    """Tests for SOP text conversion."""

    def test_basic_conversion(self) -> None:
        """Test basic SOP conversion."""
        text = "1. collect input\n2. classify issue\n3. respond"
        skills = convert_sop_text(text, "Support Flow", "flow.md")

        assert len(skills) == 3
        assert skills[0].meta.category == SkillCategory.atomic
        assert skills[0].source.step_index == 1
        assert skills[2].source.step_index == 3

    def test_skill_id_format(self) -> None:
        """Test skill ID format."""
        text = "1. first step"
        skills = convert_sop_text(text, "Test SOP")

        assert skills[0].skill_id.startswith("uskill-atomic-")
        assert skills[0].skill_id.endswith("-v1-0-0")

    def test_meta_fields(self) -> None:
        """Test metadata fields."""
        text = "1. first step"
        skills = convert_sop_text(text, "Test SOP", domain="testing", owner="tester")

        assert skills[0].meta.domain == "testing"
        assert skills[0].meta.owner == "tester"
        assert "converted" in skills[0].meta.tags

    def test_empty_text_raises_error(self) -> None:
        """Test that empty text raises error."""
        with pytest.raises(ConversionError):
            convert_sop_text("", "Empty SOP")

    def test_whitespace_only_raises_error(self) -> None:
        """Test that whitespace-only text raises error."""
        with pytest.raises(ConversionError):
            convert_sop_text("   \n\n   ", "Whitespace SOP")


class TestConvertSopFile:
    """Tests for SOP file conversion."""

    def test_convert_file(self, tmp_path: Path) -> None:
        """Test file conversion."""
        source = tmp_path / "sample.md"
        source.write_text("1. gather\n2. answer\n", encoding="utf-8")

        output_dir = tmp_path / "out"
        written = convert_sop_file(source, output_dir)

        assert len(written) == 2
        assert all(p.suffix == ".yaml" for p in written)
        assert all(p.exists() for p in written)

    def test_convert_nonexistent_file(self, tmp_path: Path) -> None:
        """Test conversion of nonexistent file."""
        source = tmp_path / "nonexistent.md"

        with pytest.raises(FileNotFoundError):
            convert_sop_file(source)

    def test_convert_empty_file(self, tmp_path: Path) -> None:
        """Test conversion of empty file."""
        source = tmp_path / "empty.md"
        source.write_text("", encoding="utf-8")

        with pytest.raises(ConversionError):
            convert_sop_file(source)

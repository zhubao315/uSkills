from pathlib import Path

from core.uskills.converter import convert_sop_file, convert_sop_text, extract_steps


def test_extract_steps_from_numbered_list() -> None:
    text = "1. first step\n2. second step\n"
    assert extract_steps(text) == ["first step", "second step"]


def test_convert_sop_text_builds_atomic_skills() -> None:
    skills = convert_sop_text("1. collect input\n2. classify issue", "Support Flow", "flow.md")
    assert len(skills) == 2
    assert skills[0].meta.category.value == "atomic"
    assert skills[0].source.step_index == 1


def test_convert_sop_file_writes_yaml(tmp_path: Path) -> None:
    source = tmp_path / "sample.md"
    source.write_text("1. gather\n2. answer\n", encoding="utf-8")
    written = convert_sop_file(source, tmp_path / "out")
    assert len(written) == 2
    assert written[0].suffix == ".yaml"

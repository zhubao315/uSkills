from core.uskills.validator import load_skill, validate_skill_file


def test_validate_existing_skill() -> None:
    ok, message = validate_skill_file("skills/atomic/text_keyword_extract.yaml")
    assert ok is True
    assert "valid:" in message


def test_load_skill_fields() -> None:
    skill = load_skill("skills/governance/execution_guard.yaml")
    assert skill.meta.category.value == "governance"
    assert skill.control.interrupt is True

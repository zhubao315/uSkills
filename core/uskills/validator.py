from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from .schema import USkill


def _read_data(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(raw)
    return yaml.safe_load(raw)


def load_skill(path: str | Path) -> USkill:
    skill_path = Path(path)
    return USkill.model_validate(_read_data(skill_path))


def validate_skill_file(path: str | Path) -> tuple[bool, str]:
    skill = load_skill(path)
    return True, f"valid: {skill.skill_id}"

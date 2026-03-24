from __future__ import annotations

from pathlib import Path

from core.uskills.validator import load_skill


def as_langchain_spec(path: str | Path) -> dict:
    skill = load_skill(path)
    return {
        "name": skill.meta.name,
        "description": skill.meta.description,
        "args_schema": {param.name: param.type for param in skill.input.params},
        "prompt_template": skill.execute.prompt_template,
    }

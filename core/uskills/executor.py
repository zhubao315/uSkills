"""uSkills Execution Engine.

This module provides the core executor for running uSkills directly
with LLM providers, including parameter injection and output formatting.
"""

from __future__ import annotations

import json
import os
import time
from typing import Any

from openai import OpenAI
from .schema import USkill


class SkillExecutor:
    """Core execution engine for uSkills."""

    def __init__(self, api_key: str | None = None, default_model: str = "gpt-4o-mini"):
        """Initialize executor with API configuration."""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None
        self.default_model = default_model

    def execute(self, skill: USkill, inputs: dict[str, Any]) -> dict[str, Any]:
        """Execute a uSkill with provided inputs.

        Args:
            skill: The USkill instance to execute.
            inputs: Dictionary of input parameters.

        Returns:
            Structured execution results.
        """
        if not self.client:
            raise ValueError("OpenAI API key is required for execution.")

        # 1. Parameter Injection (basic jinja-like substitution)
        prompt = skill.execute.prompt_template
        for key, value in inputs.items():
            placeholder = f"{{{{{key}}}}}"
            prompt = prompt.replace(placeholder, str(value))

        # 2. LLM Call
        start_time = time.time()
        
        # Prepare response format based on skill output config
        response_format = {"type": "json_object"} if skill.output.format == "json" else {"type": "text"}
        
        response = self.client.chat.completions.create(
            model=skill.execute.model or self.default_model,
            messages=[
                {"role": "system", "content": "Execute according to the skill instructions."},
                {"role": "user", "content": prompt},
            ],
            temperature=skill.execute.temperature,
            response_format=response_format,
        )

        content = response.choices[0].message.content
        execution_time = time.time() - start_time

        # 3. Output Processing
        result = content
        if skill.output.format == "json":
            try:
                result = json.loads(content)
            except json.JSONDecodeError:
                print("Warning: LLM output was not valid JSON.")

        return {
            "skill_id": skill.skill_id,
            "result": result,
            "meta": {
                "execution_time": execution_time,
                "model": skill.execute.model,
                "usage": response.usage.model_dump() if response.usage else None,
            }
        }

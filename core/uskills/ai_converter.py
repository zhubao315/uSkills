"""AI-powered uSkills Converter.

This module uses LLMs to intelligently extract structured uSkills
from unstructured SOP text, including parameter inference and
optimal prompt generation.
"""

from __future__ import annotations

import json
import os
from typing import Any

from openai import OpenAI
from pydantic import ValidationError

from .schema import USkill


class AIConverter:
    """Intelligent SOP to uSkill converter using LLMs."""

    def __init__(self, api_key: str | None = None, model: str = "gpt-4o"):
        """Initialize with API configuration."""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None
        self.model = model

    def convert_sop(self, text: str, sop_name: str) -> list[USkill]:
        """Convert SOP text to a list of validated USkill objects via LLM.

        Args:
            text: Raw SOP text content.
            sop_name: Name of the SOP.

        Returns:
            List of USkill instances.
        """
        if not self.client:
            raise ValueError("OpenAI API key is required for AI conversion.")

        system_prompt = (
            "You are a Senior Agent Architect. Your goal is to convert standard "
            "operating procedures (SOPs) into structured Agent Skills (uSkills).\n"
            "Each uSkill must follow a specific JSON schema with metadata, inputs, "
            "execution prompts, and output definitions."
        )

        user_prompt = (
            f"Please analyze this SOP and break it down into atomic, reusable skills.\n\n"
            f"SOP Name: {sop_name}\n"
            f"SOP Content:\n{text}\n\n"
            "Return a JSON array of skill objects. Each object MUST match the uSkill schema."
        )

        # For demo purposes, we provide a structured response format instruction
        # In a real scenario, we might use JSON Mode or Function Calling
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
        )

        try:
            raw_data = json.loads(response.choices[0].message.content)
            # Handle list vs single object wrapping
            skills_data = raw_data.get("skills", [raw_data]) if isinstance(raw_data, dict) else raw_data
            
            validated_skills = []
            for data in skills_data:
                try:
                    validated_skills.append(USkill(**data))
                except ValidationError as e:
                    print(f"Skipping invalid skill generation: {e}")
            
            return validated_skills
        except Exception as e:
            print(f"Failed to parse AI response: {e}")
            return []

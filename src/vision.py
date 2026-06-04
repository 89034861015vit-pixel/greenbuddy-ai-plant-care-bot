from __future__ import annotations

import base64
import json
from typing import Any

from openai import AsyncOpenAI


SYSTEM_PROMPT = """
You are GreenBuddy, a careful AI assistant for houseplant care.
Analyze the plant photo and return only valid JSON.
Do not invent certainty. If the image is unclear, say so.

JSON schema:
{
  "plant_state": "short state summary",
  "health_score": 0-100,
  "diagnosis": "likely issue or condition",
  "care_action": "one concrete action for the next 24 hours",
  "watering": "watering advice",
  "light": "light advice",
  "risk_level": "low|medium|high"
}
""".strip()


def _image_to_data_url(image_bytes: bytes) -> str:
    encoded = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:image/jpeg;base64,{encoded}"


def _safe_json_loads(text: str) -> dict[str, Any]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        cleaned = cleaned.replace("json", "", 1).strip()
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        return {
            "plant_state": "Analysis returned non-JSON text",
            "health_score": 50,
            "diagnosis": cleaned[:500],
            "care_action": "Check soil moisture, light, and visible damage. Try another clearer photo.",
            "watering": "Check the top 2-3 cm of soil before watering.",
            "light": "Use bright indirect light unless the plant type requires otherwise.",
            "risk_level": "medium",
        }
    if not isinstance(data, dict):
        raise ValueError("Vision response is not a JSON object")
    return data


async def analyze_plant_photo(
    image_bytes: bytes,
    api_key: str,
    base_url: str,
    model: str,
) -> dict[str, Any]:
    client = AsyncOpenAI(api_key=api_key, base_url=base_url)
    image_url = _image_to_data_url(image_bytes)

    response = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Analyze this houseplant photo and return JSON only."},
                    {"type": "image_url", "image_url": {"url": image_url}},
                ],
            },
        ],
        temperature=0.2,
    )
    content = response.choices[0].message.content or "{}"
    return _safe_json_loads(content)

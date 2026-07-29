import json
import re


def extract_json_template(text):
    """
    Extracts the first JSON object found in the user's message.
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        return None

    try:
        return json.loads(match.group())
    except Exception:
        return None


def extract_json_response(text):
    """
    Extract JSON from an LLM response.
    Handles:
    - plain JSON
    - ```json ... ```
    - extra text before/after JSON
    """

    # Remove markdown fences
    text = re.sub(r"```json", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```", "", text)

    # Find first JSON object
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        return None

    try:
        return json.loads(match.group())
    except Exception:
        return None
import json
from json import JSONDecodeError

import google.generativeai as genai

from app.config import GEMINI_API_KEY

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


REQUIRED_RESULT_KEYS = {
    "overall_score",
    "grade",
    "overall_verdict",
    "parameters",
    "top_3_critical_issues",
    "ats_keywords_missing",
    "rewritten_sections",
}

COMPACT_RETRY_SUFFIX = """

IMPORTANT RETRY INSTRUCTIONS:
- Your previous response was too long or incomplete.
- Return the same JSON schema again.
- Keep every string very short.
- Do not include any text outside the JSON object.
"""


def _collect_response_text(response) -> str:
    text = getattr(response, "text", None)
    if text:
        return text.strip()

    parts: list[str] = []
    for candidate in getattr(response, "candidates", []) or []:
        content = getattr(candidate, "content", None)
        for part in getattr(content, "parts", []) or []:
            part_text = getattr(part, "text", None)
            if part_text:
                parts.append(part_text)

    combined = "\n".join(parts).strip()
    if not combined:
        raise ValueError("EMPTY_AI_RESPONSE")
    return combined


def _extract_first_json_object(raw_text: str) -> str:
    normalized = raw_text.replace("```json", "```").strip()
    if normalized.startswith("```") and normalized.endswith("```"):
        normalized = normalized[3:-3].strip()

    start = normalized.find("{")
    if start == -1:
        raise ValueError("INVALID_JSON_FROM_AI")

    depth = 0
    in_string = False
    escape = False

    for index in range(start, len(normalized)):
        char = normalized[index]

        if in_string:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                in_string = False
            continue

        if char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return normalized[start:index + 1]

    raise ValueError("INCOMPLETE_JSON_FROM_AI")


def _validate_result_shape(result: dict) -> dict:
    missing_keys = REQUIRED_RESULT_KEYS.difference(result.keys())
    if missing_keys:
        print(f"GEMINI RESULT MISSING KEYS: {sorted(missing_keys)}")
        raise ValueError("INVALID_JSON_FROM_AI")

    if not isinstance(result.get("parameters"), list) or len(result["parameters"]) != 10:
        raise ValueError("INVALID_JSON_FROM_AI")

    if not isinstance(result.get("top_3_critical_issues"), list) or len(result["top_3_critical_issues"]) != 3:
        raise ValueError("INVALID_JSON_FROM_AI")

    if not isinstance(result.get("ats_keywords_missing"), list):
        raise ValueError("INVALID_JSON_FROM_AI")

    if not isinstance(result.get("rewritten_sections"), dict):
        raise ValueError("INVALID_JSON_FROM_AI")

    try:
        result["overall_score"] = int(result["overall_score"])
    except (TypeError, ValueError):
        raise ValueError("INVALID_JSON_FROM_AI")

    return result


def _generate_response_text(model, prompt: str) -> str:
    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.1,
            "top_p": 0.8,
            "max_output_tokens": 8192,
            "response_mime_type": "application/json",
        },
    )
    return _collect_response_text(response)


def analyze_with_gemini(prompt: str) -> dict:
    if not GEMINI_API_KEY:
        print("GEMINI ERROR: Missing GEMINI_API_KEY")
        raise ValueError("AI_API_ERROR")

    try:
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        prompts_to_try = [prompt, f"{prompt.rstrip()}\n{COMPACT_RETRY_SUFFIX}"]

        for attempt_index, attempt_prompt in enumerate(prompts_to_try, start=1):
            raw_text = _generate_response_text(model, attempt_prompt)
            print(f"\n===== RAW AI RESPONSE ATTEMPT {attempt_index} =====\n")
            print(raw_text)
            print("\n=========================================\n")

            try:
                try:
                    parsed = json.loads(raw_text)
                except JSONDecodeError:
                    json_text = _extract_first_json_object(raw_text)
                    parsed = json.loads(json_text)

                if not isinstance(parsed, dict):
                    raise ValueError("INVALID_JSON_FROM_AI")

                return _validate_result_shape(parsed)
            except ValueError as exc:
                if str(exc) != "INCOMPLETE_JSON_FROM_AI" or attempt_index == len(prompts_to_try):
                    raise
                print("AI response was truncated before JSON completion, retrying with a compact prompt")

    except ValueError as exc:
        if str(exc) == "INCOMPLETE_JSON_FROM_AI":
            print("AI response was truncated before JSON completion")
        raise
    except Exception as exc:
        print("Gemini FULL ERROR:", repr(exc))
        raise ValueError("AI_API_ERROR")

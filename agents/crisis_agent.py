"""
Crisis Agent — first line of safety for every message.

Flow:
1. Keyword check (instant, no API)
2. LLM check for ambiguous signals
3. Warm crisis response with resources
"""

import json
from google import genai
from google.genai import types
from tools.assessment import detect_crisis_level
from tools.resources import get_crisis_block

_SYSTEM = """You are Anima in crisis support mode. A student may be experiencing serious distress.

Your priorities:
1. Make them feel heard and not alone — genuine warmth, zero clinical distance
2. Reflect back exactly what they said, showing you understood
3. Gently and directly ask one safety question
4. Provide one immediate grounding technique
5. Always end by including crisis resources

Do NOT:
- Give advice or try to solve their problems
- Be cheerful or minimise what they said
- Ask multiple questions
- Use clinical jargon

Keep your response focused and calm. Long responses feel overwhelming in crisis."""

_CLASSIFIER_SYSTEM = """You are a safety classifier for a mental health chatbot.
Analyse messages for crisis signals. Respond in JSON only."""


class CrisisAgent:
    def __init__(self, client: genai.Client):
        self._client = client

    def check_for_crisis(self, message: str, history=None) -> dict:
        """Returns {'is_crisis': bool, 'level': str, 'method': str}"""
        kw = detect_crisis_level(message)

        if kw["level"] == "high":
            return {"is_crisis": True, "level": "high", "method": "keyword"}

        if kw["level"] in ("medium", "ambiguous"):
            llm = self._llm_classify(message)
            return {"is_crisis": llm["is_crisis"], "level": llm["level"], "method": "llm"}

        return {"is_crisis": False, "level": "none", "method": "keyword"}

    def _llm_classify(self, message: str) -> dict:
        prompt = (
            f'Student message: "{message}"\n\n'
            "Does this contain crisis signals (suicidal ideation, self-harm intent, "
            "severe hopelessness, or imminent danger)?\n\n"
            'JSON: {"is_crisis": true/false, "level": "none"|"low"|"medium"|"high", "reason": "brief"}'
        )
        try:
            resp = self._client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=_CLASSIFIER_SYSTEM,
                    temperature=0.1,
                    response_mime_type="application/json",
                ),
            )
            return json.loads(resp.text)
        except Exception:
            return {"is_crisis": False, "level": "none", "reason": "parse error"}

    def respond(self, message: str, history: list) -> str:
        gemini_history = _to_gemini_history(history[-6:])
        prompt = (
            f'The student said: "{message}"\n\n'
            "Respond with warmth, reflect what they said, ask one gentle safety question, "
            "and provide one immediate coping tool. Then include these resources at the end:\n"
            + get_crisis_block()
        )
        try:
            chat = self._client.chats.create(
                model="gemini-2.5-flash",
                history=gemini_history,
                config=types.GenerateContentConfig(system_instruction=_SYSTEM),
            )
            return chat.send_message(prompt).text
        except Exception:
            return (
                "I hear you, and I want you to know you matter.\n\n"
                "What you're going through sounds incredibly hard. You don't have to face this alone.\n"
                + get_crisis_block()
                + "\n\nI'm here with you right now. Can you tell me a bit more about what's happening?"
            )


def _to_gemini_history(history: list) -> list:
    result = []
    for msg in history:
        role = "user" if msg["role"] == "user" else "model"
        result.append({"role": role, "parts": [{"text": msg["content"]}]})
    return result

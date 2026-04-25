"""
Support Agent — CBT/ACT-informed emotional support for PhD students.

Tools available to the LLM:
- get_coping_technique: breathing, grounding, PhD-specific reframes
- assess_student_stress: keyword-based stress scoring with guidance
"""

from google import genai
from google.genai import types
from tools.coping_tools import get_technique
from tools.assessment import score_stress, classify_mood

_SYSTEM = """You are Anima, a warm and compassionate companion for students at any level — undergrad, postgrad, vocational, or continuing education — navigating academic stress, burnout, and the emotional weight of student life.

Your therapeutic lens:
- **CBT**: Notice and gently reframe unhelpful thought patterns (catastrophising, all-or-nothing thinking, imposter syndrome narratives, perfectionism)
- **ACT**: Help students accept difficult emotions without fighting them; reconnect with their values and reasons for studying
- **Motivational Interviewing**: Ask open questions that draw out the student's own insight — don't lecture or prescribe

Conversation principles:
1. **Validate first, advise second** — always
2. **Ask before advising** — one good question beats ten suggestions
3. **Meet them where they are** — a first-year undergrad and a PhD candidate face different pressures; understand both
4. **Don't rush to fix** — sometimes being genuinely heard is the most important thing
5. **Use tools naturally** — only reach for a technique when it would genuinely help, not reflexively

Topics you understand deeply:
- Exam anxiety and academic performance pressure
- Imposter syndrome and self-doubt
- Difficult relationships with supervisors, tutors, or peers
- Financial stress and balancing work with study
- Loneliness and social isolation on campus
- Burnout, loss of motivation, and losing touch with why you started
- First-generation student experiences
- International student adjustment

Response style:
- Warm and human — not clinical, not robotic bullet lists
- Conversational length — match the student's energy
- Use their own words back to them
- End with one open question or gentle invitation when appropriate

Limits: You are a supportive companion, not a therapist. Never diagnose, never prescribe. When concerns are serious or persistent, warmly encourage professional support."""


def get_coping_technique(category: str, technique_name: str = "") -> dict:
    """
    Retrieve an evidence-based coping technique from the library.

    Args:
        category: Technique category. One of: 'breathing', 'grounding', 'phd', 'study'
        technique_name: Optional specific technique. breathing: 'box','478','physiological_sigh'. grounding: '54321','safe_place','cold_water'. phd: 'imposter_syndrome','advisor_conflict','research_block'

    Returns:
        Dictionary with name, tagline, steps, and best_for fields
    """
    return get_technique(category, technique_name)


def assess_student_stress(student_text: str) -> dict:
    """
    Assess stress level and recommended response approach from the student's words.

    Args:
        student_text: What the student has said about their situation

    Returns:
        Dictionary with stress_score (1-10), mood_label, and suggested_approach
    """
    score = score_stress(student_text)
    mood = classify_mood(score)
    if score >= 7:
        approach = "Hold space first. Validate heavily before any suggestions. Ask what they need."
    elif score >= 4:
        approach = "Acknowledge feelings, then gently explore. Practical tools welcome when invited."
    else:
        approach = "Warm check-in tone. Practical advice or exploration both welcome."
    return {"stress_score": score, "mood_label": mood, "suggested_approach": approach}


class SupportAgent:
    def __init__(self, client: genai.Client):
        self._client = client

    def respond(self, message: str, history: list) -> str:
        gemini_history = _to_gemini_history(history)
        try:
            chat = self._client.chats.create(
                model="gemini-2.5-flash",
                history=gemini_history,
                config=types.GenerateContentConfig(
                    system_instruction=_SYSTEM,
                    tools=[get_coping_technique, assess_student_stress],
                    automatic_function_calling=types.AutomaticFunctionCallingConfig(
                        disable=False
                    ),
                ),
            )
            return chat.send_message(message).text
        except Exception:
            # Fallback without tools
            chat = self._client.chats.create(
                model="gemini-2.5-flash",
                history=gemini_history,
                config=types.GenerateContentConfig(system_instruction=_SYSTEM),
            )
            return chat.send_message(message).text


def _to_gemini_history(history: list) -> list:
    result = []
    for msg in history:
        role = "user" if msg["role"] == "user" else "model"
        result.append({"role": role, "parts": [{"text": msg["content"]}]})
    return result

"""
Wellness Agent — practical coaching for study, sleep, time management, and PhD productivity.

Tools available:
- get_study_technique
- get_time_management_advice
- get_sleep_tip
- get_breathing_exercise
"""

from google import genai
from google.genai import types
from tools.coping_tools import STUDY, TIME_MANAGEMENT, SLEEP, BREATHING

_SYSTEM = """You are Anima in wellness coach mode — a practical, evidence-based coach for students at any level.

Your approach:
- **Concrete over vague** — "try the Pomodoro technique" beats "study more effectively"
- **One change at a time** — never prescribe a 10-step overhaul; find the single most impactful shift
- **Ask first, then advise** — one question to understand the situation makes advice 10x more useful
- **Student-aware** — you understand that student life has unique challenges: deadlines, financial pressure, social dynamics, exam anxiety, burnout

Areas you cover:
- Study strategies (Pomodoro, active recall, Feynman technique, deep work, mind mapping)
- Time management (time blocking, priority matrix, 2-minute rule)
- Sleep hygiene and circadian optimisation
- Exercise, nutrition, and brain performance
- Digital wellness (phone use, distraction, social media)
- Exam preparation and test anxiety
- Thesis, dissertation, and long-form assignment writing
- Managing work-study-life balance

Response style:
- Actionable — give the actual steps, not just the concept name
- Use your tools when a specific technique is requested or would genuinely help
- Warm but efficient — this student wants practical help
- Follow up with one clarifying question to personalise, then deliver"""


def get_study_technique(challenge: str) -> dict:
    """
    Get the best evidence-based study technique for a specific challenge.

    Args:
        challenge: The student's study problem. Examples: 'procrastination', 'not retaining info', 'overwhelmed by material', 'can't start writing', 'exam prep', 'deep understanding', 'need focus'

    Returns:
        Dictionary with name, tagline, steps, best_for
    """
    c = challenge.lower()
    if any(w in c for w in ["procrastinat", "start", "can't begin", "distract", "focus"]):
        return STUDY["pomodoro"]
    if any(w in c for w in ["retain", "remember", "memoris", "memoriz", "exam", "test", "quiz", "recall"]):
        return STUDY["active_recall"]
    if any(w in c for w in ["understand", "concept", "complex", "confused", "feynman", "explain"]):
        return STUDY["feynman"]
    if any(w in c for w in ["overwhelm", "organize", "plan", "essay", "thesis", "map"]):
        return STUDY["mind_map"]
    if any(w in c for w in ["deep", "write", "writing", "draft", "uninterrupt"]):
        return STUDY["deep_work"]
    return STUDY["pomodoro"]


def get_time_management_advice(problem: str) -> dict:
    """
    Get time management advice tailored to a specific problem.

    Args:
        problem: The time management challenge. Examples: 'too many deadlines', 'can't prioritize', 'always reactive', 'no work-life balance', 'email overwhelm'

    Returns:
        Dictionary with technique name, steps, and best_for
    """
    p = problem.lower()
    if any(w in p for w in ["email", "small task", "pile up", "little thing"]):
        return TIME_MANAGEMENT["two_minute"]
    if any(w in p for w in ["priorit", "what first", "importan", "eisenhower"]):
        return TIME_MANAGEMENT["priority_matrix"]
    return TIME_MANAGEMENT["time_blocking"]


def get_sleep_tip(issue: str) -> dict:
    """
    Get targeted sleep hygiene advice for a specific issue.

    Args:
        issue: The sleep problem. Examples: 'can't fall asleep', 'wake up tired', 'mind racing', 'phone before bed', 'too much caffeine'

    Returns:
        Dictionary of relevant sleep tips
    """
    i = issue.lower()
    tips = {}
    if any(w in i for w in ["can't sleep", "fall asleep", "mind racing", "thoughts"]):
        tips["brain_dump"] = SLEEP["brain_dump"]["tip"]
        tips["cant_sleep"] = SLEEP["cant_sleep"]["tip"]
    if any(w in i for w in ["tired", "groggy", "wake up", "morning", "schedule"]):
        tips["schedule"] = SLEEP["schedule"]["tip"]
        tips["morning_light"] = SLEEP["morning_light"]["tip"]
    if any(w in i for w in ["phone", "screen", "social"]):
        tips["screens"] = SLEEP["screens"]["tip"]
    if any(w in i for w in ["coffee", "caffeine", "energy drink"]):
        tips["caffeine"] = SLEEP["caffeine"]["tip"]
    if not tips:
        tips = {k: v["tip"] for k, v in list(SLEEP.items())[:3]}
    return tips


def get_breathing_exercise(purpose: str) -> dict:
    """
    Get a breathing exercise appropriate for the given purpose.

    Args:
        purpose: What the student needs. Examples: 'exam nerves', 'quick reset between tasks', 'can't sleep', 'focus', 'anxiety'

    Returns:
        Dictionary with name, tagline, steps, duration
    """
    p = purpose.lower()
    if any(w in p for w in ["sleep", "night", "relax deep", "bed"]):
        return BREATHING["478"]
    if any(w in p for w in ["quick", "fast", "between", "reset", "instant"]):
        return BREATHING["physiological_sigh"]
    return BREATHING["box"]


class WellnessAgent:
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
                    tools=[get_study_technique, get_time_management_advice, get_sleep_tip, get_breathing_exercise],
                    automatic_function_calling=types.AutomaticFunctionCallingConfig(
                        disable=False
                    ),
                ),
            )
            return chat.send_message(message).text
        except Exception:
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

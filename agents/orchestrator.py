"""
Orchestrator — the brain of Anima.

Every message passes through here:
1. Crisis check  2. Intent classification  3. Route to agent
4. Detect inline cards  5. Persist session  6. Return rich response
"""

import json
from google import genai
from google.genai import types
from tools.session_tools import load_session, save_session, log_mood
from tools.assessment import score_stress, classify_mood
from tools.coping_tools import BREATHING, GROUNDING, STUDY, TIME_MANAGEMENT
from tools.counsellors import COUNSELLORS
from agents.crisis_agent import CrisisAgent
from agents.support_agent import SupportAgent
from agents.wellness_agent import WellnessAgent

_CLASSIFIER_SYSTEM = """You are a routing classifier for Anima, a student mental health companion.
Classify incoming messages to route them to the right support agent.
Respond with valid JSON only — no explanation, no markdown."""

# Keyword → (card_category, card_key) mapping
_TECHNIQUE_MAP = [
    (["box breathing", "box breath"],         ("breathing", "box")),
    (["physiological sigh", "double inhale"], ("breathing", "physiological_sigh")),
    (["4-7-8", "4–7–8", "478"],              ("breathing", "478")),
    (["5-4-3-2-1", "5–4–3–2–1", "sensory grounding"], ("grounding", "54321")),
    (["safe place visuali"],                  ("grounding", "safe_place")),
    (["cold water reset"],                    ("grounding", "cold_water")),
    (["pomodoro"],                            ("study", "pomodoro")),
    (["active recall"],                       ("study", "active_recall")),
    (["feynman"],                             ("study", "feynman")),
    (["mind map", "mind-map"],               ("study", "mind_map")),
    (["deep work"],                           ("study", "deep_work")),
    (["time blocking", "time-blocking"],      ("time_management", "time_blocking")),
    (["priority matrix", "eisenhower"],       ("time_management", "priority_matrix")),
]

_CATEGORY_LIBS = {
    "breathing": BREATHING,
    "grounding": GROUNDING,
    "study": STUDY,
    "time_management": TIME_MANAGEMENT,
}

_CATEGORY_ICONS = {
    "breathing": "🌬️",
    "grounding": "⚓",
    "study": "📚",
    "time_management": "⏱️",
}


def _strip_json(text: str) -> str:
    text = text.strip()
    if "```" in text:
        for part in text.split("```"):
            part = part.strip()
            if part.startswith("json"):
                part = part[4:].strip()
            if part.startswith("{"):
                return part
    return text


class Orchestrator:
    def __init__(self, api_key: str):
        self._client = genai.Client(api_key=api_key)
        self.crisis_agent = CrisisAgent(self._client)
        self.support_agent = SupportAgent(self._client)
        self.wellness_agent = WellnessAgent(self._client)

    def process(self, message: str, session_id: str) -> dict:
        session = load_session(session_id)
        history = session.get("history", [])

        agent_steps = []

        # 1. Crisis check
        agent_steps.append("Checking wellbeing signals…")
        crisis = self.crisis_agent.check_for_crisis(message, history)

        if crisis["is_crisis"]:
            agent_steps.append("Crisis Support activated…")
            response = self.crisis_agent.respond(message, history)
            agent_type = "crisis"
        else:
            # 2. Classify
            agent_steps.append("Reading your message…")
            intent = self._classify(message, history)
            cat = intent.get("category", "emotional_support")

            # 3. Route
            if cat in ("wellness", "study", "sleep", "productivity"):
                agent_steps.append("Wellness Coach responding…")
                response = self.wellness_agent.respond(message, history)
                agent_type = "wellness"
            else:
                agent_steps.append("Support Agent responding…")
                response = self.support_agent.respond(message, history)
                agent_type = "support"

        # 4. Inline cards
        cards = self._build_cards(response, agent_type, history, crisis["is_crisis"])
        if cards:
            agent_steps.append("Attaching personalised resources…")

        # 5. Quick replies
        quick_replies = self._quick_replies(agent_type, crisis["is_crisis"])

        # 6. Mood logging
        mood_score = score_stress(message)
        log_mood(session_id, mood_score, classify_mood(mood_score))

        # 7. Persist
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": response})
        session["history"] = history
        save_session(session_id, session)

        return {
            "response": response,
            "agent_type": agent_type,
            "crisis_detected": crisis["is_crisis"],
            "cards": cards,
            "quick_replies": quick_replies,
            "agent_steps": agent_steps,
            "mood_score": mood_score,
        }

    # ------------------------------------------------------------------

    def _classify(self, message: str, history: list) -> dict:
        snippet = "\n".join(
            f"{'Student' if m['role']=='user' else 'Anima'}: {m['content'][:100]}"
            for m in history[-4:]
        ) or "(start)"
        prompt = (
            f"Conversation so far:\n{snippet}\n\nNew message: \"{message}\"\n\n"
            "Classify for routing:\n"
            '{"category":"emotional_support"|"wellness"|"study"|"sleep"|"productivity"|"general",'
            '"severity":1-5,"tone":"distressed"|"frustrated"|"anxious"|"neutral"|"hopeful"|"positive"}\n\n'
            "emotional_support: processing feelings, anxiety, imposter syndrome, loneliness, advisor/teacher stress\n"
            "wellness: physical wellbeing, sleep, exercise, burnout recovery\n"
            "study: study techniques, focus, comprehension, research\n"
            "sleep: sleep-specific problems\n"
            "productivity: time management, deadlines, procrastination\n"
            "general: greetings, check-ins"
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
            return json.loads(_strip_json(resp.text))
        except Exception:
            return {"category": "emotional_support", "severity": 2, "tone": "neutral"}

    def _build_cards(self, response: str, agent_type: str, history: list, crisis: bool) -> list:
        cards = []
        r = response.lower()

        # Technique card — first match wins
        for keywords, (cat, key) in _TECHNIQUE_MAP:
            if any(kw in r for kw in keywords):
                lib = _CATEGORY_LIBS.get(cat, {})
                tech = lib.get(key, {})
                if tech:
                    cards.append({
                        "type": "technique",
                        "icon": _CATEGORY_ICONS.get(cat, "🛠️"),
                        "title": tech.get("name", key),
                        "tagline": tech.get("tagline", ""),
                        "steps": tech.get("steps", []),
                        "duration": tech.get("duration", ""),
                        "best_for": tech.get("best_for", []),
                    })
                break

        # Counsellor suggestion — after several messages or on crisis
        user_msgs = sum(1 for m in history if m["role"] == "user")
        suggest_threshold = 4
        if crisis or (
            user_msgs >= suggest_threshold
            and agent_type == "support"
            and any(kw in r for kw in ["professional", "counsellor", "therapist", "seek help", "support from"])
        ):
            top3 = sorted(COUNSELLORS, key=lambda c: c["distance_miles"])[:3]
            cards.append({
                "type": "counsellor_suggest",
                "counsellors": [
                    {
                        "id": c["id"],
                        "name": c["name"],
                        "initials": c["initials"],
                        "color": c["color"],
                        "specialty": c["specialty"][:2],
                        "distance_miles": c["distance_miles"],
                        "free_for_students": c["free_for_students"],
                        "rating": c["rating"],
                    }
                    for c in top3
                ],
            })

        return cards

    def _quick_replies(self, agent_type: str, crisis: bool) -> list:
        if crisis:
            return ["I'm feeling safer now", "I need more resources", "Book a session"]
        if agent_type == "wellness":
            return ["Try this now", "More techniques", "I need to talk"]
        if agent_type == "support":
            return ["Tell me more", "I need a technique", "Find a counsellor"]
        return ["I'm doing okay", "I need support", "Find help"]

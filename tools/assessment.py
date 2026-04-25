"""
Keyword-based assessment helpers used by agents.
Fast, local, no API calls needed.
"""

# --- Crisis detection ---

_CRISIS_HIGH = [
    "kill myself", "end my life", "suicide", "suicidal", "want to die",
    "no reason to live", "better off dead", "can't go on", "hurt myself",
    "self-harm", "self harm", "cut myself", "don't want to be here anymore",
]
_CRISIS_MEDIUM = [
    "hopeless", "worthless", "no way out", "can't take it anymore",
    "giving up on everything", "nobody cares", "wish i was dead",
    "can't see the point", "disappear forever",
]
_CRISIS_AMBIGUOUS = [
    "can't do this anymore", "so done", "tired of everything",
    "what's the point", "never going to get better", "nobody understands me",
]


def detect_crisis_level(text: str) -> dict:
    """
    Returns {'level': 'none'|'ambiguous'|'medium'|'high', 'is_crisis': bool}
    """
    t = text.lower()
    for kw in _CRISIS_HIGH:
        if kw in t:
            return {"level": "high", "is_crisis": True}
    for kw in _CRISIS_MEDIUM:
        if kw in t:
            return {"level": "medium", "is_crisis": True}
    for kw in _CRISIS_AMBIGUOUS:
        if kw in t:
            return {"level": "ambiguous", "is_crisis": False}
    return {"level": "none", "is_crisis": False}


# --- Stress / burnout scoring ---

_STRESS_HIGH = [
    "overwhelmed", "drowning", "breaking down", "falling apart", "can't breathe",
    "panic attack", "complete mess", "failing everything", "disaster",
    "total breakdown", "can't function",
]
_STRESS_MED = [
    "stressed", "anxious", "worried", "exhausted", "burned out", "burnout",
    "burned out", "can't focus", "can't sleep", "can't concentrate",
    "imposter syndrome", "not good enough", "fraud", "behind on everything",
    "dissertation", "qualifying exam", "comps", "advisor", "committee",
    "research is going nowhere", "no progress",
]
_STRESS_LOW = [
    "a bit stressed", "slightly worried", "some anxiety", "kind of tired",
    "a little overwhelmed",
]

# PhD-specific burnout signals
_BURNOUT_SIGNALS = [
    "lost motivation", "don't care anymore", "going through the motions",
    "no energy", "dread going to lab", "hate my research", "questioning everything",
    "why am i doing this", "drop out", "leave academia", "quit the phd",
    "years of my life", "wasted time", "no end in sight",
]


def score_stress(text: str) -> int:
    """Returns 1-10 stress score."""
    t = text.lower()
    score = 2
    for kw in _STRESS_HIGH:
        if kw in t:
            score = max(score, 8)
    for kw in _STRESS_MED:
        if kw in t:
            score = max(score, 5)
    for kw in _STRESS_LOW:
        if kw in t:
            score = max(score, 3)
    return min(score, 10)


def detect_burnout_signals(text: str) -> list:
    """Returns list of detected burnout signals."""
    t = text.lower()
    return [sig for sig in _BURNOUT_SIGNALS if sig in t]


def classify_mood(score: int) -> str:
    if score >= 8:
        return "high distress"
    if score >= 5:
        return "moderate stress"
    if score >= 3:
        return "mild stress"
    return "stable"

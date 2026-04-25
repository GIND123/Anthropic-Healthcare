"""Crisis and professional help resources."""

CRISIS_LINES = {
    "US": [
        {"name": "988 Suicide & Crisis Lifeline", "contact": "Call or text **988**", "note": "24/7, free, confidential"},
        {"name": "Crisis Text Line", "contact": "Text **HOME** to **741741**", "note": "24/7 text-based support"},
        {"name": "Trevor Project (LGBTQ+)", "contact": "1-866-488-7386", "note": "24/7"},
    ],
    "UK": [
        {"name": "Samaritans", "contact": "**116 123**", "note": "24/7, free"},
        {"name": "SHOUT Crisis Text", "contact": "Text **SHOUT** to **85258**", "note": "24/7"},
    ],
    "India": [
        {"name": "iCall (TISS)", "contact": "**9152987821**", "note": "Mon–Sat 8am–10pm"},
        {"name": "Vandrevala Foundation", "contact": "**1860-2662-345**", "note": "24/7"},
        {"name": "NIMHANS", "contact": "**080-46110007**", "note": "Mon–Sat 8am–8pm"},
    ],
    "International": [
        {"name": "IASP Crisis Centre Directory", "contact": "https://www.iasp.info/resources/Crisis_Centres/", "note": "Find local help by country"},
    ],
}

CAMPUS_RESOURCES = [
    "**University Counseling Center** — most offer free sessions for enrolled students; search '[your university] counseling center'",
    "**Graduate Student Association** — many have mental health advocates or peer support programs",
    "**Student Health Services** — can refer to psychiatry for medication if needed",
    "**Ombudsman Office** — confidential advisor for advisor/department conflicts",
    "**Graduate Division Dean of Students** — escalation path for serious program issues",
]

ONLINE_THERAPY = [
    "**BetterHelp** (betterhelp.com) — affordable weekly therapy, sliding scale",
    "**Open Path Collective** (openpathcollective.org) — $30–$80/session for students",
    "**7 Cups** (7cups.com) — free peer support + paid therapy",
]


def get_crisis_block() -> str:
    """Returns a formatted markdown block with immediate crisis resources."""
    return (
        "\n\n---\n"
        "**If you're in crisis right now:**\n"
        "- 📞 Call or text **988** (US Suicide & Crisis Lifeline — 24/7, free)\n"
        "- 💬 Text **HOME** to **741741** (Crisis Text Line — 24/7)\n"
        "- 🌍 [Find local crisis line](https://www.iasp.info/resources/Crisis_Centres/)\n\n"
        "You don't have to face this alone. These are free and confidential.\n"
        "---"
    )


def get_all_crisis_lines() -> dict:
    return CRISIS_LINES


def get_campus_resources() -> list:
    return CAMPUS_RESOURCES

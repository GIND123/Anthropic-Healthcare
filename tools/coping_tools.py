"""
Evidence-based coping technique library, tuned for PhD / graduate student context.
All content is structured for easy injection into LLM tool responses.
"""

BREATHING = {
    "box": {
        "name": "Box Breathing (4-4-4-4)",
        "tagline": "Calm your nervous system in under 4 minutes",
        "steps": [
            "Find a comfortable position and exhale completely",
            "**Inhale** slowly through your nose for **4 counts**",
            "**Hold** at the top for **4 counts**",
            "**Exhale** through your mouth for **4 counts**",
            "**Hold** at the bottom for **4 counts**",
            "Repeat 4–6 cycles",
        ],
        "best_for": ["pre-exam anxiety", "meeting with advisor", "acute stress", "focus reset"],
        "duration": "4 minutes",
        "science": "Activates the parasympathetic nervous system, counteracting the fight-or-flight response",
    },
    "478": {
        "name": "4-7-8 Breathing",
        "tagline": "For sleep and deep anxiety relief",
        "steps": [
            "Exhale completely through your mouth",
            "**Inhale** quietly through your nose for **4 counts**",
            "**Hold** your breath for **7 counts**",
            "**Exhale** completely through your mouth for **8 counts**",
            "Repeat only 3–4 cycles (no more)",
        ],
        "best_for": ["falling asleep", "panic", "deep anxiety", "after a hard conversation"],
        "duration": "3 minutes",
        "science": "Extended exhale activates the vagal brake, rapidly reducing heart rate and cortisol",
    },
    "physiological_sigh": {
        "name": "Physiological Sigh",
        "tagline": "Fastest stress reset — takes 30 seconds",
        "steps": [
            "Take a deep inhale through your nose",
            "At the top of that breath, sniff once more to fully inflate your lungs",
            "Exhale slowly and completely through your mouth",
            "Repeat 1–3 times",
        ],
        "best_for": ["between tasks", "quick reset", "during a stressful moment", "lab frustration"],
        "duration": "30 seconds",
        "science": "Reinflates collapsed alveoli and triggers an immediate parasympathetic response — fastest known breath technique for stress",
    },
}

GROUNDING = {
    "54321": {
        "name": "5-4-3-2-1 Sensory Grounding",
        "tagline": "Anchor yourself in the present moment",
        "steps": [
            "Look around and name **5 things you can see**",
            "Notice and touch **4 things you can feel** (desk, chair, phone...)",
            "Listen and identify **3 things you can hear**",
            "Notice **2 things you can smell** (or recall a favourite scent)",
            "Notice **1 thing you can taste**",
        ],
        "best_for": ["anxiety spiral", "dissociation", "panic", "overwhelm", "before a presentation"],
        "duration": "5 minutes",
    },
    "safe_place": {
        "name": "Safe Place Visualisation",
        "tagline": "Create a mental sanctuary you can return to",
        "steps": [
            "Close your eyes and take 3 slow breaths",
            "Picture a place — real or imagined — where you feel completely safe",
            "Notice what you *see* there: colours, light, shapes",
            "Notice what you *hear*: silence, water, birds, music",
            "Notice what you *feel*: warmth, breeze, texture",
            "Stay for 5 minutes, then slowly return",
        ],
        "best_for": ["chronic stress", "before sleep", "emotional overwhelm"],
        "duration": "5–10 minutes",
    },
    "cold_water": {
        "name": "Cold Water Reset",
        "tagline": "Activate your dive reflex instantly",
        "steps": [
            "Fill a bowl with cold water, or run cold water from the tap",
            "Submerge your face for 15–30 seconds, OR hold an ice cube in each hand",
            "This triggers the mammalian dive reflex, rapidly slowing heart rate",
            "Breathe slowly when you come up",
        ],
        "best_for": ["panic attack", "emotional flooding", "intense distress", "rage or frustration"],
        "duration": "2 minutes",
    },
}

STUDY = {
    "pomodoro": {
        "name": "Pomodoro Technique",
        "tagline": "Work in focused 25-minute sprints",
        "steps": [
            "Choose **one task only** — write it on a sticky note",
            "Set a timer for **25 minutes** and work on nothing else",
            "When the timer rings, take a **5-minute break** (stand, stretch, breathe)",
            "After **4 rounds**, take a **20–30 minute break**",
            "Track your pomodoros to build an honest picture of your pace",
        ],
        "best_for": ["procrastination", "distraction", "large writing tasks", "analysis paralysis"],
        "tips": [
            "Turn off all notifications during the pomodoro",
            "If an intrusive thought comes up, jot it on a 'later' list and return to work",
            "Start with just 2 pomodoros if 4 feels impossible — momentum matters more than perfection",
        ],
    },
    "active_recall": {
        "name": "Active Recall + Spaced Repetition",
        "tagline": "The most evidence-backed way to retain information",
        "steps": [
            "Read or study a section",
            "Close your notes completely",
            "Write or say everything you remember (don't peek)",
            "Check what you missed",
            "Review only the gaps, then repeat",
            "Space your repetitions: next day → 3 days → 1 week → 2 weeks",
        ],
        "best_for": ["exam prep", "reading comprehension", "literature review retention"],
        "science": "Retrieval practice strengthens memory consolidation more than re-reading by a factor of 2–4x",
    },
    "feynman": {
        "name": "Feynman Technique",
        "tagline": "If you can't explain it simply, you don't know it yet",
        "steps": [
            "Write the concept at the top of a blank page",
            "Explain it in **simple language** as if teaching a curious 12-year-old",
            "Identify the gaps — places where your explanation breaks down or gets vague",
            "Go back to source material to fill exactly those gaps",
            "Simplify again using analogies and concrete examples",
        ],
        "best_for": ["deep understanding", "thesis writing", "conference talks", "complex theory"],
    },
    "mind_map": {
        "name": "Mind Mapping",
        "tagline": "Visual thinking for complex, interconnected ideas",
        "steps": [
            "Write the main topic in the **centre** of a blank page",
            "Draw branches for each major subtopic",
            "Add sub-branches with details and examples",
            "Use **different colours** for different themes",
            "Keep nodes to **1–2 keywords** — no full sentences",
            "Connect related ideas across branches with dotted lines",
        ],
        "best_for": ["literature review structure", "thesis chapter planning", "brainstorming", "proposal writing"],
    },
    "deep_work": {
        "name": "Deep Work Blocks",
        "tagline": "Protect 3–4 hours of uninterrupted cognitive time",
        "steps": [
            "Identify your **peak cognitive window** (morning for most people)",
            "Block 3–4 hours daily as a non-negotiable deep work block",
            "Set phone to Do Not Disturb; close email, Slack, everything",
            "Work on your hardest, most cognitively demanding task ONLY",
            "Do shallow work (email, admin) in a separate window",
        ],
        "best_for": ["thesis writing", "complex analysis", "paper writing", "grant applications"],
        "science": "Cal Newport's research shows 4 hours of deep work produces more than 8 hours of fragmented work",
    },
}

TIME_MANAGEMENT = {
    "time_blocking": {
        "name": "Time Blocking",
        "tagline": "Give every hour of your week a purpose",
        "steps": [
            "Sunday evening: list ALL tasks and deadlines for the week",
            "Estimate realistic time for each (multiply your gut estimate by 1.5)",
            "Block time in your calendar — include meals, transit, breaks",
            "Add a **daily buffer block** (30–60 min) for unexpected things",
            "Protect your blocks — treat them like external appointments",
            "End of day: spend 5 minutes adjusting tomorrow",
        ],
        "best_for": ["multiple deadlines", "work-life balance", "feeling reactive instead of proactive"],
    },
    "priority_matrix": {
        "name": "Eisenhower Priority Matrix",
        "tagline": "Separate urgent from important — they are not the same",
        "steps": [
            "List all your current tasks",
            "Sort into 4 quadrants:\n  **Q1** Urgent + Important → Do now\n  **Q2** Not urgent + Important → Schedule (this is where PhD progress lives)\n  **Q3** Urgent + Not important → Delegate or minimise\n  **Q4** Not urgent + Not important → Eliminate",
            "The key insight: most people live in Q1 and Q3. **PhD progress lives in Q2.**",
            "Block Q2 time first, before Q3 fills your calendar",
        ],
        "best_for": ["overwhelm", "reactive mode", "poor prioritisation", "too many meetings"],
    },
    "two_minute": {
        "name": "2-Minute Rule",
        "tagline": "If it takes under 2 minutes, do it now — not later",
        "steps": [
            "When a task lands (email, request, thought), ask: 'Can I do this in under 2 minutes?'",
            "If **yes**: do it immediately — don't write it down, don't schedule it",
            "If **no**: schedule it properly in your calendar or task list",
            "This clears 'mental RAM' and prevents backlog of tiny unfinished things",
        ],
        "best_for": ["email overwhelm", "task backlog", "decision fatigue"],
    },
}

SLEEP = {
    "schedule": {
        "tip": "**Consistent wake time** is the single most important sleep habit. Same time every day — even weekends. This anchors your circadian rhythm.",
        "effort": "low",
    },
    "screens": {
        "tip": "**Screen sunset 1 hour before bed.** Blue light from screens suppresses melatonin by up to 50%. Use Night Shift or f.lux if you must use screens.",
        "effort": "low",
    },
    "temperature": {
        "tip": "**Cool room = better sleep.** Your body needs to drop core temperature to fall asleep. Optimal range: 18–20°C (65–68°F).",
        "effort": "low",
    },
    "caffeine": {
        "tip": "**Caffeine curfew at 2pm.** Caffeine has a 5–6 hour half-life — an afternoon coffee is still 50% active at midnight.",
        "effort": "low",
    },
    "brain_dump": {
        "tip": "**Write tomorrow's top 3 tasks before bed.** This offloads 'open loops' from your working memory and reduces the mental chatter that keeps you awake.",
        "effort": "low",
    },
    "cant_sleep": {
        "tip": "**If you can't fall asleep in 20 minutes, get up.** Do something calm in dim light (read, stretch, meditate). Only return to bed when genuinely sleepy. Lying awake in bed trains your brain that bed = wakefulness.",
        "effort": "medium",
    },
    "morning_light": {
        "tip": "**5–10 minutes of outdoor light within 1 hour of waking** sets your circadian clock for the day. This is the most powerful natural sleep signal.",
        "effort": "low",
    },
}

PHD_SPECIFIC = {
    "imposter_syndrome": {
        "name": "Reframing Imposter Syndrome",
        "tagline": "Almost every PhD student feels this — you're not broken",
        "reframes": [
            "Imposter syndrome is actually a sign of **metacognitive awareness** — you know enough to know what you don't know. Beginners don't feel it.",
            "Your advisor accepted you because they saw your potential — they've read thousands of applications and chose yours.",
            "The feeling of 'not belonging' often reflects the **culture** of academia (competitive, perfectionistic) more than your actual ability.",
            "Research shows imposter syndrome is most common in **high-achieving, conscientious people** — not low performers.",
        ],
        "cbt_exercise": "Write down one piece of evidence that contradicts your imposter narrative (e.g., a paper you got through, a concept you taught someone, a problem you solved).",
    },
    "advisor_conflict": {
        "name": "Navigating Difficult Advisor Dynamics",
        "tagline": "The most common and most undertalked PhD challenge",
        "strategies": [
            "**Document everything.** After verbal conversations, send a brief email summary: 'Following up on our conversation — my understanding is X. Please let me know if I've misunderstood.'",
            "**Name the meta-conversation.** 'I'd like to talk about how we're communicating, not just the research.' Many advisors don't realise there's a problem.",
            "**Use your committee.** Committee members are *supposed* to be a resource, not just evaluators. A co-advisor or trusted committee member can mediate.",
            "**Graduate Ombudsman.** Completely confidential. Not on your record. Can help you think through options without committing to any action.",
            "**It is not always your fault.** Advisor issues are structural — they are not trained managers, have perverse incentives, and often replicate what was done to them.",
        ],
    },
    "research_block": {
        "name": "Breaking Through Research Stagnation",
        "tagline": "When the work isn't going anywhere",
        "strategies": [
            "**Change your input.** Read one paper outside your field. Talk to someone in a different lab. Go to a seminar. Novel input breaks stale thinking.",
            "**Rubber duck debugging.** Explain your problem out loud to an inanimate object (seriously). The act of articulating it often reveals the path forward.",
            "**Lower the stakes.** Write 'bad' code or 'bad' text for 20 minutes. Perfectionism is often the blocker, not lack of ideas.",
            "**Timeboxed exploration.** Give yourself 2 hours to explore a dead-end idea fully. Knowing it's bounded makes it feel safe.",
            "**Talk to your future self.** Write a letter from yourself 5 years from now. What does she/he tell you about this moment?",
        ],
    },
}


def get_technique(category: str, key: str = "") -> dict:
    """Get a technique from the library by category and optional key."""
    libraries = {
        "breathing": BREATHING,
        "grounding": GROUNDING,
        "study": STUDY,
        "time_management": TIME_MANAGEMENT,
        "phd": PHD_SPECIFIC,
    }
    lib = libraries.get(category, {})
    if key and key in lib:
        return lib[key]
    if lib:
        return lib[next(iter(lib))]
    return {}


def list_techniques(category: str) -> list:
    """List available technique keys for a category."""
    libraries = {
        "breathing": BREATHING,
        "grounding": GROUNDING,
        "study": STUDY,
        "time_management": TIME_MANAGEMENT,
        "phd": PHD_SPECIFIC,
    }
    return list(libraries.get(category, {}).keys())

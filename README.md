# Anima — Student Wellbeing Companion

> **Hackathon Track:** Health and Wellbeing · Anthropic

A multi-agent chatbot that detects stress and burnout patterns in students — undergrads, grad students, and PhDs — and routes them to the right support before crisis hits. Powered by Gemini 2.5 Flash, a four-agent pipeline, a counsellor booking system, and a full dashboard — all running locally with Flask.

---

## The Problem in One Sentence

Academic stress compounds silently. By the time someone asks for help, they've been struggling for months.

### Who it Affects

| Role | Core Stressors |
|---|---|
| **Undergrad** | Exam anxiety, social isolation, major uncertainty, financial pressure |
| **Grad / PhD** | Advisor conflict, research stagnation, publication pressure, imposter syndrome, funding |
| **All students** | Sleep disruption, motivation loss, procrastination, deadline overload |

### Why Existing Tools Fail

- University counseling has 3–6 week waitlists
- Generic apps (Calm, Headspace) don't understand academic context
- Chatbots without memory can't detect *patterns* — one bad week looks the same as six
- No system connects emotional signals to *specific* campus resources

---

## What Anima Does

1. **Multi-agent routing** — Orchestrator classifies each message and sends it to the right specialist agent (Crisis / Support / Wellness)
2. **Pattern detection** — Mood scores are logged per session; the Dashboard shows trends over time
3. **Inline resource cards** — When an agent recommends a technique, a structured card appears in-chat with step-by-step instructions
4. **Counsellor booking** — Browse six campus counsellors, filter by specialty, and book an appointment slot — all from the app
5. **Safe escalation** — Hard-coded crisis guard surfaces 988 + text line instantly on any crisis signal
6. **Calendar** — All booked appointments appear on a monthly calendar with full event list

---

## System Architecture

```
User (Browser)
    │
    ▼
Flask App (app.py)
    │
    ▼
Orchestrator
    ├── CrisisAgent      ← runs first, always; keyword + LLM classification
    │       └── If crisis → warm response + 988 block; stops pipeline
    ├── SupportAgent     ← emotional support, CBT/ACT, coping techniques (tool use)
    └── WellnessAgent    ← study strategies, sleep hygiene, time management (tool use)

Tools (called automatically by Gemini function calling)
    ├── get_coping_technique(category, key)
    ├── assess_student_stress(text)
    ├── get_study_technique(challenge)
    ├── get_time_management_advice(problem)
    ├── get_sleep_tip(issue)
    └── get_breathing_exercise(purpose)

Session Storage
    ├── data/sessions/{session_id}.json   ← mood log + message history
    └── data/appointments.json            ← booked counsellor appointments
```

---

## Four-Tab SPA

| Tab | What it does |
|---|---|
| **Chat** | Conversational agent with agent-step ticker, inline technique cards, quick-reply chips |
| **Dashboard** | Stat grid (messages, mood entries, avg mood), Chart.js mood trend line, upcoming appointments |
| **Calendar** | Monthly grid view with appointments on dates; prev/next/today navigation |
| **Find a Counsellor** | Six dummy counsellors with filter chips (free / online / nearby), slot grid, booking modal |

---

## Agent Design

### Orchestrator
- Entry point for every message
- Crisis check → agent classification → route to specialist → build inline cards → log mood
- Returns: `response`, `agent_type`, `crisis_detected`, `cards`, `quick_replies`, `agent_steps`, `mood_score`

### Crisis Agent
- **Runs first, always — no bypass**
- Keyword pattern match (fast path) for high-certainty crisis signals
- LLM fallback (`application/json` response) for ambiguous signals
- If triggered: warm empathetic response + 988 Lifeline + Crisis Text Line + IASP link

### Support Agent
- Emotional support using CBT, ACT, and Motivational Interviewing principles
- Gemini automatic function calling → `get_coping_technique`, `assess_student_stress`
- System prompt covers all student types; validates first, never diagnoses
- Maintains session context (last 5 turns)

### Wellness Agent
- Practical skills: study techniques, sleep hygiene, time management, breathing exercises
- Gemini automatic function calling → `get_study_technique`, `get_time_management_advice`, `get_sleep_tip`, `get_breathing_exercise`
- Pulls structured technique data from the coping library and injects it into the response

---

## Inline Technique Cards

When the agent response mentions a specific technique (e.g. "box breathing", "Pomodoro", "Feynman"), the UI renders a collapsible card below the message with:
- Technique name, tagline, duration
- Step-by-step instructions (expandable)
- Science note where available

Detection is done server-side via `_TECHNIQUE_MAP` — a keyword → `(category, key)` mapping evaluated against the lowercased response before it leaves the Orchestrator.

---

## Knowledge Library (`tools/coping_tools.py`)

| Category | Techniques |
|---|---|
| `breathing` | Box breathing, 4-7-8, Physiological sigh |
| `grounding` | 5-4-3-2-1 sensory, Safe place visualisation, Cold water reset |
| `study` | Pomodoro, Active recall + spaced repetition, Feynman, Mind mapping, Deep work |
| `time_management` | Time blocking, Eisenhower matrix, 2-minute rule |
| `phd` | Reframing imposter syndrome, Advisor conflict strategies, Research block |
| `sleep` | Consistent wake time, Screen sunset, Caffeine curfew, Brain dump |

---

## Repository Structure

```
Anthropic-Healthcare/
├── app.py                          # Flask entry point + all API routes
├── requirements.txt
├── .env.example
│
├── agents/
│   ├── orchestrator.py             # Routes messages across agents
│   ├── crisis_agent.py             # Crisis detection + response
│   ├── support_agent.py            # Emotional support (tool use)
│   └── wellness_agent.py           # Practical wellness skills (tool use)
│
├── tools/
│   ├── session_tools.py            # Session + appointment CRUD (JSON files)
│   ├── assessment.py               # Crisis level detection, stress scoring
│   ├── coping_tools.py             # Full evidence-based technique library
│   ├── resources.py                # Crisis lines by region
│   └── counsellors.py              # Dummy counsellor data + slot generation
│
├── templates/
│   └── index.html                  # Single-page app (Chat / Dashboard / Calendar / Find)
│
└── data/
    ├── sessions/                   # {session_id}.json — per-session mood + history
    └── appointments.json           # All booked appointments
```

---

## Quick Start

```bash
git clone https://github.com/GIND123/Anthropic-Healthcare
cd Anthropic-Healthcare
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Add your GEMINI_API_KEY to .env

PORT=5001 python app.py
```

Open `http://127.0.0.1:5001` in your browser.

> **Note for macOS users:** Port 5000 is occupied by AirPlay Receiver. Always use `PORT=5001`.

---

## API Routes

| Method | Route | Purpose |
|---|---|---|
| `GET` | `/` | Serve the SPA |
| `POST` | `/api/chat` | Send a message, get agent response |
| `POST` | `/api/clear` | Clear session history |
| `GET` | `/api/session` | Get current session stats |
| `GET` | `/api/dashboard` | Mood trend data for Chart.js |
| `GET` | `/api/counsellors` | All counsellors with next available slot |
| `GET` | `/api/counsellors/<id>/slots` | Available slots for one counsellor |
| `GET/POST` | `/api/appointments` | List or create appointments |
| `DELETE` | `/api/appointments/<id>` | Cancel an appointment |

---

## Tech Stack

| Layer | Choice | Why |
|---|---|---|
| UI | Flask + vanilla JS | Zero build step, ships in minutes |
| LLM | Gemini 2.5 Flash (`google-genai` SDK) | Fast, cost-efficient, native function calling |
| Agent orchestration | Custom Python pipeline | Full control, no framework overhead |
| Tool execution | Gemini automatic function calling | Agent decides when to call tools |
| Knowledge base | Plain Python dicts (`coping_tools.py`) | No vector DB needed for demo |
| Session storage | Local JSON files | Simple, persistent across restarts |
| Charts | Chart.js 4 (CDN) | No npm required |
| Markdown rendering | marked.js 9 (CDN) | Rich agent responses in chat bubbles |

---

## Safety Design

**Hard rules — no exceptions:**
- Never diagnose mental illness
- Never give medical advice
- Always surface 988 when crisis signals detected
- Crisis agent runs before any other agent — it cannot be bypassed

**Crisis threshold:** any of — `suicidal ideation`, `self-harm`, `hopelessness severe`, `"I want to disappear"` pattern → immediate 988 surface + session flag.

---

## What's Not in Scope (Hackathon Cut)

- Real university database integration
- Persistent multi-user auth / login
- Push notifications or reminders
- Multilingual support
- IRB-approved deployment

---

## References

- Evans et al., *Nature Biotechnology*, 2018 — graduate student mental health survey
- Levecque et al., *Research Policy*, 2017 — PhD mental health risk factors
- [Gemini API Docs](https://ai.google.dev/gemini-api/docs)
- [988 Suicide & Crisis Lifeline](https://988lifeline.org)
- [Crisis Text Line](https://www.crisistextline.org)

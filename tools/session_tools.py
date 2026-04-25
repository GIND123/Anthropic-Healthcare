import json
import uuid
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
SESSIONS_DIR = DATA_DIR / "sessions"
APPOINTMENTS_FILE = DATA_DIR / "appointments.json"

SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)


# ── Session helpers ──────────────────────────────────────────────────────────

def _session_path(session_id: str) -> Path:
    return SESSIONS_DIR / f"{session_id}.json"


def load_session(session_id: str) -> dict:
    p = _session_path(session_id)
    if p.exists():
        with open(p) as f:
            return json.load(f)
    return {
        "session_id": session_id,
        "created_at": datetime.now().isoformat(),
        "history": [],
        "mood_log": [],
    }


def save_session(session_id: str, data: dict) -> None:
    data["updated_at"] = datetime.now().isoformat()
    with open(_session_path(session_id), "w") as f:
        json.dump(data, f, indent=2)


def log_mood(session_id: str, score: int, label: str) -> None:
    data = load_session(session_id)
    data.setdefault("mood_log", []).append({
        "ts": datetime.now().isoformat(),
        "score": score,
        "label": label,
    })
    save_session(session_id, data)


def get_session_stats(session_id: str) -> dict:
    data = load_session(session_id)
    mood_log = data.get("mood_log", [])
    avg = round(sum(e["score"] for e in mood_log) / len(mood_log), 1) if mood_log else None
    return {
        "message_count": len(data.get("history", [])),
        "mood_entries": len(mood_log),
        "avg_mood": avg,
        "session_start": data.get("created_at", ""),
        "last_active": data.get("updated_at", ""),
        "mood_log": mood_log,
    }


# ── Appointments helpers ─────────────────────────────────────────────────────

def _load_appointments() -> list:
    if APPOINTMENTS_FILE.exists():
        with open(APPOINTMENTS_FILE) as f:
            return json.load(f)
    return []


def _save_appointments(appts: list) -> None:
    with open(APPOINTMENTS_FILE, "w") as f:
        json.dump(appts, f, indent=2)


def add_appointment(counsellor_id: str, counsellor_name: str,
                    date: str, time: str, note: str = "") -> dict:
    appts = _load_appointments()
    appt = {
        "id": str(uuid.uuid4())[:8],
        "counsellor_id": counsellor_id,
        "counsellor_name": counsellor_name,
        "date": date,
        "time": time,
        "note": note,
        "status": "confirmed",
        "created_at": datetime.now().isoformat(),
    }
    appts.append(appt)
    _save_appointments(appts)
    return appt


def get_appointments(upcoming_only: bool = False) -> list:
    appts = _load_appointments()
    if upcoming_only:
        today = datetime.now().strftime("%Y-%m-%d")
        appts = [a for a in appts if a["date"] >= today]
    return sorted(appts, key=lambda a: (a["date"], a["time"]))


def cancel_appointment(appt_id: str) -> bool:
    appts = _load_appointments()
    for a in appts:
        if a["id"] == appt_id:
            a["status"] = "cancelled"
            _save_appointments(appts)
            return True
    return False

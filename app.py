"""
Anima — Student Wellbeing Companion
Flask application
"""

import os
import uuid
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "anima-dev-secret-2024")

api_key = os.getenv("GEMINI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")

from agents.orchestrator import Orchestrator
from tools.session_tools import (
    get_session_stats, log_mood,
    add_appointment, get_appointments, cancel_appointment,
)
from tools.counsellors import COUNSELLORS, get_slots, get_counsellor_list_with_next_slot

orchestrator = Orchestrator(api_key=api_key) if api_key else None


def _sid():
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
    return session["session_id"]


# ── Pages ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    _sid()
    return render_template("index.html")


@app.route("/healthz")
def healthz():
    return jsonify({
        "status": "ok",
        "model_configured": bool(api_key),
    })


# ── Chat ─────────────────────────────────────────────────────────────────────

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    if not message:
        return jsonify({"error": "Empty message"}), 400
    if orchestrator is None:
        return jsonify({
            "response": (
                "Anima is online, but the model API key is not configured yet. "
                "Add GEMINI_API_KEY in the Render service environment and redeploy."
            ),
            "agent_type": "support",
            "crisis_detected": False,
            "cards": [],
            "quick_replies": ["Configure GEMINI_API_KEY", "Try again later"],
            "agent_steps": ["App is healthy", "Model key missing"],
            "mood_score": 3,
        }), 503
    try:
        result = orchestrator.process(message, _sid())
        return jsonify(result)
    except Exception as e:
        app.logger.error("Orchestrator error: %s", e, exc_info=True)
        return jsonify({
            "response": "Something went wrong on my end — please try again.",
            "agent_type": "support",
            "crisis_detected": False,
            "cards": [],
            "quick_replies": [],
            "agent_steps": [],
            "mood_score": 3,
        })


@app.route("/api/clear", methods=["POST"])
def clear():
    session["session_id"] = str(uuid.uuid4())
    return jsonify({"status": "cleared"})


# ── Dashboard ─────────────────────────────────────────────────────────────────

@app.route("/api/dashboard", methods=["GET"])
def dashboard():
    stats = get_session_stats(_sid())
    upcoming = get_appointments(upcoming_only=True)[:5]

    # Build 7-day mood timeline (real + fill gaps with None)
    mood_log = stats.get("mood_log", [])
    today = datetime.now().date()
    day_scores: dict = {}
    for entry in mood_log:
        try:
            d = datetime.fromisoformat(entry["ts"]).date()
            day_scores.setdefault(str(d), []).append(entry["score"])
        except Exception:
            pass

    timeline = []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        key = str(d)
        scores = day_scores.get(key, [])
        avg = round(sum(scores) / len(scores), 1) if scores else None
        timeline.append({"date": key, "label": d.strftime("%a"), "score": avg})

    return jsonify({
        "message_count": stats["message_count"],
        "avg_mood": stats["avg_mood"],
        "mood_timeline": timeline,
        "upcoming_appointments": upcoming,
        "session_start": stats["session_start"],
    })


# ── Counsellors ───────────────────────────────────────────────────────────────

@app.route("/api/counsellors", methods=["GET"])
def counsellors():
    booked = get_appointments()
    data = get_counsellor_list_with_next_slot(booked)
    return jsonify({"counsellors": data})


@app.route("/api/counsellors/<counsellor_id>/slots", methods=["GET"])
def counsellor_slots(counsellor_id):
    booked = get_appointments()
    booked_keys = {
        f"{a['date']}_{a['time']}"
        for a in booked
        if a.get("counsellor_id") == counsellor_id and a.get("status") != "cancelled"
    }
    slots = get_slots(counsellor_id, booked_keys)
    return jsonify({"slots": slots})


# ── Appointments ──────────────────────────────────────────────────────────────

@app.route("/api/appointments", methods=["GET"])
def list_appointments():
    upcoming = request.args.get("upcoming", "false").lower() == "true"
    return jsonify({"appointments": get_appointments(upcoming_only=upcoming)})


@app.route("/api/appointments", methods=["POST"])
def book_appointment():
    data = request.get_json(silent=True) or {}
    cid = data.get("counsellor_id", "")
    date = data.get("date", "")
    time = data.get("time", "")
    note = data.get("note", "")

    if not all([cid, date, time]):
        return jsonify({"error": "counsellor_id, date, and time are required"}), 400

    c = next((x for x in COUNSELLORS if x["id"] == cid), None)
    if not c:
        return jsonify({"error": "Unknown counsellor"}), 404

    appt = add_appointment(cid, c["name"], date, time, note)
    return jsonify({"appointment": appt}), 201


@app.route("/api/appointments/<appt_id>", methods=["DELETE"])
def delete_appointment(appt_id):
    ok = cancel_appointment(appt_id)
    return jsonify({"status": "cancelled" if ok else "not_found"})


# ── Run ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=True)

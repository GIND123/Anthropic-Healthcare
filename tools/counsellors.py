"""
Dummy counsellor data with slot generation.
All data is fictional and for demonstration purposes only.
"""

from datetime import datetime, timedelta

COUNSELLORS = [
    {
        "id": "dr_sarah_chen",
        "name": "Dr. Sarah Chen",
        "initials": "SC",
        "credentials": "PhD, Licensed Psychologist",
        "specialty": ["Anxiety", "Academic Burnout", "Imposter Syndrome", "CBT"],
        "approaches": ["Cognitive Behavioural Therapy", "Mindfulness-Based Therapy", "ACT"],
        "location": "Student Wellness Center, Room 204",
        "distance_miles": 0.3,
        "rating": 4.9,
        "review_count": 48,
        "available": True,
        "free_for_students": True,
        "online_available": False,
        "color": "#667eea",
        "bio": "Dr. Chen specialises in helping students navigate academic pressure, anxiety, and imposter syndrome using evidence-based CBT with a warm, non-judgmental approach.",
        "slot_days": [1, 3, 4],
        "slot_times": ["10:00", "11:00", "14:00", "15:30"],
    },
    {
        "id": "dr_marcus_williams",
        "name": "Dr. Marcus Williams",
        "initials": "MW",
        "credentials": "PsyD, Licensed Counsellor",
        "specialty": ["Depression", "Grief", "Life Transitions", "Relationships"],
        "approaches": ["Psychodynamic Therapy", "CBT", "Narrative Therapy"],
        "location": "Health & Wellness Building, Suite 310",
        "distance_miles": 0.8,
        "rating": 4.7,
        "review_count": 35,
        "available": True,
        "free_for_students": True,
        "online_available": True,
        "color": "#764ba2",
        "bio": "Dr. Williams brings warmth and depth to his work with students navigating depression, grief, and major life transitions. He integrates psychodynamic insight with practical tools.",
        "slot_days": [0, 2, 4],
        "slot_times": ["09:00", "11:30", "14:30", "16:00"],
    },
    {
        "id": "dr_priya_patel",
        "name": "Dr. Priya Patel",
        "initials": "PP",
        "credentials": "PhD, Counselling Psychologist",
        "specialty": ["Cultural Adjustment", "International Students", "Identity", "Anxiety"],
        "approaches": ["Culturally Informed CBT", "Mindfulness", "Narrative Therapy"],
        "location": "International Student Services, Room 118",
        "distance_miles": 0.5,
        "rating": 4.8,
        "review_count": 52,
        "available": True,
        "free_for_students": True,
        "online_available": True,
        "color": "#f093fb",
        "bio": "Dr. Patel specialises in supporting international students and students from diverse backgrounds navigating cultural transitions, identity questions, and academic pressures.",
        "slot_days": [1, 2, 4],
        "slot_times": ["10:30", "13:00", "15:00", "16:30"],
    },
    {
        "id": "dr_james_rodriguez",
        "name": "Dr. James Rodriguez",
        "initials": "JR",
        "credentials": "PhD, Licensed Psychologist",
        "specialty": ["ADHD", "Academic Stress", "Executive Function", "Procrastination"],
        "approaches": ["DBT", "Coaching Psychology", "Mindfulness"],
        "location": "Academic Support Center, 2nd Floor",
        "distance_miles": 1.2,
        "rating": 4.6,
        "review_count": 29,
        "available": True,
        "free_for_students": False,
        "online_available": True,
        "color": "#4facfe",
        "bio": "Dr. Rodriguez helps students with attention challenges, procrastination, and executive function. His coaching psychology approach centres on practical strategies and self-compassion.",
        "slot_days": [0, 3, 4],
        "slot_times": ["08:30", "10:00", "13:30", "15:00"],
    },
    {
        "id": "dr_emily_foster",
        "name": "Dr. Emily Foster",
        "initials": "EF",
        "credentials": "PsyD, Trauma-Informed Therapist",
        "specialty": ["Trauma", "PTSD", "Burnout Recovery", "Chronic Stress"],
        "approaches": ["EMDR", "Trauma-Informed CBT", "Somatic Therapy"],
        "location": "Community Mental Health Clinic",
        "distance_miles": 2.4,
        "rating": 4.9,
        "review_count": 67,
        "available": True,
        "free_for_students": False,
        "online_available": True,
        "color": "#43e97b",
        "bio": "Dr. Foster is a trauma specialist working with students recovering from burnout, adverse experiences, and high-stress environments. She uses EMDR and somatic approaches.",
        "slot_days": [1, 3],
        "slot_times": ["11:00", "13:00", "15:00", "17:00"],
    },
    {
        "id": "dr_aisha_thompson",
        "name": "Dr. Aisha Thompson",
        "initials": "AT",
        "credentials": "MSc, LCSW",
        "specialty": ["Social Anxiety", "Relationships", "Communication", "Self-Esteem"],
        "approaches": ["CBT", "Social Skills Training", "ACT"],
        "location": "Student Union Building, Room 22B",
        "distance_miles": 0.6,
        "rating": 4.8,
        "review_count": 41,
        "available": True,
        "free_for_students": True,
        "online_available": True,
        "color": "#fa709a",
        "bio": "Dr. Thompson helps students develop social confidence, navigate relationship challenges, and overcome anxiety in academic and social settings.",
        "slot_days": [0, 2, 3],
        "slot_times": ["09:30", "11:00", "14:00", "16:00"],
    },
]


def get_slots(counsellor_id: str, booked_keys: set = None) -> list:
    """Generate available appointment slots for the next 14 days."""
    c = next((x for x in COUNSELLORS if x["id"] == counsellor_id), None)
    if not c:
        return []
    booked_keys = booked_keys or set()
    today = datetime.now()
    slots = []
    for i in range(1, 15):
        day = today + timedelta(days=i)
        if day.weekday() in c["slot_days"]:
            for t in c["slot_times"]:
                key = f"{day.strftime('%Y-%m-%d')}_{t}"
                if key not in booked_keys:
                    slots.append({
                        "key": key,
                        "date": day.strftime("%Y-%m-%d"),
                        "time": t,
                        "display": f"{day.strftime('%A, %b %d')} at {t}",
                        "day_label": day.strftime("%a %d"),
                    })
    return slots


def get_counsellor_list_with_next_slot(booked: list = None) -> list:
    """Return all counsellors with their next available slot pre-computed."""
    booked = booked or []
    booked_keys = {f"{a['date']}_{a['time']}" for a in booked if a.get("counsellor_id") == "x"}
    result = []
    for c in COUNSELLORS:
        c_booked = {f"{a['date']}_{a['time']}" for a in booked if a.get("counsellor_id") == c["id"]}
        slots = get_slots(c["id"], c_booked)
        entry = {k: v for k, v in c.items() if k not in ("slot_days", "slot_times")}
        entry["next_slot"] = slots[0]["display"] if slots else "No slots available"
        entry["next_slot_key"] = slots[0]["key"] if slots else None
        result.append(entry)
    return result

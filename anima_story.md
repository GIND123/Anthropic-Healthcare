# Anima: A PhD Survival Companion
### *Anthropic Hackathon — Health & Wellbeing Track*

---

## 💡 Inspiration

The PhD experience is one of the most intellectually demanding journeys a person can undertake — and one of the loneliest.

I've seen it firsthand at the University of Maryland: brilliant people slowly worn down by years of uncertain progress, invisible advisors, and the quiet dread of wondering *"Am I the only one struggling?"* Research consistently confirms what we already feel. Graduate students are **six times more likely** to experience depression and anxiety than the general population. The problem isn't weakness — it's that the system provides almost no structured emotional or cognitive support.

When Anthropic opened the **Health & Wellbeing** track with a focus on making healthcare less confusing and more accessible, one question immediately came to mind:

> *What if we could give every PhD student a compassionate, always-available companion that truly understood what they were going through?*

That became **Anima** — Latin for *soul*, and the quiet voice every PhD student deserves in their corner.

---

## 🧠 What We Built

Anima is an AI-powered PhD survival companion designed specifically for graduate students facing burnout, isolation, and mental health challenges. It provides:

- **Empathetic check-ins** — daily mood and stress tracking powered by conversational AI
- **Burnout early detection** — a lightweight ML model that identifies at-risk patterns before they escalate
- **Resource routing** — intelligently connects students to the right campus mental health services, peer support groups, or counseling centers
- **Advisor relationship coaching** — structured prompts to help students navigate difficult advisor dynamics
- **Anonymous community signals** — aggregated, privacy-preserving insights showing students they are *not alone*

The backend is built in **Python (Flask)**, using the **Claude API** for the conversational layer, with a **PyTorch** burnout risk model and **TensorFlow** for sentiment analysis of journal entries.

---

## 🔨 How We Built It

### Architecture Overview

```
User Input (Chat / Journal)
        │
        ▼
  Sentiment Analysis          ← TensorFlow NLP model
  (TF-IDF + LSTM)
        │
        ▼
  Burnout Risk Score          ← PyTorch classifier
        │
        ▼
  Claude API                  ← Empathetic response generation
  (System prompt tuned        with context injection
   for PhD context)
        │
        ▼
  Resource Router             ← Rule-based + semantic matching
        │
        ▼
  Response to User
```

### The Burnout Risk Model

We framed burnout detection as a binary classification problem. Given a feature vector $\mathbf{x} \in \mathbb{R}^d$ derived from a student's journal entries and check-in responses, our PyTorch model outputs a burnout risk score:

$$P(\text{burnout} \mid \mathbf{x}) = \sigma\left(\mathbf{w}^\top \phi(\mathbf{x}) + b\right)$$

where $\phi(\mathbf{x})$ is a learned embedding from a two-layer feedforward network and $\sigma$ is the sigmoid activation.

We trained on a publicly available **PhD student mental health survey dataset** (UCI) with features including:

- Self-reported stress levels $s_t \in [1, 10]$
- Sleep hours $h_t$
- Social interaction frequency
- Academic progress sentiment score $\hat{y}_t \in [-1, 1]$ (from TF sentiment model)

The composite risk index at time $t$ is a weighted rolling average:

$$R_t = \frac{\sum_{k=0}^{T} \lambda^k \cdot r_{t-k}}{\sum_{k=0}^{T} \lambda^k}, \quad \lambda \in (0, 1)$$

This exponential decay ensures **recent behavior weighs more heavily**, preventing a single bad week from permanently flagging a student as high-risk.

### Claude API Integration

The hardest design decision was making the Claude API responses feel **safe, warm, and appropriate** for someone in genuine distress — not clinical, not dismissive, and never overconfident about medical matters.

We engineered the system prompt around three principles:

1. **Validate first, advise second** — the model acknowledges feelings before offering any suggestions
2. **Never diagnose** — the assistant explicitly avoids clinical language and always defers to human professionals for medical concerns
3. **Soft escalation** — when burnout risk score exceeds a threshold $R_t > \tau$, the assistant gently surfaces campus crisis resources without alarming the user

```python
system_prompt = """
You are a compassionate companion for PhD students navigating stress,
isolation, and burnout. Your role is to listen, validate, and gently
support — never to diagnose or replace professional care. When a student
seems to be in distress, warmly encourage them to reach out to their
campus counseling center.
"""
```

---

## 🚧 Challenges We Faced

### 1. Making AI Responses Feel Safe

This was our biggest challenge. Early versions of the system were either **too clinical** (feeling like a symptom checker) or **too cheerful** (dismissively optimistic). We ran multiple rounds of prompt iteration, testing with peers and evaluating responses against a rubric of:

- Emotional validation
- Absence of unsolicited advice
- Appropriate escalation without alarmism
- Avoidance of diagnosis language

Achieving the right tone required treating the system prompt as a first-class engineering artifact — just as important as the model architecture.

### 2. Privacy and Sensitive Data

PhD students won't share their mental health struggles if they fear surveillance. We made the deliberate choice to **never store raw journal entries** — only the derived sentiment scores and risk indices. All data is processed in-session and anonymized before any aggregation.

### 3. Threshold Calibration

Setting the escalation threshold $\tau$ for the burnout risk score was non-trivial. Too low, and students get unsolicited crisis resources when they're just having a rough day. Too high, and genuinely at-risk students slip through. We used a validation set and prioritized **high recall** over precision — it's better to gently surface a resource one time too many than to miss someone who needs it:

$$\text{Recall} = \frac{TP}{TP + FN} \geq 0.90$$

### 4. Scope Creep Under Time Pressure

A hackathon is a sprint. We started with an ambitious list of features — peer support matching, advisor mediation tools, a wellness dashboard — and had to ruthlessly cut scope. The final product focuses on the core loop: **check in → assess → respond → route**. Everything else is a future roadmap item.

---

## 📚 What We Learned

- **Prompt engineering is as important as model engineering** when safety is the primary concern
- **PhD students are not a monolith** — international students, first-generation students, and students in experimental fields face structurally different stressors
- **Trust is the product** — no matter how good the AI is, students won't use it if they don't believe it's on their side
- Building with the **Claude API** gave us fine-grained control over tone and safety guardrails that would have taken weeks to replicate from scratch

---

## 🚀 What's Next

- Expand dataset with IRB-approved longitudinal check-in data
- Integrate with university counseling center APIs for real-time appointment booking
- Add multilingual support for international graduate students
- Explore federated learning so risk models can improve across institutions **without sharing any individual data**

---

## 🙏 Acknowledgments

Built at the **Anthropic Hackathon**, Health & Wellbeing Track.  
Powered by the **Claude API**, **PyTorch**, **TensorFlow**, and a lot of empathy.

> *"The PhD is a marathon, not a sprint. Anima is the water station nobody built until now."*

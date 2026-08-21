import os
import joblib


# ==========================================
# LOAD TRAINED ML MODEL
# ==========================================

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "models",
    "intent_model.pkl"
)

model = joblib.load(MODEL_PATH)


# ==========================================
# CLASSIFY INTENT
# ==========================================

def classify_intent(user_input):

    text = user_input.lower().strip()

    # ======================================
    # EXIT
    # ======================================

    if text in [
        "bye",
        "goodbye",
        "good bye",
        "see you",
        "see ya",
        "quit",
        "exit",
        "stop"
    ] or (
        text.startswith("bye")
        and len(text) <= 10
    ):

        return "exit"

    # ======================================
    # RECOMMENDATION
    # ======================================

    if any(
        phrase in text
        for phrase in [
            "recommend",
            "recommendation",
            "what do you recommend",
            "what should i do",
            "what should i focus on",
            "what can i improve",
            "how can i improve",
            "give me advice",
            "give me a suggestion",
            "suggestion",
            "suggest",
            "advice",
            "improve"
        ]
    ):

        return "recommendation"

    # ======================================
    # LOWEST
    # ======================================

    if any(
        phrase in text
        for phrase in [
            "what about the lowest",
            "what about lowest",
            "what is the lowest",
            "which is the lowest",
            "lowest one"
        ]
    ):

        return "lowest_subject"

    # ======================================
    # HIGHEST
    # ======================================

    if any(
        phrase in text
        for phrase in [
            "what about the highest",
            "what about highest",
            "what is the highest",
            "which is the highest",
            "highest one"
        ]
    ):

        return "highest_subject"

    # ======================================
    # HIGHEST / STRONGEST SUBJECT
    # ======================================

    if "subject" in text and (
        "highest" in text
        or "best" in text
        or "top" in text
        or "strongest" in text
        or "strong" in text
    ):

        return "highest_subject"

    # ======================================
    # LOWEST / WEAK SUBJECT
    # ======================================

    if "subject" in text and (
        "lowest" in text
        or "weak" in text
        or "weakest" in text
        or "worst" in text
    ):

        return "lowest_subject"

    # ======================================
    # ATTENDANCE
    # ======================================

    if any(
        word in text
        for word in [
            "attendance",
            "present",
            "absent"
        ]
    ):

        return "attendance"

    # ======================================
    # AVERAGE
    # ======================================

    if any(
        word in text
        for word in [
            "average",
            "overall mark",
            "overall marks"
        ]
    ):

        return "average"

    # ======================================
    # RISK
    # ======================================

    if any(
        word in text
        for word in [
            "risk",
            "at risk",
            "danger"
        ]
    ):

        return "risk"

    # ======================================
    # TREND
    # ======================================

    if any(
        word in text
        for word in [
            "improving",
            "trend",
            "progress",
            "getting better",
            "getting worse",
            "changed",
            "change",
            "compared to",
            "compared with",
            "previous",
            "earlier",
            "before",
            "last exam",
            "previous exam"
        ]
    ):

        return "trend"

    # ======================================
    # MARKS
    # ======================================

    if any(
        word in text
        for word in [
            "marks",
            "mark",
            "scores",
            "score",
            "results"
        ]
    ):

        return "marks"

    # ======================================
    # GENERAL PERFORMANCE
    # ======================================

    if any(
        word in text
        for word in [
            "performance",
            "performing",
            "doing"
        ]
    ):

        return "performance"

    # ======================================
    # ML FALLBACK
    # ======================================

    probabilities = model.predict_proba([text])[0]

    max_probability = max(probabilities)

    prediction = model.classes_[
        probabilities.argmax()
    ]

    CONFIDENCE_THRESHOLD = 0.55

    if max_probability >= CONFIDENCE_THRESHOLD:

        return prediction

    return "unknown"
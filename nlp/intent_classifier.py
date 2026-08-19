import os
from pydoc import text
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
    # RULE-BASED INTENTS
    # ======================================

    # Exit
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

    # Follow-up / short subject questions
    if any(phrase in text for phrase in [
    "what about the lowest",
    "what about lowest",
    "what is the lowest",
    "which is the lowest",
    "lowest one"
]):
       return "lowest_subject"

    if any(phrase in text for phrase in [
    "what about the highest",
    "what about highest",
    "what is the highest",
    "which is the highest",
    "highest one"
]):
      return "highest_subject"


    # Highest / strongest subject
    if "subject" in text and (
        "highest" in text
        or "best" in text
        or "top" in text
        or "strongest" in text
        or "strong" in text
    ):
        return "highest_subject"


    # Lowest / weak subject
    if "subject" in text and (
        "lowest" in text
        or "weak" in text
        or "weakest" in text
        or "worst" in text
    ):
        return "lowest_subject"


    # Attendance
    if any(word in text for word in [
        "attendance",
        "present",
        "absent"
    ]):
        return "attendance"


    # Average
    if any(word in text for word in [
        "average",
        "overall mark",
        "overall marks"
    ]):
        return "average"

     # Risk
    if any(word in text for word in [
        "risk",
        "at risk",
        "attention",
        "danger"
    ]):
        return "risk"


    # Recommendation
    if any(word in text for word in [
        "recommend",
        "recommendation",
        "suggestion",
        "suggest",
        "improve"
    ]):
        return "recommendation"

    #trend
    if any(word in text for word in [
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
    ]):
        return "trend"


    # Marks
    if any(word in text for word in [
        "marks",
        "mark",
        "scores",
        "score",
        "results"
    ]):
        return "marks"


    # General performance
    if any(word in text for word in [
        "performance",
        "performing",
        "doing"
    ]):
        return "performance"


   # ======================================
   # ML FALLBACK WITH CONFIDENCE
   # ======================================

    probabilities = model.predict_proba([text])[0]

    max_probability = max(probabilities)

    prediction = model.classes_[probabilities.argmax()]

    CONFIDENCE_THRESHOLD = 0.55

    if max_probability >= CONFIDENCE_THRESHOLD:
         return prediction

    return "unknown"
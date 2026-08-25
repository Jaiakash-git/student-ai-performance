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

    exit_phrases = [
        "bye",
        "goodbye",
        "good bye",
        "see you",
        "see ya",
        "quit",
        "exit",
        "stop",
        "i'm finished",
        "im finished",
        "i am finished",
        "i'm done",
        "im done",
        "i am done",
        "i want to leave",
        "leave",
        "that's all",
        "thats all"
    ]

    if text in exit_phrases:
        return "exit"

    if text.startswith("bye") and len(text) <= 10:
        return "exit"

    # ======================================
    # GREETING
    # ======================================

    if text in [
        "hi",
        "hii",
        "hiii",
        "hello",
        "hey",
        "heyy",
        "good morning",
        "good afternoon",
        "good evening"
    ]:
        return "greeting"

    # ======================================
    # RISK
    # ======================================

    risk_phrases = [
        "at risk",
        "am i at risk",
        "risk level",
        "academic risk",
        "performance concerning",
        "is my performance concerning",
        "is my academic performance concerning",
        "is my performance risky",
        "is my academic performance risky",
        "should i be concerned",
        "should i worry",
        "is my performance bad",
        "is my performance dangerous",
        "should i be worried",
        "is my performance concerning",
        "is this concerning",
        "danger"
    ]

    if any(phrase in text for phrase in risk_phrases):
        return "risk"

    # Explicit risk words
    if "risk" in text:
        return "risk"

    # ======================================
    # HIGHEST SUBJECT
    # ======================================

    highest_phrases = [
        "highest score",
        "highest mark",
        "maximum score",
        "maximum mark",
        "best score",
        "best mark",
        "top score",
        "top mark",
        "strongest subject",
        "best subject",
        "highest subject",
        "which subject is my strongest",
"which subject is strongest",
"which is my strongest subject",
"tell me my strongest subject",
"what is my strongest subject",
"my strongest subject"
        "which subject is highest",
        "which subject has the highest",
        "which subject has my highest",
        "which subject has my best",
        "which subject is my best",
        "greatest score",
        "greatest mark"
    ]

    if any(phrase in text for phrase in highest_phrases):
        return "highest_subject"

    # ======================================
    # LOWEST SUBJECT
    # ======================================

    lowest_phrases = [
        "lowest score",
        "lowest mark",
        "minimum score",
        "minimum mark",
        "worst score",
        "worst mark",
        "bottom score",
        "weakest subject",
        "weakest",
        "worst subject",
        "lowest subject",
        "which subject is lowest",
        "which subject has the lowest",
        "which subject has my lowest",
        "which subject has my worst",
        "which subject is my worst",
        "weak subject",
        "where am i weak",
        "performance is weakest"
    ]

    if any(phrase in text for phrase in lowest_phrases):
        return "lowest_subject"

    # ======================================
    # TREND
    # ======================================

    trend_phrases = [
        "performance trend",
        "marks trend",
        "score trend",
        "what happened to my marks",
        "what happened to my scores",
        "how are my marks changing",
        "how are my scores changing",
        "how did my marks change",
        "how did my scores change",
        "what changed in my marks",
        "what changed in my scores",
        "am i improving",
        "am i getting better",
        "are my marks improving",
        "are my scores improving",
        "are my marks getting better",
        "are my scores getting better",
        "have my marks gotten better",
        "have my scores gotten better",
        "getting worse",
        "compared to previous",
        "compared with previous",
        "previous exam",
        "last exam",
        "recent marks",
        "recent scores",
        "recent performance",
        "improving",
        "trend",
        "progress",
        "getting better",
        "getting worse",
        "changed",
        "change",
        "how have my marks changed",
        "how did my marks change",
        "how are my marks changing",
        "compared to",
        "compared with",
        "previous",
        "earlier",
        "before",
        "last exam",
        "previous exam",
        "recently"
    ]

    if any(phrase in text for phrase in trend_phrases):
        return "trend"

    # ======================================
    # RECOMMENDATION
    # ======================================

    recommendation_phrases = [
        "recommendation",
        "recommend",
        "what should i do",
        "what should i improve",
        "what can i improve",
        "how can i improve",
        "what should i focus on",
        "where should i focus",
        "where do i need to improve",
        "what should i work on",
        "what can i work on",
        "what are my weak areas",
        "which areas need improvement",
        "which subject should i improve",
        "which subject should i focus on",
        "which subject should i focus on improving",
        "which subject requires more attention",
        "which subject needs my attention",
        "what should i concentrate on",
        "where am i weak",
        "give me advice",
        "give me a suggestion",
        "suggestion",
        "suggest",
        "improve",
        "where should i focus",
        "what are my weak areas",
        "which subject needs more attention",
        "which subject needs attention",
        "advice"
    ]

    if any(phrase in text for phrase in recommendation_phrases):
        return "recommendation"

    # ======================================
    # ATTENDANCE
    # ======================================

    if any(
        word in text
        for word in [
            "attendance",
            "present percentage",
            "attendance percentage",
            "how much attendance",
            "how many days present"
        ]
    ):
        return "attendance"

    # ======================================
    # AVERAGE
    # ======================================

    if any(
        phrase in text
        for phrase in [
            "average",
            "overall average",
            "average mark",
            "average marks",
            "average score"
        ]
    ):
        return "average"

    # ======================================
    # MARKS
    # ======================================

    if any(
        phrase in text
        for phrase in [
            "show my marks",
            "show my scores",
            "list my marks",
            "list my scores",
            "give me my marks",
            "give me my scores",
            "my marks",
            "my scores",
            "marks details",
            "mark details",
            "score details",
            "results",
            "exam marks",
            "marks",
            "mark",
            "scores",
            "score",
            "results"
        ]
    ):
        return "marks"

    # ======================================
    # PERFORMANCE
    # ======================================

    performance_phrases = [
        "performance",
        "performing",
        "how am i doing",
        "how am i doing academically",
        "how am i doing in my studies",
        "how good am i",
        "how good are my studies",
        "how well am i doing",
        "how well am i doing academically",
        "how are my studies going",
        "how are my studies going overall",
        "evaluate my studies",
        "evaluate my performance",
        "assess my studies",
        "assess my performance",
        "rate my studies",
        "rate my performance",
        "academic performance"
        "doing well",
        "how am i doing",
        "how am i performing",
        "how are my academics",
        "am i doing well"

    ]

    if any(phrase in text for phrase in performance_phrases):
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
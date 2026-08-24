from nlp.intent_classifier import classify_intent
from nlp.intent_router import route_intent


# ==========================================
# PROCESS ONE MESSAGE
# ==========================================

def process_message(student_name, user_input, context=None):

    # ======================================
    # CREATE / RESTORE CONTEXT
    # ======================================

    if context is None:
        context = {
            "student_name": student_name,
            "last_intent": None,
            "last_subject": None,
            "follow_up": False,
            "subject_query": False,
            "requested_subject": None
        }

    # Make sure student name is available
    context["student_name"] = student_name

    text = user_input.lower().strip()

    # ======================================
    # RESET FOLLOW-UP FLAGS
    # ======================================

    context["follow_up"] = False
    context["subject_query"] = False
    context["requested_subject"] = None

    # ======================================
    # ANALYTICS DETECTION
    # ======================================

    analytics_phrases = [
        "complete analysis",
        "academic analysis",
        "academic report",
        "detailed analysis",
        "detailed report",
        "overall analysis",
        "overall report",
        "analyze my performance",
        "analyse my performance",
        "analyze my academics",
        "analyse my academics",
        "give me an analysis",
        "give me a report",
        "full analysis",
        "full report"
    ]

    if any(
        phrase in text
        for phrase in analytics_phrases
    ):
        intent = "analytics"
    else:
        intent = classify_intent(user_input)

    # ======================================
    # SUBJECT FOLLOW-UP
    # ======================================

    # --------------------------------------
    # HOW MUCH?
    # --------------------------------------

    if (
        context["last_subject"] is not None
        and text in [
            "how much",
            "how much?",
            "how many marks",
            "how many marks?",
            "what mark",
            "what mark?"
        ]
    ):
        intent = "subject_detail"
        context["follow_up"] = True
        context["subject_query"] = True
        context["requested_subject"] = (
            context["last_subject"]
        )

    # --------------------------------------
    # WHY SUBJECT?
    # --------------------------------------

    elif (
        context["last_subject"] is not None
        and context["last_intent"] in [
            "highest_subject",
            "lowest_subject"
        ]
        and text in [
            "why",
            "why?",
            "why is it weak",
            "why is it weak?",
            "why is that weak",
            "why is that weak?",
            "why is it strong",
            "why is it strong?",
            "why is that strong",
            "why is that strong?"
        ]
    ):
        intent = context["last_intent"]
        context["follow_up"] = True
        context["subject_query"] = True
        context["requested_subject"] = (
            context["last_subject"]
        )

    # --------------------------------------
    # HOW DID I IMPROVE?
    # --------------------------------------

    elif (
        context["last_subject"] is not None
        and any(
            phrase in text
            for phrase in [
                "how did i improve in it",
                "how did i improve",
                "how much did i improve",
                "how has it improved",
                "how did it improve",
                "how is it improving",
                "how much has it improved"
            ]
        )
    ):
        intent = "subject_trend"
        context["follow_up"] = True
        context["subject_query"] = True
        context["requested_subject"] = (
            context["last_subject"]
        )

    # ======================================
    # HIGHEST → LOWEST
    # ======================================

    elif (
        context["last_intent"] == "highest_subject"
        and any(
            word in text
            for word in [
                "lowest",
                "weakest",
                "worst",
                "weak"
            ]
        )
    ):
        intent = "lowest_subject"

    # ======================================
    # LOWEST → HIGHEST
    # ======================================

    elif (
        context["last_intent"] == "lowest_subject"
        and any(
            word in text
            for word in [
                "highest",
                "strongest",
                "best",
                "top"
            ]
        )
    ):
        intent = "highest_subject"

    # ======================================
    # GENERAL WHY FOLLOW-UP
    # ======================================

    elif (
        context["last_intent"] in [
            "highest_subject",
            "lowest_subject",
            "risk",
            "trend",
            "performance",
            "average",
            "attendance",
            "recommendation"
        ]
        and text in [
            "why",
            "why?",
            "how",
            "how?",
            "why is that",
            "why is that?",
            "why is it",
            "why is it?"
        ]
    ):
        intent = context["last_intent"]
        context["follow_up"] = True

        if intent in [
            "highest_subject",
            "lowest_subject"
        ]:
            context["subject_query"] = True
            context["requested_subject"] = (
                context["last_subject"]
            )

    # ======================================
    # ATTENDANCE / STATUS FOLLOW-UP
    # ======================================

    elif (
        context["last_intent"] in [
            "attendance",
            "average",
            "performance",
            "risk"
        ]
        and any(
            phrase in text
            for phrase in [
                "is that good",
                "is that okay",
                "is that bad",
                "is it good",
                "is it okay",
                "is it bad"
            ]
        )
    ):
        intent = context["last_intent"]
        context["follow_up"] = True

    # ======================================
    # EXIT
    # ======================================

    if intent == "exit":

        response = (
            "Goodbye! Keep working hard. 👋"
        )

        context["last_intent"] = intent

        return response, context

    # ======================================
    # ROUTE REQUEST
    # ======================================

    response = route_intent(
        intent,
        student_name,
        context
    )

    # ======================================
    # UPDATE CONTEXT
    # ======================================

    context["last_intent"] = intent

    return response, context


# ==========================================
# TERMINAL ASSISTANT
# ==========================================

def start_assistant(student_name):

    print("\n============================================")
    print("          STUDENT AI ASSISTANT")
    print("============================================")

    print(f"\nHello {student_name}! 👋")
    print("Ask me about your marks, attendance,")
    print("performance, risk, recommendation, or trend.")
    print("Type 'bye' to exit.")

    # ======================================
    # CONVERSATION CONTEXT
    # ======================================

    context = {
        "student_name": student_name,
        "last_intent": None,
        "last_subject": None,
        "follow_up": False,
        "subject_query": False,
        "requested_subject": None
    }

    # ======================================
    # CONVERSATION LOOP
    # ======================================

    while True:

        user_input = input("\nYou: ")

        response, context = process_message(
            student_name,
            user_input,
            context
        )

        print(f"\nAI: {response}")

        if context["last_intent"] == "exit":
            break


# ==========================================
# PROGRAM ENTRY POINT
# ==========================================

if __name__ == "__main__":

    student_name = input(
        "Enter student name: "
    )

    start_assistant(student_name)
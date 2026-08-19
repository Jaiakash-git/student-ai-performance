from nlp.intent_classifier import classify_intent
from nlp.intent_router import route_intent
from services.student_service import get_student_marks


def find_subject_from_text(text, student_name):

    results = get_student_marks(student_name)

    text = text.lower()

    # Sort by subject length so that
    # longer names are checked first.
    subjects = sorted(
        results,
        key=lambda item: len(item[0]),
        reverse=True
    )

    for subject, _ in subjects:

        subject_lower = subject.lower().strip()

        if subject_lower in text:

            return subject

    return None


def start_assistant(student_name):

    print("\n============================================")
    print("          STUDENT AI ASSISTANT")
    print("============================================")

    print(f"\nHello {student_name}! 👋")
    print("Ask me about your marks, attendance,")
    print("performance, risk, recommendation, or trend.")
    print("Type 'bye' to exit.")

    # ==========================================
    # CONVERSATION CONTEXT
    # ==========================================

    context = {
        "student_name": student_name,
        "last_intent": None,
        "last_subject": None,
        "follow_up": False,
        "subject_query": False,
        "requested_subject": None
    }

    # ==========================================
    # CONVERSATION LOOP
    # ==========================================

    while True:

        user_input = input("\nYou: ")

        text = user_input.lower().strip()

        # ======================================
        # EMPTY INPUT
        # ======================================

        if not text:
            continue

        # ======================================
        # RESET FOLLOW-UP VALUES
        # ======================================

        context["follow_up"] = False
        context["subject_query"] = False
        context["requested_subject"] = None

        # ======================================
        # EXIT
        # ======================================

        intent = classify_intent(user_input)

        if intent == "exit":

            print(
                "\nAI: Goodbye! Keep working hard. 👋"
            )

            break

        # ======================================
        # SUBJECT DETECTION
        # ======================================

        detected_subject = find_subject_from_text(
            text,
            student_name
        )

        # ======================================
        # SUBJECT-SPECIFIC QUESTION
        # ======================================

        if detected_subject is not None:

            subject_question_words = [
                "what about",
                "what is my",
                "what is the",
                "how did i do",
                "how did i perform",
                "how am i doing",
                "is",
                "why is",
                "why",
                "tell me about",
                "show me"
            ]

            if any(
                phrase in text
                for phrase in subject_question_words
            ):

                context["subject_query"] = True
                context["requested_subject"] = detected_subject

                # ----------------------------------
                # "why is BEEE weak?"
                # ----------------------------------

                if any(
                    phrase in text
                    for phrase in [
                        "why is",
                        "why"
                    ]
                ):

                    context["follow_up"] = True

                intent = "subject_query"

        # ======================================
        # WHY / HOW FOLLOW-UP
        # ======================================

        elif text in [
            "why",
            "why?",
            "how",
            "how?",
            "explain",
            "explain why",
            "can you explain"
        ]:

            if context["last_intent"] is not None:

                intent = context["last_intent"]
                context["follow_up"] = True

        # ======================================
        # EXTENDED WHY QUESTIONS
        # ======================================

        elif any(
            phrase in text
            for phrase in [
                "why is that",
                "why is it",
                "why so",
                "how so",
                "can you explain that",
                "what makes it"
            ]
        ):

            if context["last_intent"] is not None:

                intent = context["last_intent"]
                context["follow_up"] = True

        # ======================================
        # HOW CAN I IMPROVE IT?
        # ======================================

        elif (
            context["last_subject"] is not None
            and any(
                phrase in text
                for phrase in [
                    "how can i improve it",
                    "how do i improve it",
                    "how can i improve",
                    "how should i improve it",
                    "what can i do about it",
                    "how do i get better at it",
                    "how can i get better at it"
                ]
            )
        ):

            intent = "recommendation"
            context["follow_up"] = True

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
        # ATTENDANCE / PERFORMANCE FOLLOW-UP
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
        # UPDATE CONTEXT
        # ======================================

        context["last_intent"] = intent

        # ======================================
        # ROUTE REQUEST
        # ======================================

        response = route_intent(
            intent,
            student_name,
            context
        )

        print(f"\nAI: {response}")


# ==========================================
# PROGRAM ENTRY POINT
# ==========================================

if __name__ == "__main__":

    student_name = input(
        "Enter student name: "
    )

    start_assistant(student_name)
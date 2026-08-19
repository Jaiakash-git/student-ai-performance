from nlp.intent_classifier import classify_intent
from nlp.intent_router import route_intent


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
        "follow_up": False
    }

    # ==========================================
    # CONVERSATION LOOP
    # ==========================================

    while True:

        user_input = input("\nYou: ")

        text = user_input.lower().strip()

        # ======================================
        # RESET FOLLOW-UP FLAG
        # ======================================

        context["follow_up"] = False

        # ======================================
        # INTENT DETECTION
        # ======================================

        intent = classify_intent(user_input)

        # ======================================
        # FOLLOW-UP QUESTIONS
        # ======================================

        # --------------------------------------
        # Highest → Lowest
        # --------------------------------------

        if (
            context["last_intent"] == "highest_subject"
            and any(word in text for word in [
                "lowest",
                "weakest",
                "worst",
                "weak"
            ])
        ):
            intent = "lowest_subject"

        # --------------------------------------
        # Lowest → Highest
        # --------------------------------------

        elif (
            context["last_intent"] == "lowest_subject"
            and any(word in text for word in [
                "highest",
                "strongest",
                "best",
                "top"
            ])
        ):
            intent = "highest_subject"

        # --------------------------------------
        # Context-dependent questions
        # Example:
        # "How is my attendance?"
        # "Is that good?"
        # --------------------------------------

        elif (
            context["last_intent"] in [
                "attendance",
                "average",
                "performance",
                "risk"
            ]
            and any(phrase in text for phrase in [
                "is that good",
                "is that okay",
                "is that bad",
                "is it good",
                "is it okay",
                "is it bad"
            ])
        ):
            intent = context["last_intent"]
            context["follow_up"] = True

        # ======================================
        # EXIT
        # ======================================

        if intent == "exit":

            print(
                "\nAI: Goodbye! Keep working hard. 👋"
            )

            break

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
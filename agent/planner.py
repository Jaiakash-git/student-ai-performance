# ==========================================
# AGENT PLANNER
# ==========================================
# Decides which tools are required
# to answer the user's question.
# ==========================================


def create_plan(user_input):
    """
    Analyze the user's question and return
    the tools required to answer it.

    Example:

        "What is my average?"
        -> ["average"]

        "How am I performing and what
         should I improve?"
        -> ["performance", "recommendation"]
    """

    text = user_input.lower().strip()

    plan = []

    # ======================================
    # AVERAGE
    # ======================================

    if "average" in text:
        plan.append("average")

    # ======================================
    # ATTENDANCE
    # ======================================

    if "attendance" in text:
        plan.append("attendance")

    # ======================================
    # HIGHEST SUBJECT
    # ======================================

    if any(
        phrase in text
        for phrase in [
            "highest subject",
            "strongest subject",
            "best subject",
            "highest mark",
            "highest score"
        ]
    ):
        plan.append("highest_subject")

    # ======================================
    # LOWEST SUBJECT
    # ======================================

    if any(
        phrase in text
        for phrase in [
            "lowest subject",
            "weakest subject",
            "worst subject",
            "lowest mark",
            "lowest score"
        ]
    ):
        plan.append("lowest_subject")

    # ======================================
    # PERFORMANCE
    # ======================================

    if any(
        phrase in text
        for phrase in [
            "performance",
            "performing",
            "how am i doing"
        ]
    ):
        plan.append("performance")

    # ======================================
    # RISK
    # ======================================

    if "risk" in text:
        plan.append("risk")

    # ======================================
    # RECOMMENDATION
    # ======================================

    if any(
        phrase in text
        for phrase in [
            "recommendation",
            "recommend",
            "what should i do",
            "what should i improve",
            "how can i improve",
            "what should i focus on"
        ]
    ):
        plan.append("recommendation")

    # ======================================
    # TREND
    # ======================================

    if any(
        phrase in text
        for phrase in [
            "trend",
            "improving",
            "getting better",
            "getting worse",
            "progress"
        ]
    ):
        plan.append("trend")

    # ======================================
    # REMOVE DUPLICATES
    # ======================================

    plan = list(dict.fromkeys(plan))

    return plan


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    test_questions = [
        "What is my average?",
        "What is my attendance?",
        "Which is my highest subject?",
        "Which is my lowest subject?",
        "How am I performing?",
        "What is my risk?",
        "What should I improve?",
        "What is my trend?",
        "How am I performing and what should I improve?"
    ]

    print("\n========================================")
    print("          AGENT PLANNER TEST")
    print("========================================")

    for question in test_questions:

        plan = create_plan(question)

        print(f"\nQuestion: {question}")
        print(f"Plan    : {plan}")


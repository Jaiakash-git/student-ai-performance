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

    Examples:

        "What is my average?"
        -> ["average"]

        "How am I performing and what
         should I improve?"
        -> ["performance", "recommendation"]

        "What does an improving trend mean?"
        -> ["academic_question"]
    """

    text = user_input.lower().strip()

    plan = []

    # ======================================
    # GENERAL ACADEMIC QUESTION
    # ======================================
    # These questions should be handled
    # by the RAG pipeline instead of
    # personal student analytics.
    # ======================================

    personal_indicators = [
        "my ",
        "i ",
        "i'm ",
        "im ",
        "i am ",
        "me ",
        "mine",
        "myself"
    ]

    general_question_indicators = [
        "what does",
        "what is",
        "what are",
        "explain",
        "define",
        "meaning of",
        "what do you mean",
        "is ",
        "are ",
        "does ",
        "how does",
        "how do",
        "why is",
        "why are"
    ]

    general_academic_topics = [
        "academic performance",
        "academic risk",
        "academic recommendation",
        "performance trend",
        "improving trend",
        "declining trend",
        "stable trend",
        "average mark",
        "average score",
        "attendance"
    ]

    is_personal = any(
        phrase in text
        for phrase in personal_indicators
    )

    is_general_question = (
        any(
            text.startswith(phrase)
            for phrase in general_question_indicators
        )
        or any(
            topic in text
            for topic in general_academic_topics
        )
    )

    if is_general_question and not is_personal:
        plan.append("academic_question")

        # General question is handled by RAG,
        # so don't continue to personal tools.
        return plan

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

        # Personal questions
        "What is my average?",
        "What is my attendance?",
        "Which is my highest subject?",
        "Which is my lowest subject?",
        "How am I performing?",
        "What is my risk?",
        "What should I improve?",
        "What is my trend?",

        # Multi-tool questions
        "How am I performing and what should I improve?",
        "What is my risk and what should I improve?",
        "What is my highest subject and lowest subject?",

        # General academic questions
        "What does an improving trend mean?",
        "Is 80% attendance good?",
        "What is academic performance?",
        "What is academic risk?",
        "What does average mark mean?"
    ]

    print("\n========================================")
    print("          AGENT PLANNER TEST")
    print("========================================")

    for question in test_questions:

        plan = create_plan(question)

        print(
            f"\nQuestion: {question}"
        )

        print(
            f"Plan    : {plan}"
        )
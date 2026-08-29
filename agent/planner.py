# ==========================================
# AGENT PLANNER
# ==========================================
# Decides which tools are required
# to answer the user's question.
#
# The planner also uses conversation memory
# to understand follow-up questions.
# ==========================================


def create_plan(user_input, context=None):
    """
    Analyze the user's question and return
    the tools required to answer it.

    The planner uses conversation memory
    to understand short follow-up questions.
    """

    text = user_input.lower().strip()

    plan = []

    # ======================================
    # GET MEMORY
    # ======================================

    if context is None:
        context = {}

    last_intent = context.get("last_intent")
    last_subject = context.get("last_subject")

    # ======================================
    # GOODBYE
    # ======================================

    goodbye_phrases = [
        "bye",
        "bye bye",
        "byee",
        "byeee",
        "goodbye",
        "good bye",
        "see you",
        "see ya",
        "exit",
        "quit"
    ]

    if text in goodbye_phrases:
        return ["goodbye"]

    # ======================================
    # ACADEMIC QUESTION
    # ======================================

    academic_phrases = [
        "what does",
        "what is academic",
        "academic performance",
        "academic risk",
        "what does an improving trend mean",
        "what does a declining trend mean",
        "what does a stable trend mean",
        "attendance good",
        "attendance acceptable",
        "attendance considered",
        "is 80%",
        "is 75%",
        "is 85%",
        "meaning",
        "mean",
        "study habits",
        "how can students"
    ]

    is_academic_question = any(
        phrase in text
        for phrase in academic_phrases
    )

    if is_academic_question:
        return ["academic_question"]

    # ======================================
    # SUBJECT DETAIL FOLLOW-UP
    # ======================================

    subject_detail_phrases = [
        "how much",
        "what is the mark",
        "what's the mark",
        "what is my mark",
        "what's my mark",
        "my mark",
        "my score",
        "what is my score",
        "what's my score",
        "how many marks",
        "how did i score"
    ]

    if (
        last_subject is not None
        and any(
            phrase in text
            for phrase in subject_detail_phrases
        )
    ):
        plan.append("subject_detail")

    # ======================================
    # SUBJECT TREND FOLLOW-UP
    # ======================================

    subject_trend_phrases = [
        "how did i improve",
        "did i improve",
        "how did it improve",
        "how is it improving",
        "how is it progressing",
        "is it improving",
        "is it getting better",
        "is it getting worse",
        "subject trend",
        "subject progress",
        "how did my marks change",
        "how did my mark change"
    ]

    if (
        last_subject is not None
        and any(
            phrase in text
            for phrase in subject_trend_phrases
        )
    ):
        plan.append("subject_trend")

    # ======================================
    # SUBJECT EXPLANATION / WHY
    # ======================================

    # Short follow-up questions such as:
    #
    # "Why?"
    # "Why is OS my lowest?"
    # "Why is this my weakest subject?"
    #
    # depend on the previous subject.

    why_phrases = [
        "why",
        "why is it",
        "why is this",
        "why is that",
        "why this subject",
        "why this",
        "why is it low",
        "why is this low",
        "why is this my lowest",
        "why is this my highest"
    ]

    if (
        last_subject is not None
        and any(
            phrase == text
            or phrase in text
            for phrase in why_phrases
        )
    ):
        plan.append("subject_explanation")

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
    # OVERALL TREND
    # ======================================

    overall_trend_phrases = [
        "what is my trend",
        "what's my trend",
        "my overall trend",
        "overall trend",
        "overall progress",
        "overall improvement",
        "am i improving overall",
        "am i getting better overall",
        "am i getting worse overall"
    ]

    general_trend_words = [
        "trend",
        "improving",
        "getting better",
        "getting worse",
        "progress"
    ]

    if any(
        phrase in text
        for phrase in overall_trend_phrases
    ):
        plan.append("trend")

    elif not any(
        phrase in text
        for phrase in subject_trend_phrases
    ):
        if any(
            phrase in text
            for phrase in general_trend_words
        ):
            plan.append("trend")

    # ======================================
    # MEMORY-BASED SUBJECT DETAIL
    # ======================================

    if not plan and last_subject is not None:

        if any(
            phrase in text
            for phrase in [
                "what is it",
                "what about it",
                "tell me more",
                "more about it",
                "what about this subject"
            ]
        ):
            plan.append("subject_detail")

    # ======================================
    # MEMORY-BASED SUBJECT TREND
    # ======================================

    if not plan and last_subject is not None:

        if any(
            phrase in text
            for phrase in [
                "improved",
                "improve",
                "progressing",
                "progress",
                "getting better",
                "getting worse",
                "changed"
            ]
        ):
            plan.append("subject_trend")

    # ======================================
    # REMOVE DUPLICATES
    # ======================================

    plan = list(
        dict.fromkeys(plan)
    )

    return plan


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    print("\n========================================")
    print("          AGENT PLANNER TEST")
    print("========================================")

    # ======================================
    # NORMAL MEMORY
    # ======================================

    context = {
        "student_name": "Jaiakash",
        "last_intent": "lowest_subject",
        "last_subject": "OS",
        "last_result": {
            "success": True,
            "subject": "OS",
            "mark": 82.0
        }
    }

    test_questions = [
        "What is my average?",
        "What is my attendance?",
        "Which is my highest subject?",
        "Which is my lowest subject?",
        "How am I performing?",
        "What is my risk?",
        "What should I improve?",
        "What is my trend?",
        "How much?",
        "How did I improve?",
        "Why?",
        "Why is it low?",
        "What about it?",
        "bye",
        "byee",
        "bye bye",
        "goodbye",
        "What does an improving trend mean?",
        "Is 80% attendance good?"
    ]

    for question in test_questions:

        plan = create_plan(
            question,
            context
        )

        print(
            f"\nQuestion: {question}"
        )

        print(
            f"Plan    : {plan}"
        )
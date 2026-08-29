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
    """

    text = user_input.lower().strip()

    if context is None:
        context = {}

    last_subject = context.get("last_subject")

    plan = []

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
    # GREETING
    # ======================================

    greeting_phrases = [
        "hi",
        "hii",
        "hiii",
        "hello",
        "hey",
        "heyy",
        "good morning",
        "good afternoon",
        "good evening"
    ]

    if text in greeting_phrases:
        return ["greeting"]

    # ======================================
    # THANKS
    # ======================================

    thanks_phrases = [
        "thanks",
        "thank you",
        "thankyou",
        "thx",
        "okay",
        "ok",
        "cool",
        "nice"
    ]

    if text in thanks_phrases:
        return ["thanks"]

    # ======================================
    # ACADEMIC / GENERAL KNOWLEDGE QUESTION
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
        "study habits",
        "how can students"
    ]

    if any(phrase in text for phrase in academic_phrases):

        # IMPORTANT:
        # "Am I at academic risk?" is a personal
        # student-risk question, not a general
        # academic definition question.
        if text in [
            "am i at academic risk",
            "am i at academic risk?"
        ]:
            pass
        else:
            return ["academic_question"]

    # ======================================
    # AVERAGE
    # ======================================
    # Check average before subject-detail.
    #
    # Example:
    # "How much do I score on average?"
    #
    # Should become:
    # ['average']
    # ======================================

    average_phrases = [
        "average",
        "avrage",
        "averge",
        "avg"
    ]

    if any(phrase in text for phrase in average_phrases):
        plan.append("average")

    # ======================================
    # ATTENDANCE
    # ======================================

    attendance_phrases = [
        "attendance",
        "attendence",
        "attndance"
    ]

    if any(phrase in text for phrase in attendance_phrases):
        plan.append("attendance")

    # ======================================
    # HIGHEST SUBJECT
    # ======================================

    highest_phrases = [
        "highest subject",
        "highest-subject",
        "strongest subject",
        "best subject",
        "which subject is my best",
        "which is my best subject",
        "highest mark",
        "highest score",
        "higgest subject",
        "higest subject",
        "best mark",
        "best score",
        "highest"
    ]

    has_highest = any(
        phrase in text
        for phrase in highest_phrases
    )

    # ======================================
    # LOWEST SUBJECT
    # ======================================

    lowest_phrases = [
        "lowest subject",
        "lowest-subject",
        "weakest subject",
        "worst subject",
        "lowest mark",
        "lowest score",
        "lowst subject",
        "weakest",
        "lowest"
    ]

    has_lowest = any(
        phrase in text
        for phrase in lowest_phrases
    )

    # ======================================
    # HIGHEST + LOWEST MULTI-INTENT
    # ======================================
    #
    # Example:
    # "What are my highest and lowest subjects?"
    #
    # Expected:
    # ['highest_subject', 'lowest_subject']
    # ======================================

    if has_highest:
        plan.append("highest_subject")

    if has_lowest:
        plan.append("lowest_subject")

    # ======================================
    # PERFORMANCE
    # ======================================

    performance_phrases = [
        "performance",
        "performing",
        "perfomance",
        "how am i doing",
        "how am i performing",
        "am i performing well",
        "how is my performance"
    ]

    if any(
        phrase in text
        for phrase in performance_phrases
    ):
        plan.append("performance")

    # ======================================
    # RISK
    # ======================================

    risk_phrases = [
        "risk",
        "at risk",
        "academic risk"
    ]

    if any(
        phrase in text
        for phrase in risk_phrases
    ):
        plan.append("risk")

    # ======================================
    # RECOMMENDATION
    # ======================================

    recommendation_phrases = [
        "recommendation",
        "recommend",
        "what should i do",
        "what should i improve",
        "how can i improve",
        "what should i focus on",
        "what do i need to improve",
        "where should i improve",
        "what can i improve"
    ]

    if any(
        phrase in text
        for phrase in recommendation_phrases
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
        "am i improving",
        "am i improving overall",
        "am i getting better",
        "am i getting better overall",
        "am i getting worse",
        "am i getting worse overall",
        "how are my marks changing",
        "how is my performance changing",
        "overall marks changing"
    ]

    if any(
        phrase in text
        for phrase in overall_trend_phrases
    ):
        plan.append("trend")

    # ======================================
    # SUBJECT TREND FOLLOW-UP
    # ======================================
    #
    # Examples:
    #
    # "How did I improve?"
    # "Did I improve?"
    # "How is it progressing?"
    #
    # These require remembered subject.
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
        "how did my mark change",
        "how is my subject improving",
        "how is my subject progressing",
        "how has it changed",
        "how has my mark changed"
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
    # SUBJECT DETAIL FOLLOW-UP
    # ======================================
    #
    # Examples:
    #
    # "How much?"
    # "What's the mark?"
    # "Tell me more"
    #
    # But NOT:
    #
    # "How much do I score on average?"
    #
    # because average has already been detected.
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
        "how did i score",
        "what is it",
        "what about it",
        "tell me more",
        "more about it",
        "what about this subject"
    ]

    has_average_context = any(
        phrase in text
        for phrase in average_phrases
    )

    if (
        last_subject is not None
        and not has_average_context
        and any(
            phrase in text
            for phrase in subject_detail_phrases
        )
    ):
        plan.append("subject_detail")

    # ======================================
    # SUBJECT EXPLANATION / EVALUATION
    # ======================================
    #
    # Examples:
    #
    # "Why?"
    # "Why is it low?"
    # "Is that good?"
    # "Is that bad?"
    #
    # These require remembered subject.
    # ======================================

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
        "why is this my highest",
        "why macha",
        "why bro"
    ]

    evaluation_phrases = [
        "is that good",
        "is that bad",
        "is this good",
        "is this bad",
        "is it good",
        "is it bad",
        "is my mark good",
        "is my mark bad"
    ]

    if last_subject is not None:

        if any(
            phrase == text or phrase in text
            for phrase in why_phrases
        ):
            plan.append("subject_explanation")

        elif any(
            phrase == text or phrase in text
            for phrase in evaluation_phrases
        ):
            plan.append("subject_explanation")

    # ======================================
    # MEMORY-BASED SUBJECT DETAIL
    # ======================================
    #
    # Handles short follow-up questions.
    # ======================================

    if not plan and last_subject is not None:

        memory_detail_phrases = [
            "what is it",
            "what about it",
            "tell me more",
            "more about it",
            "what about this subject"
        ]

        if any(
            phrase in text
            for phrase in memory_detail_phrases
        ):
            plan.append("subject_detail")

    # ======================================
    # MEMORY-BASED SUBJECT TREND
    # ======================================

    if not plan and last_subject is not None:

        memory_trend_phrases = [
            "improved",
            "improve",
            "progressing",
            "progress",
            "getting better",
            "getting worse",
            "changed"
        ]

        if any(
            phrase in text
            for phrase in memory_trend_phrases
        ):
            plan.append("subject_trend")

    # ======================================
    # FALLBACK TREND
    # ======================================

    if not any(
        item == "trend"
        for item in plan
    ):

        general_trend_words = [
            "trend",
            "improving",
            "getting better",
            "getting worse",
            "progress"
        ]

        # Do not treat a subject-trend follow-up
        # as overall trend.

        if (
            "subject_trend" not in plan
            and any(
                word in text
                for word in general_trend_words
            )
        ):
            plan.append("trend")

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

    context = {
        "student_name": "Jagadish",
        "last_intent": "lowest_subject",
        "last_subject": "OS",
        "requested_subject": "OS",
        "last_result": {
            "success": True,
            "subject": "OS",
            "mark": 68.0
        },
        "last_subject_type": "lowest"
    }

    test_questions = [

        # ==================================
        # Average
        # ==================================

        "What is my average?",
        "Tell me my average",
        "How much do I score on average?",

        # ==================================
        # Attendance
        # ==================================

        "What is my attendance?",
        "What percentage of attendance do I have?",
        "what is my attendence",

        # ==================================
        # Highest
        # ==================================

        "What is my highest subject?",
        "Which subject is my best?",
        "Which is my best subject?",
        "What is my highest mark?",
        "what is my higgest subject",

        # ==================================
        # Lowest
        # ==================================

        "What is my lowest subject?",
        "Which subject is my weakest?",
        "Which is my weakest subject?",
        "What is my lowest mark?",
        "what is my lowst subject",

        # ==================================
        # Performance
        # ==================================

        "How am I performing?",
        "How am I doing?",
        "Am I performing well?",
        "what is my perfomance",

        # ==================================
        # Risk
        # ==================================

        "What is my risk?",
        "Am I at academic risk?",
        "Am I at risk?",

        # ==================================
        # Recommendation
        # ==================================

        "What should I improve?",
        "How can I improve?",
        "What should I focus on?",
        "What should I do?",

        # ==================================
        # Trend
        # ==================================

        "What is my trend?",
        "Am I improving?",
        "Am I getting better?",

        # ==================================
        # Subject Follow-ups
        # ==================================

        "How much?",
        "How did I improve?",
        "Why?",
        "Why is it low?",
        "Why macha",
        "Is that good?",
        "Is that bad?",
        "What about it?",
        "Tell me more",

        # ==================================
        # Multi-intent
        # ==================================

        "What is my average and attendance?",
        "What are my highest and lowest subjects?",
        "Tell me my performance and risk.",

        # ==================================
        # Academic
        # ==================================

        "What does an improving trend mean?",
        "What is academic performance?",
        "What is academic risk?",
        "Is 80% attendance good?",

        # ==================================
        # Greeting
        # ==================================

        "hii",
        "hello",
        "hey",
        "good morning",

        # ==================================
        # Thanks
        # ==================================

        "thanks",
        "thank you",
        "okay",
        "cool",

        # ==================================
        # Goodbye
        # ==================================

        "bye",
        "byee",
        "bye bye",
        "goodbye"
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
            f"Plan     : {plan}"
        )
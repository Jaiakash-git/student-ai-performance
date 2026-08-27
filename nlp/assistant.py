from nlp.intent_classifier import classify_intent
from nlp.intent_router import route_intent

from rag.rag_pipeline import answer_question

from agent.agent_core import run_agent


# ==========================================
# GENERAL ACADEMIC QUESTION DETECTION
# ==========================================

def is_general_question(text):

    text = text.lower().strip()

    # ------------------------------------------
    # PERSONAL / STUDENT INDICATORS
    # ------------------------------------------

    personal_phrases = [
        "my ",
        "i ",
        "i'm ",
        "im ",
        "i am ",
        "me ",
        "mine",
        "myself",
        "how am i",
        "how are my",
        "how is my",
        "what are my",
        "what is my",
        "show my",
        "give me my",
        "tell me my",
        "calculate my",
        "analyze my",
        "analyse my",
        "evaluate my",
        "assess my"
    ]

    # ------------------------------------------
    # CLEARLY PERSONAL QUESTION
    # ------------------------------------------

    if any(
        phrase in text
        for phrase in personal_phrases
    ):
        return False

    # ------------------------------------------
    # GENERAL QUESTION INDICATORS
    # ------------------------------------------

    general_question_words = [
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

    if any(
        text.startswith(phrase)
        for phrase in general_question_words
    ):
        return True

    # ------------------------------------------
    # GENERAL ACADEMIC TOPICS
    # ------------------------------------------

    general_topics = [
        "attendance",
        "average mark",
        "average score",
        "academic performance",
        "performance trend",
        "improving trend",
        "declining trend",
        "stable trend",
        "academic risk",
        "study recommendation",
        "academic recommendation"
    ]

    if any(
        topic in text
        for topic in general_topics
    ):
        return True

    return False


# ==========================================
# FORMAT AGENT RESPONSE
# ==========================================

def format_agent_response(agent_output):

    tool = agent_output.get("tool")
    result = agent_output.get("result", {})

    # ------------------------------------------
    # TOOL ERROR
    # ------------------------------------------

    if not result.get("success", False):

        return result.get(
            "message",
            "I couldn't process that request."
        )

    # ------------------------------------------
    # AVERAGE
    # ------------------------------------------

    if tool == "average":

        return (
            f"Your average mark is "
            f"{result['average']:.2f}."
        )

    # ------------------------------------------
    # ATTENDANCE
    # ------------------------------------------

    if tool == "attendance":

        return (
            f"Your overall attendance is "
            f"{result['attendance']:.2f}%."
        )

    # ------------------------------------------
    # HIGHEST SUBJECT
    # ------------------------------------------

    if tool == "highest_subject":

        return (
            f"{result['subject']} is your "
            f"highest scoring subject with "
            f"{result['mark']:.2f} marks."
        )

    # ------------------------------------------
    # LOWEST SUBJECT
    # ------------------------------------------

    if tool == "lowest_subject":

        return (
            f"{result['subject']} is your "
            f"lowest scoring subject with "
            f"{result['mark']:.2f} marks."
        )

    # ------------------------------------------
    # PERFORMANCE
    # ------------------------------------------

    if tool == "performance":

        return (
            f"Your performance status is "
            f"{result['status']}.\n"
            f"Average mark: {result['average']:.2f}\n"
            f"Overall attendance: "
            f"{result['attendance']:.2f}%."
        )

    # ------------------------------------------
    # RISK
    # ------------------------------------------

    if tool == "risk":

        return (
            f"Your academic risk level is "
            f"{result['risk_level']}.\n"
            f"Risk probability: "
            f"{result['risk_probability']:.2f}%.\n"
            f"Average mark: "
            f"{result['average']:.2f}\n"
            f"Overall attendance: "
            f"{result['attendance']:.2f}%."
        )

    # ------------------------------------------
    # RECOMMENDATION
    # ------------------------------------------

    if tool == "recommendation":

        return (
            f"{result['recommendation']}\n"
            f"Priority subject: "
            f"{result['priority_subject']} "
            f"({result['priority_mark']:.2f})"
        )

    # ------------------------------------------
    # TREND
    # ------------------------------------------

    if tool == "trend":

        response = (
            f"Your overall performance trend is "
            f"{result['overall_trend']}.\n\n"
        )

        for subject in result["subjects"]:

            improvement = subject["improvement"]

            if improvement > 0:
                change = f"+{improvement:.2f}"
            else:
                change = f"{improvement:.2f}"

            response += (
                f"{subject['subject']}: "
                f"{subject['first_mark']:.2f} → "
                f"{subject['latest_mark']:.2f} "
                f"({change})\n"
            )

        response += (
            f"\nAverage improvement: "
            f"{result['average_improvement']:+.2f}"
        )

        return response

    # ------------------------------------------
    # UNKNOWN TOOL
    # ------------------------------------------

    return (
        "I couldn't determine how to present "
        "the result."
    )


# ==========================================
# PROCESS ONE MESSAGE
# ==========================================

def process_message(
    student_name,
    user_input,
    context=None
):

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

    context["student_name"] = student_name

    text = user_input.lower().strip()

    # ======================================
    # RESET FOLLOW-UP FLAGS
    # ======================================

    context["follow_up"] = False
    context["subject_query"] = False
    context["requested_subject"] = None

    # ======================================
    # EXIT
    # ======================================

    if text in [
        "bye",
        "exit",
        "quit",
        "byeeeee",
        "goodbye"
    ]:

        response = (
            "Goodbye! Keep working hard. 👋"
        )

        context["last_intent"] = "exit"

        return response, context

    # ======================================
    # RAG FOR GENERAL QUESTIONS
    # ======================================

    if is_general_question(text):

        rag_answer, _ = answer_question(
            user_input
        )

        return rag_answer, context

    # ======================================
    # AGENTIC AI CORE
    # ======================================

    agent_output = run_agent(
        student_name,
        user_input
    )

    # --------------------------------------
    # IF AGENT FOUND A TOOL
    # --------------------------------------

    if agent_output.get("tool") is not None:

        response = format_agent_response(
            agent_output
        )

        context["last_intent"] = (
            agent_output["tool"]
        )

        return response, context

    # ======================================
    # EXISTING NLP PIPELINE
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

        intent = classify_intent(
            user_input
        )

    # ======================================
    # SUBJECT FOLLOW-UP
    # ======================================

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

    # ======================================
    # WHY SUBJECT?
    # ======================================

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

    # ======================================
    # HOW DID I IMPROVE?
    # ======================================

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
        context["last_intent"]
        == "highest_subject"
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
        context["last_intent"]
        == "lowest_subject"
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
        context["last_intent"]
        in [
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
        context["last_intent"]
        in [
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

    print(
        "\n============================================"
    )

    print(
        "          STUDENT AI ASSISTANT"
    )

    print(
        "============================================"
    )

    print(
        f"\nHello {student_name}! 👋"
    )

    print(
        "Ask me about your marks, attendance,"
    )

    print(
        "performance, risk, recommendation, "
        "or trend."
    )

    print(
        "You can also ask general academic questions."
    )

    print(
        "Type 'bye' to exit."
    )

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

        user_input = input(
            "\nYou: "
        )

        response, context = process_message(
            student_name,
            user_input,
            context
        )

        print(
            f"\nAI: {response}"
        )

        if context["last_intent"] == "exit":
            break


# ==========================================
# PROGRAM ENTRY POINT
# ==========================================

if __name__ == "__main__":

    student_name = input(
        "Enter student name: "
    )

    start_assistant(
        student_name
    )

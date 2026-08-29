# ==========================================
# AGENT CORE
# ==========================================

from agent.tools import (
    get_average,
    get_attendance,
    get_highest_subject,
    get_lowest_subject,
    get_performance,
    get_risk,
    get_recommendation,
    get_trend,
    get_subject_detail,
    get_subject_trend,
    answer_academic_question
)

from agent.planner import (
    create_plan
)

from agent.memory import (
    create_context,
    update_context
)

from agent.response_generator import (
    generate_response
)


# ==========================================
# TOOL EXECUTOR
# ==========================================

def execute_tool(
    tool_name,
    student_name,
    user_input=None,
    context=None
):
    """
    Execute one tool based on the tool
    selected by the planner.
    """

    # ======================================
    # BASIC PERFORMANCE TOOLS
    # ======================================

    if tool_name == "average":
        return get_average(
            student_name
        )

    if tool_name == "attendance":
        return get_attendance(
            student_name
        )

    if tool_name == "highest_subject":
        return get_highest_subject(
            student_name
        )

    if tool_name == "lowest_subject":
        return get_lowest_subject(
            student_name
        )

    if tool_name == "performance":
        return get_performance(
            student_name
        )

    if tool_name == "risk":
        return get_risk(
            student_name
        )

    if tool_name == "recommendation":
        return get_recommendation(
            student_name
        )

    if tool_name == "trend":
        return get_trend(
            student_name
        )


    # ======================================
    # SUBJECT DETAIL
    # ======================================

    if tool_name == "subject_detail":

        if context is None:
            return {
                "success": False,
                "message": "Context is missing."
            }

        subject = context.get(
            "requested_subject"
        )

        if subject is None:
            subject = context.get(
                "last_subject"
            )

        if subject is None:
            return {
                "success": False,
                "message": (
                    "I don't know which subject "
                    "you are referring to."
                )
            }

        return get_subject_detail(
            student_name,
            subject
        )


    # ======================================
    # SUBJECT TREND
    # ======================================

    if tool_name == "subject_trend":

        if context is None:
            return {
                "success": False,
                "message": "Context is missing."
            }

        subject = context.get(
            "requested_subject"
        )

        if subject is None:
            subject = context.get(
                "last_subject"
            )

        if subject is None:
            return {
                "success": False,
                "message": (
                    "I don't know which subject "
                    "you are referring to."
                )
            }

        return get_subject_trend(
            student_name,
            subject
        )


    # ======================================
    # SUBJECT EXPLANATION
    # ======================================

    if tool_name == "subject_explanation":

        if context is None:
            return {
                "success": False,
                "message": "Context is missing."
            }

        # ----------------------------------
        # Find subject from memory
        # ----------------------------------

        subject = context.get(
            "requested_subject"
        )

        if subject is None:
            subject = context.get(
                "last_subject"
            )

        if subject is None:
            return {
                "success": False,
                "message": (
                    "I don't know which subject "
                    "you are referring to."
                )
            }

        # ----------------------------------
        # Previous conversation state
        # ----------------------------------

        last_subject_type = context.get(
            "last_subject_type"
        )

        last_result = context.get(
            "last_result"
        )

        previous_result = context.get(
            "previous_result"
        )

        # ----------------------------------
        # Find the most useful mark
        # ----------------------------------

        mark = None

        if isinstance(
            last_result,
            dict
        ):
            mark = last_result.get(
                "mark"
            )

        if mark is None:
            if isinstance(
                previous_result,
                dict
            ):
                mark = previous_result.get(
                    "mark"
                )

        # ----------------------------------
        # IMPORTANT:
        # Check the CURRENT USER QUESTION
        # BEFORE highest/lowest explanation.
        #
        # This fixes:
        # "Is that good?"
        # "Is that bad?"
        # ----------------------------------

        user_text = (
            user_input or ""
        ).lower().strip()

        is_good_question = any(
            phrase in user_text
            for phrase in [
                "is that good",
                "is it good",
                "is that okay",
                "is it okay"
            ]
        )

        is_bad_question = any(
            phrase in user_text
            for phrase in [
                "is that bad",
                "is it bad"
            ]
        )

        # ==================================
        # GOOD / BAD EVALUATION
        # ==================================

        if (
            is_good_question
            or is_bad_question
        ):

            if mark is None:
                return {
                    "success": False,
                    "message": (
                        "I don't have the mark "
                        "needed to evaluate it."
                    )
                }

            # --------------------------------
            # GOOD QUESTION
            # --------------------------------

            if is_good_question:

                if mark >= 85:
                    explanation = (
                        f"Your {subject} mark is "
                        f"{mark:.2f}. "
                        f"Yes, that's a strong mark."
                    )

                elif mark >= 70:
                    explanation = (
                        f"Your {subject} mark is "
                        f"{mark:.2f}. "
                        f"Yes, that's a good mark."
                    )

                elif mark >= 50:
                    explanation = (
                        f"Your {subject} mark is "
                        f"{mark:.2f}. "
                        f"It's an average mark, "
                        f"so there is room for "
                        f"improvement."
                    )

                else:
                    explanation = (
                        f"Your {subject} mark is "
                        f"{mark:.2f}. "
                        f"It needs improvement."
                    )

            # --------------------------------
            # BAD QUESTION
            # --------------------------------

            else:

                if mark >= 85:
                    bad_response = (
                        "No, that's not a bad mark. "
                        "It's a strong mark, though "
                        "you can always improve."
                    )

                elif mark >= 70:
                    bad_response = (
                        "No, that's not a bad mark. "
                        "It's a good mark, though "
                        "there is still room to improve."
                    )

                elif mark >= 50:
                    bad_response = (
                        "It isn't a failing mark, "
                        "but there is definitely "
                        "room for improvement."
                    )

                else:
                    bad_response = (
                        "Yes, that mark needs "
                        "improvement."
                    )

                explanation = (
                    f"Your {subject} mark is "
                    f"{mark:.2f}. "
                    f"{bad_response}"
                )

            return {
                "success": True,
                "subject": subject,
                "mark": mark,
                "explanation": explanation,
                "explanation_type": "evaluation"
            }


        # ==================================
        # WHY AFTER LOWEST SUBJECT
        # ==================================

        if last_subject_type == "lowest":

            if mark is not None:
                explanation = (
                    f"{subject} is your "
                    f"lowest-scoring subject "
                    f"because its mark of "
                    f"{mark:.2f} is the lowest "
                    f"among your subjects."
                )

            else:
                explanation = (
                    f"{subject} is your "
                    f"lowest-scoring subject "
                    f"because it has the lowest "
                    f"mark among your subjects."
                )

            return {
                "success": True,
                "subject": subject,
                "mark": mark,
                "explanation": explanation,
                "explanation_type": "lowest"
            }


        # ==================================
        # WHY AFTER HIGHEST SUBJECT
        # ==================================

        if last_subject_type == "highest":

            if mark is not None:
                explanation = (
                    f"{subject} is your "
                    f"highest-scoring subject "
                    f"because its mark of "
                    f"{mark:.2f} is the highest "
                    f"among your subjects."
                )

            else:
                explanation = (
                    f"{subject} is your "
                    f"highest-scoring subject "
                    f"because it has the highest "
                    f"mark among your subjects."
                )

            return {
                "success": True,
                "subject": subject,
                "mark": mark,
                "explanation": explanation,
                "explanation_type": "highest"
            }


        # ==================================
        # GENERIC EXPLANATION
        # ==================================

        return {
            "success": True,
            "subject": subject,
            "mark": mark,
            "explanation": (
                f"{subject} is the subject "
                f"we were discussing."
            )
        }


    # ======================================
    # RAG / ACADEMIC QUESTION
    # ======================================

    if tool_name == "academic_question":

        if user_input is None:
            return {
                "success": False,
                "message": (
                    "Academic question is missing."
                )
            }

        return answer_academic_question(
            user_input
        )


    # ======================================
    # GREETING
    # ======================================

    if tool_name == "greeting":

        return {
            "success": True,
            "response": (
                f"Hello {student_name}! 👋 "
                "How can I help you with your "
                "academics today?"
            )
        }


    # ======================================
    # THANKS
    # ======================================

    if tool_name == "thanks":

        return {
            "success": True,
            "response": (
                "You're welcome! 😊 "
                "I'm here if you need help "
                "with your academic performance."
            )
        }


    # ======================================
    # GOODBYE
    # ======================================

    if tool_name == "goodbye":

        return {
            "success": True,
            "response": (
                f"Goodbye, {student_name}! 👋"
            )
        }


    # ======================================
    # UNKNOWN TOOL
    # ======================================

    return {
        "success": False,
        "message": (
            f"Unknown tool: {tool_name}"
        )
    }


# ==========================================
# AGENT CORE
# ==========================================

def run_agent(
    student_name,
    user_input,
    context=None
):
    """
    Plan, execute tools, update memory,
    and generate final response.
    """

    # ======================================
    # CREATE / RESTORE MEMORY
    # ======================================

    if context is None:
        context = create_context(
            student_name
        )

    context["student_name"] = (
        student_name
    )


    # ======================================
    # CREATE PLAN
    # ======================================

    plan = create_plan(
        user_input,
        context
    )


    # ======================================
    # NO TOOL REQUIRED
    # ======================================

    if not plan:

        response = (
            "I don't know which tool to use "
            "for this question."
        )

        return {
            "success": False,
            "message": response,
            "response": response,
            "plan": [],
            "results": {},
            "context": context
        }


    # ======================================
    # EXECUTE TOOLS
    # ======================================

    results = {}

    for tool_name in plan:

        try:

            result = execute_tool(
                tool_name,
                student_name,
                user_input,
                context
            )

        except Exception as error:

            result = {
                "success": False,
                "message": (
                    f"Tool '{tool_name}' failed: "
                    f"{str(error)}"
                )
            }

        results[tool_name] = result


        # ----------------------------------
        # UPDATE MEMORY
        # ----------------------------------

        context = update_context(
            context,
            tool_name,
            result,
            user_input
        )


    # ======================================
    # GENERATE RESPONSE
    # ======================================

    response = generate_response(
        plan,
        results,
        student_name
    )


    # ======================================
    # RETURN COMPLETE RESULT
    # ======================================

    return {
        "success": True,
        "response": response,
        "plan": plan,
        "results": results,
        "context": context
    }


# ==========================================
# FULL INTEGRATION TEST
# ==========================================

if __name__ == "__main__":

    student_name = input(
        "Enter student name: "
    )

    context = create_context(
        student_name
    )

    test_questions = [

        "What is my lowest subject?",

        "How much?",

        "Why?",

        "Is that good?",

        "Is that bad?",

        "How did I improve?",

        "What is my highest subject?",

        "How much?",

        "Why?",

        "Is that good?",

        "Is that bad?",

        "How did I improve?",

        "What is my average?",

        "What is my attendance?",

        "Am I performing well?",

        "Am I at risk?",

        "What should I improve?",

        "What is my trend?",

        "What is my average and attendance?",

        "What are my highest and lowest subjects?",

        "Tell me my performance and risk.",

        "hii",

        "hello",

        "thanks",

        "okay",

        "bye"
    ]


    print(
        "\n========================================"
    )

    print(
        "       AGENT FULL INTEGRATION TEST"
    )

    print(
        "========================================"
    )


    for question in test_questions:

        print(
            f"\nQuestion: {question}"
        )

        result = run_agent(
            student_name,
            question,
            context
        )

        print(
            "\nResponse:"
        )

        print(
            result["response"]
        )

        print(
            "\nPlan:"
        )

        print(
            result["plan"]
        )

        print(
            "\nMemory:"
        )

        print(
            result["context"]
        )

        context = result["context"]
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

from agent.planner import create_plan

from agent.memory import (
    create_context,
    update_context
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
    Execute one tool based on the
    tool selected by the planner.
    """

    # ======================================
    # BASIC PERFORMANCE TOOLS
    # ======================================

    if tool_name == "average":
        return get_average(student_name)

    if tool_name == "attendance":
        return get_attendance(student_name)

    if tool_name == "highest_subject":
        return get_highest_subject(student_name)

    if tool_name == "lowest_subject":
        return get_lowest_subject(student_name)

    if tool_name == "performance":
        return get_performance(student_name)

    if tool_name == "risk":
        return get_risk(student_name)

    if tool_name == "recommendation":
        return get_recommendation(student_name)

    if tool_name == "trend":
        return get_trend(student_name)

    # ======================================
    # SUBJECT DETAIL
    # ======================================

    if tool_name == "subject_detail":

        if context is None:
            return {
                "success": False,
                "message": "Context is missing."
            }

        subject = context.get("requested_subject")

        if subject is None:
            subject = context.get("last_subject")

        if subject is None:
            return {
                "success": False,
                "message": "I don't know which subject you are referring to."
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

        subject = context.get("requested_subject")

        if subject is None:
            subject = context.get("last_subject")

        if subject is None:
            return {
                "success": False,
                "message": "I don't know which subject you are referring to."
            }

        return get_subject_trend(
            student_name,
            subject
        )

    # ======================================
    # RAG / ACADEMIC QUESTION
    # ======================================

    if tool_name == "academic_question":

        if user_input is None:
            return {
                "success": False,
                "message": "Academic question is missing."
            }

        return answer_academic_question(
            user_input
        )

    # ======================================
    # UNKNOWN TOOL
    # ======================================

    return {
        "success": False,
        "message": f"Unknown tool: {tool_name}"
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
    Plan, execute tools, and update
    agent memory.
    """

    # ======================================
    # CREATE / RESTORE MEMORY
    # ======================================

    if context is None:
        context = create_context(
            student_name
        )

    context["student_name"] = student_name

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
        return {
            "success": False,
            "message": (
                "I don't know which tool to use "
                "for this question."
            ),
            "plan": [],
            "results": {},
            "context": context
        }

    # ======================================
    # EXECUTE TOOLS
    # ======================================

    results = {}

    for tool_name in plan:

        result = execute_tool(
            tool_name,
            student_name,
            user_input,
            context
        )

        results[tool_name] = result

        # ==================================
        # UPDATE MEMORY
        # ==================================

        context = update_context(
            context,
            tool_name,
            result
        )

    # ======================================
    # RETURN AGENT RESULT
    # ======================================

    return {
        "success": True,
        "plan": plan,
        "results": results,
        "context": context
    }


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    student_name = input(
        "Enter student name: "
    )

    # ======================================
    # CREATE CONVERSATION MEMORY
    # ======================================

    context = create_context(
        student_name
    )

    # ======================================
    # TEST QUESTIONS
    # ======================================

    test_questions = [

        "What is my average?",

        "What is my lowest subject?",

        "What is my highest subject?",

        "How much?",

        "How did I improve?",

        "What is my trend?",

        "What is my risk?",

        "What should I improve?",

        "What does an improving trend mean?",

        "Is 80% attendance good?"
    ]

    print("\n========================================")
    print("       AGENT MEMORY INTEGRATION TEST")
    print("========================================")

    for question in test_questions:

        print(
            f"\nQuestion: {question}"
        )

        result = run_agent(
            student_name,
            question,
            context
        )

        # ==================================
        # PRINT PLAN
        # ==================================

        print("\nPlan:")
        print(result["plan"])

        # ==================================
        # PRINT RESULTS
        # ==================================

        print("\nResults:")

        for (
            tool_name,
            tool_result
        ) in result["results"].items():

            print(
                f"\n[{tool_name}]"
            )

            print(tool_result)

        # ==================================
        # RESTORE UPDATED MEMORY
        # ==================================

        context = result["context"]

        print("\nMemory:")
        print(context)
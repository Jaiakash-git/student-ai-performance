from agent.tools import (
    get_average,
    get_attendance,
    get_highest_subject,
    get_lowest_subject,
    get_performance,
    get_risk,
    get_recommendation,
    get_trend,
    answer_academic_question
)

from agent.planner import create_plan


# ==========================================
# TOOL EXECUTOR
# ==========================================

def execute_tool(
    tool_name,
    student_name,
    user_input=None
):
    """
    Execute one tool based on the
    tool selected by the planner.
    """

    # ======================================
    # PERSONAL ANALYTICS TOOLS
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
    user_input
):
    """
    Plan and execute the tools required
    to answer the user's question.
    """

    # ======================================
    # CREATE PLAN
    # ======================================

    plan = create_plan(
        user_input
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
            "results": {}
        }

    # ======================================
    # EXECUTE TOOLS
    # ======================================

    results = {}

    for tool_name in plan:

        result = execute_tool(
            tool_name,
            student_name,
            user_input
        )

        results[tool_name] = result

    # ======================================
    # RETURN AGENT RESULT
    # ======================================

    return {
        "success": True,
        "plan": plan,
        "results": results
    }


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    student_name = input(
        "Enter student name: "
    )

    test_questions = [

        "What is my average?",

        "What is my attendance?",

        "How am I performing and what should I improve?",

        "What is my risk and what should I improve?",

        "What is my highest subject and lowest subject?",

        "What does an improving trend mean?",

        "Is 80% attendance good?",

        "What is academic performance?"
    ]

    print("\n========================================")
    print("       AGENT CORE TEST")
    print("========================================")

    for question in test_questions:

        print(
            f"\nQuestion: {question}"
        )

        result = run_agent(
            student_name,
            question
        )

        print("\nPlan:")
        print(
            result["plan"]
        )

        print("\nResults:")

        for (
            tool_name,
            tool_result
        ) in result["results"].items():

            print(
                f"\n[{tool_name}]"
            )

            print(
                tool_result
            )
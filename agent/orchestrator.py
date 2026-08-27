from agent.planner import create_plan
from agent.agent_core import execute_tool
from agent.response_generator import generate_response


# ==========================================
# AGENT ORCHESTRATOR
# ==========================================

def run_orchestrator(
    student_name,
    user_input
):
    """
    Complete agent workflow:

    1. Understand the request
    2. Create a tool plan
    3. Execute required tools
    4. Generate a natural-language response
    """

    # ======================================
    # STEP 1: CREATE PLAN
    # ======================================

    plan = create_plan(user_input)

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
            "response": (
                "I don't know which tool to use "
                "for this question."
            )
        }

    # ======================================
    # STEP 2: EXECUTE TOOLS
    # ======================================

    results = {}

    for tool_name in plan:

        result = execute_tool(
            tool_name,
            student_name
        )

        results[tool_name] = result

    # ======================================
    # STEP 3: GENERATE RESPONSE
    # ======================================

    response = generate_response(
        plan,
        results
    )

    # ======================================
    # STEP 4: RETURN COMPLETE RESULT
    # ======================================

    return {
        "success": True,
        "plan": plan,
        "results": results,
        "response": response
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

        "What is my highest subject and lowest subject?"

    ]

    print("\n========================================")
    print("       AGENT ORCHESTRATOR TEST")
    print("========================================")

    for question in test_questions:

        print("\n----------------------------------------")
        print(f"Question: {question}")
        print("----------------------------------------")

        result = run_orchestrator(
            student_name,
            question
        )

        print("\nPlan:")
        print(result["plan"])

        print("\nFinal Response:")
        print(result["response"])


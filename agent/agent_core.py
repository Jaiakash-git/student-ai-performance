from agent.tools import (
    get_average,
    get_attendance,
    get_highest_subject,
    get_lowest_subject,
    get_performance,
    get_risk,
    get_recommendation,
    get_trend
)


# ==========================================
# AGENT CORE
# ==========================================

def run_agent(student_name, user_input):

    text = user_input.lower().strip()

    # ======================================
    # AVERAGE
    # ======================================

    if "average" in text:

        return {
            "tool": "average",
            "result": get_average(student_name)
        }

    # ======================================
    # ATTENDANCE
    # ======================================

    if "attendance" in text:

        return {
            "tool": "attendance",
            "result": get_attendance(student_name)
        }

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

        return {
            "tool": "highest_subject",
            "result": get_highest_subject(student_name)
        }

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

        return {
            "tool": "lowest_subject",
            "result": get_lowest_subject(student_name)
        }

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

        return {
            "tool": "performance",
            "result": get_performance(student_name)
        }

    # ======================================
    # RISK
    # ======================================

    if "risk" in text:

        return {
            "tool": "risk",
            "result": get_risk(student_name)
        }

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

        return {
            "tool": "recommendation",
            "result": get_recommendation(student_name)
        }

    # ======================================
    # TREND
    # ======================================

    if any(
        phrase in text
        for phrase in [
            "trend",
            "improving",
            "improve",
            "getting better",
            "getting worse",
            "progress"
        ]
    ):

        return {
            "tool": "trend",
            "result": get_trend(student_name)
        }

    # ======================================
    # UNKNOWN
    # ======================================

    return {
        "tool": None,
        "result": {
            "success": False,
            "message": (
                "I don't know which tool to use "
                "for this question."
            )
        }
    }


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    student_name = input(
        "Enter student name: "
    )

    while True:

        user_input = input(
            "\nYou: "
        )

        if user_input.lower().strip() in [
            "bye",
            "exit",
            "quit"
        ]:

            print(
                "\nAgent: Goodbye! 👋"
            )

            break

        result = run_agent(
            student_name,
            user_input
        )

        print("\nAgent:")
        print(result)

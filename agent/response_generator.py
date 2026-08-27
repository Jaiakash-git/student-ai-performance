# ==========================================
# AGENT RESPONSE GENERATOR
# ==========================================
# Converts tool results into a natural
# language response.
# ==========================================


def generate_response(plan, results):
    """
    Convert the agent's tool results into
    a user-friendly response.
    """

    responses = []

    # ======================================
    # AVERAGE
    # ======================================

    if "average" in results:

        result = results["average"]

        if result["success"]:

            responses.append(
                f"Your average mark is "
                f"{result['average']:.2f}."
            )

    # ======================================
    # ATTENDANCE
    # ======================================

    if "attendance" in results:

        result = results["attendance"]

        if result["success"]:

            responses.append(
                f"Your overall attendance is "
                f"{result['attendance']:.2f}%."
            )

    # ======================================
    # HIGHEST SUBJECT
    # ======================================

    if "highest_subject" in results:

        result = results["highest_subject"]

        if result["success"]:

            responses.append(
                f"{result['subject']} is your highest "
                f"scoring subject with "
                f"{result['mark']:.2f} marks."
            )

    # ======================================
    # LOWEST SUBJECT
    # ======================================

    if "lowest_subject" in results:

        result = results["lowest_subject"]

        if result["success"]:

            responses.append(
                f"{result['subject']} is your lowest "
                f"scoring subject with "
                f"{result['mark']:.2f} marks."
            )

    # ======================================
    # PERFORMANCE
    # ======================================

    if "performance" in results:

        result = results["performance"]

        if result["success"]:

            responses.append(
                f"Your performance status is "
                f"{result['status']}.\n"
                f"Average mark: "
                f"{result['average']:.2f}\n"
                f"Overall attendance: "
                f"{result['attendance']:.2f}%."
            )

    # ======================================
    # RISK
    # ======================================

    if "risk" in results:

        result = results["risk"]

        if result["success"]:

            responses.append(
                f"Your academic risk level is "
                f"{result['risk_level']}.\n"
                f"Risk probability: "
                f"{result['risk_probability']:.2f}%."
            )

    # ======================================
    # RECOMMENDATION
    # ======================================

    if "recommendation" in results:

        result = results["recommendation"]

        if result["success"]:

            recommendation = result[
                "recommendation"
            ]

            priority_subject = result[
                "priority_subject"
            ]

            priority_mark = result[
                "priority_mark"
            ]

            responses.append(
                f"{recommendation}\n"
                f"Priority subject: "
                f"{priority_subject} "
                f"({priority_mark:.2f})"
            )

    # ======================================
    # TREND
    # ======================================

    if "trend" in results:

        result = results["trend"]

        if result["success"]:

            overall_trend = result[
                "overall_trend"
            ]

            average_improvement = result[
                "average_improvement"
            ]

            responses.append(
                f"Your overall performance trend "
                f"is {overall_trend}.\n"
                f"Average improvement: "
                f"{average_improvement:+.2f}."
            )

    # ======================================
    # NO SUCCESSFUL RESULTS
    # ======================================

    if not responses:

        return (
            "I couldn't find enough information "
            "to answer your question."
        )

    # ======================================
    # COMBINE RESPONSES
    # ======================================

    return "\n\n".join(responses)


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    print("\n========================================")
    print("       RESPONSE GENERATOR TEST")
    print("========================================")

    # --------------------------------------
    # TEST 1
    # --------------------------------------

    plan = [
        "performance",
        "recommendation"
    ]

    results = {

        "performance": {
            "success": True,
            "status": "Excellent",
            "average": 89.17,
            "attendance": 94.17
        },

        "recommendation": {
            "success": True,
            "recommendation": (
                "Performance is currently stable. "
                "Continue maintaining good marks "
                "and attendance, especially in DBMS."
            ),
            "priority_subject": "OS",
            "priority_mark": 82.0
        }
    }

    print("\nTest 1:")
    print(
        generate_response(
            plan,
            results
        )
    )

    # --------------------------------------
    # TEST 2
    # --------------------------------------

    plan = [
        "highest_subject",
        "lowest_subject"
    ]

    results = {

        "highest_subject": {
            "success": True,
            "subject": "DBMS",
            "mark": 94.0
        },

        "lowest_subject": {
            "success": True,
            "subject": "OS",
            "mark": 82.0
        }
    }

    print("\nTest 2:")
    print(
        generate_response(
            plan,
            results
        )
    )

    # --------------------------------------
    # TEST 3
    # --------------------------------------

    plan = [
        "risk"
    ]

    results = {

        "risk": {
            "success": True,
            "risk_level": "Low",
            "risk_probability": 3.23,
            "average": 89.17,
            "attendance": 94.17
        }
    }

    print("\nTest 3:")
    print(
        generate_response(
            plan,
            results
        )
    )

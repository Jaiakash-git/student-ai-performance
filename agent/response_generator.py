# ==========================================
# AGENT RESPONSE GENERATOR
# ==========================================
# Converts tool results into natural
# language responses.
# ==========================================


def generate_response(
    plan,
    results,
    student_name=None
):
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
    # Important:
    # Do NOT show the mark here.
    #
    # The user can ask:
    # "How much?"
    #
    # and the subject_detail tool will
    # provide the actual mark.

    if "highest_subject" in results:

        result = results["highest_subject"]

        if result["success"]:

            responses.append(
                f"{result['subject']} is your "
                f"highest-scoring subject."
            )

    # ======================================
    # LOWEST SUBJECT
    # ======================================
    # Do NOT show the mark here.
    #
    # The user can ask:
    # "How much?"
    #
    # and the subject_detail tool will
    # provide the actual mark.

    if "lowest_subject" in results:

        result = results["lowest_subject"]

        if result["success"]:

            responses.append(
                f"{result['subject']} is your "
                f"lowest-scoring subject."
            )

    # ======================================
    # SUBJECT DETAIL
    # ======================================

    if "subject_detail" in results:

        result = results["subject_detail"]

        if result["success"]:

            responses.append(
                f"Your mark in "
                f"{result['subject']} is "
                f"{result['mark']:.2f}."
            )

    # ======================================
    # SUBJECT TREND
    # ======================================

    if "subject_trend" in results:

        result = results["subject_trend"]

        if result["success"]:

            subject = result["subject"]

            first_mark = result["first_mark"]

            latest_mark = result["latest_mark"]

            improvement = result["improvement"]

            if improvement > 0:

                trend_message = (
                    f"Your mark in {subject} "
                    f"improved by "
                    f"{improvement:.2f} marks."
                )

            elif improvement < 0:

                trend_message = (
                    f"Your mark in {subject} "
                    f"decreased by "
                    f"{abs(improvement):.2f} marks."
                )

            else:

                trend_message = (
                    f"Your mark in {subject} "
                    f"remained stable."
                )

            responses.append(
                f"{trend_message}\n"
                f"First mark: {first_mark:.2f}\n"
                f"Latest mark: {latest_mark:.2f}"
            )

    # ======================================
    # SUBJECT EXPLANATION
    # ======================================
    # Handles questions such as:
    #
    # "Why?"
    # "Why is OS my lowest?"
    # "Why is this my weakest subject?"

    if "subject_explanation" in results:

        result = results["subject_explanation"]

        if result["success"]:

            responses.append(
                result["explanation"]
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
    # OVERALL TREND
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
    # RAG / ACADEMIC QUESTION
    # ======================================

    if "academic_question" in results:

        result = results["academic_question"]

        if result["success"]:

            responses.append(
                result["answer"]
            )

    # ======================================
    # GOODBYE
    # ======================================

    if "goodbye" in results:

        if student_name:

            responses.append(
                f"Goodbye, {student_name}! 👋"
            )

        else:

            responses.append(
                "Goodbye! 👋"
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
    # TEST 1 - HIGHEST SUBJECT
    # --------------------------------------

    plan = [
        "highest_subject"
    ]

    results = {

        "highest_subject": {

            "success": True,

            "subject": "DBMS",

            "mark": 94.0
        }
    }

    print("\nTest 1:")

    print(
        generate_response(
            plan,
            results,
            "Jaiakash"
        )
    )

    # --------------------------------------
    # TEST 2 - LOWEST SUBJECT
    # --------------------------------------

    plan = [
        "lowest_subject"
    ]

    results = {

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
            results,
            "Jaiakash"
        )
    )

    # --------------------------------------
    # TEST 3 - SUBJECT DETAIL
    # --------------------------------------

    plan = [
        "subject_detail"
    ]

    results = {

        "subject_detail": {

            "success": True,

            "subject": "OS",

            "mark": 82.0
        }
    }

    print("\nTest 3:")

    print(
        generate_response(
            plan,
            results,
            "Jaiakash"
        )
    )

    # --------------------------------------
    # TEST 4 - SUBJECT EXPLANATION
    # --------------------------------------

    plan = [
        "subject_explanation"
    ]

    results = {

        "subject_explanation": {

            "success": True,

            "explanation": (
                "OS is your lowest-scoring subject "
                "because it has the lowest mark "
                "among your subjects."
            )
        }
    }

    print("\nTest 4:")

    print(
        generate_response(
            plan,
            results,
            "Jaiakash"
        )
    )

    # --------------------------------------
    # TEST 5 - GOODBYE
    # --------------------------------------

    plan = [
        "goodbye"
    ]

    results = {

        "goodbye": {

            "success": True
        }
    }

    print("\nTest 5:")

    print(
        generate_response(
            plan,
            results,
            "Jaiakash"
        )
    )

    # --------------------------------------
    # TEST 6 - SUBJECT TREND
    # --------------------------------------

    plan = [
        "subject_trend"
    ]

    results = {

        "subject_trend": {

            "success": True,

            "subject": "OS",

            "first_mark": 82.0,

            "latest_mark": 88.0,

            "improvement": 6.0
        }
    }

    print("\nTest 6:")

    print(
        generate_response(
            plan,
            results,
            "Jaiakash"
        )
    )

    # --------------------------------------
    # TEST 7 - ACADEMIC QUESTION
    # --------------------------------------

    plan = [
        "academic_question"
    ]

    results = {

        "academic_question": {

            "success": True,

            "answer": (
                "An improving trend means that "
                "recent marks are higher than "
                "earlier marks."
            )
        }
    }

    print("\nTest 7:")

    print(
        generate_response(
            plan,
            results,
            "Jaiakash"
        )
    )


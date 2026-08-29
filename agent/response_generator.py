# ==========================================
# RESPONSE GENERATOR
# ==========================================


def generate_response(
    plan,
    results,
    student_name
):
    """
    Convert tool results into a natural-language
    response.
    """

    responses = []


    # ======================================
    # LOOP THROUGH TOOLS
    # ======================================

    for tool_name in plan:

        result = results.get(
            tool_name
        )

        if not result:
            continue

        # ----------------------------------
        # TOOL FAILED
        # ----------------------------------

        if not result.get("success", False):

            message = result.get(
                "message",
                "Something went wrong."
            )

            responses.append(
                message
            )

            continue


        # ==================================
        # AVERAGE
        # ==================================

        if tool_name == "average":

            average = result.get(
                "average"
            )

            responses.append(
                f"Your average mark is "
                f"{average:.2f}."
            )


        # ==================================
        # ATTENDANCE
        # ==================================

        elif tool_name == "attendance":

            attendance = result.get(
                "attendance"
            )

            responses.append(
                f"Your overall attendance is "
                f"{attendance:.2f}%."
            )


        # ==================================
        # HIGHEST SUBJECT
        # ==================================

        elif tool_name == "highest_subject":

            subject = result.get(
                "subject"
            )

            responses.append(
                f"{subject} is your "
                f"highest-scoring subject."
            )


        # ==================================
        # LOWEST SUBJECT
        # ==================================

        elif tool_name == "lowest_subject":

            subject = result.get(
                "subject"
            )

            responses.append(
                f"{subject} is your "
                f"lowest-scoring subject."
            )


        # ==================================
        # SUBJECT DETAIL
        # ==================================

        elif tool_name == "subject_detail":

            subject = result.get(
                "subject"
            )

            mark = result.get(
                "mark"
            )

            responses.append(
                f"Your mark in {subject} "
                f"is {mark:.2f}."
            )


        # ==================================
        # SUBJECT EXPLANATION
        # ==================================

        elif tool_name == "subject_explanation":

            explanation = result.get(
                "explanation"
            )

            if explanation:

                responses.append(
                    explanation
                )

            else:

                responses.append(
                    result.get(
                        "message",
                        "I couldn't explain that."
                    )
                )


        # ==================================
        # SUBJECT TREND
        # ==================================

        elif tool_name == "subject_trend":

            subject = result.get(
                "subject"
            )

            first_mark = result.get(
                "first_mark"
            )

            latest_mark = result.get(
                "latest_mark"
            )

            improvement = result.get(
                "improvement"
            )

            if improvement > 0:

                responses.append(
                    f"Your mark in {subject} "
                    f"improved by {improvement:.2f} marks.\n"
                    f"First mark: {first_mark:.2f}\n"
                    f"Latest mark: {latest_mark:.2f}"
                )

            elif improvement < 0:

                responses.append(
                    f"Your mark in {subject} "
                    f"decreased by "
                    f"{abs(improvement):.2f} marks.\n"
                    f"First mark: {first_mark:.2f}\n"
                    f"Latest mark: {latest_mark:.2f}"
                )

            else:

                responses.append(
                    f"Your mark in {subject} "
                    f"remained the same.\n"
                    f"First mark: {first_mark:.2f}\n"
                    f"Latest mark: {latest_mark:.2f}"
                )


        # ==================================
        # PERFORMANCE
        # ==================================

        elif tool_name == "performance":

            status = result.get(
                "status"
            )

            average = result.get(
                "average"
            )

            attendance = result.get(
                "attendance"
            )

            responses.append(
                f"Your performance status is "
                f"{status}.\n"
                f"Average mark: {average:.2f}\n"
                f"Overall attendance: "
                f"{attendance:.2f}%."
            )


        # ==================================
        # RISK
        # ==================================

        elif tool_name == "risk":

            risk_level = result.get(
                "risk_level"
            )

            probability = result.get(
                "risk_probability"
            )

            responses.append(
                f"Your academic risk level is "
                f"{risk_level}.\n"
                f"Risk probability: "
                f"{probability:.2f}%."
            )


        # ==================================
        # RECOMMENDATION
        # ==================================

        elif tool_name == "recommendation":

            recommendation = result.get(
                "recommendation"
            )

            priority_subject = result.get(
                "priority_subject"
            )

            priority_mark = result.get(
                "priority_mark"
            )

            if priority_subject:

                responses.append(
                    f"{recommendation}\n"
                    f"Priority subject: "
                    f"{priority_subject} "
                    f"({priority_mark:.2f})"
                )

            else:

                responses.append(
                    recommendation
                )


        # ==================================
        # OVERALL TREND
        # ==================================

        elif tool_name == "trend":

            overall_trend = result.get(
                "overall_trend"
            )

            average_improvement = result.get(
                "average_improvement"
            )

            if average_improvement > 0:

                responses.append(
                    f"Your overall performance "
                    f"trend is {overall_trend}.\n"
                    f"Average improvement: "
                    f"+{average_improvement:.2f}."
                )

            elif average_improvement < 0:

                responses.append(
                    f"Your overall performance "
                    f"trend is {overall_trend}.\n"
                    f"Average change: "
                    f"{average_improvement:.2f}."
                )

            else:

                responses.append(
                    f"Your overall performance "
                    f"trend is {overall_trend}.\n"
                    f"Average improvement: 0.00."
                )


        # ==================================
        # ACADEMIC QUESTION
        # ==================================

        elif tool_name == "academic_question":

            answer = result.get(
                "answer"
            )

            responses.append(
                answer
            )


        # ==================================
        # GREETING
        # ==================================

        elif tool_name == "greeting":

            responses.append(
                f"Hello {student_name}! 👋 "
                f"How can I help you with your "
                f"academics today?"
            )


        # ==================================
        # THANKS
        # ==================================

        elif tool_name == "thanks":

            responses.append(
                "You're welcome! 😊 "
                "I'm here if you need help with "
                "your academic performance."
            )


        # ==================================
        # GOODBYE
        # ==================================

        elif tool_name == "goodbye":

            responses.append(
                f"Goodbye, {student_name}! 👋"
            )


        # ==================================
        # UNKNOWN
        # ==================================

        else:

            message = result.get(
                "message",
                "I couldn't generate a response."
            )

            responses.append(
                message
            )


    # ======================================
    # COMBINE RESPONSES
    # ======================================

    return "\n\n".join(
        responses
    )
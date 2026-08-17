from services.performance_service import (
    analyze_performance,
    get_performance_status
)

from services.attendance_service import (
    get_student_attendance
)

from services.student_service import (
    get_student_marks,
    get_student_exam_marks,
    get_student_id
)

from services.trend_service import analyze_trend

from ml.predict import predict_performance

from services.recommendation_service import (
    generate_recommendation
)


def route_intent(intent, student_name):

    # ==========================================
    # GET STUDENT ID
    # ==========================================

    student_id = get_student_id(student_name)

    if not student_id:
        return "Student not found."


    # ==========================================
    # GET MARKS
    # ==========================================

    results = get_student_marks(student_name)

    if not results:
        return "No marks found for this student."


    # ==========================================
    # GET ATTENDANCE
    # ==========================================

    attendance_results = get_student_attendance(
        student_id
    )


    # ==========================================
    # GET EXAM-WISE MARKS
    # ==========================================

    exam_results = get_student_exam_marks(
        student_name
    )


    # ==========================================
    # COMMON PERFORMANCE ANALYSIS
    # ==========================================

    average, highest_mark, highest_subject, overall_attendance = (
        analyze_performance(
            results,
            attendance_results
        )
    )


    # ==========================================
    # LOWEST MARK
    # ==========================================

    lowest_subject, lowest_mark = min(
        results,
        key=lambda item: float(item[1])
    )

    lowest_mark = float(lowest_mark)


    # ==========================================
    # AVERAGE
    # ==========================================

    if intent == "average":

        return (
            f"Your average mark is "
            f"{average:.2f}."
        )


    # ==========================================
    # ATTENDANCE
    # ==========================================

    elif intent == "attendance":

        return (
            f"Your overall attendance is "
            f"{overall_attendance:.2f}%."
        )


    # ==========================================
    # MARKS
    # ==========================================

    elif intent == "marks":

        response = "Here are your marks:\n"

        for subject, mark in results:

            response += (
                f"{subject}: "
                f"{float(mark):.2f}\n"
            )

        return response.strip()


    # ==========================================
    # HIGHEST SUBJECT
    # ==========================================

    elif intent == "highest_subject":

        return (
            f"Your highest scoring subject is "
            f"{highest_subject} with "
            f"{highest_mark:.2f} marks."
        )


    # ==========================================
    # LOWEST SUBJECT
    # ==========================================

    elif intent == "lowest_subject":

        return (
            f"Your lowest scoring subject is "
            f"{lowest_subject} with "
            f"{lowest_mark:.2f} marks."
        )


    # ==========================================
    # PERFORMANCE
    # ==========================================

    elif intent == "performance":

        status = get_performance_status(
            average,
            overall_attendance
        )

        return (
            f"Your current performance is "
            f"{status}.\n"
            f"Average mark: {average:.2f}\n"
            f"Overall attendance: "
            f"{overall_attendance:.2f}%"
        )


    # ==========================================
    # RISK
    # ==========================================

    elif intent == "risk":

        ml_prediction, risk_probability = (
            predict_performance(
                average,
                overall_attendance,
                highest_mark,
                lowest_mark
            )
        )

        return (
            f"Your current ML prediction is "
            f"{ml_prediction}.\n"
            f"Risk probability: "
            f"{risk_probability:.2f}%."
        )


    # ==========================================
    # RECOMMENDATION
    # ==========================================

    elif intent == "recommendation":

        ml_prediction, risk_probability = (
            predict_performance(
                average,
                overall_attendance,
                highest_mark,
                lowest_mark
            )
        )

        recommendation = generate_recommendation(
            average,
            overall_attendance,
            risk_probability,
            lowest_subject,
            highest_subject
        )

        return recommendation


    # ==========================================
    # TREND
    # ==========================================

    elif intent == "trend":

        trend, average_improvement, overall_trend = (
            analyze_trend(
                exam_results
            )
        )

        if not trend:

            return (
                "There is not enough exam data "
                "to calculate your trend."
            )

        response = (
            f"Your overall performance trend "
            f"is {overall_trend}.\n\n"
        )

        for (
            subject,
            first_mark,
            second_mark,
            improvement
        ) in trend:

            response += (
                f"{subject}: "
                f"{first_mark:.2f} → "
                f"{second_mark:.2f} "
                f"({improvement:+.2f})\n"
            )

        response += (
            f"\nAverage improvement: "
            f"{average_improvement:+.2f}"
        )

        return response


    # ==========================================
    # UNKNOWN
    # ==========================================

    return (
        "I'm not sure what you're asking. "
        "Try asking about your marks, average, "
        "attendance, highest subject, "
        "lowest subject, performance, "
        "risk, recommendation, or trend."
    )
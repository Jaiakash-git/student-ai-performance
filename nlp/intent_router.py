from services.performance_service import analyze_performance
from services.attendance_service import get_student_attendance
from services.student_service import (
    get_student_marks,
    get_student_exam_marks,
    get_student_id
)
from services.trend_service import analyze_trend


def route_intent(intent, student_name, context=None):

    # Create context if not provided
    if context is None:
        context = {
            "last_intent": None,
            "last_subject": None
        }

    # ==========================================
    # GET STUDENT DATA
    # ==========================================

    student_id = get_student_id(student_name)

    if student_id is None:
        return "Student not found."

    results = get_student_marks(student_name)

    if not results:
        return "Student not found."

    attendance_results = get_student_attendance(student_id)

    exam_results = get_student_exam_marks(student_name)


    # ==========================================
    # AVERAGE
    # ==========================================

    if intent == "average":

        average, _, _, _ = analyze_performance(
            results,
            attendance_results
        )

        return f"Your average mark is {average:.2f}."


    # ==========================================
    # ATTENDANCE
    # ==========================================

    elif intent == "attendance":

        _, _, _, overall_attendance = analyze_performance(
            results,
            attendance_results
        )

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

        _, highest_mark, highest_subject, _ = analyze_performance(
            results,
            attendance_results
        )

        # Store subject in context
        context["last_subject"] = highest_subject

        return (
            f"Your highest scoring subject is "
            f"{highest_subject} with "
            f"{highest_mark:.2f} marks."
        )


    # ==========================================
    # LOWEST SUBJECT
    # ==========================================

    elif intent == "lowest_subject":

        lowest_subject, lowest_mark = min(
            results,
            key=lambda item: float(item[1])
        )

        # Store subject in context
        context["last_subject"] = lowest_subject

        return (
            f"Your lowest scoring subject is "
            f"{lowest_subject} with "
            f"{float(lowest_mark):.2f} marks."
        )


    # ==========================================
    # TREND
    # ==========================================

    elif intent == "trend":

        trend, average_improvement, overall_trend = analyze_trend(
            exam_results
        )

        if not trend:
            return (
                "There is not enough exam data "
                "to calculate your trend."
            )

        response = (
            f"Your overall performance trend is "
            f"{overall_trend}.\n\n"
        )

        for subject, first_mark, second_mark, improvement in trend:

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
    # PERFORMANCE
    # ==========================================

    elif intent == "performance":

        average, _, _, overall_attendance = analyze_performance(
            results,
            attendance_results
        )

        if average >= 85 and overall_attendance >= 85:
            status = "Excellent"

        elif average >= 70 and overall_attendance >= 75:
            status = "Good"

        elif average >= 50 and overall_attendance >= 65:
            status = "Average"

        else:
            status = "Needs Attention"

        return (
            f"Your current performance is {status}.\n"
            f"Average mark: {average:.2f}\n"
            f"Overall attendance: {overall_attendance:.2f}%"
        )


        # ==========================================
    # RECOMMENDATION
    # ==========================================

    elif intent == "recommendation":

        average, _, _, overall_attendance = analyze_performance(
            results,
            attendance_results
        )

        lowest_subject, lowest_mark = min(
            results,
            key=lambda item: float(item[1])
        )

        return (
            f"Based on your current performance, "
            f"you should focus on {lowest_subject} "
            f"({float(lowest_mark):.2f} marks).\n"
            f"Your average mark is {average:.2f} and "
            f"your attendance is {overall_attendance:.2f}%.\n"
            f"Keep maintaining your attendance and "
            f"give extra attention to your weaker subject."
        )

        # ==========================================
    # RISK
    # ==========================================

    elif intent == "risk":

        average, _, _, overall_attendance = analyze_performance(
            results,
            attendance_results
        )

        if average < 50 or overall_attendance < 65:
            risk_level = "High"
        elif average < 70 or overall_attendance < 75:
            risk_level = "Moderate"
        else:
            risk_level = "Low"

        return (
            f"Your current academic risk level is {risk_level}.\n"
            f"Average mark: {average:.2f}\n"
            f"Overall attendance: {overall_attendance:.2f}%"
        )


    # ==========================================
    # UNKNOWN
    # ==========================================

    return (
        "I'm not sure what you're asking. "
        "Try asking about your marks, average, "
        "attendance, highest subject, lowest subject, "
        "performance, risk, recommendation, or trend."
    )
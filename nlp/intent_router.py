from services.performance_service import analyze_performance
from services.attendance_service import get_student_attendance
from services.student_service import (
    get_student_marks,
    get_student_exam_marks,
    get_student_id
)
from services.trend_service import analyze_trend


def route_intent(intent, student_name):

    # Get student ID
    student_id = get_student_id(student_name)

    # Get marks
    results = get_student_marks(student_name)

    if not results:
        return "Student not found."

    # Get attendance
    attendance_results = get_student_attendance(student_id)

    # Get exam-wise marks
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
            response += f"{subject}: {float(mark):.2f}\n"

        return response.strip()


    # ==========================================
    # HIGHEST SUBJECT
    # ==========================================

    elif intent == "highest_subject":

        _, highest_mark, highest_subject, _ = analyze_performance(
            results,
            attendance_results
        )

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
            return "There is not enough exam data to calculate your trend."

        response = f"Your overall performance trend is {overall_trend}.\n\n"

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
    # UNKNOWN
    # ==========================================

    return (
        "I'm not sure what you're asking. "
        "Try asking about your marks, average, "
        "attendance, highest subject, lowest subject, "
        "or performance trend."
    )
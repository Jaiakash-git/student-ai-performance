from services.performance_service import analyze_performance
from services.attendance_service import get_student_attendance
from services.student_service import (
    get_student_marks,
    get_student_exam_marks,
    get_student_id,
    get_subject_mark
)
from services.trend_service import analyze_trend
from services.analytics_service import generate_academic_analysis


def route_intent(intent, student_name, context=None):

    # ==========================================
    # CREATE CONTEXT
    # ==========================================

    if context is None:

        context = {
            "last_intent": None,
            "last_subject": None,
            "follow_up": False,
            "subject_query": False,
            "requested_subject": None
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
    # SUBJECT FOLLOW-UP
    # ==========================================

    if context.get("subject_query", False):

        subject_name = context.get(
            "requested_subject"
        )

        if subject_name:

            subject, mark = get_subject_mark(
                student_name,
                subject_name
            )

            if subject is None:

                return (
                    f"I couldn't find a subject named "
                    f"{subject_name}."
                )

            mark = float(mark)

            context["last_subject"] = subject

            # ==================================
            # SUBJECT DETAIL
            # ==================================

            if intent == "subject_detail":

                return (
                    f"Your mark in {subject} is "
                    f"{mark:.2f}."
                )

            # ==================================
            # WHY SUBJECT IS WEAK / STRONG
            # ==================================

            if (
                context.get("follow_up", False)
                and intent in [
                    "highest_subject",
                    "lowest_subject"
                ]
            ):

                highest_subject, highest_mark = max(
                    results,
                    key=lambda item: float(item[1])
                )

                lowest_subject, lowest_mark = min(
                    results,
                    key=lambda item: float(item[1])
                )

                if (
                    subject.lower()
                    == highest_subject.lower()
                ):

                    return (
                        f"{subject} is your strongest subject "
                        f"because it has your highest mark of "
                        f"{float(highest_mark):.2f}."
                    )

                elif (
                    subject.lower()
                    == lowest_subject.lower()
                ):

                    return (
                        f"{subject} is your weakest subject "
                        f"because it has your lowest mark of "
                        f"{float(lowest_mark):.2f}."
                    )

                return (
                    f"You scored {mark:.2f} in "
                    f"{subject}."
                )

            # ==================================
            # SUBJECT TREND
            # ==================================

            if intent == "subject_trend":

                subject_exams = []

                for (
                    exam_subject,
                    exam_type,
                    exam_mark
                ) in exam_results:

                    if (
                        exam_subject.lower()
                        == subject.lower()
                    ):

                        subject_exams.append(
                            float(exam_mark)
                        )

                if len(subject_exams) < 2:

                    return (
                        f"There is not enough exam data "
                        f"to calculate improvement for "
                        f"{subject}."
                    )

                first_mark = subject_exams[0]
                latest_mark = subject_exams[-1]

                improvement = (
                    latest_mark - first_mark
                )

                if improvement > 0:

                    return (
                        f"Your {subject} mark improved "
                        f"from {first_mark:.2f} to "
                        f"{latest_mark:.2f} "
                        f"({improvement:+.2f})."
                    )

                elif improvement < 0:

                    return (
                        f"Your {subject} mark changed "
                        f"from {first_mark:.2f} to "
                        f"{latest_mark:.2f} "
                        f"({improvement:+.2f})."
                    )

                return (
                    f"Your {subject} mark remained "
                    f"stable at {latest_mark:.2f}."
                )

    # ==========================================
    # AVERAGE
    # ==========================================

    if intent == "average":

        average, _, _, _ = analyze_performance(
            results,
            attendance_results
        )

        if context.get("follow_up", False):

            return (
                f"Your average mark is {average:.2f}. "
                f"This represents your overall "
                f"academic score."
            )

        return (
            f"Your average mark is "
            f"{average:.2f}."
        )

    # ==========================================
    # ATTENDANCE
    # ==========================================

    elif intent == "attendance":

        _, _, _, overall_attendance = (
            analyze_performance(
                results,
                attendance_results
            )
        )

        if overall_attendance >= 85:

            status = (
                "Yes, your attendance is good."
            )

        elif overall_attendance >= 75:

            status = (
                "Your attendance is acceptable, "
                "but you should try to improve it."
            )

        else:

            status = (
                "Your attendance needs attention."
            )

        if context.get("follow_up", False):

            return (
                f"Your attendance is "
                f"{overall_attendance:.2f}%. "
                f"{status}"
            )

        return (
            f"Your overall attendance is "
            f"{overall_attendance:.2f}%.\n"
            f"{status}"
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

        _, highest_mark, highest_subject, _ = (
            analyze_performance(
                results,
                attendance_results
            )
        )

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

        lowest_mark = float(lowest_mark)

        context["last_subject"] = lowest_subject

        return (
            f"Your lowest scoring subject is "
            f"{lowest_subject} with "
            f"{lowest_mark:.2f} marks."
        )

    # ==========================================
    # TREND
    # ==========================================

    elif intent == "trend":

        trend, average_improvement, overall_trend = (
            analyze_trend(exam_results)
        )

        if not trend:

            return (
                "There is not enough exam data "
                "to calculate your trend."
            )

        if context.get("follow_up", False):

            if average_improvement > 0:

                return (
                    f"Your performance is "
                    f"{overall_trend.lower()} because "
                    f"your marks increased by an average "
                    f"of {average_improvement:.2f} marks."
                )

            elif average_improvement < 0:

                return (
                    f"Your performance is "
                    f"{overall_trend.lower()} because "
                    f"your marks decreased by an average "
                    f"of {abs(average_improvement):.2f} marks."
                )

            return (
                "Your performance has remained "
                "relatively stable because there has "
                "been no significant change in your marks."
            )

        response = (
            f"Your overall performance trend is "
            f"{overall_trend}.\n\n"
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
    # PERFORMANCE
    # ==========================================

    elif intent == "performance":

        average, _, _, overall_attendance = (
            analyze_performance(
                results,
                attendance_results
            )
        )

        if (
            average >= 85
            and overall_attendance >= 85
        ):

            status = "Excellent"

        elif (
            average >= 70
            and overall_attendance >= 75
        ):

            status = "Good"

        elif (
            average >= 50
            and overall_attendance >= 65
        ):

            status = "Average"

        else:

            status = "Needs Attention"

        if context.get("follow_up", False):

            return (
                f"Your performance is rated "
                f"{status} because your average "
                f"mark is {average:.2f} and your "
                f"attendance is "
                f"{overall_attendance:.2f}%."
            )

        return (
            f"Your current performance is "
            f"{status}.\n"
            f"Average mark: {average:.2f}\n"
            f"Overall attendance: "
            f"{overall_attendance:.2f}%"
        )

    # ==========================================
    # RECOMMENDATION
    # ==========================================

    elif intent == "recommendation":

        average, _, _, overall_attendance = (
            analyze_performance(
                results,
                attendance_results
            )
        )

        # --------------------------------------
        # Follow-up for previously mentioned
        # subject
        # --------------------------------------

        if (
            context.get("last_subject") is not None
            and context.get("follow_up", False)
        ):

            subject_name = context["last_subject"]

            subject_mark = None

            for subject, mark in results:

                if (
                    subject.lower()
                    == subject_name.lower()
                ):

                    subject_mark = float(mark)
                    break

            if subject_mark is not None:

                return (
                    f"To improve {subject_name}, "
                    f"give extra attention to that "
                    f"subject, practice more questions, "
                    f"and review the topics where you "
                    f"are losing marks.\n"
                    f"Your current mark in "
                    f"{subject_name} is "
                    f"{subject_mark:.2f}."
                )

        lowest_subject, lowest_mark = min(
            results,
            key=lambda item: float(item[1])
        )

        lowest_mark = float(lowest_mark)

        context["last_subject"] = lowest_subject

        return (
            f"Based on your current performance, "
            f"you should focus on "
            f"{lowest_subject} "
            f"({lowest_mark:.2f} marks).\n"
            f"Your average mark is "
            f"{average:.2f} and your attendance "
            f"is {overall_attendance:.2f}%.\n"
            f"Keep maintaining your attendance and "
            f"give extra attention to your weaker "
            f"subject."
        )

    # ==========================================
    # ACADEMIC ANALYTICS
    # ==========================================

    elif intent == "analytics":

        average, _, _, overall_attendance = (
            analyze_performance(
                results,
                attendance_results
            )
        )

        analysis = generate_academic_analysis(
            results,
            exam_results,
            average,
            overall_attendance
        )

        response = (
            "Here is your complete academic "
            "analysis:\n\n"
        )

        # --------------------------------------
        # Overall
        # --------------------------------------

        response += (
            f"Overall Average: "
            f"{average:.2f}\n"
            f"Attendance: "
            f"{overall_attendance:.2f}%\n\n"
        )

        # --------------------------------------
        # Subject Performance
        # --------------------------------------

        response += "Subject Performance:\n"

        for (
            subject,
            mark
        ) in analysis["subject_averages"].items():

            response += (
                f"{subject}: {mark:.2f}\n"
            )

        response += "\n"

        # --------------------------------------
        # Improvement
        # --------------------------------------

        if analysis["below_85"]:

            response += (
                "Subjects Needing Improvement:\n"
            )

            for (
                subject,
                mark
            ) in analysis["below_85"].items():

                response += (
                    f"{subject}: {mark:.2f}\n"
                )

            response += "\n"

        else:

            response += (
                "Subjects Needing Improvement: "
                "None\n\n"
            )

        # --------------------------------------
        # Strong Subjects
        # --------------------------------------

        if analysis["above_85"]:

            response += "Strong Subjects:\n"

            for (
                subject,
                mark
            ) in analysis["above_85"].items():

                response += (
                    f"{subject}: {mark:.2f}\n"
                )

            response += "\n"

        # --------------------------------------
        # Most Improved
        # --------------------------------------

        if analysis["most_improved"]:

            (
                subject,
                first_mark,
                latest_mark,
                improvement
            ) = analysis["most_improved"]

            response += (
                f"Most Improved Subject: "
                f"{subject}\n"
                f"{first_mark:.2f} → "
                f"{latest_mark:.2f} "
                f"({improvement:+.2f})\n\n"
            )

        # --------------------------------------
        # Least Improved
        # --------------------------------------

        if analysis["least_improved"]:

            (
                subject,
                first_mark,
                latest_mark,
                improvement
            ) = analysis["least_improved"]

            response += (
                f"Least Improved Subject: "
                f"{subject}\n"
                f"{first_mark:.2f} → "
                f"{latest_mark:.2f} "
                f"({improvement:+.2f})\n\n"
            )

        # --------------------------------------
        # Average Improvement
        # --------------------------------------

        response += (
            f"Average Improvement: "
            f"{analysis['average_improvement']:+.2f}"
            f"\n\n"
        )

        # --------------------------------------
        # Priority Subject
        # --------------------------------------

        if analysis["priority_subject"]:

            subject, mark = (
                analysis["priority_subject"]
            )

            response += (
                f"Priority Subject: "
                f"{subject} ({mark:.2f})\n\n"
            )

        # --------------------------------------
        # Performance Factors
        # --------------------------------------

        response += "Performance Factors:\n"

        for factor in analysis[
            "performance_factors"
        ]:

            response += (
                f"- {factor}\n"
            )

        return response

    # ==========================================
    # RISK
    # ==========================================

    elif intent == "risk":

        average, _, _, overall_attendance = (
            analyze_performance(
                results,
                attendance_results
            )
        )

        if (
            average < 50
            or overall_attendance < 65
        ):

            risk_level = "High"

        elif (
            average < 70
            or overall_attendance < 75
        ):

            risk_level = "Moderate"

        else:

            risk_level = "Low"

        if context.get("follow_up", False):

            return (
                f"Your risk level is "
                f"{risk_level} because your average "
                f"mark is {average:.2f} and your overall "
                f"attendance is "
                f"{overall_attendance:.2f}%."
            )

        return (
            f"Your current academic risk level is "
            f"{risk_level}.\n"
            f"Average mark: {average:.2f}\n"
            f"Overall attendance: "
            f"{overall_attendance:.2f}%"
        )

    # ==========================================
    # UNKNOWN
    # ==========================================

    return (
        "I'm not sure what you're asking. "
        "Try asking about your marks, average, "
        "attendance, highest subject, lowest "
        "subject, performance, risk, "
        "recommendation, or trend."
    )
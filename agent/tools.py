from services.student_service import (
    get_student_id,
    get_student_marks,
    get_student_exam_marks,
    get_subject_mark
)

from services.attendance_service import (
    get_student_attendance
)

from services.performance_service import (
    analyze_performance
)

from services.trend_service import (
    analyze_trend
)

from services.recommendation_service import (
    generate_recommendation
)

from ml.predict import (
    predict_performance
)

from rag.rag_pipeline import (
    answer_question
)


# ==========================================
# GET STUDENT DATA
# ==========================================

def get_student_data(student_name):

    student_id = get_student_id(student_name)

    if student_id is None:
        return {
            "success": False,
            "message": "Student not found."
        }

    marks = get_student_marks(student_name)
    exam_marks = get_student_exam_marks(student_name)
    attendance = get_student_attendance(student_id)

    return {
        "success": True,
        "student_name": student_name,
        "student_id": student_id,
        "marks": marks,
        "exam_marks": exam_marks,
        "attendance": attendance
    }


# ==========================================
# GET AVERAGE
# ==========================================

def get_average(student_name):

    student_id = get_student_id(student_name)

    if student_id is None:
        return {
            "success": False,
            "message": "Student not found."
        }

    marks = get_student_marks(student_name)
    attendance = get_student_attendance(student_id)

    if not marks:
        return {
            "success": False,
            "message": "No marks found."
        }

    average, _, _, _ = analyze_performance(
        marks,
        attendance
    )

    return {
        "success": True,
        "average": round(float(average), 2)
    }


# ==========================================
# GET ATTENDANCE
# ==========================================

def get_attendance(student_name):

    student_id = get_student_id(student_name)

    if student_id is None:
        return {
            "success": False,
            "message": "Student not found."
        }

    marks = get_student_marks(student_name)
    attendance = get_student_attendance(student_id)

    if not marks:
        return {
            "success": False,
            "message": "No student data found."
        }

    _, _, _, overall_attendance = analyze_performance(
        marks,
        attendance
    )

    return {
        "success": True,
        "attendance": round(
            float(overall_attendance),
            2
        )
    }


# ==========================================
# GET HIGHEST SUBJECT
# ==========================================

def get_highest_subject(student_name):

    student_id = get_student_id(student_name)

    if student_id is None:
        return {
            "success": False,
            "message": "Student not found."
        }

    marks = get_student_marks(student_name)
    attendance = get_student_attendance(student_id)

    if not marks:
        return {
            "success": False,
            "message": "No marks found."
        }

    _, highest_mark, highest_subject, _ = (
        analyze_performance(
            marks,
            attendance
        )
    )

    return {
        "success": True,
        "subject": highest_subject,
        "mark": round(
            float(highest_mark),
            2
        )
    }


# ==========================================
# GET LOWEST SUBJECT
# ==========================================

def get_lowest_subject(student_name):

    marks = get_student_marks(student_name)

    if not marks:
        return {
            "success": False,
            "message": "No marks found."
        }

    lowest_subject, lowest_mark = min(
        marks,
        key=lambda item: float(item[1])
    )

    return {
        "success": True,
        "subject": lowest_subject,
        "mark": round(
            float(lowest_mark),
            2
        )
    }


# ==========================================
# GET SUBJECT MARK
# ==========================================

def get_mark_for_subject(
    student_name,
    subject
):

    if not subject:
        return {
            "success": False,
            "message": "Subject name is required."
        }

    result = get_subject_mark(
        student_name,
        subject
    )

    if result[0] is None:
        return {
            "success": False,
            "message": (
                f"I couldn't find a subject named "
                f"{subject}."
            )
        }

    found_subject, mark = result

    return {
        "success": True,
        "subject": found_subject,
        "mark": round(
            float(mark),
            2
        )
    }


# ==========================================
# GET SUBJECT DETAIL
# ==========================================

def get_subject_detail(
    student_name,
    subject
):

    if not subject:
        return {
            "success": False,
            "message": "Subject name is required."
        }

    result = get_subject_mark(
        student_name,
        subject
    )

    if result[0] is None:
        return {
            "success": False,
            "message": (
                f"I couldn't find a subject named "
                f"{subject}."
            )
        }

    found_subject, mark = result

    return {
        "success": True,
        "subject": found_subject,
        "mark": round(
            float(mark),
            2
        )
    }


# ==========================================
# GET SUBJECT TREND
# ==========================================

def get_subject_trend(
    student_name,
    subject
):

    if not subject:
        return {
            "success": False,
            "message": "Subject name is required."
        }

    exam_results = get_student_exam_marks(
        student_name
    )

    if not exam_results:
        return {
            "success": False,
            "message": "No exam data found."
        }

    trend, _, _ = analyze_trend(
        exam_results
    )

    if not trend:
        return {
            "success": False,
            "message": (
                "There is not enough exam data "
                "to calculate the trend."
            )
        }

    # Find the requested subject
    for (
        trend_subject,
        first_mark,
        latest_mark,
        improvement
    ) in trend:

        if trend_subject.lower() == subject.lower():

            return {
                "success": True,
                "subject": trend_subject,
                "first_mark": round(
                    float(first_mark),
                    2
                ),
                "latest_mark": round(
                    float(latest_mark),
                    2
                ),
                "improvement": round(
                    float(improvement),
                    2
                )
            }

    return {
        "success": False,
        "message": (
            f"I couldn't find trend data for "
            f"{subject}."
        )
    }


# ==========================================
# GET PERFORMANCE
# ==========================================

def get_performance(student_name):

    student_id = get_student_id(student_name)

    if student_id is None:
        return {
            "success": False,
            "message": "Student not found."
        }

    marks = get_student_marks(student_name)
    attendance = get_student_attendance(student_id)

    if not marks:
        return {
            "success": False,
            "message": "No marks found."
        }

    average, _, _, overall_attendance = (
        analyze_performance(
            marks,
            attendance
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

    return {
        "success": True,
        "status": status,
        "average": round(
            float(average),
            2
        ),
        "attendance": round(
            float(overall_attendance),
            2
        )
    }


# ==========================================
# GET RISK
# ==========================================

def get_risk(student_name):

    student_id = get_student_id(student_name)

    if student_id is None:
        return {
            "success": False,
            "message": "Student not found."
        }

    marks = get_student_marks(student_name)
    attendance = get_student_attendance(student_id)

    if not marks:
        return {
            "success": False,
            "message": "No marks found."
        }

    (
        average,
        highest_mark,
        _,
        overall_attendance
    ) = analyze_performance(
        marks,
        attendance
    )

    lowest_mark = min(
        float(mark)
        for _, mark in marks
    )

    _, risk_probability = predict_performance(
        average,
        overall_attendance,
        highest_mark,
        lowest_mark
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

    return {
        "success": True,
        "risk_level": risk_level,
        "risk_probability": round(
            float(risk_probability),
            2
        ),
        "average": round(
            float(average),
            2
        ),
        "attendance": round(
            float(overall_attendance),
            2
        )
    }


# ==========================================
# GET TREND
# ==========================================

def get_trend(student_name):

    exam_results = get_student_exam_marks(
        student_name
    )

    if not exam_results:
        return {
            "success": False,
            "message": "No exam data found."
        }

    (
        trend,
        average_improvement,
        overall_trend
    ) = analyze_trend(
        exam_results
    )

    if not trend:
        return {
            "success": False,
            "message": (
                "There is not enough exam data "
                "to calculate the trend."
            )
        }

    trend_data = []

    for (
        subject,
        first_mark,
        second_mark,
        improvement
    ) in trend:

        trend_data.append({
            "subject": subject,
            "first_mark": round(
                float(first_mark),
                2
            ),
            "latest_mark": round(
                float(second_mark),
                2
            ),
            "improvement": round(
                float(improvement),
                2
            )
        })

    return {
        "success": True,
        "overall_trend": overall_trend,
        "average_improvement": round(
            float(average_improvement),
            2
        ),
        "subjects": trend_data
    }


# ==========================================
# GET RECOMMENDATION
# ==========================================

def get_recommendation(student_name):

    student_id = get_student_id(student_name)

    if student_id is None:
        return {
            "success": False,
            "message": "Student not found."
        }

    marks = get_student_marks(student_name)
    attendance = get_student_attendance(student_id)

    if not marks:
        return {
            "success": False,
            "message": "No marks found."
        }

    (
        average,
        highest_mark,
        highest_subject,
        overall_attendance
    ) = analyze_performance(
        marks,
        attendance
    )

    lowest_subject, lowest_mark = min(
        marks,
        key=lambda item: float(item[1])
    )

    _, risk_probability = predict_performance(
        average,
        overall_attendance,
        highest_mark,
        float(lowest_mark)
    )

    recommendation = generate_recommendation(
        average,
        overall_attendance,
        risk_probability,
        lowest_subject,
        highest_subject
    )

    return {
        "success": True,
        "recommendation": recommendation,
        "priority_subject": lowest_subject,
        "priority_mark": round(
            float(lowest_mark),
            2
        )
    }


# ==========================================
# RAG / ACADEMIC KNOWLEDGE
# ==========================================

def answer_academic_question(question):

    if not question:
        return {
            "success": False,
            "message": "Academic question is missing."
        }

    answer, results = answer_question(
        question
    )

    return {
        "success": True,
        "answer": answer,
        "retrieved_results": results
    }


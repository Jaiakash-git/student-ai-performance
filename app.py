from services.student_service import (
    get_student_marks,
    get_student_exam_marks,
    get_student_id
)

from services.performance_service import (
    analyze_performance,
    get_performance_status
)

from services.attendance_service import get_student_attendance

from services.recommendation_service import generate_recommendation

from services.trend_service import analyze_trend

from ml.predict import predict_performance


# ==========================================
#          GET STUDENT INFORMATION
# ==========================================

student_name = input("Enter student name: ")

student_id = get_student_id(student_name)

results = get_student_marks(student_name)

exam_results = get_student_exam_marks(student_name)


# ==========================================
#          CHECK STUDENT
# ==========================================

if not results:

    print("\nStudent not found!")

else:

    # ==========================================
    #          FIND LOWEST SUBJECT
    # ==========================================

    lowest_subject = min(
        results,
        key=lambda item: float(item[1])
    )[0]


    # ==========================================
    #          FETCH ATTENDANCE
    # ==========================================

    attendance_results = get_student_attendance(student_id)


    # ==========================================
    #          ANALYZE PERFORMANCE
    # ==========================================

    average, highest_mark, highest_subject, overall_attendance = analyze_performance(
        results,
        attendance_results
    )


    # ==========================================
    #          RULE-BASED STATUS
    # ==========================================

    status = get_performance_status(
        average,
        overall_attendance
    )


    # ==========================================
    #          ML PREDICTION
    # ==========================================

    ml_prediction, risk_probability = predict_performance(
        average,
        overall_attendance,
        highest_mark,
        min(float(mark) for subject, mark in results)
    )


    # ==========================================
    #          RECOMMENDATION
    # ==========================================

    recommendation = generate_recommendation(
        average,
        overall_attendance,
        risk_probability,
        lowest_subject,
        highest_subject
    )


    # ==========================================
    #          TREND ANALYSIS
    # ==========================================

    trend, average_improvement, overall_trend = analyze_trend(
        exam_results
    )


    # ==========================================
    #          STUDENT PERFORMANCE REPORT
    # ==========================================

    print("\n============================================")
    print("       STUDENT AI PERFORMANCE REPORT")
    print("============================================")

    print(f"\nStudent Name: {student_name}")


    # ==========================================
    #          MARKS - EXAM WISE
    # ==========================================

    print("\n--------------- MARKS ---------------------")

    exam_marks = {}

    for subject, exam_type, mark in exam_results:

        if exam_type not in exam_marks:
            exam_marks[exam_type] = []

        exam_marks[exam_type].append(
            (subject, mark)
        )


    for exam_type, marks in exam_marks.items():

        print(f"\n{exam_type}")
        print("-" * 20)

        for subject, mark in marks:
            print(f"{subject:<10}: {mark:.2f}")


    # ==========================================
    #          PERFORMANCE TREND
    # ==========================================

    print("\n---------- PERFORMANCE TREND ---------------")

    for subject, first_mark, second_mark, improvement in trend:

        if improvement > 0:
            change = f"+{improvement:.2f}"

        else:
            change = f"{improvement:.2f}"

        print(
            f"{subject:<10}: "
            f"{first_mark:.2f} -> "
            f"{second_mark:.2f} "
            f"({change})"
        )


    print(
        f"\nAverage Improvement : "
        f"{average_improvement:+.2f}"
    )

    print(
        f"Overall Trend       : "
        f"{overall_trend}"
    )


    # ==========================================
    #          ATTENDANCE
    # ==========================================

    print("\n------------- ATTENDANCE ------------------")

    for subject, attended, total in attendance_results:

        percentage = (attended / total) * 100

        print(f"{subject:<10}: {percentage:.2f}%")


    print(
        f"\nOverall Attendance      : "
        f"{overall_attendance:.2f}%"
    )


    # ==========================================
    #          AI ANALYSIS
    # ==========================================

    print("\n-------------- AI ANALYSIS ----------------")

    print(
        f"Rule-Based Status       : "
        f"{status}"
    )

    print(
        f"ML Prediction           : "
        f"{ml_prediction}"
    )

    print(
        f"Risk Probability        : "
        f"{risk_probability:.2f}%"
    )


    # ==========================================
    #          PERFORMANCE SUMMARY
    # ==========================================

    print("\n----------- PERFORMANCE SUMMARY ------------")

    print(
        f"Average Mark            : "
        f"{average:.2f}"
    )

    print(
        f"Highest Mark            : "
        f"{highest_mark:.2f}"
    )

    print(
        f"Highest Scoring Subject : "
        f"{highest_subject}"
    )


    # ==========================================
    #          RECOMMENDATION
    # ==========================================

    print("\n------------ RECOMMENDATION ---------------")

    print(recommendation)


    # ==========================================
    #          END OF REPORT
    # ==========================================

   

    from nlp.assistant import start_assistant

    start_assistant(student_name)
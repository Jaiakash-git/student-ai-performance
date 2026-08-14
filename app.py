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

from ml.predict import predict_performance

from services.recommendation_service import generate_recommendation


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

    print(f"Rule-Based Status       : {status}")

    print(f"ML Prediction           : {ml_prediction}")

    print(
        f"Risk Probability        : "
        f"{risk_probability:.2f}%"
    )


    # ==========================================
    #          PERFORMANCE SUMMARY
    # ==========================================

    print("\n----------- PERFORMANCE SUMMARY ------------")

    print(f"Average Mark            : {average:.2f}")

    print(f"Highest Mark            : {highest_mark:.2f}")

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

    print("\n============================================")
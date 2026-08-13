from services.student_service import get_student_marks, get_student_id
from services.performance_service import analyze_performance
from services.attendance_service import get_student_attendance
from services.performance_service import (
    analyze_performance,
    get_performance_status
)
from ml.predict import predict_performance


# Get student name
student_name = input("Enter student name: ")

# Get student ID
student_id = get_student_id(student_name)

# Fetch marks
results = get_student_marks(student_name)

# Fetch attendance
attendance_results = get_student_attendance(student_id)


if not results:
    print("Student not found!")

else:
    print(f"\nMarks for {student_name}:")

    for subject, mark in results:
        print(f"{subject}: {mark:.2f}")

    # Analyze performance
    average, highest_mark, highest_subject, overall_attendance = analyze_performance(
    results, attendance_results
)


    print(f"\nAverage Mark: {average:.2f}")
    print(f"Highest Mark: {highest_mark:.2f}")
    print(f"Highest Scoring Subject: {highest_subject}")

    # Display attendance
    print("\nAttendance:")

    for subject, attended, total in attendance_results:
        percentage = (attended / total) * 100
        print(f"{subject}: {percentage:.2f}%")

    print(f"\nOverall Attendance: {overall_attendance:.2f}%")

    # Get performance status
    status = get_performance_status(average, overall_attendance)

    ml_prediction = predict_performance(
    average,
    overall_attendance,
    highest_mark,
    min(float(mark) for subject, mark in results)
)
    print(f"Rule-Based Status: {status}")
    print(f"ML Prediction: {ml_prediction}")
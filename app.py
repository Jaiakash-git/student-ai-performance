from services.student_service import get_student_marks
from services.performance_service import analyze_performance

# Get student name
student_name = input("Enter student name: ")

# Fetch marks
results = get_student_marks(student_name)

if not results:
    print("Student not found!")

else:
    print(f"\nMarks for {student_name}:")

    for subject, mark in results:
        print(f"{subject}: {mark:.2f}")

# Analyze performance

    average, highest_mark, highest_subject = analyze_performance(results) 

    print(f"\nAverage Mark: {average:.2f}")
    print(f"Highest Mark: {highest_mark:.2f}")
    print(f"Highest Scoring Subject: {highest_subject}")


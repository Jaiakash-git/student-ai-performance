from services.student_service import (
    get_student_marks,
    get_student_exam_marks,
    get_student_id
)

from services.attendance_service import get_student_attendance

from services.performance_service import analyze_performance

from services.analytics_service import (
    get_subject_averages,
    get_subjects_below_mark,
    get_subjects_above_mark,
    get_subjects_needing_improvement,
    get_most_improved_subject,
    get_least_improved_subject,
    get_average_improvement,
    get_priority_subject,
    get_performance_factors
)


student_name = input("Enter student name: ")

student_id = get_student_id(student_name)

if student_id is None:
    print("Student not found.")
    exit()

results = get_student_marks(student_name)
exam_results = get_student_exam_marks(student_name)
attendance_results = get_student_attendance(student_id)

average, _, _, attendance = analyze_performance(
    results,
    attendance_results
)


print("\n============================================")
print("        STUDENT ANALYTICS TEST")
print("============================================")


# Subject averages
print("\nSubject Averages:")

subject_averages = get_subject_averages(results)

for subject, mark in subject_averages.items():
    print(f"{subject}: {mark:.2f}")


# Subjects below 85
print("\nSubjects Below 85:")

below_85 = get_subjects_below_mark(
    results,
    85
)

if below_85:
    for subject, mark in below_85.items():
        print(f"{subject}: {mark:.2f}")
else:
    print("None")


# Subjects above 85
print("\nSubjects Above or Equal to 85:")

above_85 = get_subjects_above_mark(
    results,
    85
)

if above_85:
    for subject, mark in above_85.items():
        print(f"{subject}: {mark:.2f}")
else:
    print("None")


# Subjects needing improvement
print("\nSubjects Needing Improvement:")

needs_improvement = get_subjects_needing_improvement(
    results
)

if needs_improvement:
    for subject, mark in needs_improvement.items():
        print(f"{subject}: {mark:.2f}")
else:
    print("None")


# Most improved
print("\nMost Improved Subject:")

most_improved = get_most_improved_subject(
    exam_results
)

if most_improved:

    subject, first, latest, improvement = most_improved

    print(
        f"{subject}: "
        f"{first:.2f} → {latest:.2f} "
        f"({improvement:+.2f})"
    )

else:
    print("Not enough exam data.")


# Least improved
print("\nLeast Improved Subject:")

least_improved = get_least_improved_subject(
    exam_results
)

if least_improved:

    subject, first, latest, improvement = least_improved

    print(
        f"{subject}: "
        f"{first:.2f} → {latest:.2f} "
        f"({improvement:+.2f})"
    )

else:
    print("Not enough exam data.")


# Average improvement
print("\nAverage Improvement:")

average_improvement = get_average_improvement(
    exam_results
)

print(f"{average_improvement:+.2f}")


# Priority subject
print("\nPriority Subject:")

priority = get_priority_subject(
    results
)

if priority:

    subject, mark = priority

    print(
        f"{subject}: {mark:.2f}"
    )

else:
    print("No subject data.")


# Performance factors
print("\nPerformance Factors:")

factors = get_performance_factors(
    results,
    average,
    attendance
)

for factor in factors:
    print(f"- {factor}")


print("\n============================================")
print("Analytics test completed.")
print("============================================")
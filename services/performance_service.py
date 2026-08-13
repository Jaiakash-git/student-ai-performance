def analyze_performance(results, attendance_results):

    # Marks analysis
    marks_list = [float(mark) for subject, mark in results]

    average = sum(marks_list) / len(marks_list)

    highest_mark = max(marks_list)

    highest_subject = None

    for subject, mark in results:
        if float(mark) == highest_mark:
            highest_subject = subject
            break

    # Attendance analysis
    attendance_percentages = []

    for subject, attended, total in attendance_results:
        percentage = (attended / total) * 100
        attendance_percentages.append(percentage)

    overall_attendance = (
        sum(attendance_percentages) / len(attendance_percentages)
    )

    return average, highest_mark, highest_subject, overall_attendance

def get_performance_status(average, attendance):

    if average >= 85 and attendance >= 85:
        return "Excellent"

    elif average >= 70 and attendance >= 75:
        return "Good"

    elif average >= 50 and attendance >= 65:
        return "Average"

    else:
        return "Needs Attention"
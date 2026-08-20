from collections import defaultdict


# =========================================================
# SUBJECT MARK ANALYSIS
# =========================================================

def get_subject_averages(results):

    subject_marks = defaultdict(list)

    for subject, mark in results:
        subject_marks[subject].append(float(mark))

    subject_averages = {}

    for subject, marks in subject_marks.items():
        subject_averages[subject] = sum(marks) / len(marks)

    return subject_averages


# =========================================================
# SUBJECTS BELOW A MARK
# =========================================================

def get_subjects_below_mark(results, threshold):

    subject_averages = get_subject_averages(results)

    return {
        subject: mark
        for subject, mark in subject_averages.items()
        if mark < float(threshold)
    }


# =========================================================
# SUBJECTS ABOVE A MARK
# =========================================================

def get_subjects_above_mark(results, threshold):

    subject_averages = get_subject_averages(results)

    return {
        subject: mark
        for subject, mark in subject_averages.items()
        if mark >= float(threshold)
    }


# =========================================================
# SUBJECTS NEEDING IMPROVEMENT
# =========================================================

def get_subjects_needing_improvement(results, threshold=85):

    return get_subjects_below_mark(results, threshold)


# =========================================================
# MOST IMPROVED SUBJECT
# =========================================================

def get_most_improved_subject(exam_results):

    subject_exams = defaultdict(list)

    for subject, exam_type, mark in exam_results:
        subject_exams[subject].append(float(mark))

    improvements = []

    for subject, marks in subject_exams.items():

        if len(marks) < 2:
            continue

        first_mark = marks[0]
        latest_mark = marks[-1]
        improvement = latest_mark - first_mark

        improvements.append(
            (
                subject,
                first_mark,
                latest_mark,
                improvement
            )
        )

    if not improvements:
        return None

    return max(
        improvements,
        key=lambda item: item[3]
    )


# =========================================================
# LEAST IMPROVED SUBJECT
# =========================================================

def get_least_improved_subject(exam_results):

    subject_exams = defaultdict(list)

    for subject, exam_type, mark in exam_results:
        subject_exams[subject].append(float(mark))

    improvements = []

    for subject, marks in subject_exams.items():

        if len(marks) < 2:
            continue

        first_mark = marks[0]
        latest_mark = marks[-1]
        improvement = latest_mark - first_mark

        improvements.append(
            (
                subject,
                first_mark,
                latest_mark,
                improvement
            )
        )

    if not improvements:
        return None

    return min(
        improvements,
        key=lambda item: item[3]
    )


# =========================================================
# AVERAGE IMPROVEMENT
# =========================================================

def get_average_improvement(exam_results):

    subject_exams = defaultdict(list)

    for subject, exam_type, mark in exam_results:
        subject_exams[subject].append(float(mark))

    improvements = []

    for subject, marks in subject_exams.items():

        if len(marks) < 2:
            continue

        improvement = marks[-1] - marks[0]
        improvements.append(improvement)

    if not improvements:
        return 0.0

    return sum(improvements) / len(improvements)


# =========================================================
# PRIORITY SUBJECT
# =========================================================

def get_priority_subject(results):

    subject_averages = get_subject_averages(results)

    if not subject_averages:
        return None

    subject = min(
        subject_averages,
        key=subject_averages.get
    )

    return subject, subject_averages[subject]


# =========================================================
# PERFORMANCE FACTORS
# =========================================================

def get_performance_factors(
    results,
    average,
    attendance
):

    factors = []

    subject_averages = get_subject_averages(results)

    if average < 70:

        factors.append(
            "Your overall average mark is below 70."
        )

    if attendance < 75:

        factors.append(
            "Your attendance is below 75%."
        )

    weak_subjects = {
        subject: mark
        for subject, mark in subject_averages.items()
        if mark < 70
    }

    if weak_subjects:

        subjects = ", ".join(
            weak_subjects.keys()
        )

        factors.append(
            f"These subjects need attention: {subjects}."
        )

    if not factors:

        factors.append(
            "Your current marks and attendance "
            "do not show a major performance concern."
        )

    return factors


# =========================================================
# COMPLETE ACADEMIC ANALYSIS
# =========================================================

def generate_academic_analysis(
    results,
    exam_results,
    average,
    attendance
):
    """
    Generate a complete academic analysis
    using all available analytics.
    """

    subject_averages = get_subject_averages(results)

    below_85 = get_subjects_below_mark(
        results,
        85
    )

    above_85 = get_subjects_above_mark(
        results,
        85
    )

    most_improved = get_most_improved_subject(
        exam_results
    )

    least_improved = get_least_improved_subject(
        exam_results
    )

    average_improvement = get_average_improvement(
        exam_results
    )

    priority_subject = get_priority_subject(
        results
    )

    factors = get_performance_factors(
        results,
        average,
        attendance
    )

    return {
        "subject_averages": subject_averages,
        "below_85": below_85,
        "above_85": above_85,
        "most_improved": most_improved,
        "least_improved": least_improved,
        "average_improvement": average_improvement,
        "priority_subject": priority_subject,
        "performance_factors": factors
    }
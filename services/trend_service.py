def analyze_trend(exam_results):
    """
    Compare Internal 1 and Internal 2 marks
    and calculate subject-wise improvement.
    """

    internal_1 = {}
    internal_2 = {}

    # Separate marks by exam
    for subject, exam_type, mark in exam_results:

        mark = float(mark)

        if exam_type == "Internal 1":
            internal_1[subject] = mark

        elif exam_type == "Internal 2":
            internal_2[subject] = mark

    trend = []

    # Compare subjects available in both exams
    for subject in internal_1:

        if subject in internal_2:

            first_mark = internal_1[subject]
            second_mark = internal_2[subject]

            improvement = second_mark - first_mark

            trend.append(
                (
                    subject,
                    first_mark,
                    second_mark,
                    improvement
                )
            )

    # Calculate overall improvement
    if trend:
        average_improvement = sum(
            item[3] for item in trend
        ) / len(trend)
    else:
        average_improvement = 0

    # Determine overall trend
    if average_improvement > 0:
        overall_trend = "Improving"

    elif average_improvement < 0:
        overall_trend = "Declining"

    else:
        overall_trend = "Stable"

    return trend, average_improvement, overall_trend
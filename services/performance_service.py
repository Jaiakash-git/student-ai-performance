def analyze_performance(results):

    marks_list = [float(mark) for subject, mark in results]

    # Calculate average
    average = sum(marks_list) / len(marks_list)

    # Find highest mark
    highest_mark = max(marks_list)

    # Find subject with highest mark
    highest_subject = None

    for subject, mark in results:
        if float(mark) == highest_mark:
            highest_subject = subject
            break

    return average, highest_mark, highest_subject
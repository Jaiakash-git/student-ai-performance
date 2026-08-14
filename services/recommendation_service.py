def generate_recommendation(
    average_marks,
    attendance,
    risk_probability,
    lowest_subject,
    highest_subject
):

    if risk_probability >= 70:
        return (
            f"High academic attention required. "
            f"Focus on improving {lowest_subject} and maintain regular attendance."
        )

    elif risk_probability >= 40:
        return (
            f"Moderate attention recommended. "
            f"Improve weaker subjects, especially {lowest_subject}, "
            f"and maintain attendance."
        )

    else:
        return (
            f"Performance is currently stable. "
            f"Continue maintaining good marks and attendance, "
            f"especially in {highest_subject}."
        )
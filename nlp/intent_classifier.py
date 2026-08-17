def classify_intent(user_input):

    text = user_input.lower().strip()

    # Exit
    if text in ["bye", "exit", "quit", "stop"]:
        return "exit"

    # Highest / strongest subject
    if "subject" in text and (
       "highest" in text
        or "best" in text
        or "top" in text
        or "strongest" in text
        or "strong" in text
   ):
     return "highest_subject"

    # Lowest / weak subject
    if "subject" in text and (
        "lowest" in text
        or "weak" in text
        or "weakest" in text
        or "worst" in text
    ):
        return "lowest_subject"

    # Attendance
    if any(word in text for word in [
        "attendance",
        "present",
        "absent"
    ]):
        return "attendance"

    # Average
    if any(word in text for word in [
        "average",
        "overall mark",
        "overall marks"
    ]):
        return "average"

    # Trend
    if any(word in text for word in [
        "improving",
        "improvement",
        "trend",
        "progress",
        "getting better",
        "getting worse"
    ]):
        return "trend"

    # Risk
    if any(word in text for word in [
        "risk",
        "at risk",
        "attention",
        "danger"
    ]):
        return "risk"

    # Recommendation
    if any(word in text for word in [
        "recommend",
        "recommendation",
        "suggestion",
        "suggest",
        "improve"
    ]):
        return "recommendation"

    # Marks
    if any(word in text for word in [
        "marks",
        "mark",
        "scores",
        "score",
        "results"
    ]):
        return "marks"

    # General performance
    if any(word in text for word in [
        "performance",
        "performing",
        "doing"
    ]):
        return "performance"

    return "unknown"
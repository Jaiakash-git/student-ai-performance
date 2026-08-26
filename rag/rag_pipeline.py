import re

from rag.retriever import retrieve_chunks
from rag.generator import generate_answer


# ==========================================
# CONFIGURATION
# ==========================================

SIMILARITY_THRESHOLD = 0.40


# ==========================================
# FALLBACK RESPONSE
# ==========================================

FALLBACK_RESPONSE = (
    "I don't have enough information to answer that."
)


# ==========================================
# ATTENDANCE RULE CHECKER
# ==========================================

def check_attendance_rule(question):

    question_lower = question.lower()

    # Only activate for attendance-related questions
    if "attendance" not in question_lower:
        return None

    # Find percentage in the question
    match = re.search(
        r"(\d+(?:\.\d+)?)\s*%",
        question_lower
    )

    if not match:
        return None

    attendance = float(match.group(1))

    # Rules from academic_guide.txt
    if attendance > 85:
        return (
            f"Yes, {attendance:g}% attendance is considered good."
        )

    elif attendance >= 75:
        return (
            f"{attendance:g}% attendance is considered "
            "acceptable, but students should try to improve "
            "their attendance."
        )

    else:
        return (
            f"{attendance:g}% attendance needs attention "
            "because regular attendance is important for "
            "academic performance."
        )


# ==========================================
# ACADEMIC PERFORMANCE RULE CHECKER
# ==========================================

def check_average_mark_rule(question):

    question_lower = question.lower()

    # Detect average/mark related questions
    keywords = [
        "average mark",
        "average score",
        "average",
        "mean mark"
    ]

    if not any(
        keyword in question_lower
        for keyword in keywords
    ):
        return None

    # Find a number in the question
    match = re.search(
        r"\b(\d+(?:\.\d+)?)\b",
        question_lower
    )

    if not match:
        return None

    mark = float(match.group(1))

    # Only treat reasonable values as marks
    if mark < 0 or mark > 100:
        return None

    # Rules from academic_guide.txt
    if mark >= 85:
        return (
            f"An average mark of {mark:g} generally "
            "indicates excellent academic performance."
        )

    elif mark >= 70:
        return (
            f"An average mark of {mark:g} generally "
            "indicates good academic performance."
        )

    elif mark >= 50:
        return (
            f"An average mark of {mark:g} generally "
            "indicates average academic performance."
        )

    else:
        return (
            f"An average mark of {mark:g} indicates that "
            "the student needs significant academic attention."
        )


# ==========================================
# ANSWER QUESTION
# ==========================================

def answer_question(question):

    # --------------------------------------
    # RETRIEVAL
    # --------------------------------------

    results = retrieve_chunks(
        question,
        top_k=2
    )

    # --------------------------------------
    # CHECK IF RESULTS EXIST
    # --------------------------------------

    if not results:
        return FALLBACK_RESPONSE, results

    # --------------------------------------
    # CHECK RELEVANCE
    # --------------------------------------

    best_score = results[0]["score"]

    if best_score < SIMILARITY_THRESHOLD:
        return FALLBACK_RESPONSE, results

    # --------------------------------------
    # BUILD CONTEXT
    # --------------------------------------

    context = "\n\n".join(
        result["chunk"]
        for result in results
    )

    # --------------------------------------
    # DETERMINISTIC RULE CHECKS
    # --------------------------------------

    attendance_answer = check_attendance_rule(
        question
    )

    if attendance_answer:
        return attendance_answer, results

    average_answer = check_average_mark_rule(
        question
    )

    if average_answer:
        return average_answer, results

    # --------------------------------------
    # GENERATE USING QWEN
    # --------------------------------------

    answer = generate_answer(
        question,
        context
    )

    return answer, results


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    question = input(
        "Enter your question: "
    )

    answer, results = answer_question(
        question
    )

    print("\n================================")
    print("RETRIEVED INFORMATION")
    print("================================")

    for i, result in enumerate(
        results,
        start=1
    ):

        print(
            f"\nResult {i} "
            f"(Score: {result['score']:.4f})"
        )

        print(result["chunk"])

    print("\n================================")
    print("FINAL RAG ANSWER")
    print("================================")

    print(answer)
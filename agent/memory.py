# ==========================================
# AGENT MEMORY
# ==========================================


def create_context(student_name):
    """
    Create a fresh conversation context
    for the student.
    """

    return {
        "student_name": student_name,
        "last_intent": None,
        "last_subject": None,
        "last_result": None
    }


# ==========================================
# UPDATE MEMORY
# ==========================================

def update_context(
    context,
    intent,
    result
):
    """
    Update conversation memory after
    executing a tool.
    """

    context["last_intent"] = intent
    context["last_result"] = result

    # --------------------------------------
    # Remember subject
    # --------------------------------------

    if intent in [
        "highest_subject",
        "lowest_subject"
    ]:

        if result.get("success"):

            subject = result.get("subject")

            if subject:
                context["last_subject"] = subject

    # --------------------------------------
    # Subject detail
    # --------------------------------------
    # Keep the remembered subject.

    elif intent == "subject_detail":

        if result.get("success"):

            subject = result.get("subject")

            if subject:
                context["last_subject"] = subject

    # --------------------------------------
    # Subject trend
    # --------------------------------------
    # Keep the subject used for the trend.

    elif intent == "subject_trend":

        if result.get("success"):

            subject = result.get("subject")

            if subject:
                context["last_subject"] = subject

    return context


# ==========================================
# GET LAST SUBJECT
# ==========================================

def get_last_subject(context):

    return context.get(
        "last_subject"
    )


# ==========================================
# GET LAST INTENT
# ==========================================

def get_last_intent(context):

    return context.get(
        "last_intent"
    )


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    context = create_context(
        "Jaiakash"
    )

    print("\n========================================")
    print("          AGENT MEMORY TEST")
    print("========================================")

    print("\nInitial Context:")
    print(context)

    result = {
        "success": True,
        "subject": "OS",
        "mark": 82.0
    }

    context = update_context(
        context,
        "lowest_subject",
        result
    )

    print("\nAfter lowest_subject:")
    print(context)

    # --------------------------------------
    # Simulate subject detail
    # --------------------------------------

    result = {
        "success": True,
        "subject": "OS",
        "mark": 82.0
    }

    context = update_context(
        context,
        "subject_detail",
        result
    )

    print("\nAfter subject_detail:")
    print(context)

    print(
        "\nLast Subject:",
        get_last_subject(context)
    )

    print(
        "Last Intent:",
        get_last_intent(context)
    )
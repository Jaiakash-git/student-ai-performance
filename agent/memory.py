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

        # Last detected intent/tool
        "last_intent": None,

        # Last subject discussed
        "last_subject": None,

        # Subject explicitly requested by user
        "requested_subject": None,

        # Last tool result
        "last_result": None,

        # Previous tool result
        "previous_result": None,

        # Used to remember whether the
        # last subject was highest or lowest
        "last_subject_type": None,

        # Last user question
        "last_user_input": None
    }


# ==========================================
# UPDATE MEMORY
# ==========================================

def update_context(
    context,
    intent,
    result,
    user_input=None
):
    """
    Update conversation memory after
    executing a tool.
    """

    # --------------------------------------
    # Store previous result
    # --------------------------------------

    context["previous_result"] = context.get(
        "last_result"
    )

    # --------------------------------------
    # Update latest information
    # --------------------------------------

    context["last_intent"] = intent
    context["last_result"] = result

    if user_input is not None:
        context["last_user_input"] = user_input

    # --------------------------------------
    # Remember highest / lowest subject
    # --------------------------------------

    if intent == "highest_subject":

        if result.get("success"):

            subject = result.get("subject")

            if subject:
                context["last_subject"] = subject
                context["requested_subject"] = subject
                context["last_subject_type"] = "highest"

    elif intent == "lowest_subject":

        if result.get("success"):

            subject = result.get("subject")

            if subject:
                context["last_subject"] = subject
                context["requested_subject"] = subject
                context["last_subject_type"] = "lowest"

    # --------------------------------------
    # Subject detail
    # --------------------------------------

    elif intent == "subject_detail":

        if result.get("success"):

            subject = result.get("subject")

            if subject:
                context["last_subject"] = subject
                context["requested_subject"] = subject

    # --------------------------------------
    # Subject trend
    # --------------------------------------

    elif intent == "subject_trend":

        if result.get("success"):

            subject = result.get("subject")

            if subject:
                context["last_subject"] = subject
                context["requested_subject"] = subject

    # --------------------------------------
    # Subject explanation
    # --------------------------------------

    elif intent == "subject_explanation":

        if result.get("success"):

            subject = result.get("subject")

            if subject:
                context["last_subject"] = subject
                context["requested_subject"] = subject

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
# GET REQUESTED SUBJECT
# ==========================================

def get_requested_subject(context):

    return context.get(
        "requested_subject"
    )


# ==========================================
# CLEAR SUBJECT CONTEXT
# ==========================================

def clear_subject(context):

    context["last_subject"] = None
    context["requested_subject"] = None
    context["last_subject_type"] = None

    return context


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

    # --------------------------------------
    # Lowest subject
    # --------------------------------------

    result = {
        "success": True,
        "subject": "OS",
        "mark": 82.0
    }

    context = update_context(
        context,
        "lowest_subject",
        result,
        "What is my lowest subject?"
    )

    print("\nAfter lowest_subject:")
    print(context)

    # --------------------------------------
    # Subject detail
    # --------------------------------------

    result = {
        "success": True,
        "subject": "OS",
        "mark": 82.0
    }

    context = update_context(
        context,
        "subject_detail",
        result,
        "How much?"
    )

    print("\nAfter subject_detail:")
    print(context)

    # --------------------------------------
    # Subject explanation
    # --------------------------------------

    result = {
        "success": True,
        "subject": "OS",
        "mark": 82.0,
        "explanation": (
            "OS is your lowest-scoring subject "
            "because its mark is the lowest among "
            "your subjects."
        )
    }

    context = update_context(
        context,
        "subject_explanation",
        result,
        "Why?"
    )

    print("\nAfter subject_explanation:")
    print(context)

    print(
        "\nLast Subject:",
        get_last_subject(context)
    )

    print(
        "Requested Subject:",
        get_requested_subject(context)
    )

    print(
        "Last Intent:",
        get_last_intent(context)
    )

    print(
        "Last Result:",
        context.get("last_result")
    )

    # --------------------------------------
    # Clear subject
    # --------------------------------------

    context = clear_subject(context)

    print("\nAfter clearing subject:")
    print(context)


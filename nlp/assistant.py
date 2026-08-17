from nlp.intent_classifier import classify_intent
from nlp.intent_router import route_intent


def start_assistant(student_name):

    print("\n============================================")
    print("          STUDENT AI ASSISTANT")
    print("============================================")

    print(f"\nHello {student_name}! 👋")
    print("Ask me about your marks, attendance,")
    print("performance, risk, recommendation, or trend.")
    print("Type 'bye' to exit.")

    while True:

        user_input = input("\nYou: ")

        intent = classify_intent(user_input)

        if intent == "exit":
            print("\nAI: Goodbye! Keep working hard. 👋")
            break

        response = route_intent(
            intent,
            student_name
        )

        print(f"\nAI: {response}")


if __name__ == "__main__":
    student_name = input("Enter student name: ")
    start_assistant(student_name)
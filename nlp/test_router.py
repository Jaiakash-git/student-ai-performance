from nlp.intent_classifier import classify_intent
from nlp.intent_router import route_intent


student_name = input("Enter student name: ")

while True:

    user_input = input("\nAsk something: ")

    intent = classify_intent(user_input)

    if intent == "exit":
        print("Goodbye!")
        break

    response = route_intent(
        intent,
        student_name
    )

    print("\nAI:", response)
from nlp.intent_classifier import classify_intent


while True:

    user_input = input("\nAsk something: ")

    intent = classify_intent(user_input)

    print("Detected Intent:", intent)

    if intent == "exit":
        print("Goodbye!")
        break
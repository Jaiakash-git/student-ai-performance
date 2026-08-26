import requests


# ==========================================
# OLLAMA CONFIGURATION
# ==========================================

OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL_NAME = "qwen2.5:3b"


# ==========================================
# GENERATE ANSWER
# ==========================================

def generate_answer(question, context):

    prompt = f"""
You are an academic assistant for a student management system.

You MUST answer the user's question using ONLY the provided context.

STRICT RULES:

1. Use only information explicitly supported by the context.

2. Do NOT use your general or pretrained knowledge.

3. Do NOT make assumptions or guesses.

4. Do NOT add information that is not present in the context.

5. If the context does not contain enough information to answer
   the question, respond EXACTLY with:

   I don't have enough information to answer that.

6. Follow all numerical values, ranges, thresholds, and boundaries
   exactly as written in the context.

7. Before answering, check whether the answer is actually supported
   by the context.

8. Keep the answer concise and direct.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
    )

    response.raise_for_status()

    data = response.json()

    return data["response"].strip()


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    question = "Is 90% attendance good?"

    context = """
Attendance Guidelines

Attendance above 85% is considered good.

Attendance between 75% and 85% is acceptable,
but students should try to improve their attendance.

Attendance below 75% needs attention.
"""

    answer = generate_answer(
        question,
        context
    )

    print("\n================================")
    print("GENERATED ANSWER")
    print("================================")

    print(answer)
import pandas as pd
from pathlib import Path

# ============================================================
# CONFIG
# ============================================================

INPUT_FILE = Path("nlp/intent_dataset_v3.csv")
OUTPUT_FILE = Path("nlp/intent_dataset_v4.csv")


# ============================================================
# LOAD DATASET
# ============================================================

df = pd.read_csv(INPUT_FILE)

print("Original V3 dataset:")
print(f"Total samples: {len(df)}")


# ============================================================
# CLEAN TEXT
# ============================================================

df["text"] = (
    df["text"]
    .astype(str)
    .str.strip()
    .str.lower()
)

df["intent"] = (
    df["intent"]
    .astype(str)
    .str.strip()
    .str.lower()
)


# ============================================================
# REMOVE DUPLICATES
# ============================================================

before = len(df)

df = df.drop_duplicates(subset=["text"], keep="first")

removed = before - len(df)

print(f"Duplicate questions removed: {removed}")


# ============================================================
# FIX KNOWN AMBIGUOUS LABELS
# ============================================================

label_corrections = {

    # Recommendation
    "which subject should i improve": "recommendation",

    # Recommendation rather than lowest_subject
    "which subject needs my attention": "recommendation",

    # Trend
    "show my performance trend": "trend",
}


for text, intent in label_corrections.items():

    mask = df["text"] == text

    if mask.any():
        df.loc[mask, "intent"] = intent
        print(f"Corrected: '{text}' -> {intent}")


# ============================================================
# V4 TARGETED TRAINING EXAMPLES
# ============================================================

new_examples = [

    # ========================================================
    # RISK
    # ========================================================

    ("is there a risk in my performance", "risk"),
    ("is my performance putting me at risk", "risk"),
    ("should i be worried about my results", "risk"),
    ("should i worry about my marks", "risk"),
    ("are my marks a cause for concern", "risk"),
    ("do my results show any risk", "risk"),
    ("is there anything wrong with my academic performance", "risk"),
    ("is my academic performance a concern", "risk"),
    ("do i have any academic risk", "risk"),
    ("am i academically at risk", "risk"),
    ("should i be concerned about my marks", "risk"),
    ("is there a warning in my performance", "risk"),
    ("do my marks indicate a problem", "risk"),
    ("is my academic performance concerning", "risk"),
    ("is my current performance risky", "risk"),

    # ========================================================
    # MARKS
    # ========================================================

    ("give me my marks", "marks"),
    ("give me my scores", "marks"),
    ("show me my marks details", "marks"),
    ("show me my score details", "marks"),
    ("list all my marks", "marks"),
    ("list my subject marks", "marks"),
    ("show my subject scores", "marks"),
    ("display all my marks", "marks"),
    ("display my scores", "marks"),
    ("tell me all my marks", "marks"),
    ("tell me all my scores", "marks"),
    ("what marks did i get in my subjects", "marks"),
    ("what scores did i get", "marks"),
    ("can you list my marks", "marks"),
    ("can you show all my marks", "marks"),

    # ========================================================
    # TREND
    # ========================================================

    ("show my marks trend", "trend"),
    ("show my score trend", "trend"),
    ("show my improvement", "trend"),
    ("show my progress", "trend"),
    ("how are my marks changing", "trend"),
    ("how are my scores changing", "trend"),
    ("are my marks improving", "trend"),
    ("are my scores improving", "trend"),
    ("have my marks improved recently", "trend"),
    ("have my scores improved recently", "trend"),
    ("did my marks improve", "trend"),
    ("did my scores improve", "trend"),
    ("how have my marks changed over time", "trend"),
    ("how have my scores changed over time", "trend"),
    ("compare my marks over time", "trend"),

    # ========================================================
    # RECOMMENDATION
    # ========================================================

    ("what do you recommend for me", "recommendation"),
    ("what should i do next", "recommendation"),
    ("what can i do to improve my studies", "recommendation"),
    ("what should i do to improve my marks", "recommendation"),
    ("what should i do about my weak subject", "recommendation"),
    ("how can i improve my weak areas", "recommendation"),
    ("what should i concentrate on improving", "recommendation"),
    ("which areas should i give more attention to", "recommendation"),
    ("what should i study more", "recommendation"),
    ("what should i spend more time on", "recommendation"),
    ("how can i get better marks", "recommendation"),
    ("what can i do to perform better", "recommendation"),
    ("what study advice can you give me", "recommendation"),
    ("what do you recommend i improve", "recommendation"),
    ("which areas should i improve", "recommendation"),

    # ========================================================
    # ATTENDANCE
    # ========================================================

    ("how regular is my attendance", "attendance"),
    ("am i attending enough classes", "attendance"),
    ("what is my attendance rate", "attendance"),
    ("how many classes was i present for", "attendance"),
    ("how often do i attend classes", "attendance"),

    # ========================================================
    # AVERAGE
    # ========================================================

    ("what is my overall average score", "average"),
    ("what is my average marks", "average"),
    ("what is my average percentage", "average"),
    ("how much did i score overall", "average"),
    ("what is my overall academic score", "average"),

]


# ============================================================
# ADD ONLY NEW QUESTIONS
# ============================================================

existing_questions = set(df["text"])

added = 0

for text, intent in new_examples:

    if text not in existing_questions:

        df.loc[len(df)] = {
            "text": text,
            "intent": intent
        }

        existing_questions.add(text)
        added += 1


print(f"New V4 examples added: {added}")


# ============================================================
# FINAL SHUFFLE
# ============================================================

df = df.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)


# ============================================================
# SAVE V4
# ============================================================

df.to_csv(
    OUTPUT_FILE,
    index=False
)


print("\n============================================")
print("DATASET V4 CREATED SUCCESSFULLY")
print("============================================")

print(f"Total samples: {len(df)}")

print("\nClass distribution:")
print(df["intent"].value_counts())

print(f"\nSaved to: {OUTPUT_FILE}")
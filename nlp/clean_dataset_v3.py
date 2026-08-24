import pandas as pd
from pathlib import Path

# ============================================================
# CONFIG
# ============================================================

INPUT_FILE = Path("nlp/intent_dataset_v2.csv")
OUTPUT_FILE = Path("nlp/intent_dataset_v3.csv")


# ============================================================
# LOAD DATASET
# ============================================================

df = pd.read_csv(INPUT_FILE)

print("Original dataset:")
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
# REMOVE EXACT DUPLICATES
# ============================================================

before = len(df)

df = df.drop_duplicates(subset=["text"], keep="first")

removed = before - len(df)

print(f"Duplicate questions removed: {removed}")


# ============================================================
# FIX INCORRECT / AMBIGUOUS LABELS
# ============================================================

label_corrections = {

    # Performance, NOT average
    "how am i doing academically": "performance",

    # This asks what to improve, so recommendation
    "which subject should i improve": "recommendation",
}


for text, intent in label_corrections.items():

    mask = df["text"] == text

    if mask.any():
        df.loc[mask, "intent"] = intent
        print(f"Corrected: '{text}' -> {intent}")


# ============================================================
# ADD TARGETED TRAINING EXAMPLES
# ============================================================

new_examples = [

    # --------------------------------------------------------
    # HIGHEST SUBJECT
    # --------------------------------------------------------

    ("what is my highest mark", "highest_subject"),
    ("what is my highest score", "highest_subject"),
    ("what is my maximum score", "highest_subject"),
    ("what is my maximum mark", "highest_subject"),
    ("what is my best score", "highest_subject"),
    ("what is my best mark", "highest_subject"),
    ("tell me my highest score", "highest_subject"),
    ("tell me my highest mark", "highest_subject"),
    ("which subject has my highest score", "highest_subject"),
    ("which subject has my maximum score", "highest_subject"),
    ("which subject has my best score", "highest_subject"),
    ("what is my top score", "highest_subject"),

    # --------------------------------------------------------
    # LOWEST SUBJECT
    # --------------------------------------------------------

    ("what is my lowest mark", "lowest_subject"),
    ("what is my lowest score", "lowest_subject"),
    ("what is my minimum score", "lowest_subject"),
    ("what is my minimum mark", "lowest_subject"),
    ("what is my worst mark", "lowest_subject"),
    ("tell me my lowest score", "lowest_subject"),
    ("tell me my lowest mark", "lowest_subject"),
    ("which subject has my lowest score", "lowest_subject"),
    ("which subject has my minimum score", "lowest_subject"),
    ("which subject has my worst mark", "lowest_subject"),
    ("what is my bottom score", "lowest_subject"),

    # --------------------------------------------------------
    # TREND
    # --------------------------------------------------------

    ("what happened to my marks recently", "trend"),
    ("what happened to my scores recently", "trend"),
    ("how are my marks changing recently", "trend"),
    ("are my marks getting better", "trend"),
    ("are my scores getting better", "trend"),
    ("have my marks gotten better", "trend"),
    ("have my scores gotten better", "trend"),
    ("what changed in my recent marks", "trend"),
    ("how did my marks change recently", "trend"),
    ("am i doing better recently", "trend"),
    ("what is happening with my marks", "trend"),
    ("are my marks improving recently", "trend"),

    # --------------------------------------------------------
    # PERFORMANCE
    # --------------------------------------------------------

    ("how good are my studies", "performance"),
    ("how good am i doing in my studies", "performance"),
    ("can you evaluate my studies", "performance"),
    ("evaluate my studies", "performance"),
    ("how well am i doing academically", "performance"),
    ("how good am i academically", "performance"),
    ("how would you rate my studies", "performance"),
    ("what do you think about my studies", "performance"),
    ("how are my studies going overall", "performance"),
    ("can you assess my studies", "performance"),

    # --------------------------------------------------------
    # RECOMMENDATION
    # --------------------------------------------------------

    ("where should i focus", "recommendation"),
    ("what should i work on", "recommendation"),
    ("what are my weak areas", "recommendation"),
    ("which subject should i focus on", "recommendation"),
    ("where am i weak", "recommendation"),
    ("which subject requires more attention", "recommendation"),
    ("what should i concentrate on", "recommendation"),
    ("which area should i focus on", "recommendation"),
    ("which areas need improvement", "recommendation"),
    ("what should i pay attention to", "recommendation"),
    ("where do i need to improve", "recommendation"),
    ("which subject needs my attention", "recommendation"),
    ("what should i focus on improving", "recommendation"),
    ("what areas should i work on", "recommendation"),
    ("what do i need to work on", "recommendation"),
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


print(f"New examples added: {added}")


# ============================================================
# FINAL SHUFFLE
# ============================================================

df = df.sample(frac=1, random_state=42).reset_index(drop=True)


# ============================================================
# SAVE
# ============================================================

df.to_csv(OUTPUT_FILE, index=False)

print("\n============================================")
print("DATASET V3 CREATED SUCCESSFULLY")
print("============================================")

print(f"Total samples: {len(df)}")

print("\nClass distribution:")
print(df["intent"].value_counts())

print(f"\nSaved to: {OUTPUT_FILE}")
import os
import pandas as pd


# ==========================================
# PATHS
# ==========================================

base_dir = os.path.dirname(__file__)

clean_path = os.path.join(
    base_dir,
    "intent_dataset_clean.csv"
)

v2_path = os.path.join(
    base_dir,
    "intent_dataset_v2.csv"
)


# ==========================================
# LOAD CLEAN DATASET
# ==========================================

data = pd.read_csv(clean_path)

print("Clean dataset loaded!")
print(f"Existing samples: {len(data)}")


# ==========================================
# NEW HIGH-QUALITY EXAMPLES
# ==========================================

new_examples = [

        # Performance
    ("show my current performance", "performance"),
    ("tell me my current performance", "performance"),
    ("what is my current performance", "performance"),
    ("give me my current performance", "performance"),
    ("how is my academic performance", "performance"),
    ("what does my performance look like", "performance"),
    ("tell me about my current performance", "performance"),
    ("give me an overview of my performance", "performance"),
    ("how would you describe my performance", "performance"),
    ("what is my performance status", "performance"),

    # Trend
    ("how has my performance changed", "trend"),
    ("how is my performance changing", "trend"),
    ("has my performance improved", "trend"),
    ("did my performance change over time", "trend"),
    ("how did my performance change from before", "trend"),

    # Risk
    ("is my performance concerning", "risk"),
    ("should i be concerned about my results", "risk"),
    ("does my performance indicate risk", "risk"),
    ("is there any risk in my academic performance", "risk"),
    ("should i worry about my academic performance", "risk"),

    # Highest subject
    ("which subject has my maximum score", "highest_subject"),
    ("where did i get my highest marks", "highest_subject"),
    ("which subject has my best result", "highest_subject"),
    ("which subject did i score the most marks in", "highest_subject"),
    ("which subject has my greatest score", "highest_subject"),
]


# ==========================================
# ADD NEW EXAMPLES
# ==========================================

new_data = pd.DataFrame(
    new_examples,
    columns=["text", "intent"]
)

data = pd.concat(
    [data, new_data],
    ignore_index=True
)


# ==========================================
# REMOVE DUPLICATES
# ==========================================

data["text"] = (
    data["text"]
    .str.lower()
    .str.strip()
)

data = data.drop_duplicates(
    subset=["text", "intent"]
)


# ==========================================
# SAVE V2
# ==========================================

data.to_csv(
    v2_path,
    index=False
)


# ==========================================
# REPORT
# ==========================================

print(f"\nFinal samples: {len(data)}")

print("\nClass distribution:")
print(data["intent"].value_counts())

print("\nV2 dataset saved:")
print(v2_path)
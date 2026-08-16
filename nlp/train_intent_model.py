import os
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics import confusion_matrix


# ==========================================
# LOAD DATASET
# ==========================================

dataset_path = os.path.join(
    os.path.dirname(__file__),
    "intent_dataset.csv"
)

data = pd.read_csv(dataset_path)

print("Dataset loaded successfully!")
print(f"Total samples: {len(data)}")

print("\nClass distribution:")
print(data["intent"].value_counts())


# ==========================================
# FEATURES AND TARGET
# ==========================================

X = data["text"]
y = data["intent"]


# ==========================================
# TRAIN / TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# ==========================================
# TF-IDF + LOGISTIC REGRESSION
# ==========================================

model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2)
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=1000
        )
    )
])


# ==========================================
# TRAIN MODEL
# ==========================================

model.fit(X_train, y_train)


# ==========================================
# PREDICTION
# ==========================================

y_pred = model.predict(X_test)


# ==========================================
# EVALUATION
# ==========================================

accuracy = accuracy_score(y_test, y_pred)

print(f"\nModel Accuracy: {accuracy:.2f}")

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)

print("\nConfusion Matrix:")

labels = sorted(y.unique())

cm = confusion_matrix(
    y_test,
    y_pred,
    labels=labels
)

cm_df = pd.DataFrame(
    cm,
    index=labels,
    columns=labels
)

print(cm_df)


# ==========================================
# TEST SAMPLE QUESTIONS
# ==========================================

test_questions = [
    "Which subject am I strongest in?",
    "How much attendance do I have?",
    "Am I getting better?",
    "What should I improve?",
    "Am I at risk?",
    "Tell me my average"
]

print("\nSample Predictions:")

for question in test_questions:

    prediction = model.predict([question])[0]

    print(
        f"{question} -> {prediction}"
    )


# ==========================================
# SAVE MODEL
# ==========================================

import joblib

models_directory = os.path.join(
    os.path.dirname(__file__),
    "models"
)

os.makedirs(
    models_directory,
    exist_ok=True
)

model_path = os.path.join(
    models_directory,
    "intent_model.pkl"
)

joblib.dump(
    model,
    model_path
)

print("\nIntent model saved successfully!")
print(f"Saved to: {model_path}")
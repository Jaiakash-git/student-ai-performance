import pandas as pd
import joblib

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# Load dataset
data = pd.read_csv("ml/dataset.csv")


# Display class distribution
print("Class distribution:")
print(data["needs_attention"].value_counts())


# Features
X = data[
    [
        "average_marks",
        "attendance_percentage",
        "highest_mark",
        "lowest_mark"
    ]
]


# Target
y = data["needs_attention"]


# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# Create ML pipeline
model = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", LogisticRegression())
])


# Train model
model.fit(X_train, y_train)


# Feature coefficients
coefficients = model.named_steps["classifier"].coef_[0]

print("\nFeature Coefficients:")

for feature, coefficient in zip(X.columns, coefficients):
    print(f"{feature}: {coefficient:.4f}")


# Cross-validation
cv_scores = cross_val_score(
    model,
    X,
    y,
    cv=5,
    scoring="accuracy"
)

print("\nCross-validation scores:")
print(cv_scores)

print(f"Mean CV Accuracy: {cv_scores.mean():.2f}")


# Test predictions
y_pred = model.predict(X_test)


# Confusion matrix
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))


# Accuracy
accuracy = accuracy_score(y_test, y_pred)

print(f"\nModel Accuracy: {accuracy:.2f}")


# Classification report
print("\nClassification Report:")
print(classification_report(y_test, y_pred))


# Save model
joblib.dump(
    model,
    "ml/student_performance_model.pkl"
)

print("\nModel saved successfully!")
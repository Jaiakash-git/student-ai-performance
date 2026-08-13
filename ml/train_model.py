import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


# Load dataset
data = pd.read_csv("ml/dataset.csv")


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


# Create model
model = LogisticRegression()


# Train model
model.fit(X_train, y_train)


# Make predictions
y_pred = model.predict(X_test)


# Evaluate model
accuracy = accuracy_score(y_test, y_pred)

print(f"Model Accuracy: {accuracy:.2f}")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))


# Save trained model
joblib.dump(model, "ml/student_performance_model.pkl")

print("\nModel saved successfully!")
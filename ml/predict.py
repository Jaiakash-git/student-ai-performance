import joblib
import pandas as pd


# Load trained model once when this module is imported
MODEL_PATH = "ml/student_performance_model.pkl"
model = joblib.load(MODEL_PATH)


def predict_performance(
    average_marks,
    attendance,
    highest_mark,
    lowest_mark
):
    # Prepare student data
    student_data = pd.DataFrame([{
        "average_marks": average_marks,
        "attendance_percentage": attendance,
        "highest_mark": highest_mark,
        "lowest_mark": lowest_mark
    }])

    # Prediction
    prediction = model.predict(student_data)[0]

    # Probability of each class
    probabilities = model.predict_proba(student_data)[0]

    # Probability of "Needs Attention" (class 1)
    risk_probability = probabilities[1] * 100

    if prediction == 1:
        status = "Needs Attention"
    else:
        status = "No Attention Required"

    return status, risk_probability

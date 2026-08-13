import joblib
import pandas as pd


def predict_performance(average_marks, attendance,
                        highest_mark, lowest_mark):

    # Load trained model
    model = joblib.load("ml/student_performance_model.pkl")

    # Prepare student data
    student_data = pd.DataFrame([{
        "average_marks": average_marks,
        "attendance_percentage": attendance,
        "highest_mark": highest_mark,
        "lowest_mark": lowest_mark
    }])

    # Make prediction
    prediction = model.predict(student_data)[0]

    if prediction == 1:
        return "Needs Attention"
    else:
        return "No Attention Required"
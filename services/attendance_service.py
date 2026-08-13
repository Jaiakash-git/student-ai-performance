from database import get_connection


def get_student_attendance(student_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            subjects.subject_name,
            attendance.classes_attended,
            attendance.total_classes
        FROM attendance
        JOIN subjects
            ON subjects.subject_id = attendance.subject_id
        WHERE attendance.student_id = %s
    """, (student_id,))

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results
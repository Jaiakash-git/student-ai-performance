from database import get_connection


def get_student_marks(student_name):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT subjects.subject_name, marks.marks
        FROM students
        JOIN marks
            ON students.student_id = marks.student_id
        JOIN subjects
            ON subjects.subject_id = marks.subject_id
        WHERE students.name = %s
    """, (student_name,))

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results
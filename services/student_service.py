from database import get_connection


def get_student_id(student_name):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT student_id
        FROM students
        WHERE name = %s
    """, (student_name,))

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    if result:
        return result[0]

    return None


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


def get_student_exam_marks(student_name):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            subjects.subject_name,
            marks.exam_type,
            marks.marks
        FROM students
        JOIN marks
            ON students.student_id = marks.student_id
        JOIN subjects
            ON subjects.subject_id = marks.subject_id
        WHERE students.name = %s
        ORDER BY marks.exam_date, subjects.subject_name
    """, (student_name,))

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results
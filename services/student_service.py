from database import get_connection


# ==========================================
# GET STUDENT ID
# ==========================================

def get_student_id(student_name: str):

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT student_id
            FROM students
            WHERE name = %s
            """,
            (student_name,)
        )

        result = cursor.fetchone()

        if result:
            return result[0]

        return None

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==========================================
# GET STUDENT MARKS
# ==========================================
#
# Returns ONLY the latest mark for each subject.
#
# Example:
#
# OS   Internal 1 = 82
# OS   Internal 2 = 88
#
# Returns:
#
# OS   88
#
# Used for:
# - Average
# - Highest subject
# - Lowest subject
# - Performance
# - Risk
# - Recommendation
# - Subject details
#
# ==========================================

def get_student_marks(student_name: str):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                subjects.subject_name,
                marks.marks
            FROM students

            JOIN marks
                ON students.student_id = marks.student_id

            JOIN subjects
                ON subjects.subject_id = marks.subject_id

            WHERE students.name = %s

            AND marks.exam_date = (

                SELECT MAX(m2.exam_date)

                FROM marks m2

                WHERE m2.student_id = marks.student_id

                AND m2.subject_id = marks.subject_id

            )

            ORDER BY subjects.subject_name
            """,
            (student_name,)
        )

        return cursor.fetchall()

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==========================================
# GET ALL EXAM MARKS
# ==========================================
#
# Returns ALL internal exam marks.
#
# Used ONLY for trend analysis.
#
# ==========================================

def get_student_exam_marks(student_name: str):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
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

            ORDER BY
                marks.exam_date,
                subjects.subject_name
            """,
            (student_name,)
        )

        return cursor.fetchall()

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==========================================
# GET MARK FOR SPECIFIC SUBJECT
# ==========================================

def get_subject_mark(
    student_name: str,
    subject_name: str
):

    if not subject_name:
        return None, None

    results = get_student_marks(student_name)

    subject_name = subject_name.lower().strip()

    for subject, mark in results:

        if subject.lower().strip() == subject_name:

            return subject, float(mark)

    return None, None
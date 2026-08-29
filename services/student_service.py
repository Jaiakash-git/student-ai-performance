from database import get_connection


# ==========================================
# GET STUDENT ID
# ==========================================

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


# ==========================================
# GET STUDENT MARKS
# ==========================================
#
# IMPORTANT:
# Returns ONLY the latest mark for each subject.
#
# Example:
#
# OS      Internal 1 = 82
# OS      Internal 2 = 88
#
# This function returns:
#
# OS      88
#
# This is used for:
# - Average
# - Highest subject
# - Lowest subject
# - Performance
# - Risk
# - Recommendation
# - Subject detail
#
# ==========================================

def get_student_marks(student_name):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
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
    """, (student_name,))

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results


# ==========================================
# GET ALL EXAM MARKS
# ==========================================
#
# IMPORTANT:
# This function intentionally returns ALL
# internal exam marks.
#
# Used ONLY for trend analysis.
#
# Example:
#
# OS      Internal 1    82
# OS      Internal 2    88
# DBMS    Internal 1    91
# DBMS    Internal 2    94
#
# ==========================================

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


# ==========================================
# GET MARK FOR A SPECIFIC SUBJECT
# ==========================================
#
# Returns the latest mark because
# get_student_marks() already contains
# only the latest mark for each subject.
#
# ==========================================

def get_subject_mark(student_name, subject_name):

    results = get_student_marks(student_name)

    if not subject_name:
        return None, None

    subject_name = subject_name.lower().strip()

    for subject, mark in results:

        if subject.lower().strip() == subject_name:

            return subject, float(mark)

    return None, None


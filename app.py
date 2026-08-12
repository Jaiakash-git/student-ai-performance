from database import get_connection

# Connect to MySQL
connection = get_connection()
cursor = connection.cursor()

# Get student name
student_name = input("Enter student name: ")

# Fetch marks
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

if not results:
    print("Student not found!")

else:
    print(f"\nMarks for {student_name}:")

    for subject, mark in results:
        print(f"{subject}: {mark:.2f}")

    # Extract marks
    marks_list = [float(mark) for subject, mark in results]

    # Calculate average
    average = sum(marks_list) / len(marks_list)

    # Find highest mark
    highest_mark = max(marks_list)

    # Find subject with highest mark
    highest_subject = None

    for subject, mark in results:
        if float(mark) == highest_mark:
            highest_subject = subject
            break

    print(f"\nAverage Mark: {average:.2f}")
    print(f"Highest Mark: {highest_mark:.2f}")
    print(f"Highest Scoring Subject: {highest_subject}")

# Close connection
cursor.close()
connection.close()
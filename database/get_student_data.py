async def get_student_id_by_email(cursor, student_email):
    cursor.execute("SELECT student_id FROM students WHERE email = %s", (student_email,))
    student = cursor.fetchone()
    if student:
        return student[0]  # Вернуть student_id
    return None  # Вернуть None, если студент не найден
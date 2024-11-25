def insert_student(cursor, data):
    cursor.execute(
        "INSERT INTO students (first_name, second_name, last_name, email, group_id, course) VALUES (%s, %s, %s, %s, %s, %s)",
        (data['first_name'], data['second_name'], data['last_name'], data['email'], data['group_id'], data['course'])
    )
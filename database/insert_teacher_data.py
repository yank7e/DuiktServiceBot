class TeachersInfo():
    def insert_teacher(self, cursor, data):
        cursor.execute(
            "INSERT INTO teachers (name, email) VALUES (%s, %s) RETURNING teacher_id",
            (data['name'], data['email'])
        )
        teacher_id = cursor.fetchone()[0]
        return teacher_id

    def insert_teacher_courses_groups(self, cursor, teacher_id, courses, groups):
        for course in courses:
            for group in groups:
                cursor.execute(
                    """
                    INSERT INTO teacher_courses_groups (teacher_id, course_name, group_id)
                    VALUES (%s, %s, %s) ON CONFLICT DO NOTHING
                    """,
                    (teacher_id, course, group)
                )
    
    def insert_teacher_subjects(self, cursor, teacher_id, subjects):
        for subject in subjects:
            cursor.execute(
                """
                INSERT INTO teacher_subjects (teacher_id, subject_name)
                VALUES (%s, %s) ON CONFLICT DO NOTHING
                """,
                (teacher_id, subject)
            )
import logging
from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from bot_instance import dp
from database.db_connection import get_db_connection
from database.get_student_data import get_student_id_by_email

# Настройка логирования
logging.basicConfig(level=logging.INFO)

class StudentMenu(StatesGroup):
    view_grades = State()

# Получаем подключение к базе данных
conn, cursor = get_db_connection()

# Главное меню для студентов
student_menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
student_menu_keyboard.add(types.KeyboardButton("Мої бали"))

# async def student_menu_dialog(message: types.Message):
#     logging.info("Функция student_menu_dialog была вызвана.")
#     print("Функция student_menu_dialog была вызвана.")  # Дополнительный отладочный вывод
#     await StudentMenu.view_grades.set()
#     await message.answer("Вітаємо! Ось ваше головне меню:", reply_markup=student_menu_keyboard)

async def student_menu_dialog(message: types.Message, state: FSMContext):
    logging.info("Функция student_menu_dialog была вызвана.")
    print("Функция student_menu_dialog была вызвана.")
    await StudentMenu.view_grades.set()
    await message.answer("Вітаємо! Ось ваше головне меню:", reply_markup=student_menu_keyboard)

@dp.message_handler(lambda message: message.text == "Мої бали", state=StudentMenu.view_grades)
async def view_grades(message: types.Message, state: FSMContext):
    data = await state.get_data()
    student_email = data.get('email')
    print(f"Email студента из состояния: {student_email}")

    if student_email:
        student_id = await get_student_id_by_email(cursor, student_email)
        print(student_email)
        print(student_id)

        if student_id:
            cursor.execute("""
                SELECT s.subject_name, g.grade
                FROM grades g
                JOIN subjects s ON g.subject_name = s.subject_name
                WHERE g.student_id = %s
            """, (student_id,))
            grades = cursor.fetchall()
            if grades:
                response = "Ваші оцінки по предметам:\n"
                for idx, (subject, grade) in enumerate(grades, start=1):
                    response += f"{idx}. {subject}: {grade}\n"
                await message.answer(response)
            else:
                await message.answer("Ви ще не маєте оцінок.")
        else:
            await message.answer("Вас немає в базі студентів. Будь ласка, зареєструйтесь.")
    else:
        await message.answer("Не знайдено email. Будь ласка, зареєструйтесь.")

# dp.message_handler(lambda message: message.text == "Мої бали", state=StudentMenu.view_grades)
# async def view_grades(message: types.Message):
#     student_email = message.from_user.username  # Используем username Telegram для идентификации
#     cursor.execute("SELECT student_id FROM students WHERE email = %s", (student_email,))
#     student = cursor.fetchone()

#     if student:
#         student_id = student[0]
#         cursor.execute("""
#             SELECT s.subject_name, g.grade
#             FROM grades g
#             JOIN subjects s ON g.subject_name = s.subject_name
#             WHERE g.student_id = %s@
#         """, (student_id,))

#         grades = cursor.fetchall()
#         if grades:
#             response = "Ваші оцінки по предметам:\n"
#             for idx, (subject, grade) in enumerate(grades, start=1):
#                 response += f"{idx}. {subject}\nрезультат {grade}\n"
#             await message.answer(response)
#         else:
#             await message.answer("Ви ще не маєте оцінок.")
#     else:
#         await message.answer("Вас немає в базі студентів. Будь ласка, зареєструйтесь.")

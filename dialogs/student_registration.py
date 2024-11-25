from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Dispatcher, types
from database.insert_student_data import insert_student
import asyncio
import logging
from aiogram.dispatcher import FSMContext
from bot_instance import dp
from dialogs.menus.student_menu import student_menu_dialog


class StudentRegistration(StatesGroup):
    first_name = State()
    second_name = State()
    last_name = State()
    email = State()
    group_id = State()
    course = State()

async def register_student_dialog(dp: Dispatcher, message: types.Message, cursor, conn):
    await StudentRegistration.first_name.set()
    await message.answer("Введіть ваше ім'я:")

    @dp.message_handler(state=StudentRegistration.first_name)
    async def student_first_name(message: types.Message, state: FSMContext):
        await state.update_data(first_name=message.text)
        await StudentRegistration.next()
        await message.answer("Введіть ваше по батькові:")

    @dp.message_handler(state=StudentRegistration.second_name)
    async def student_second_name(message: types.Message, state: FSMContext):
        await state.update_data(second_name=message.text)
        await StudentRegistration.next()
        await message.answer("Введіть ваше прізвище:")

    @dp.message_handler(state=StudentRegistration.last_name)
    async def student_last_name(message: types.Message, state: FSMContext):
        await state.update_data(last_name=message.text)
        await StudentRegistration.next()
        await message.answer("Введіть вашу електронну пошту:")

    @dp.message_handler(state=StudentRegistration.email)
    async def student_email(message: types.Message, state: FSMContext):
        await state.update_data(email=message.text)
        await StudentRegistration.next()
        await message.answer("Введіть номер групи:")

    @dp.message_handler(state=StudentRegistration.group_id)
    async def student_group_number(message: types.Message, state: FSMContext):
        await state.update_data(group_id=message.text)
        await StudentRegistration.next()
        await message.answer("Введіть курс:")

    logging.basicConfig(level=logging.INFO)

    @dp.message_handler(state=StudentRegistration.course)
    async def student_course(message: types.Message, state: FSMContext):
        await state.update_data(course=message.text)
        data = await state.get_data()

        try:
            student_email = data.get('email')  # Получить email из состояния
            if not student_email:
                await message.answer("Не вдалося знайти email студента в стані. Спробуйте ще раз.")
                await state.finish()
                return

            cursor.execute("SELECT student_id FROM students WHERE email = %s", (student_email,))
            existing_student = cursor.fetchone()

            if existing_student:
                await message.answer("Такий студент вже існує. Будь ласка, спробуйте інший email або увійдіть у свій аккаунт.")
                await state.finish()
                return

            # Вставляем нового студента
            insert_student(cursor, data)

            try:
                conn.commit()
            except Exception as e:
                await message.answer(f"Виникла помилка при збереженні змін. Спробуйте ще раз. Помилка: {e}")
                await state.finish()
                return

            await message.answer("Реєстрацію студента завершено! Дякую, ось ваше головне меню:")
            await state.update_data(email=student_email)  # Сохраните email студента в состоянии для дальнейшего использования
            print(f"Email сохранен в состоянии: {student_email}")
            await student_menu_dialog(message, state)  # Передаем state в функцию

        except Exception as e:
            await message.answer(f"Виникла помилка при реєстрації. Спробуйте ще раз. Помилка: {e}")
            await state.finish()
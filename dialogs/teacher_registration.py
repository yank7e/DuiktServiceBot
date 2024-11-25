from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Dispatcher, types
from database.insert_teacher_data import TeachersInfo

class TeacherRegistration(StatesGroup):
    name = State()
    email = State()
    groups = State()
    courses = State()
    subjects = State()

async def register_teacher_dialog(dp: Dispatcher, message: types.Message, cursor, conn):
    await TeacherRegistration.name.set()
    await message.answer("Введіть ваше ім'я:")

    @dp.message_handler(state=TeacherRegistration.name)
    async def teacher_last_name(message: types.Message, state: FSMContext):
        await state.update_data(name=message.text)
        await TeacherRegistration.next()
        await message.answer("Введіть вашу електронну пошту:")

    @dp.message_handler(state=TeacherRegistration.email)
    async def teacher_email(message: types.Message, state: FSMContext):
        await state.update_data(email=message.text)
        await TeacherRegistration.next()
        await message.answer("Введіть номери груп в яких ви викдладаєте, через кому (наприклад 'ПД-24, ПД-23, ПД-22'):")

    @dp.message_handler(state=TeacherRegistration.groups)
    async def teacher_groups(message: types.Message, state: FSMContext):
        groups = [group.strip() for group in message.text.split(',')]
        await state.update_data(groups=groups)
        await TeacherRegistration.next()
        await message.answer("Введіть курси у яких ви викладаєте, через кому (наприклад '1, 2, 3'):")

    @dp.message_handler(state=TeacherRegistration.courses)
    async def teacher_subjects(message: types.Message, state: FSMContext):
        courses = [course.strip() for course in message.text.split(',')]
        await state.update_data(courses=courses)  
        await TeacherRegistration.next()
        await message.answer("Введите предметы, які ви викладаєте, через кому якщо більше одного (наприклад 'ВМ, ІМ, КДС'):")

    @dp.message_handler(state=TeacherRegistration.subjects)
    async def teacher_subjects(message: types.Message, state: FSMContext):
        subjects = [subject.strip() for subject in message.text.split(',')]
        await state.update_data(subjects=subjects)

        data = await state.get_data()

        if 'courses' not in data or 'groups' not in data:
            await message.answer("Ошибка: данные о курсах или группах не сохранены.")
            return

        print(data['courses'], data['groups'], data['subjects'])

        # Вставка данных в базу данных
        teacher_id = TeachersInfo().insert_teacher(cursor, data)
        TeachersInfo().insert_teacher_courses_groups(cursor, teacher_id, data['courses'], data['groups'])
        TeachersInfo().insert_teacher_subjects(cursor, teacher_id, data['subjects'])
        conn.commit()

        await message.answer("Регистрация завершена! Спасибо за регистрацию.")
        await state.finish()
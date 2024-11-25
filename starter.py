from aiogram import Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database.db_connection import get_db_connection
from dialogs.teacher_registration import register_teacher_dialog
from config import ApplicationConfig
from bot_instance import bot, dp
from dialogs.student_registration import register_student_dialog
import os

config = ApplicationConfig()

conn, cursor = get_db_connection()

role_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
role_keyboard.add(KeyboardButton("Студент"))
role_keyboard.add(KeyboardButton("Викладач"))

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Вітаємо! Ласкаво просимо до університетського бота. Виберіть, хто ви: студент чи викладач.", reply_markup=role_keyboard)

@dp.message_handler(lambda message: message.text == "Студент")
async def student_role_selected(message: types.Message):
    await register_student_dialog(dp, message, cursor, conn)

@dp.message_handler(lambda message: message.text == "Викладач")
async def teacher_role_selected(message: types.Message):
    await register_teacher_dialog(dp, message, cursor, conn)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

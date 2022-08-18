from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from utils.db_api import database

db = database.DBCommands()


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Привіт, {message.from_user.full_name}! Натисни /menu щоб продовжити спілкування")
    await db.add_new_user()

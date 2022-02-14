from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_buttons = [
    "Кава", 'Ціни', 'Інстаграм', '!Кошик'
]
user_keyboards = ReplyKeyboardMarkup(resize_keyboard=True)
user_keyboards.add(*start_buttons)
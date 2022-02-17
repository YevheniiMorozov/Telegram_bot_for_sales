from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_buttons = [
    "Тут магазин", 'Тут про нас', '!Кошик'
]
tableware = KeyboardButton(text="", )
user_keyboards = ReplyKeyboardMarkup(resize_keyboard=True)
user_keyboards.add(*start_buttons)
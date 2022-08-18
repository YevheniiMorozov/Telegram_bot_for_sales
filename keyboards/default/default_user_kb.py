from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_buttons = [
    "Тут магазин", 'Тут про нас', 'Кошик'
]
tableware = KeyboardButton(text="", )
user_keyboards = ReplyKeyboardMarkup(resize_keyboard=True)
user_keyboards.add(*start_buttons)

purchase_user = [
    "Оплатити", "Видалити замовлення", "Продовжити покупки"
]
purchase_buttons = ReplyKeyboardMarkup(resize_keyboard=True)
purchase_buttons.add(*purchase_user)
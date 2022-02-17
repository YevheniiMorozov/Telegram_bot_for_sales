from aiogram.types import ReplyKeyboardMarkup


admin_kb = ["Додати лот", "Видалити лот"]
admin_keyboards = ReplyKeyboardMarkup(resize_keyboard=True)
admin_keyboards.add(*admin_kb)

beans_or_drip = ["Кава в зернах", "Кава в дріпах", "Кава в капсулах", "Посуд", "Відмінити"]
beans_or_drip_kb = ReplyKeyboardMarkup(resize_keyboard=True)
beans_or_drip_kb.add(*beans_or_drip)

cancel_kb = "Відмінити"
cancel_button = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_button.add(cancel_kb)


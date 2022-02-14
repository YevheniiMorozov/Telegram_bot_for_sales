from aiogram.dispatcher.filters.state import StatesGroup, State


class FSMAdmin(StatesGroup):
    photo = State()
    category = State()
    name = State()
    description = State()
    price = State()

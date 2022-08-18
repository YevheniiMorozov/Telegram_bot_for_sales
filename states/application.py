from aiogram.dispatcher.filters.state import StatesGroup, State


class Application(StatesGroup):
    EnterQuantity = State()


class Delivery(StatesGroup):
    FullName = State()
    PhoneNumber = State()
    Address = State()

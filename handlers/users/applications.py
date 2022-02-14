from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command

from loader import dp, types
from states import Application


@dp.message_handler(Command('Кошик', prefixes="!"), state=None)
async def enter_application(message: types.Message, state: FSMContext):

    data = await state.get_data()
    await message.answer("Напишіть Ваше ім'я та прізвище")

    await Application.Q1.set()


@dp.message_handler(state=Application.Q1)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text

    await state.update_data(answer1=answer)

    await message.answer("Оберіть спосіб доставки")
    await Application.next()


@dp.message_handler(state=Application.Q2)
async def answer_q2(message: types.Message, state: FSMContext):

    data = await state.get_data()
    answer1 = data.get('answer1')
    answer2 = message.text

    await message.answer("Перевірте Ваші данні")
    await message.answer(f"{answer1}\n{answer2}")

    await state.reset_state(with_data=False)


import hashlib

from aiogram import types

from loader import dp, tx, bot

from utils.db_api.db import sql_read

from keyboards.default.default_user_kb import user_keyboards
from keyboards.inline.user_inline_kb import choice


@dp.message_handler(commands="menu")
async def start(message: types.Message):

    await message.answer("Обери категорію", reply_markup=user_keyboards)


@dp.message_handler(tx(equals='Кава'))
async def coffee_beans(message: types.Message):
    await message.answer("Яку каву бажаєте обрати", reply_markup=choice)


@dp.inline_handler(text=["Кава в дріпах"])
async def inline_handler_drip(query: types.InlineQuery):
    text = query.query or "echo"
    button = "Кава в дріпах"
    items = await sql_read(category=button)
    result_id: str = hashlib.md5(text.encode()).hexdigest()
    articles = [
        types.InlineQueryResultCachedPhoto(
            id=result_id,
            photo_file_id=item[0],
            title=item[2],
            caption=f'{item[2]}\n{item[3]}\n{item[4]}'
        ) for item in items
    ]
    await query.answer(articles, cache_time=1, is_personal=True)


@dp.inline_handler(text="Кава в зернах")
async def inline_handler_drip(query: types.InlineQuery):
    text = query.query
    button = "Кава в зернах"
    items = await sql_read(category=button)
    result_id: str = hashlib.md5(text.encode()).hexdigest()
    articles = [
        types.InlineQueryResultCachedPhoto(
            id=result_id,
            photo_file_id=item[0],
            title=item[2],
            caption=f'{item[2]}\n{item[3]}\n{item[4]}'
        ) for item in items
    ]
    if query.query == 0:
        await query.answer([], cache_time=1, is_personal=True)
    else:
        await query.answer(articles, cache_time=1, is_personal=True)



@dp.message_handler(tx(equals='Ціни'))
async def coffee_beans(message: types.Message):
    pass


@dp.message_handler(tx(equals='Інстаграм'))
async def coffee_beans(message: types.Message):
    await message.answer("https://www.instagram.com/tut.bude/")


@dp.message_handler(tx(equals='Кошик'))
async def basket(message: types.Message):
    pass


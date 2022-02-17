import hashlib
import random
from aiogram import types

from loader import dp, tx, bot

from utils.db_api.db import sql_read

from keyboards.default.default_user_kb import user_keyboards
from keyboards.inline.user_inline_kb import choice, take_it


@dp.message_handler(commands="menu")
async def start(message: types.Message):

    await message.answer("Тут натисни на одну з кнопок", reply_markup=user_keyboards)


@dp.message_handler(tx(equals='Тут магазин'))
async def coffee_beans(message: types.Message):
    await message.answer("Обери, що саме тебе цікавить", reply_markup=choice)


@dp.inline_handler(text=["Кава в дріпах"])
async def inline_handler_drip(query: types.InlineQuery):
    text = query.query or "echo"
    button = "Кава в дріпах"
    items = await sql_read(category=button)
    result_id: str = hashlib.md5(text.encode()).hexdigest()
    articles = [
        types.InlineQueryResultArticle(
            id=result_id + str(random.randint(1, 100000000)),
            title=f"{item[2]}, ціна - {item[4]} грн.",
            description=item[3],
            hide_url=True,
            thumb_url=item[0],
            input_message_content=types.InputTextMessageContent(
                message_text=f'<a href="{item[0]}"> </a>\n{item[2]}\n{item[3]}\n{item[4]}', parse_mode="HTML"),
            reply_markup=take_it,
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
        types.InlineQueryResultArticle(
            id=result_id + str(random.randint(1, 100000000)),
            title=f"{item[2]}, ціна - {item[4]} грн.",
            description=item[3],
            hide_url=True,
            thumb_url=item[0],
            input_message_content=types.InputTextMessageContent(
                message_text=f'<a href="{item[0]}"> </a>\n{item[2]}\n{item[3]}\n{item[4]}', parse_mode="HTML"),
            reply_markup=take_it,
        ) for item in items
    ]
    if query.query == 0:
        await query.answer([], cache_time=1, is_personal=True)
    else:
        await query.answer(articles, cache_time=1, is_personal=True)
    await query.answer()


@dp.inline_handler(text="Кава в капсулах")
async def inline_handler_drip(query: types.InlineQuery):
    text = query.query
    button = "Кава в капсулах"
    items = await sql_read(category=button)
    result_id: str = hashlib.md5(text.encode()).hexdigest()
    articles = [
        types.InlineQueryResultArticle(
            id=result_id + str(random.randint(1, 100000000)),
            title=f"{item[2]}, ціна - {item[4]} грн.",
            description=item[3],
            hide_url=True,
            thumb_url=item[0],
            input_message_content=types.InputTextMessageContent(
                message_text=f'<a href="{item[0]}"> </a>\n{item[2]}\n{item[3]}\n{item[4]}', parse_mode="HTML"),
            reply_markup=take_it,
        ) for item in items
    ]
    if query.query == 0:
        await query.answer([], cache_time=1, is_personal=True)
    else:
        await query.answer(articles, cache_time=1, is_personal=True)


@dp.inline_handler(text="Посуд")
async def inline_handler_drip(query: types.InlineQuery):
    text = query.query
    button = "Посуд"
    items = await sql_read(category=button)
    result_id: str = hashlib.md5(text.encode()).hexdigest()
    articles = [
        types.InlineQueryResultArticle(
            id=result_id + str(random.randint(1, 100000000)),
            title=f"{item[2]}, ціна - {item[4]} грн.",
            description=item[3],
            hide_url=True,
            thumb_url=item[0],
            input_message_content=types.InputTextMessageContent(
                message_text=f'<a href="{item[0]}"> </a>\n{item[2]}\n{item[3]}\n{item[4]}', parse_mode="HTML"),
            reply_markup=take_it,
        ) for item in items
    ]
    if query.query == 0:
        await query.answer([], cache_time=1, is_personal=True)
    else:
        await query.answer(articles, cache_time=1, is_personal=True)


@dp.message_handler(tx(equals='Тут про нас'))
async def coffee_beans(message: types.Message):
    await message.answer("https://www.instagram.com/tut.bude/")


@dp.message_handler(tx(equals='Кошик'))
async def basket(message: types.Message):
    pass


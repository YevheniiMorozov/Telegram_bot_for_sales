from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import dp, types, tx, bot, telegraph
from states import FSMAdmin

from utils.db_api.db import *

from keyboards.default.admins_kb import *


ID = None


@dp.message_handler(commands=["Модератор"], is_chat_admin=True)
async def make_change(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, "Домінуй, володарюй та принижуй", reply_markup=admin_keyboards)
    await message.delete()


@dp.message_handler(tx(equals="Додати лот"), state=None)
async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply("Завантаж фото", reply_markup=cancel_button)


@dp.message_handler(state="*", commands=["Відмінити"])
@dp.message_handler(tx(equals='Відмінити', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Уупс, щось зламалося, данні не збереглися =(", reply_markup=admin_keyboards)


@dp.message_handler(content_types=["photo"], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state=FSMContext):
    if message.from_user.id == ID:
        url = await telegraph.upload_from_url(await message.photo[-1].get_url())
        async with state.proxy() as data:
            data['photo'] = url

        await FSMAdmin.next()
        await message.answer("Обери категорію на клавіатурі", reply_markup=beans_or_drip_kb)


@dp.message_handler(state=FSMAdmin.category)
async def load_category(message: types.Message, state=FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['category'] = message.text

        await FSMAdmin.next()
        await message.answer("Напиши назву", reply_markup=cancel_button)


@dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state=FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text

        await FSMAdmin.next()
        await message.answer('Опиши лот')


@dp.message_handler(state=FSMAdmin.description)
async def load_description(message: types.Message, state=FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text

        await FSMAdmin.next()
        await message.answer('Ціна цього лоту')


@dp.message_handler(state=FSMAdmin.price)
async def load_price(message: types.Message, state=FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = float(message.text)

        await sql_add_command(state)
        await message.answer(f"Товар збережений у категорії {data['category']}")

        await state.finish()
    await message.answer("Що далі?", reply_markup=admin_keyboards)


@dp.callback_query_handler(lambda x: x.data.startswith("del "))
async def del_callback_run(callback: types.CallbackQuery):
    await sql_del_command(callback.data.replace("del ", ''))
    await callback.answer(text=f'{callback.data.replace("del ", "")} видалена', show_alert=True)


@dp.message_handler(tx(equals="Видалити лот"))
async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        items = await sql_read_admin()
        for item in items:
            await bot.send_photo(message.from_user.id, item[0], f'{item[2]}\n{item[3]}\n{item[4]}')
            await bot.send_message(message.from_user.id, text="Обери це", reply_markup=InlineKeyboardMarkup().\
                                   add(InlineKeyboardButton("Видалити", callback_data=f'del {item[2]}')))

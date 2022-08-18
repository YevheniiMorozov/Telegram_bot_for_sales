from io import BytesIO

from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


from loader import dp, types, tx, bot, telegraph
from states import FSMAdmin, Mailing
from utils.db_api import database
from utils.db_api.database import Item, User

from keyboards.default.admins_kb import *


from asyncio import sleep

db = database.DBCommands()



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


async def photo_link_aiograph(photo: types.photo_size.PhotoSize) -> str:
    with await photo.download(BytesIO()) as file:
        links = await telegraph.upload(file)
    return links[0]


@dp.message_handler(content_types=["photo"], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state=FSMContext):
    if message.from_user.id == ID:
        photo = message.photo[-1]
        link = await photo_link_aiograph(photo)
        async with state.proxy() as data:
            data['img'] = link
        await FSMAdmin.next()
        await message.answer("Обери категорію на клавіатурі", reply_markup=beans_or_drip_kb)


@dp.message_handler(state=FSMAdmin.category)
async def load_category(message: types.Message, state=FSMContext):
    if message.from_user.id == ID:
        category = message.text
        async with state.proxy() as data:
            data['category'] = category
        await FSMAdmin.next()
        await message.answer("Напиши назву", reply_markup=cancel_button)


@dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state=FSMContext):
    if message.from_user.id == ID:
        name = message.text
        async with state.proxy() as data:
            data['name'] = name
        await FSMAdmin.next()
        await message.answer('Опиши лот')


@dp.message_handler(state=FSMAdmin.description)
async def load_description(message: types.Message, state=FSMContext):
    if message.from_user.id == ID:
        description = message.text
        async with state.proxy() as data:
            data['description'] = description
        await FSMAdmin.next()
        await message.answer('Ціна цього лоту')


@dp.message_handler(state=FSMAdmin.price)
async def load_price(message: types.Message, state=FSMContext):
    if message.from_user.id == ID:
        try:
            price = float(message.text)
        except ValueError:
            await message.answer("Ціна має містити у собі лише цифри")
            return
        item = Item()
        async with state.proxy() as data:
            data['price'] = price
            item.img = data["img"]
            item.category = data["category"]
            item.name = data["name"]
            item.description = data["description"]
            item.price = data["price"]

        await item.create()
        await message.answer(f"Товар збережений")
        await state.reset_state()
    await message.answer("Що далі?", reply_markup=admin_keyboards)


@dp.callback_query_handler(lambda x: x.data.startswith("del "))
async def del_callback_run(callback: types.CallbackQuery):
    name = callback.data.replace("del ", '')
    await db.delete_items(name=callback.data.replace("del ", ''))
    await callback.answer(text=f'{name} видалена', show_alert=True)


@dp.message_handler(tx(equals="Видалити лот"))
async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        await message.answer("Обери категорію на клавіатурі", reply_markup=beans_or_drip_kb)


@dp.message_handler(tx(startswith="Кава в" or "Посуд"))
async def delete_from_category(message: types.Message):
    if message.from_user.id == ID:
        category = message.text
        items = await db.show_items(category=category)
        for item in items:
            await bot.send_photo(message.from_user.id, item.img, f'{item.name}\n{item.description}\n{item.price}')
            await bot.send_message(message.from_user.id, text="Обери це", reply_markup=InlineKeyboardMarkup(). \
                                   add(InlineKeyboardButton("Видалити", callback_data=f'del {item.name}')))
        await message.answer("Видали або обери на клавіатурі інше", reply_markup=admin_keyboards)


@dp.message_handler(tx(equals="Розповісти всім"))
async def mailing(message: types.Message):
    if message.from_user.id == ID:
        await message.answer("Напиши, про що ти хочеш повідомити користувачів бота")
        await Mailing.Text.set()


@dp.message_handler(state=Mailing.Text)
async def enter_text(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        text = message.text
        await state.update_data(text=text)
        data = await state.get_data("text")
        text = data.get("text")
        await state.reset_state()
        users = await User.query.gino.all()
        for user in users:
            try:
                await bot.send_message(chat_id=user.user_id, text=text)
                await sleep(0.3)
            except Exception:
                pass
        await message.answer("Повідомлення відправлено")






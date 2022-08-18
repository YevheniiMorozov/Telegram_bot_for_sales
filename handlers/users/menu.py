from aiogram import types

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from loader import dp, tx, bot
from aiogram.dispatcher import FSMContext
from keyboards.default.default_user_kb import user_keyboards, purchase_buttons
from keyboards.inline.user_inline_kb import choice
from utils.db_api import database
from states import Application, Delivery



db = database.DBCommands()

@dp.message_handler(commands="menu")
async def start(message: types.Message):

    await message.answer("Тут натисни на одну з кнопок", reply_markup=user_keyboards)


@dp.message_handler(tx(equals='Тут магазин'))
async def coffee_beans(message: types.Message):
    await message.answer("Обери, що саме тебе цікавить", reply_markup=choice)


@dp.inline_handler(text=["Кава в дріпах", "Кава в зернах", "Кава в капсулах", "Посуд"])
async def inline_handler_drip(query: types.InlineQuery):
    text = query.query or "echo"
    button = text
    items = await db.show_items(category=button)
    articles = [
        types.InlineQueryResultArticle(
            id=item.id,
            title=f"{item.name}, ціна - {item.price} грн.",
            description=item.description,
            hide_url=True,
            thumb_url=item.img,
            input_message_content=types.InputTextMessageContent(
                message_text=f'<a href="{item.img}"> </a>\n\n{item.name}\n\n{item.description}\n\n{item.price}',
                parse_mode="HTML"),
            reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(
                "Додати у кошик", callback_data=f"buy {item.id}")),
        ) for item in items
    ]
    await query.answer(articles, cache_time=1, is_personal=True)


@dp.callback_query_handler(text_startswith="buy")
async def add_to_basket(callback: CallbackQuery, state: FSMContext):
    item_id = int(callback.data.replace("buy ", ''))
    item = await database.Item.get(item_id)
    if not item:
        await bot.send_message(text="Нажаль такий товар зараз відсутній", chat_id=callback.from_user.id)
        return
    await bot.send_message(text=f"{item.name} додано у кошик. Напишіть кількість, яку бажаєте придбати", chat_id=callback.from_user.id)
    await Application.EnterQuantity.set()
    async with state.proxy() as data:
        data["name"] = item.name
        data["price"] = item.price


@dp.message_handler(regexp=r"^(\d+)$", state=Application.EnterQuantity)
async def enter_quantity(message: types.Message, state: FSMContext):
    quantity = int(message.text)
    new_buy = database.Purchase()
    async with state.proxy() as data:
        new_buy.buyer = message.from_user.id
        new_buy.item_name = data["name"]
        new_buy.quantity = quantity
        new_buy.amount = data["price"] * quantity
    await new_buy.create()
    await state.reset_state()
    await message.answer("Товар доданий до кошику")

@dp.message_handler(state=Application.EnterQuantity)
async def wrong_quantity(message: types.Message):
    await message.answer("Мабуть щось трапилось з клавіатурою... Введіть, будь-ласка, кількість цифрами")


@dp.message_handler(text='Кошик')
async def basket(message: types.Message):
    current_buyer = await db.get_buyer(user_id=message.from_user.id)
    if not current_buyer:
        await message.answer("Тут поки що нічого немає, потрібно заповнити пустоту :(")
        return
    await message.answer("У вашій корзині зараз такі товари:")
    for item in current_buyer:
        await message.answer(
            f"{item.item_name} у кількості {item.quantity} на суму {item.amount} грн.", reply_markup=InlineKeyboardMarkup().\
                             add(InlineKeyboardButton("Видалити з кошику", callback_data=f'only_buyer_del {item.item_name}')))

    await message.answer("Бажаєте перейти до сплати чи продовжити покупки?", reply_markup=purchase_buttons)


@dp.callback_query_handler(text_startswith="only_buyer_del")
async def delete_item_from_basket(callback: CallbackQuery):
    item_name = callback.data.replace("buyer_del ", '')
    await db.delete_purchase_item(user_id=callback.from_user.id, item_name=item_name)
    await callback.answer(text=f'{item_name} видалено з кошику', show_alert=True)


@dp.message_handler(text="Видалити замовлення")
async def delete_purchase(message: types.Message):
    await message.answer("Видаляю позиції з корзини...")
    await db.delete_purchase_buyer(user_id=message.from_user.id)
    await message.answer("Корзина знову пуста", reply_markup=user_keyboards)


@dp.message_handler(text="Продовжити покупки")
async def return_to_purchase(message: types.Message):
    await message.answer("Продовжуємо! Оберіть категорію на клавіатурі", reply_markup=user_keyboards)


@dp.message_handler(tx(equals='Відмінити', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Уупс, щось зламалося, данні не збереглися =(",)


@dp.message_handler(text="Оплатити")
async def purchace_agree(message: types.Message, state: FSMContext):
    full_amount = 0
    current_buyer = await db.get_buyer(user_id=message.from_user.id)
    for item in current_buyer:
        full_amount += item.amount
    await message.answer(f"Повна сума до сплати буде {full_amount} грн.")
    buyer = await db.get_user(user_id=message.from_user.id)
    await message.answer("Напишіть ваші данні для доставки")
    await Delivery.FullName.set()


# @dp.message_handler(state=Delivery.FullName)
# async def user_full_name(message: types.Message):



@dp.message_handler(tx(equals='Тут про нас'))
async def coffee_beans(message: types.Message):
    await message.answer("https://www.instagram.com/tut.bude/")


from aiogram import executor

from loader import dp, bot
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands

from utils.db_api import database


async def on_startup(dp):
    # Устанавливаем дефолтные команды
    await set_default_commands(dp)

    # Уведомляет про запуск
    await on_startup_notify(dp)

    await database.create_db()


async def on_shutdown(dispatcher):
    await bot.close()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)


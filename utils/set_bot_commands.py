from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Тут зможеш розпочати роботу бота"),
            types.BotCommand("menu", "Тут наше меню"),
        ]
    )

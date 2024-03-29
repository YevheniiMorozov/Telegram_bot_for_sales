from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.dispatcher.filters import Text
from data import config
from aiograph import Telegraph


telegraph = Telegraph()
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
# storage = MemoryStorage()
storage = RedisStorage2()
dp = Dispatcher(bot, storage=storage)
tx = Text

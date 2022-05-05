from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from config import TOKEN
from aiogram import Bot


bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

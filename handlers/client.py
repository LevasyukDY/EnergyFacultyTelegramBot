from tkinter import E
from turtle import title
from aiogram import Dispatcher, types
from create_bot import dp, bot
from keyboards import kb_client
import requests
from pprint import pprint


async def command_start(message : types.Message):
  try:
    await bot.send_message(message.from_user.id, 
      'Привет!\nПока что я почти ничего не умею, но скоро это исправится.\n\nМожешь пока написать мне: /start, /help, "привет", "пока", "сколько время?" или "который час?".', reply_markup=kb_client)
    await message.delete()
  except:
    await message.reply('Общение с ботом происходит в лс, напишите ему!')

async def get_news(message : types.Message):
  try:
    if message.text.lower() == 'новости':
      r = requests.get("http://127.0.0.1:8000/api/news")
      data = r.json()

      # Метод send_photo() ищет картинки с серверов телеграм и не находит нашу локальную БД
      # storageURL = "http://127.0.0.1:8000/storage/"
      # photoURL = ""

      i = 0
      while i < len(data):
        # photoURL = storageURL + data[i]["preview"]
        await bot.send_photo(
          chat_id=message.chat.id, 
          photo="https://www.morristourism.org/wp-content/uploads/2017/09/this-is-a-test-image.png", 
          caption=data[i]["title"]
        )
        i += 1
  except Exception as ex:
    print(ex)
    print('Ошибка получения списка новостей')


def register_handlers_client(dp : Dispatcher):
  dp.register_message_handler(command_start, commands=['start', 'help'])
  dp.register_message_handler(get_news)
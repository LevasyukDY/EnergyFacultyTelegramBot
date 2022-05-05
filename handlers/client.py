from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.input_file import InputFile
from aiogram.dispatcher.filters import Text
from aiogram import Dispatcher, types
from create_bot import bot
from keyboards import kb_client
import requests
import os
import re


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
      data.reverse()

      storageURL = "http://127.0.0.1:8000/storage/"

      i = 0
      while i < 5:
        if data[i]["preview"] is not None:
          if 'http' not in data[i]["preview"]: 
            photoURL = storageURL + data[i]["preview"]
            p = requests.get(photoURL)
            newsId = data[i]["id"]
            out = open(f"{newsId}.jpg", "wb")
            out.write(p.content)
            out.close()
            photo = InputFile(f"{newsId}.jpg")
          else:
            photo = data[i]["preview"]
        else:
          photo = data[i]["images"][0]

        messageText = "<b>" + data[i]["title"] + "</b>\n\n"

        contentText = re.sub(r"<[^>]*>", " ", data[i]["content"])
        contentText = re.sub(r"&[^;]*;", " ", contentText)
        contentText = contentText.strip()
        contentText = re.sub(r" +", " ", contentText)

        messageText = messageText + contentText[:283] + "..."
        
        btn = InlineKeyboardButton("Читать", "http://192.168.1.6:8080/news/" + str(data[i]["id"]))
        ikb_postURL = InlineKeyboardMarkup()
        ikb_postURL.row(btn)

        await bot.send_photo(
          chat_id=message.chat.id, 
          photo=photo,
          caption=messageText,
          parse_mode="HTML",
          reply_markup=ikb_postURL
        )

        if data[i]["preview"] is not None:
          if 'http' not in data[i]["preview"]: 
            os.remove(f"{newsId}.jpg")

        i += 1
        
  except Exception as ex:
    print(ex)
    print('Ошибка получения списка новостей')


def register_handlers_client(dp : Dispatcher):
  dp.register_message_handler(command_start, commands=['start', 'help'])
  dp.register_message_handler(get_news, Text(equals='новости', ignore_case=True))
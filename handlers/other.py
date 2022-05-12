from aiogram import types, Dispatcher
from datetime import datetime
from create_bot import dp
import string, json


async def echo_send(message : types.Message):
  if message.text.lower() == 'привет':
    await message.answer('Привет!')

  elif message.text.lower() == 'пока':
    await message.answer('До скорого!')

  elif message.text.lower() == 'сколько время?' or message.text.lower() == 'который час?':
    await message.answer(f'Сейчас {datetime.now().strftime("%H:%M")} по Читинскому времени')

  elif { i.lower().translate(str.maketrans('','', string.punctuation)) for i in message.text.split(" ") } \
      .intersection(set(json.load(open("cenz.json")))) != set():
      # await message.reply("Маты запрещены")
      await message.delete()

    # if any(word in message.text.lower() for word in obscene_words):
    #   # await message.forward(chat_id='@energy_faculty_chat')
    #   await message.delete()

  else:
    await message.reply('Я вас не понимаю...')

def register_handlers_other(dp : Dispatcher):
  dp.register_message_handler(echo_send)
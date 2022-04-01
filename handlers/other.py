from aiogram import types, Dispatcher
from datetime import datetime
from create_bot import dp


async def echo_send(message : types.Message):
  if message.text.lower() == 'привет':
    await message.answer('Привет!')
  elif message.text.lower() == 'пока':
    await message.answer('До скорого!')
  elif message.text.lower() == 'сколько время?' or message.text.lower() == 'который час?':
    await message.answer(f'Сейчас {datetime.now().strftime("%H:%M")} по Читинскому времени')
  else:
    await message.answer('Я вас не понимаю...')

def register_handlers_other(dp : Dispatcher):
  dp.register_message_handler(echo_send)
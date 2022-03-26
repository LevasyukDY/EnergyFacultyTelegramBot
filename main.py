from config import TOKEN
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def command_start(message : types.Message):
  try:
    await bot.send_message(message.from_user.id, 
      'Привет!\nПока что я почти ничего не умею, но скоро это исправится')
    await message.delete()
  except:
    await message.reply('Общение с ботом происходит в лс, напишите ему!')


@dp.message_handler()
async def echo_send(message : types.Message):
  if message.text.lower() == 'привет':
    await message.answer('Привет!')
  else:
    await message.answer('Я вас не понимаю...')



executor.start_polling(dp, skip_updates=True)
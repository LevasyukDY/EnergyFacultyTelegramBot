from aiogram import Dispatcher, types
from create_bot import dp, bot

# @dp.message_handler(commands=['start', 'help'])
async def command_start(message : types.Message):
  try:
    await bot.send_message(message.from_user.id, 
      'Привет!\nПока что я почти ничего не умею, но скоро это исправится')
    await message.delete()
  except:
    await message.reply('Общение с ботом происходит в лс, напишите ему!')

def register_handlers_client(dp : Dispatcher):
  dp.register_message_handler(command_start, commands=['start', 'help'])
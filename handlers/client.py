from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.input_file import InputFile
from aiogram.dispatcher.filters import Text
from aiogram import Dispatcher, types
from keyboards import kb_client, kb_day
from create_bot import bot
from datetime import datetime
import requests, os, re


class FSMSchedules(StatesGroup):
  group = State()
  day = State()

class FSMTeachers(StatesGroup):
  search = State()


async def command_start(message : types.Message):
  try:
    await bot.send_message(message.from_user.id, 
      'Привет!\nПока что я почти ничего не умею, но скоро это исправится.\n\nМожешь пока написать мне: /start, /help, "привет", "пока", "сколько время?" или "который час?".', reply_markup=kb_client)
    await message.delete()
  except:
    await message.reply('Общение с ботом происходит в лс, напишите ему!')


async def get_news(message : types.Message):
  r = requests.get("http://127.0.0.1:8000/api/news")
  data = r.json()
  data.reverse()

  storageURL = "http://127.0.0.1:8000/storage/"

  i = 0
  while i < 4:
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
    
    btn = InlineKeyboardButton("Читать", "http://172.20.10.3:8080/news/" + str(data[i]["id"]))
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


async def get_schedules(message : types.Message):
  await FSMSchedules.group.set()
  await message.answer('Напишите свою группу')


async def get_teachers(message : types.Message):
  await FSMTeachers.search.set()
  await message.answer('Введите хотя бы часть ФИО')


async def cancel_schedules(message : types.Message, state: FSMContext):
  current_state = await state.get_state()
  if current_state is None:
    return
  await state.finish()
  await message.answer('ОК', reply_markup=kb_client)


async def input_group(message: types.Message, state: FSMContext):
  temp = ''
  async with state.proxy() as data:
    r = requests.get("http://127.0.0.1:8000/api/schedules")
    api = r.json()
    for i in range(len(api)):
      if message.text == api[i]["lesson"]["group"]:
        temp = api[i]["lesson"]["group"]
  if temp == '':
    await message.answer('Такой группы нет', reply_markup=kb_client)
    await state.finish()
  else:
    async with state.proxy() as data:
      data['group'] = message.text
    await message.answer('Введите день', reply_markup=kb_day)
    await FSMSchedules.next()


async def input_day(message: types.Message, state: FSMContext):
  if (message.text.lower() == 'эта неделя'):
    async with state.proxy() as data:
      r = requests.get("http://127.0.0.1:8000/api/schedules")
      api = r.json()
      my_reply = ''
      for i in range(len(api)):
        if str(data["group"]) == api[i]["lesson"]["group"]:
          my_reply = my_reply + '*' + api[i]["day"] + ' ' + api[i]["class_time"]["start_time"][:5] + ' ' + api[i]["week_type"] + '*\n' + api[i]["lesson"]["discipline"] + ' (' + api[i]["class_type"] + ')' + '\n\n'
      if my_reply == '': 
        await message.answer('Пар на этой неделе нет', reply_markup=kb_client)
      else:
        await message.answer(my_reply, reply_markup=kb_client, parse_mode='Markdown')
  elif (message.text.lower() == 'сегодня'):
    async with state.proxy() as data:
      input_weekday = datetime.today().weekday()
      if str(input_weekday) == '0': data['day'] = 'ПН'
      if str(input_weekday) == '1': data['day'] = 'ВТ'
      if str(input_weekday) == '2': data['day'] = 'СР'
      if str(input_weekday) == '3': data['day'] = 'ЧТ'
      if str(input_weekday) == '4': data['day'] = 'ПТ'
      if str(input_weekday) == '5': data['day'] = 'СБ'
      if str(input_weekday) == '6': data['day'] = 'ВС'
    async with state.proxy() as data:
      r = requests.get("http://127.0.0.1:8000/api/schedules")
      api = r.json()
      my_reply = ''
      for i in range(len(api)):
        if str(data["group"]) == api[i]["lesson"]["group"]:
          if str(data["day"]) == api[i]["day"]:
            if str(data["group"]) == api[i]["lesson"]["group"]:
              my_reply = my_reply + '*' + api[i]["day"] + ' ' + api[i]["class_time"]["start_time"][:5] + ' ' + api[i]["week_type"] + '*\n' + api[i]["lesson"]["discipline"] + ' (' + api[i]["class_type"] + ')' + '\n\n'
    if my_reply == '': 
      await message.answer(f'Пар на {data["day"]} не запланировано', reply_markup=kb_client)
    else:
      await message.answer(my_reply, reply_markup=kb_client, parse_mode='Markdown')
  elif (message.text.lower() == 'завтра'):
    async with state.proxy() as data:
      input_weekday = datetime.today().weekday()
      if str(input_weekday) == '0': data['day'] = 'ВТ'
      if str(input_weekday) == '1': data['day'] = 'СР'
      if str(input_weekday) == '2': data['day'] = 'ЧТ'
      if str(input_weekday) == '3': data['day'] = 'ПТ'
      if str(input_weekday) == '4': data['day'] = 'СБ'
      if str(input_weekday) == '5': data['day'] = 'ВС'
      if str(input_weekday) == '6': data['day'] = 'ПН'
    async with state.proxy() as data:
      r = requests.get("http://127.0.0.1:8000/api/schedules")
      api = r.json()
      my_reply = ''
      for i in range(len(api)):
        if str(data["group"]) == api[i]["lesson"]["group"]:
          if str(data["day"]) == api[i]["day"]:
            if str(data["group"]) == api[i]["lesson"]["group"]:
              my_reply = my_reply + '*' + api[i]["day"] + ' ' + api[i]["class_time"]["start_time"][:5] + ' ' + api[i]["week_type"] + '*\n' + api[i]["lesson"]["discipline"] + ' (' + api[i]["class_type"] + ')' + '\n\n'
      if my_reply == '': 
        await message.answer(f'Пар на {data["day"]} не запланировано', reply_markup=kb_client)
      else:
        await message.answer(my_reply, reply_markup=kb_client, parse_mode='Markdown')
  else:
    await message.answer('Некоректные входные данные', reply_markup=kb_client)
  await state.finish()


async def input_full_name(message: types.Message, state: FSMContext):
  r = requests.get("http://127.0.0.1:8000/api/teachers?full_name=" + message.text)
  api = r.json()
  my_reply = ''
  for i in range(len(api)):
    my_reply = my_reply + '*' + api[i]["surname"] + ' ' + api[i]["name"] + ' ' + api[i]["patronymic"] + '*\n' + api[i]["post"] + ' ' + api[i]["chair"]["title"] + '\nТелефон: ' + api[i]["work_phone"] + '\nСсылка: ' + api[i]["link"] + '\n\n'
  await message.answer(my_reply, reply_markup=kb_client, parse_mode='Markdown', disable_web_page_preview=True)
  await state.finish()


def register_handlers_client(dp : Dispatcher):
  dp.register_message_handler(command_start, commands=['start', 'help'])
  dp.register_message_handler(get_news, Text(equals='новости', ignore_case=True))
  dp.register_message_handler(get_schedules, Text(equals='расписание', ignore_case=True), state=None)
  dp.register_message_handler(get_teachers, Text(equals='персоналии', ignore_case=True), state=None)
  dp.register_message_handler(cancel_schedules, state="*", commands='отмена')
  dp.register_message_handler(cancel_schedules, Text(equals='отмена', ignore_case=True), state="*")
  dp.register_message_handler(input_group, state=FSMSchedules.group)
  dp.register_message_handler(input_day, state=FSMSchedules.day)
  dp.register_message_handler(input_full_name, state=FSMTeachers.search)
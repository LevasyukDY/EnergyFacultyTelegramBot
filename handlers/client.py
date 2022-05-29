from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.input_file import InputFile
from aiogram.dispatcher.filters import Text
from aiogram import Dispatcher, types
from keyboards import kb_client, kb_day, kb_cancel, kb_schedules
from create_bot import bot, dp
from datetime import datetime
from config import SERVER_URL, WEBSITE_URL
import requests, os, re


class FSMSchedules(StatesGroup):
  search_type = State()
  teacher = State()
  group = State()
  day = State()

class FSMTeachers(StatesGroup):
  search = State()


def get_schedules_reply(api, i):
  return '*' + api[i]["day"] + ' ' + api[i]["class_time"]["start_time"][:5] + '*' + ' – _' + str(api[i]["classroom"]["corps"]) + '-' + str(api[i]["classroom"]["cabinet"]) + '_' + '\n' + api[i]["lesson"]["discipline"] + ' (' + api[i]["class_type"] + ')' + '\n' + api[i]["lesson"]["teacher"]["surname"] + ' ' + api[i]["lesson"]["teacher"]["name"] + ' ' + api[i]["lesson"]["teacher"]["patronymic"] + '\n\n'


async def command_start(message : types.Message):
  if message.chat.type == 'private':
    users = []
    with open("users.txt", "r") as n:
      for line in n:
        users.append(line.strip('\n'))
    thisUser = message.from_user.username + ':' + str(message.from_user.id)
    if thisUser not in users:
      with open('users.txt', 'a') as file:
        file.write(thisUser + '\n')
    await bot.send_message(message.from_user.id, 
      'Привет!\nПока что я почти ничего не умею, но скоро это исправится.\n\nМожешь пока написать мне: /start, /help, "привет", "пока", "сколько время?" или "который час?".', reply_markup=kb_client)
    await message.delete()


async def get_news(message : types.Message):
  if message.chat.type == 'private':
    try:
      r = requests.get(SERVER_URL + "api/news?per_page=1&page=1")
      data = r.json()
      data["data"].reverse()

      storageURL = SERVER_URL + "storage/"

      i = 0
      while i < len(data["data"]):
        if data["data"][i]["preview"] is not None:
          if 'http' not in data["data"][i]["preview"]: 
            photoURL = storageURL + data["data"][i]["preview"]
            p = requests.get(photoURL)
            newsId = data["data"][i]["id"]
            out = open(f"{newsId}.jpg", "wb")
            out.write(p.content)
            out.close()
            photo = InputFile(f"{newsId}.jpg")
          else:
            photo = data["data"][i]["preview"]
        else:
          photo = data["data"][i]["images"][0]

        messageText = "<b>" + data["data"][i]["title"] + "</b>\n\n"
        contentText = re.sub(r"<[^>]*>", " ", data["data"][i]["content"])
        contentText = re.sub(r"&[^;]*;", " ", contentText)
        contentText = contentText.strip()
        contentText = re.sub(r" +", " ", contentText)
        messageText = messageText + contentText[:283] + "..."
        
        btn = InlineKeyboardButton("Читать", WEBSITE_URL + "news/" + str(data["data"][i]["id"]))
        prev_page = InlineKeyboardButton("◀️", callback_data="prevPage:" + str(data["links"]["prev"]))
        current_page = InlineKeyboardButton(str(data["meta"]["current_page"]) + '/' + str(data["meta"]["total"]), callback_data="currentPage:" + str(data["meta"]["current_page"]) + ':' + str(data["meta"]["total"]))
        next_page = InlineKeyboardButton("▶️", callback_data="nextPage:" + str(data["links"]["next"]))
        ikb_postURL = InlineKeyboardMarkup()
        ikb_postURL.row(btn).row(prev_page, current_page, next_page)

        await bot.send_photo(
          chat_id=message.chat.id, 
          photo=photo,
          caption=messageText,
          parse_mode="HTML",
          reply_markup=ikb_postURL
        )

        if data["data"][i]["preview"] is not None:
          if 'http' not in data["data"][i]["preview"]: 
            os.remove(f"{newsId}.jpg")
        i += 1
    except Exception as ex:
      print(ex)


@dp.callback_query_handler(text_contains="currentPage")
async def current_page(callback : types.CallbackQuery):
  try:
    # current_post = callback.get_current().message.reply_markup.inline_keyboard[0][0].url.split("/")[-1]
    # r = requests.get(SERVER_URL + "api/news?page=1&per_page=1")
    # data = r.json()
    await callback.answer('Пост ' + callback.data.split(':')[1] + ' из ' + callback.data.split(':')[2])
  except Exception as ex:
    print(ex)


@dp.callback_query_handler(text_contains="prevPage")
async def prev_page(callback : types.CallbackQuery):
  try:
    page_id = callback.data.split(':')[1]
    # post_id = callback.get_current().message.reply_markup.inline_keyboard[0][0].url.split("/")[-1]
    
    if page_id == 'None':
      await callback.answer("Свежих новостей больше нет", show_alert=True)
    else:
      await callback.answer("Предыдущая новость")
      r = requests.get(SERVER_URL + "api/news?page=" + page_id.split('=')[1] + "&per_page=1")
      data = r.json()
      data["data"].reverse()
      # r = requests.get(SERVER_URL + "api/news" + data["links"]["prev"] + "&per_page=1")
      # data = r.json()

      storageURL = SERVER_URL + "storage/"

      i = 0
      while i < len(data["data"]):
        if data["data"][i]["preview"] is not None:
          if 'http' not in data["data"][i]["preview"]: 
            photoURL = storageURL + data["data"][i]["preview"]
            p = requests.get(photoURL)
            newsId = data["data"][i]["id"]
            out = open(f"{newsId}.jpg", "wb")
            out.write(p.content)
            out.close()
            photo = InputFile(f"{newsId}.jpg")
          else:
            photo = data["data"][i]["preview"]
        else:
          photo = data["data"][i]["images"][0]

        messageText = "<b>" + data["data"][i]["title"] + "</b>\n\n"
        contentText = re.sub(r"<[^>]*>", " ", data["data"][i]["content"])
        contentText = re.sub(r"&[^;]*;", " ", contentText)
        contentText = contentText.strip()
        contentText = re.sub(r" +", " ", contentText)
        messageText = messageText + contentText[:283] + "..."
        
        btn = InlineKeyboardButton("Читать", WEBSITE_URL + "news/" + str(data["data"][i]["id"]))
        prev_page = InlineKeyboardButton("◀️", callback_data="prevPage:" + str(data["links"]["prev"]))
        current_page = InlineKeyboardButton(str(data["meta"]["current_page"]) + '/' + str(data["meta"]["total"]), callback_data="currentPage:" + str(data["meta"]["current_page"]) + ':' + str(data["meta"]["total"]))
        next_page = InlineKeyboardButton("▶️", callback_data="nextPage:" + str(data["links"]["next"]))
        ikb_postURL = InlineKeyboardMarkup()
        ikb_postURL.row(btn).row(prev_page, current_page, next_page)

        await callback.message.delete()
        await bot.send_photo(
          chat_id=callback.get_current().message.chat.id, 
          photo=photo,
          caption=messageText,
          parse_mode="HTML",
          reply_markup=ikb_postURL
        )

        if data["data"][i]["preview"] is not None:
          if 'http' not in data["data"][i]["preview"]: 
            os.remove(f"{newsId}.jpg")
        i += 1
  except Exception as ex:
    print(ex)


@dp.callback_query_handler(text_contains="nextPage")
async def next_page(callback : types.CallbackQuery):
  try:
    page_id = callback.data.split(':')[1]
    # post_id = callback.get_current().message.reply_markup.inline_keyboard[0][0].url.split("/")[-1]
    if page_id == 'None':
      await callback.answer("Новостей больше нет", show_alert=True)
    else:
      await callback.answer("Следующая новость")
      r = requests.get(SERVER_URL + "api/news?page=" + page_id.split('=')[1] + "&per_page=1")
      data = r.json()
      # r = requests.get(SERVER_URL + "api/news" + data["links"]["next"] + "&per_page=1")
      # data = r.json()
      data["data"].reverse()

      storageURL = SERVER_URL + "storage/"

      i = 0
      while i < len(data["data"]):
        if data["data"][i]["preview"] is not None:
          if 'http' not in data["data"][i]["preview"]: 
            photoURL = storageURL + data["data"][i]["preview"]
            p = requests.get(photoURL)
            newsId = data["data"][i]["id"]
            out = open(f"{newsId}.jpg", "wb")
            out.write(p.content)
            out.close()
            photo = InputFile(f"{newsId}.jpg")
          else:
            photo = data["data"][i]["preview"]
        else:
          photo = data["data"][i]["images"][0]

        messageText = "<b>" + data["data"][i]["title"] + "</b>\n\n"
        contentText = re.sub(r"<[^>]*>", " ", data["data"][i]["content"])
        contentText = re.sub(r"&[^;]*;", " ", contentText)
        contentText = contentText.strip()
        contentText = re.sub(r" +", " ", contentText)
        messageText = messageText + contentText[:283] + "..."
        
        btn = InlineKeyboardButton("Читать", WEBSITE_URL + "news/" + str(data["data"][i]["id"]))
        prev_page = InlineKeyboardButton("◀️", callback_data="prevPage:" + str(data["links"]["prev"]))
        current_page = InlineKeyboardButton(str(data["meta"]["current_page"]) + '/' + str(data["meta"]["total"]), callback_data="currentPage:" + str(data["meta"]["current_page"]) + ':' + str(data["meta"]["total"]))
        next_page = InlineKeyboardButton("▶️", callback_data="nextPage:" + str(data["links"]["next"]))
        ikb_postURL = InlineKeyboardMarkup()
        ikb_postURL.row(btn).row(prev_page, current_page, next_page)

        await callback.message.delete()
        await bot.send_photo(
          chat_id=callback.get_current().message.chat.id, 
          photo=photo,
          caption=messageText,
          parse_mode="HTML",
          reply_markup=ikb_postURL
        )

        if data["data"][i]["preview"] is not None:
          if 'http' not in data["data"][i]["preview"]: 
            os.remove(f"{newsId}.jpg")
        i += 1
  except Exception as ex:
    print(ex)


async def get_schedules(message : types.Message):
  if message.chat.type == 'private':
    await FSMSchedules.search_type.set()
    await message.answer('Выберите тип поиска', reply_markup=kb_schedules)


async def get_teachers(message : types.Message):
  if message.chat.type == 'private':
    await FSMTeachers.search.set()
    await message.answer('Введите хотя бы часть ФИО для поиска', reply_markup=kb_cancel)


async def cancel_state(message: types.Message, state: FSMContext):
  if message.chat.type == 'private':
    current_state = await state.get_state()
    if current_state is None:
      return
    await state.finish()
    await message.answer('ОК', reply_markup=kb_client)


async def input_search(message: types.Message, state: FSMContext):
  if message.chat.type == 'private':
    if message.text.lower() == 'по преподавателю':
      async with state.proxy() as data:
        data['search_type'] = message.text
      await message.answer('Введите фамилию преподавателя', reply_markup=kb_cancel)
      await FSMSchedules.teacher.set()
    elif message.text.lower() == 'по группе':
      async with state.proxy() as data:
        data['search_type'] = message.text
      await message.answer('Введите группу', reply_markup=kb_cancel)
      await FSMSchedules.group.set()
    else:
      await message.answer('Я вас не понимаю...', reply_markup=kb_client)
      await state.finish()


async def input_teacher(message: types.Message, state: FSMContext):
  if message.chat.type == 'private':
    r = requests.get(SERVER_URL + "api/schedules?teacher=" + message.text)
    api = r.json()
    if api == []:
      await message.answer('Не удалось найти такого преподавателя, попробуйте ещё раз', reply_markup=kb_cancel)
      await FSMSchedules.teacher.set()
    else:
      async with state.proxy() as data:
        data['teacher'] = message.text
      await message.answer('Введите день', reply_markup=kb_day)
      await FSMSchedules.day.set()


async def input_group(message: types.Message, state: FSMContext):
  if message.chat.type == 'private':
    temp = ''
    async with state.proxy() as data:
      r = requests.get(SERVER_URL + "api/schedules")
      api = r.json()
      for i in range(len(api)):
        if message.text.lower() == str(api[i]["lesson"]["group"]).lower():
          temp = api[i]["lesson"]["group"]
    if temp == '':
      await message.answer('Такой группы нет, попробуйте ещё раз', reply_markup=kb_cancel)
      await FSMSchedules.group.set()
    else:
      async with state.proxy() as data:
        data['group'] = temp
      await message.answer('Введите день', reply_markup=kb_day)
      await FSMSchedules.next()


async def input_day(message: types.Message, state: FSMContext):
  if message.chat.type == 'private':
    if int(datetime.now().strftime("%W")) % 2 == 1:
      week = "Верхняя"
    else:
      week = "Нижняя"

    if (message.text.lower() == 'эта неделя'):
      async with state.proxy() as data:
        try:
          r = requests.get(SERVER_URL + "api/schedules?teacher=" + data["teacher"])
        except:
          r = requests.get(SERVER_URL + "api/schedules")
        api = r.json()
        my_reply = '*Сейчас ' + week + ' неделя:*\n\n'
        for i in range(len(api)):
          if week == api[i]["week_type"]:
            try:
              if str(data["group"]) == api[i]["lesson"]["group"]:
                my_reply = my_reply + get_schedules_reply(api, i)
            except:
              my_reply = my_reply + get_schedules_reply(api, i)
        if my_reply == '*Сейчас ' + week + ' неделя:*\n\n': 
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
        try:
          r = requests.get(SERVER_URL + "api/schedules?teacher=" + data["teacher"])
        except:
          r = requests.get(SERVER_URL + "api/schedules")
        api = r.json()
        my_reply = '*Сейчас ' + week + ' неделя:*\n\n'
        for i in range(len(api)):
          if week == api[i]["week_type"]:
            if str(data["day"]) == api[i]["day"]:
              try:
                if str(data["group"]) == api[i]["lesson"]["group"]:
                  my_reply = my_reply + get_schedules_reply(api, i)
              except:
                my_reply = my_reply + get_schedules_reply(api, i)
      if my_reply == '*Сейчас ' + week + ' неделя:*\n\n': 
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
        if str(input_weekday) == '6': 
          data['day'] = 'ПН'
          if week == "Верхняя":
            week = "Нижняя"
          else:
            week = "Верхняя"
      async with state.proxy() as data:
        try:
          r = requests.get(SERVER_URL + "api/schedules?teacher=" + data["teacher"])
        except:
          r = requests.get(SERVER_URL + "api/schedules")
        api = r.json()
        my_reply = '*Это будет ' + week + ' неделя:*\n\n'
        for i in range(len(api)):
          if week == api[i]["week_type"]:
            if str(data["day"]) == api[i]["day"]:
              try:
                if str(data["group"]) == api[i]["lesson"]["group"]:
                  my_reply = my_reply + get_schedules_reply(api, i)
              except:
                my_reply = my_reply + get_schedules_reply(api, i)
        if my_reply == '*Это будет ' + week + ' неделя:*\n\n': 
          await message.answer(f'Пар на {data["day"]} не запланировано', reply_markup=kb_client)
        else:
          await message.answer(my_reply, reply_markup=kb_client, parse_mode='Markdown')

    elif (message.text.lower() == 'следующая неделя'):
      if int(datetime.now().strftime("%W")) % 2 == 1:
        next_week = "Нижняя"
      else:
        next_week = "Верхняя"
      async with state.proxy() as data:
        try:
          r = requests.get(SERVER_URL + "api/schedules?teacher=" + data["teacher"])
        except:
          r = requests.get(SERVER_URL + "api/schedules")
        api = r.json()
        my_reply = '*Будет ' + next_week + ' неделя:*\n\n'
        for i in range(len(api)):
          if next_week == api[i]["week_type"]:
            try:
              if str(data["group"]) == api[i]["lesson"]["group"]:
                my_reply = my_reply + get_schedules_reply(api, i)
            except:
              my_reply = my_reply + get_schedules_reply(api, i)
        if my_reply == '*Будет ' + next_week + ' неделя:*\n\n': 
          await message.answer('Пар на следующей неделе нет', reply_markup=kb_client)
        else:
          await message.answer(my_reply, reply_markup=kb_client, parse_mode='Markdown')

    else:
      await message.answer('Некоректные входные данные', reply_markup=kb_client)
    await state.finish()


async def input_full_name(message: types.Message, state: FSMContext):
  if message.chat.type == 'private':
    try:
      r = requests.get(SERVER_URL + "api/teachers?full_name=" + message.text)
      api = r.json()
      my_reply = ''
      for i in range(len(api)):
        my_reply = my_reply + '*' + api[i]["surname"] + ' ' + api[i]["name"] + ' ' + api[i]["patronymic"] + '*\n' + api[i]["post"] + ' ' + api[i]["chair"]["title"] + ' каб. ' + api[i]["chair"]["cabinet"] + '\nТелефон: ' + api[i]["work_phone"] + '\nСсылка: ' + api[i]["link"] + '\n\n'
      await message.answer(my_reply, reply_markup=kb_client, parse_mode='Markdown', disable_web_page_preview=True)
      await state.finish()
    except:
      await message.answer('Не найдено преподавателей с таким ФИО, попробуйте ещё раз', reply_markup=kb_cancel)
      await FSMTeachers.search.set()
      


def register_handlers_client(dp : Dispatcher):
  dp.register_message_handler(command_start, commands=['start', 'help'])
  dp.register_message_handler(get_news, Text(equals='новости', ignore_case=True))
  dp.register_message_handler(get_schedules, Text(equals='расписание', ignore_case=True), state=None)
  dp.register_message_handler(get_teachers, Text(equals='персоналии', ignore_case=True), state=None)
  dp.register_message_handler(cancel_state, state="*", commands='отмена')
  dp.register_message_handler(cancel_state, Text(equals='отмена', ignore_case=True), state="*")
  dp.register_message_handler(input_search, state=FSMSchedules.search_type)
  dp.register_message_handler(input_teacher, state=FSMSchedules.teacher)
  dp.register_message_handler(input_group, state=FSMSchedules.group)
  dp.register_message_handler(input_day, state=FSMSchedules.day)
  dp.register_message_handler(input_full_name, state=FSMTeachers.search)
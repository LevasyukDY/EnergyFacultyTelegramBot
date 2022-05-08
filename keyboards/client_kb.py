from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('Новости')
b3 = KeyboardButton('Персоналии')
b2 = KeyboardButton('Расписание')

day1 = KeyboardButton('Сегодня')
day2 = KeyboardButton('Завтра')
day3 = KeyboardButton('Эта неделя')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.row(b1, b2, b3)

kb_day = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_day.row(day1, day2, day3)

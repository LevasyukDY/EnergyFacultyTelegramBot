from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('Новости')
b3 = KeyboardButton('Персоналии')
b2 = KeyboardButton('Расписание')
kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.row(b1, b2, b3)

cancel = KeyboardButton('Отмена')
kb_cancel = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_cancel.row(cancel)

day1 = KeyboardButton('Эта неделя')
day2 = KeyboardButton('Сегодня')
day3 = KeyboardButton('Завтра')
day4 = KeyboardButton('Следующая неделя')
kb_day = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_day.row(day1, day2, day3).row(day4)

search_btn1 = KeyboardButton('По преподавателю')
search_btn2 = KeyboardButton('По группе')
kb_schedules = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_schedules.row(search_btn1, search_btn2).row(cancel)
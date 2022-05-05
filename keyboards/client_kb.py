from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('Новости')
b3 = KeyboardButton('Персоналии')
b2 = KeyboardButton('Расписание')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.row(b1, b2, b3)

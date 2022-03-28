from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('Персоналии')
b2 = KeyboardButton('Расписание')

kb_client = ReplyKeyboardMarkup()

kb_client.row(b1, b2)
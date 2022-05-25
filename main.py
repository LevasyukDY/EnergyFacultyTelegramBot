import asyncio
from aiogram.utils import executor
from handlers import client, other
from create_bot import dp, bot
from aiogram.types.input_file import InputFile
from config import SERVER_URL
import logging
import requests
import os, re


async def autosend_group_news():
  while True:
    try:
      print('[INFO]: Проверяю новые новости групп для рассылки')
      r = requests.get(SERVER_URL + "api/group-news")
      data = r.json()
      data["data"].reverse()
      group_news = []
      with open("group_news.txt", "r") as f:
        for line in f:
          group_news.append(line.strip('\n'))
      users = []
      with open("users.txt", "r") as f:
        for line in f:
          users.append(line.strip('\n'))

      i = 0
      j = 0
      h = 0
      while i < len(data["data"]):
        if str(data["data"][i]["id"]) not in group_news:
          with open('group_news.txt', 'a') as f:
            f.write(str(data["data"][i]["id"]) + '\n')
          while j < len(data["data"][i]["students_tg_usernames"]):
            student_username_from_api = data["data"][i]["students_tg_usernames"][j][1:]
            while h < len(users):
              if student_username_from_api == users[h].split(':')[0]:
                chat_id = users[h].split(':')[1]
                contentText = re.sub(r"<[^>]*>", " ", data["data"][i]["content"])
                contentText = re.sub(r"&[^;]*;", " ", contentText)
                contentText = contentText.strip()
                contentText = re.sub(r" +", " ", contentText)
                message_text = '<b>Новая запись в группе\nот ' + data["data"][i]["author"] + ':</b>\n' + contentText
                await bot.send_message(chat_id=chat_id, text=message_text, parse_mode='HTML')
              h += 1
            j += 1
        i += 1

      await asyncio.sleep(20)
    except Exception as e:
      print(e)


async def autoposting():
  storageURL = SERVER_URL + "storage/"
  while True:
    try:
      print('[INFO]: Проверяю новые новости для автопостинга')
      r = requests.get(SERVER_URL + "api/news")
      data = r.json()
      data["data"].reverse()
      news = []
      with open("news.txt", "r") as n:
        for line in n:
          news.append(line.strip('\n'))

      i = 0
      while i < len(data["data"]):
        if str(data["data"][i]["id"]) not in news:
          with open('news.txt', 'a') as news_file:
            news_file.write(str(data["data"][i]["id"]) + '\n')
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

          await bot.send_photo(
            chat_id="-1001680026356", 
            photo=photo,
            caption=messageText,
            parse_mode="HTML",
          )

          if data["data"][i]["preview"] is not None:
            if 'http' not in data["data"][i]["preview"]: 
              os.remove(f"{newsId}.jpg")
        i += 1
      await asyncio.sleep(5)
    except Exception as e:
      print(e)



async def on_sturtup(_):
  print('\n\n\n<---------- БОТ ВЫШЕЛ В ОНЛАЙН ---------->\n')
  asyncio.create_task(autoposting())
  asyncio.create_task(autosend_group_news())

logging.basicConfig(level=logging.INFO)

client.register_handlers_client(dp)
other.register_handlers_other(dp)


def main():
  while True:
    try:
      executor.start_polling(dp, skip_updates=True, on_startup=on_sturtup)
      break
    except Exception as e:
      print(e)


if __name__ == '__main__':
  main()

import asyncio
from aiogram.utils import executor
from handlers import client, other
from create_bot import dp, bot
from aiogram.types.input_file import InputFile
import logging
import requests
import os, re


async def autoposting():
  storageURL = "http://127.0.0.1:8000/storage/"
  while True:
    try:
      print('[INFO]: Проверяю новые новости для автопостинга')
      r = requests.get("http://127.0.0.1:8000/api/news")
      data = r.json()
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

from aiogram.utils import executor
from handlers import client, other
from create_bot import dp
import logging


async def on_sturtup(_):
  print('\n\n\n<---------- БОТ ВЫШЕЛ В ОНЛАЙН ---------->\n')

logging.basicConfig(level=logging.INFO)

client.register_handlers_client(dp)
other.register_handlers_other(dp)


def main():
  executor.start_polling(dp, skip_updates=True, on_startup=on_sturtup)


if __name__ == '__main__':
  main()

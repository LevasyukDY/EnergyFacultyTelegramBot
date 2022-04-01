from aiogram.utils import executor
from create_bot import dp
import logging
from handlers import client, other


async def on_sturtup(_):
  print('<---------- БОТ ВЫШЕЛ В ОНЛАЙН ---------->')

logging.basicConfig(level=logging.INFO)

client.register_handlers_client(dp)
other.register_handlers_other(dp)


def main():
  executor.start_polling(dp, skip_updates=True, on_startup=on_sturtup)


if __name__ == '__main__':
  main()

import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.config.env import load_env_config


async def main() -> None:
  config = load_env_config()

  logging.basicConfig(
    level=config.log_level,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
  )

  bot = Bot(token=config.telegram_bot_token)
  dp = Dispatcher()

  logging.info("Starting bot")

  await dp.start_polling(bot)

if __name__ == "__main__":
  asyncio.run(main())
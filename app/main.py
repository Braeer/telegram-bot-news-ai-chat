import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.config.env import load_env_config
from app.utils.file_manager import ensure_project_structure


async def main() -> None:
    config = load_env_config()

    ensure_project_structure(
        main_admin_id=config.main_admin_id,
    )

    logging.basicConfig(
        level=config.log_level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    bot = Bot(token=config.telegram_bot_token)
    dp = Dispatcher()

    logging.info("Бот запущен")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

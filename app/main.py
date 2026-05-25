import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.config.container import build_container
from app.config.env import load_env_config
from app.config.router import setup_routers
from app.utils.file_manager import ensure_project_structure
from app.utils.scheduler import setup_scheduler


async def main() -> None:
    config = load_env_config()

    ensure_project_structure(
        main_admin_id=config.main_admin_id,
    )

    logging.basicConfig(
        level=config.log_level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    container = build_container()

    setup_scheduler(container.cleanup_service)

    bot = Bot(token=config.telegram_bot_token)
    dp = Dispatcher()

    setup_routers(dp, container)

    logging.info("Бот запущен")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.config.env import load_env_config
from app.handlers.start_handler import build_start_router
from app.handlers.status_handler import build_status_router
from app.middlewares.auth_middleware import AuthMiddleware
from app.services.auth_service import AuthService
from app.services.template_service import TemplateService
from app.storage.settings_storage import SettingsStorage
from app.utils.file_manager import ensure_project_structure


async def main() -> None:
    config = load_env_config()
    template_service = TemplateService()
    settings_storage = SettingsStorage()

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

    auth_service = AuthService(
        settings_storage=settings_storage,
    )

    dp.message.middleware(
        AuthMiddleware(
            auth_service=auth_service,
            template_service=template_service,
        )
    )

    dp.include_router(
        build_start_router(
            template_service=template_service,
        ),
    )
    dp.include_router(
        build_status_router(
            template_service=template_service,
        )
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

from aiogram import Dispatcher

from app.config.container import AppContainer
from app.handlers.admin_handler import build_admin_router
from app.handlers.fallback_handler import build_fallback_router
from app.handlers.start_handler import build_start_router
from app.handlers.status_handler import build_status_router
from app.middlewares.auth_middleware import AuthMiddleware


def setup_routers(dp: Dispatcher, container: AppContainer) -> None:
    dp.message.middleware(
        AuthMiddleware(
            auth_service=container.auth_service,
            template_service=container.template_service,
        )
    )

    dp.include_router(
        build_start_router(
            template_service=container.template_service,
        )
    )

    dp.include_router(
        build_status_router(
            template_service=container.template_service,
            analytics_service=container.analytics_service,
        )
    )

    dp.include_router(
        build_admin_router(
            admin_service=container.admin_service,
            template_service=container.template_service,
        )
    )

    dp.include_router(
        build_fallback_router(
            template_service=container.template_service,
        )
    )

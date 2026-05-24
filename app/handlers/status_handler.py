from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.services.analytics_service import AnalyticsService
from app.services.template_service import TemplateService


def build_status_router(
    template_service: TemplateService,
    analytics_service: AnalyticsService,
) -> Router:
    router = Router()

    @router.message(Command("status"))
    async def status_handler(message: Message, user_id: int) -> None:
        status = analytics_service.get_user_status(user_id)

        await message.answer(
            template_service.load("user/status.txt").format(
                requests=status["total_requests"],
                input_tokens=status["total_input_tokens"],
                output_tokens=status["total_output_tokens"],
                total_tokens=status["total_tokens"],
                last_request_at=status["last_request_at"] or "нет данных",
            )
        )

    return router

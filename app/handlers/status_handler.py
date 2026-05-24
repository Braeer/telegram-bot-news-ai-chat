from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.services.template_service import TemplateService


def build_status_router(template_service: TemplateService) -> Router:
    router = Router()

    @router.message(Command("status"))
    async def status_handler(message: Message, user_id: int) -> None:
        await message.answer(
            template_service.load("user/status.txt").format(
                user_id=user_id,
                requests=0,
                total_tokens=0,
            )
        )

    return router

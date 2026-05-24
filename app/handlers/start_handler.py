from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.services.template_service import TemplateService


def build_start_router(template_service: TemplateService) -> Router:
    router = Router()

    @router.message(CommandStart())
    async def start_handler(message: Message) -> None:
        await message.answer(
            template_service.load("user/start.txt"),
        )

    return router

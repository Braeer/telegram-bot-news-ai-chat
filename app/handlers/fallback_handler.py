from aiogram import F, Router
from aiogram.types import Message

from app.services.template_service import TemplateService


def build_fallback_router(
    template_service: TemplateService,
) -> Router:
    router = Router()

    @router.message(F.text.startswith("/"))
    async def unknown_command_handler(message: Message) -> None:
        await message.answer(
            template_service.load(
                "error/unknown_command.txt",
            )
        )

    return router

from aiogram import Router
from aiogram.types import Message

from app.services.template_service import TemplateService


def build_fallback_router(
    template_service: TemplateService,
) -> Router:
    router = Router()

    @router.message()
    async def fallback_handler(message: Message) -> None:
        if message.text and message.text.startswith("/"):
            await message.answer(
                template_service.load(
                    "error/unknown_command.txt",
                )
            )
            return

        await message.answer(
            template_service.load(
                "error/empty_message.txt",
            )
        )

    return router

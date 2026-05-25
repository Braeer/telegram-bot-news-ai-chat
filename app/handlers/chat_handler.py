from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from app.services.chat_service import ChatService
from app.services.template_service import TemplateService


def build_chat_router(
    chat_service: ChatService,
    template_service: TemplateService,
) -> Router:
    router = Router()

    @router.message(Command("new"))
    async def new_chat_handler(message: Message, user_id: int) -> None:
        chat_service.create_new_chat(user_id)

        await message.answer(
            template_service.load(
                "user/new_chat_success.txt",
            )
        )

    @router.message(Command("reset"))
    async def reset_chat_handler(message: Message, user_id: int) -> None:
        chat_service.reset_chat(user_id)

        await message.answer(
            template_service.load(
                "user/reset_success.txt",
            )
        )

    @router.message(F.text & ~F.text.startswith("/"))
    async def text_message_handler(message: Message, user_id: int) -> None:
        if not message.text:
            await message.answer(
                template_service.load(
                    "error/empty_message.txt",
                )
            )
            return

        answer = chat_service.continue_chat(
            user_id=user_id,
            message_text=message.text,
        )

        await message.answer(answer)

    return router

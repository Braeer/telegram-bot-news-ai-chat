from aiogram import Router
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message

from app.services.admin_service import AdminService
from app.services.template_service import TemplateService


def build_admin_router(
    admin_service: AdminService,
    template_service: TemplateService,
) -> Router:
    router = Router()

    @router.message(Command("admin-data"))
    async def admin_data_handler(message: Message, user_id: int) -> None:
        if not admin_service.is_admin(user_id):
            await message.answer(template_service.load("error/admin_only.txt"))
            return

        data = admin_service.get_admin_data()

        await message.answer(
            template_service.load("admin/admin_data.txt").format(
                users_count=data["users_count"],
                admins_count=data["admins_count"],
                total_requests=data["total_requests"],
                total_tokens=data["total_tokens"],
            )
        )

    @router.message(Command("admin-tokens"))
    async def admin_tokens_handler(message: Message, user_id: int) -> None:
        if not admin_service.is_admin(user_id):
            await message.answer(template_service.load("error/admin_only.txt"))
            return

        data = admin_service.get_tokens_info()

        await message.answer(
            template_service.load("admin/admin_tokens.txt").format(
                total_tokens=data["total_tokens"],
                input_tokens=data["input_tokens"],
                output_tokens=data["output_tokens"],
            )
        )

    @router.message(Command("add-user"))
    async def add_user_handler(message: Message, user_id: int) -> None:
        if not admin_service.is_admin(user_id):
            await message.answer(template_service.load("error/admin_only.txt"))
            return

        target_user_id = _parse_user_id(message.text)

        if target_user_id is None:
            await message.answer(template_service.load("error/invalid_user_id.txt"))
            return

        admin_service.add_user(target_user_id)

        await message.answer(
            template_service.load("admin/user_added.txt").format(
                user_id=target_user_id,
            )
        )

    @router.message(Command("add-admin"))
    async def add_admin_handler(message: Message, user_id: int) -> None:
        if not admin_service.is_admin(user_id):
            await message.answer(template_service.load("error/admin_only.txt"))
            return

        target_user_id = _parse_user_id(message.text)

        if target_user_id is None:
            await message.answer(template_service.load("error/invalid_user_id.txt"))
            return

        admin_service.add_admin(target_user_id)

        await message.answer(
            template_service.load("admin/admin_added.txt").format(
                user_id=target_user_id,
            )
        )

    return router


def _parse_user_id(text: str | None) -> int | None:
    if not text:
        return None

    parts = text.split(maxsplit=1)

    if len(parts) != 2:
        return None

    raw_user_id = parts[1].strip()

    if not raw_user_id.isdigit():
        return None

    return int(raw_user_id)

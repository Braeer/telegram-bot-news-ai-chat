from app.services.chat_service import ChatService


class CleanupService:
    def __init__(self, chat_service: ChatService) -> None:
        self.chat_service = chat_service

    def cleanup_chats(self) -> None:
        self.chat_service.cleanup_expired_messages()

class FakeChatService:
    def __init__(self) -> None:
        self.cleanup_called = False

    def cleanup_expired_messages(self) -> None:
        self.cleanup_called = True


def test_cleanup_chats_calls_chat_service():
    from app.services.cleanup_service import CleanupService

    chat_service = FakeChatService()
    service = CleanupService(chat_service=chat_service)

    service.cleanup_chats()

    assert chat_service.cleanup_called is True

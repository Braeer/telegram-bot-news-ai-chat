class AIService:
    def generate_answer(
        self,
        user_id: int,
        message_text: str,
        context: list[dict],
        config: dict,
    ) -> str:
        return f"Mock answer: {message_text}"

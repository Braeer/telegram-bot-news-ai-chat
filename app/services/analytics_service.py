from datetime import UTC, datetime

from app.storage.analytics_storage import AnalyticsStorage


class AnalyticsService:
    def __init__(self, analytics_storage: AnalyticsStorage) -> None:
        self.analytics_storage = analytics_storage

    def get_user_status(self, user_id: int) -> dict:
        return self.analytics_storage.read_user_analytics(user_id)

    def track_request(
        self,
        user_id: int,
        input_tokens: int = 0,
        output_tokens: int = 0,
    ) -> None:
        now = datetime.now(UTC).isoformat()
        total_tokens = input_tokens + output_tokens

        user_data = self.analytics_storage.read_user_analytics(user_id)
        user_data["total_requests"] += 1
        user_data["total_input_tokens"] += input_tokens
        user_data["total_output_tokens"] += output_tokens
        user_data["total_tokens"] += total_tokens
        user_data["last_request_at"] = now
        self.analytics_storage.write_user_analytics(user_id, user_data)

        global_data = self.analytics_storage.read_global_analytics()
        global_data["total_requests"] += 1
        global_data["total_input_tokens"] = global_data.get("total_input_tokens", 0) + input_tokens
        global_data["total_output_tokens"] = (
            global_data.get("total_output_tokens", 0) + output_tokens
        )
        global_data["total_tokens"] += total_tokens
        global_data["last_request_at"] = now
        self.analytics_storage.write_global_analytics(global_data)

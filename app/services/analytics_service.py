from app.storage.analytics_storage import AnalyticsStorage


class AnalyticsService:
    def __init__(self, analytics_storage: AnalyticsStorage) -> None:
        self.analytics_storage = analytics_storage

    def get_user_status(self, user_id: int) -> dict:
        return self.analytics_storage.read_user_analytics(user_id)

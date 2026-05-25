from app.services.analytics_service import AnalyticsService


class FakeAnalyticsStorage:
    def __init__(self) -> None:
        self.user_data = {}
        self.global_data = {
            "total_requests": 0,
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "total_tokens": 0,
            "last_request_at": None,
        }

    def read_user_analytics(self, user_id: int) -> dict:
        return self.user_data.get(
            user_id,
            {
                "user_id": user_id,
                "total_requests": 0,
                "total_input_tokens": 0,
                "total_output_tokens": 0,
                "total_tokens": 0,
                "last_request_at": None,
            },
        )

    def write_user_analytics(self, user_id: int, data: dict) -> None:
        self.user_data[user_id] = data

    def read_global_analytics(self) -> dict:
        return self.global_data

    def write_global_analytics(self, data: dict) -> None:
        self.global_data = data


def test_track_request_updates_user_analytics():
    storage = FakeAnalyticsStorage()
    service = AnalyticsService(analytics_storage=storage)

    service.track_request(user_id=123, input_tokens=10, output_tokens=20)

    assert storage.user_data[123]["total_requests"] == 1
    assert storage.user_data[123]["total_input_tokens"] == 10
    assert storage.user_data[123]["total_output_tokens"] == 20
    assert storage.user_data[123]["total_tokens"] == 30
    assert storage.user_data[123]["last_request_at"] is not None


def test_track_request_updates_global_analytics():
    storage = FakeAnalyticsStorage()
    service = AnalyticsService(analytics_storage=storage)

    service.track_request(user_id=123, input_tokens=10, output_tokens=20)

    assert storage.global_data["total_requests"] == 1
    assert storage.global_data["total_input_tokens"] == 10
    assert storage.global_data["total_output_tokens"] == 20
    assert storage.global_data["total_tokens"] == 30
    assert storage.global_data["last_request_at"] is not None

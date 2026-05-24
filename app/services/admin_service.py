from pathlib import Path

from app.services.auth_service import AuthService
from app.storage.analytics_storage import AnalyticsStorage
from app.storage.settings_storage import SettingsStorage


class AdminService:
    def __init__(
        self,
        auth_service: AuthService,
        settings_storage: SettingsStorage,
        analytics_storage: AnalyticsStorage,
    ) -> None:
        self.auth_service = auth_service
        self.settings_storage = settings_storage
        self.analytics_storage = analytics_storage

    def is_admin(self, user_id: int) -> bool:
        return self.auth_service.is_admin(user_id)

    def get_admin_data(self) -> dict:
        access_config = self.settings_storage.read_access_config()
        global_analytics = self.analytics_storage.read_global_analytics()

        return {
            "users_count": len(access_config["users"]),
            "admins_count": len(access_config["admins"]),
            "total_requests": global_analytics["total_requests"],
            "total_tokens": global_analytics["total_tokens"],
        }

    def get_tokens_info(self) -> dict:
        global_analytics = self.analytics_storage.read_global_analytics()

        return {
            "total_tokens": global_analytics["total_tokens"],
            "input_tokens": global_analytics.get("total_input_tokens", 0),
            "output_tokens": global_analytics.get("total_output_tokens", 0),
        }

    def add_user(self, user_id: int) -> None:
        self.settings_storage.add_user(user_id)

    def add_admin(self, user_id: int) -> None:
        self.settings_storage.add_admin(user_id)

    def get_error_file_path(self) -> Path:
        return Path("data/errors/errors.log")

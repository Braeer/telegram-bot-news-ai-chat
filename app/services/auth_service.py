from app.storage.settings_storage import SettingsStorage


class AuthService:
    def __init__(self, settings_storage: SettingsStorage) -> None:
        self.settings_storage = settings_storage

    def is_admin(self, user_id: int) -> bool:
        access_config = self.settings_storage.read_access_config()

        return user_id in access_config["admins"]

    def is_allowed_user(self, user_id: int) -> bool:
        access_config = self.settings_storage.read_access_config()

        return user_id in access_config["admins"] or user_id in access_config["users"]

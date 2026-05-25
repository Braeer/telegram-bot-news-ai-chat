from app.storage.settings_storage import SettingsStorage


class SettingsService:
    def __init__(self, settings_storage: SettingsStorage) -> None:
        self.settings_storage = settings_storage

    def get_global_settings(self) -> dict:
        return self.settings_storage.read_global_settings()

    def get_user_settings(self, user_id: int) -> dict:
        return self.settings_storage.read_user_settings(user_id)

    def build_final_config(self, user_id: int) -> dict:
        global_settings = self.get_global_settings()
        user_settings = self.get_user_settings(user_id)

        model = user_settings.get("model", global_settings["default_model"])
        if model not in global_settings["allowed_models"]:
            model = global_settings["default_model"]

        temperature = float(
            user_settings.get("temperature", global_settings["default_temperature"])
        )

        max_tokens = int(user_settings.get("max_tokens", global_settings["max_tokens_per_request"]))
        max_tokens = min(max_tokens, global_settings["max_tokens_per_request"])

        return {
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "system_prompt": user_settings.get("system_prompt", ""),
        }

    def update_user_model(self, user_id: int, model: str) -> None:
        global_settings = self.get_global_settings()

        if not global_settings["allow_user_model_change"]:
            raise ValueError("User model change is disabled")

        if model not in global_settings["allowed_models"]:
            raise ValueError("Model is not allowed")

        user_settings = self.get_user_settings(user_id)
        user_settings["model"] = model

        self.settings_storage.write_user_settings(user_id, user_settings)

    def update_user_max_tokens(self, user_id: int, max_tokens: int) -> None:
        global_settings = self.get_global_settings()

        if not global_settings["allow_user_max_tokens_change"]:
            raise ValueError("User max_tokens change is disabled")

        if max_tokens > global_settings["max_tokens_per_request"]:
            raise ValueError("max_tokens is greater than global limit")

        user_settings = self.get_user_settings(user_id)
        user_settings["max_tokens"] = max_tokens

        self.settings_storage.write_user_settings(user_id, user_settings)

    def update_user_prompt(self, user_id: int, prompt: str) -> None:
        user_settings = self.get_user_settings(user_id)
        user_settings["system_prompt"] = prompt

        self.settings_storage.write_user_settings(user_id, user_settings)

    def update_global_setting(self, key: str, value: object) -> None:
        global_settings = self.get_global_settings()
        global_settings[key] = value

        self.settings_storage.write_global_settings(global_settings)

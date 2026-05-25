import pytest

from app.services.settings_service import SettingsService


class FakeSettingsStorage:
    def __init__(self) -> None:
        self.global_settings = {
            "default_model": "mock",
            "allowed_models": ["mock", "gpt-test"],
            "default_temperature": 0.7,
            "max_tokens_per_request": 2000,
            "max_context_messages": 20,
            "allow_user_model_change": True,
            "allow_user_temperature_change": True,
            "allow_user_max_tokens_change": True,
        }
        self.user_settings = {}

    def read_global_settings(self) -> dict:
        return self.global_settings

    def read_user_settings(self, user_id: int) -> dict:
        return self.user_settings.get(user_id, {})

    def write_user_settings(self, user_id: int, data: dict) -> None:
        self.user_settings[user_id] = data

    def write_global_settings(self, data: dict) -> None:
        self.global_settings = data


def test_build_final_config_uses_global_defaults():
    storage = FakeSettingsStorage()
    service = SettingsService(settings_storage=storage)

    config = service.build_final_config(user_id=123)

    assert config["model"] == "mock"
    assert config["temperature"] == 0.7
    assert config["max_tokens"] == 2000
    assert config["system_prompt"] == ""


def test_build_final_config_uses_user_settings():
    storage = FakeSettingsStorage()
    storage.user_settings[123] = {
        "model": "gpt-test",
        "temperature": 0.3,
        "max_tokens": 1000,
        "system_prompt": "Пиши коротко",
    }

    service = SettingsService(settings_storage=storage)

    config = service.build_final_config(user_id=123)

    assert config["model"] == "gpt-test"
    assert config["temperature"] == 0.3
    assert config["max_tokens"] == 1000
    assert config["system_prompt"] == "Пиши коротко"


def test_build_final_config_fallbacks_to_default_model_if_model_not_allowed():
    storage = FakeSettingsStorage()
    storage.user_settings[123] = {"model": "bad-model"}

    service = SettingsService(settings_storage=storage)

    assert service.build_final_config(user_id=123)["model"] == "mock"


def test_build_final_config_limits_max_tokens_by_global_limit():
    storage = FakeSettingsStorage()
    storage.user_settings[123] = {"max_tokens": 5000}

    service = SettingsService(settings_storage=storage)

    assert service.build_final_config(user_id=123)["max_tokens"] == 2000


def test_update_user_model_saves_allowed_model():
    storage = FakeSettingsStorage()
    service = SettingsService(settings_storage=storage)

    service.update_user_model(user_id=123, model="gpt-test")

    assert storage.user_settings[123]["model"] == "gpt-test"


def test_update_user_model_raises_if_change_disabled():
    storage = FakeSettingsStorage()
    storage.global_settings["allow_user_model_change"] = False

    service = SettingsService(settings_storage=storage)

    with pytest.raises(ValueError):
        service.update_user_model(user_id=123, model="gpt-test")


def test_update_user_model_raises_if_model_not_allowed():
    storage = FakeSettingsStorage()
    service = SettingsService(settings_storage=storage)

    with pytest.raises(ValueError):
        service.update_user_model(user_id=123, model="bad-model")


def test_update_user_temperature_saves_value():
    storage = FakeSettingsStorage()
    service = SettingsService(settings_storage=storage)

    service.update_user_temperature(user_id=123, temperature=1.2)

    assert storage.user_settings[123]["temperature"] == 1.2


def test_update_user_temperature_raises_if_change_disabled():
    storage = FakeSettingsStorage()
    storage.global_settings["allow_user_temperature_change"] = False

    service = SettingsService(settings_storage=storage)

    with pytest.raises(ValueError):
        service.update_user_temperature(user_id=123, temperature=0.5)


def test_update_user_temperature_raises_if_value_out_of_range():
    storage = FakeSettingsStorage()
    service = SettingsService(settings_storage=storage)

    with pytest.raises(ValueError):
        service.update_user_temperature(user_id=123, temperature=3)


def test_update_user_max_tokens_saves_value():
    storage = FakeSettingsStorage()
    service = SettingsService(settings_storage=storage)

    service.update_user_max_tokens(user_id=123, max_tokens=1200)

    assert storage.user_settings[123]["max_tokens"] == 1200


def test_update_user_max_tokens_raises_if_change_disabled():
    storage = FakeSettingsStorage()
    storage.global_settings["allow_user_max_tokens_change"] = False

    service = SettingsService(settings_storage=storage)

    with pytest.raises(ValueError):
        service.update_user_max_tokens(user_id=123, max_tokens=1200)


def test_update_user_max_tokens_raises_if_above_global_limit():
    storage = FakeSettingsStorage()
    service = SettingsService(settings_storage=storage)

    with pytest.raises(ValueError):
        service.update_user_max_tokens(user_id=123, max_tokens=3000)


def test_update_user_prompt_saves_prompt():
    storage = FakeSettingsStorage()
    service = SettingsService(settings_storage=storage)

    service.update_user_prompt(user_id=123, prompt="Пиши коротко")

    assert storage.user_settings[123]["system_prompt"] == "Пиши коротко"

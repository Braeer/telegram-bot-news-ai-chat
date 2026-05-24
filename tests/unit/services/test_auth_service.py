from app.services.auth_service import AuthService


class FakeSettingsStorage:
    def read_access_config(self):
        return {
            "admins": [123],
            "users": [456],
        }


def test_is_admin_returns_true_for_admin_user():
    service = AuthService(settings_storage=FakeSettingsStorage())

    assert service.is_admin(123) is True


def test_is_admin_returns_false_for_regular_user():
    service = AuthService(settings_storage=FakeSettingsStorage())

    assert service.is_admin(456) is False


def test_is_allowed_user_returns_true_for_admin():
    service = AuthService(settings_storage=FakeSettingsStorage())

    assert service.is_allowed_user(123) is True


def test_is_allowed_user_returns_true_for_regular_user():
    service = AuthService(settings_storage=FakeSettingsStorage())

    assert service.is_allowed_user(456) is True


def test_is_allowed_user_returns_false_for_unknown_user():
    service = AuthService(settings_storage=FakeSettingsStorage())

    assert service.is_allowed_user(999) is False

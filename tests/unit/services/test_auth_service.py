from app.services.auth_service import AuthService


def test_is_admin_returns_true_for_admin_user():
    service = AuthService(admins=[123], users=[456])

    assert service.is_admin(123) is True


def test_is_allowed_user_returns_true_for_admin():
    service = AuthService(admins=[123], users=[])

    assert service.is_allowed_user(123) is True


def test_is_allowed_user_returns_true_for_regular_user():
    service = AuthService(admins=[123], users=[456])

    assert service.is_allowed_user(456) is True


def test_is_allowed_user_returns_false_for_unknown_user():
    service = AuthService(admins=[123], users=[456])

    assert service.is_allowed_user(999) is False

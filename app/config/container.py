from dataclasses import dataclass

from app.services.admin_service import AdminService
from app.services.ai_service import AIService
from app.services.analytics_service import AnalyticsService
from app.services.auth_service import AuthService
from app.services.chat_service import ChatService
from app.services.cleanup_service import CleanupService
from app.services.settings_service import SettingsService
from app.services.template_service import TemplateService
from app.storage.analytics_storage import AnalyticsStorage
from app.storage.chat_storage import ChatStorage
from app.storage.settings_storage import SettingsStorage


@dataclass(frozen=True)
class AppContainer:
    template_service: TemplateService
    auth_service: AuthService
    analytics_service: AnalyticsService
    admin_service: AdminService
    settings_service: SettingsService
    chat_service: ChatService
    cleanup_service: CleanupService
    ai_service: AIService


def build_container() -> AppContainer:
    template_service = TemplateService()

    settings_storage = SettingsStorage()
    analytics_storage = AnalyticsStorage()
    chat_storage = ChatStorage()
    ai_service = AIService()
    auth_service = AuthService(settings_storage=settings_storage)

    analytics_service = AnalyticsService(
        analytics_storage=analytics_storage,
    )

    settings_service = SettingsService(
        settings_storage=settings_storage,
    )

    chat_service = ChatService(
        chat_storage=chat_storage,
        analytics_service=analytics_service,
        settings_service=settings_service,
        ai_service=ai_service,
    )

    cleanup_service = CleanupService(
        chat_service=chat_service,
    )

    admin_service = AdminService(
        auth_service=auth_service,
        settings_storage=settings_storage,
        analytics_storage=analytics_storage,
    )

    return AppContainer(
        template_service=template_service,
        auth_service=auth_service,
        analytics_service=analytics_service,
        admin_service=admin_service,
        settings_service=settings_service,
        chat_service=chat_service,
        cleanup_service=cleanup_service,
        ai_service=ai_service,
    )

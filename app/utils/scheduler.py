from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.services.cleanup_service import CleanupService


def setup_scheduler(cleanup_service: CleanupService) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        cleanup_service.cleanup_chats,
        trigger="cron",
        hour=0,
        minute=0,
    )

    scheduler.start()

    return scheduler

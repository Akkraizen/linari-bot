from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger
from services.warn_service import WarnService
from database.models import AsyncSessionLocal

async def delete_old_warns_job():
    logger.info("Starting scheduled task: delete_old_warns")
    async with AsyncSessionLocal() as session:
        async with session.begin():
            warn_service = WarnService(session)
            deleted_count = await warn_service.delete_old_warns()
            logger.info(f"Scheduled task finished: deleted {deleted_count} old warns")

def setup_scheduler():
    scheduler = AsyncIOScheduler()
    
    # Добавляем задачу: каждый день в 00:00
    scheduler.add_job(
        delete_old_warns_job,
        "cron",
        hour=0,
        minute=0,
        id="delete_old_warns",
        replace_existing=True
    )
    
    logger.info("Scheduler configured with 'delete_old_warns' job")
    return scheduler

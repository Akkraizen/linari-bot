from sqlalchemy.ext.asyncio import AsyncSession

from database.models import PunishmentAction
from database.repositories.punishment_log_repository import PunishmentLogRepository


class PunishmentLogService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = PunishmentLogRepository(session)

    async def log_punishment(self, user_id: int, chat_id: int, admin_id: int, action: PunishmentAction, reason: str = None):
        await self.repository.log_punishment(user_id, chat_id, admin_id, action, reason)

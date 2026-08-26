from sqlalchemy.ext.asyncio import AsyncSession

from database.models import PunishmentLog, PunishmentAction


class PunishmentLogRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def log_punishment(self, user_id: int, chat_id: int, admin_id: int, action: PunishmentAction, reason: str = None):
        log = PunishmentLog(
            user_id=user_id,
            chat_id=chat_id,
            action=action,
            reason=reason,
            admin_id=admin_id
        )
        self.session.add(log)

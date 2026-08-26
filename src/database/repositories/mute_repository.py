from datetime import datetime

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import UserMute


class MuteRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_mute(self, user_id: int, chat_id: int, admin_id: int, until_date: datetime, reason: str = None):
        mute = UserMute(
            user_id=user_id,
            chat_id=chat_id,
            admin_id=admin_id,
            until_date=until_date,
            reason=reason
        )
        self.session.add(mute)

    async def get_mute(self, user_id: int, chat_id: int) -> UserMute | None:
        stmt = select(UserMute).where(UserMute.user_id == user_id, UserMute.chat_id == chat_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def remove_mute(self, user_id: int, chat_id: int):
        stmt = delete(UserMute).where(UserMute.user_id == user_id, UserMute.chat_id == chat_id)
        await self.session.execute(stmt)

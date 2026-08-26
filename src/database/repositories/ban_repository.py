from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import UserBan


class BanRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_ban(self, user_id: int, chat_id: int, admin_id: int, reason: str = None):
        ban = UserBan(
            user_id=user_id,
            chat_id=chat_id,
            admin_id=admin_id,
            reason=reason
        )
        self.session.add(ban)

    async def get_ban(self, user_id: int, chat_id: int) -> UserBan | None:
        from sqlalchemy import select
        stmt = select(UserBan).where(UserBan.user_id == user_id, UserBan.chat_id == chat_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def remove_ban(self, user_id: int, chat_id: int):
        stmt = delete(UserBan).where(UserBan.user_id == user_id, UserBan.chat_id == chat_id)
        await self.session.execute(stmt)

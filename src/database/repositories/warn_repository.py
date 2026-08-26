from sqlalchemy import select, delete, func, text
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import UserWarn


class WarnRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_warns_count(self, user_id: int, chat_id: int) -> int:
        stmt = select(func.count(UserWarn.id)).where(UserWarn.user_id == user_id, UserWarn.chat_id == chat_id)
        result = await self.session.execute(stmt)
        return result.scalar() or 0

    async def get_active_warns(self, user_id: int, chat_id: int):
        stmt = select(UserWarn).where(
            UserWarn.user_id == user_id,
            UserWarn.chat_id == chat_id
        ).order_by(UserWarn.created_at.asc())
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create_warn(self, user_id: int, chat_id: int, admin_id: int, reason: str = None) -> UserWarn:
        warn = UserWarn(user_id=user_id, chat_id=chat_id, admin_id=admin_id, reason=reason)
        self.session.add(warn)
        return warn

    async def reset_warns(self, user_id: int, chat_id: int):
        stmt = delete(UserWarn).where(UserWarn.user_id == user_id, UserWarn.chat_id == chat_id)
        await self.session.execute(stmt)

    async def remove_oldest_warn(self, user_id: int, chat_id: int) -> int:
        subquery = select(UserWarn.id).where(
            UserWarn.user_id == user_id,
            UserWarn.chat_id == chat_id
        ).order_by(UserWarn.created_at.asc()).limit(1)
        
        result = await self.session.execute(subquery)
        oldest_id = result.scalar_one_or_none()
        
        if oldest_id:
            stmt = delete(UserWarn).where(UserWarn.id == oldest_id)
            await self.session.execute(stmt)
        
        return await self.get_warns_count(user_id, chat_id)

    async def delete_old_warns(self):
        # Вызов SQL функции или прямой запрос
        stmt = delete(UserWarn).where(UserWarn.created_at <= func.now() - text("INTERVAL '1 month'"))
        result = await self.session.execute(stmt)
        return result.rowcount



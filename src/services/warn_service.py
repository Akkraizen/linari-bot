from sqlalchemy.ext.asyncio import AsyncSession

from database.models import UserWarn
from database.repositories.warn_repository import WarnRepository


class WarnService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = WarnRepository(session)

    async def get_warns_count(self, user_id: int, chat_id: int) -> int:
        return await self.repository.get_warns_count(user_id, chat_id)

    async def get_active_warns(self, user_id: int, chat_id: int):
        return await self.repository.get_active_warns(user_id, chat_id)

    async def create_warn(self, user_id: int, chat_id: int, admin_id: int, reason: str = None) -> UserWarn:
        return await self.repository.create_warn(user_id, chat_id, admin_id, reason)

    async def reset_warns(self, user_id: int, chat_id: int):
        await self.repository.reset_warns(user_id, chat_id)

    async def remove_oldest_warn(self, user_id: int, chat_id: int) -> int:
        return await self.repository.remove_oldest_warn(user_id, chat_id)

    async def delete_old_warns(self):
        return await self.repository.delete_old_warns()

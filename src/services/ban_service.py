from sqlalchemy.ext.asyncio import AsyncSession

from database.repositories.ban_repository import BanRepository


class BanService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = BanRepository(session)

    async def add_ban(self, user_id: int, chat_id: int, admin_id: int, reason: str = None):
        await self.repository.add_ban(user_id, chat_id, admin_id, reason)

    async def get_ban(self, user_id: int, chat_id: int):
        return await self.repository.get_ban(user_id, chat_id)

    async def remove_ban(self, user_id: int, chat_id: int):
        await self.repository.remove_ban(user_id, chat_id)

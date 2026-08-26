from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from database.repositories.mute_repository import MuteRepository


class MuteService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = MuteRepository(session)

    async def add_mute(self, user_id: int, chat_id: int, admin_id: int, until_date: datetime, reason: str = None):
        await self.repository.add_mute(user_id, chat_id, admin_id, until_date, reason)

    async def get_mute(self, user_id: int, chat_id: int):
        return await self.repository.get_mute(user_id, chat_id)

    async def remove_mute(self, user_id: int, chat_id: int):
        await self.repository.remove_mute(user_id, chat_id)

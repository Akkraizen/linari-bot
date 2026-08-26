from sqlalchemy.ext.asyncio import AsyncSession
from database.repositories.moderator_repository import ModeratorRepository
from database.models import Moderator, ModeratorLevel

class ModeratorService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = ModeratorRepository(session)

    async def get_moderator(self, user_id: int) -> Moderator | None:
        return await self.repository.get_moderator(user_id)

    async def add_moderator(self, user_id: int, level: int = 1) -> Moderator:
        mod_level = ModeratorLevel(level)
        return await self.repository.add_moderator(user_id, mod_level)

    async def remove_moderator(self, user_id: int):
        await self.repository.remove_moderator(user_id)

    async def set_moderator_level(self, user_id: int, level: int):
        mod_level = ModeratorLevel(level)
        await self.repository.update_moderator_level(user_id, mod_level)

    async def is_moderator(self, user_id: int) -> bool:
        mod = await self.get_moderator(user_id)
        return mod is not None

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Moderator, ModeratorLevel

class ModeratorRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_moderator(self, user_id: int) -> Moderator | None:
        stmt = select(Moderator).where(Moderator.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def add_moderator(self, user_id: int, level: ModeratorLevel = ModeratorLevel.LEVEL_1) -> Moderator:
        moderator = Moderator(user_id=user_id, level=level)
        self.session.add(moderator)
        return moderator

    async def remove_moderator(self, user_id: int):
        stmt = delete(Moderator).where(Moderator.user_id == user_id)
        await self.session.execute(stmt)

    async def update_moderator_level(self, user_id: int, level: ModeratorLevel):
        moderator = await self.get_moderator(user_id)
        if moderator:
            moderator.level = level

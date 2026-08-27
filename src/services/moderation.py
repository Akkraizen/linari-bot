from datetime import datetime

from database.models import AsyncSessionLocal, PunishmentAction
from services.ban_service import BanService
from services.mute_service import MuteService
from services.punishment_log_service import PunishmentLogService
from services.warn_service import WarnService
from services.moderator_service import ModeratorService


class ModerationService:
    async def warn_user(self, user_id: int, chat_id: int, admin_id: int, reason: str = None) -> int:
        async with AsyncSessionLocal() as session:
            async with session.begin():
                warn_service = WarnService(session)
                log_service = PunishmentLogService(session)
                
                await warn_service.create_warn(user_id, chat_id, admin_id, reason)
                await log_service.log_punishment(user_id, chat_id, admin_id, PunishmentAction.WARN, reason)
                
                count = await warn_service.get_warns_count(user_id, chat_id)
                await session.commit()
                return count

    async def ban_user(self, user_id: int, chat_id: int, admin_id: int, reason: str = None):
        async with AsyncSessionLocal() as session:
            async with session.begin():
                ban_service = BanService(session)
                log_service = PunishmentLogService(session)

                await log_service.log_punishment(user_id, chat_id, admin_id, PunishmentAction.BAN, reason)
                await ban_service.add_ban(user_id, chat_id, admin_id, reason)
                await session.commit()

    async def mute_user(self, user_id: int, chat_id: int, admin_id: int, until_date: datetime, reason: str = None):
        async with AsyncSessionLocal() as session:
            async with session.begin():
                mute_service = MuteService(session)
                log_service = PunishmentLogService(session)
                
                await log_service.log_punishment(user_id, chat_id, admin_id, PunishmentAction.MUTE, reason)
                await mute_service.add_mute(user_id, chat_id, admin_id, until_date, reason)
                await session.commit()

    async def unwarn_user(self, user_id: int, chat_id: int, admin_id: int) -> int:
        async with AsyncSessionLocal() as session:
            async with session.begin():
                warn_service = WarnService(session)
                log_service = PunishmentLogService(session)
                
                count = await warn_service.remove_oldest_warn(user_id, chat_id)
                await log_service.log_punishment(user_id, chat_id, admin_id, PunishmentAction.UNWARN, "Анварн")
                await session.commit()
                return count

    async def get_user_warns(self, user_id: int, chat_id: int):
        async with AsyncSessionLocal() as session:
            async with session.begin():
                warn_service = WarnService(session)
                return await warn_service.get_active_warns(user_id, chat_id)

    async def unban_user(self, user_id: int, chat_id: int, admin_id: int):
        async with AsyncSessionLocal() as session:
            async with session.begin():
                ban_service = BanService(session)
                log_service = PunishmentLogService(session)
                
                await ban_service.remove_ban(user_id, chat_id)
                await log_service.log_punishment(user_id, chat_id, admin_id, PunishmentAction.UNBAN, "Разбан")
                await session.commit()

    async def unmute_user(self, user_id: int, chat_id: int, admin_id: int):
        async with AsyncSessionLocal() as session:
            async with session.begin():
                mute_service = MuteService(session)
                log_service = PunishmentLogService(session)
                
                await mute_service.remove_mute(user_id, chat_id)
                await log_service.log_punishment(user_id, chat_id, admin_id, PunishmentAction.UNMUTE, "Размут")
                await session.commit()

    async def is_moderator(self, user_id: int) -> bool:
        async with AsyncSessionLocal() as session:
            async with session.begin():
                mod_service = ModeratorService(session)
                return await mod_service.is_moderator(user_id)

    async def get_moderator(self, user_id: int):
        async with AsyncSessionLocal() as session:
            async with session.begin():
                mod_service = ModeratorService(session)
                return await mod_service.get_moderator(user_id)

    async def add_moderator(self, user_id: int, level: int = 1):
        async with AsyncSessionLocal() as session:
            async with session.begin():
                mod_service = ModeratorService(session)
                await mod_service.add_moderator(user_id, level)
                await session.commit()

    async def remove_moderator(self, user_id: int):
        async with AsyncSessionLocal() as session:
            async with session.begin():
                mod_service = ModeratorService(session)
                await mod_service.remove_moderator(user_id)
                await session.commit()

    async def get_mute(self, user_id: int, chat_id: int):
        async with AsyncSessionLocal() as session:
            async with session.begin():
                mute_service = MuteService(session)
                return await mute_service.get_mute(user_id, chat_id)

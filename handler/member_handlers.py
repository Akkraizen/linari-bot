from aiogram import Router
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER
from aiogram.types import ChatMemberUpdated, ChatMemberLeft, ChatMemberRestricted, ChatMemberBanned

from config import Config
from utils import get_member_status

router = Router(name="member_router")
config = Config()


@router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def new_member_handler(event: ChatMemberUpdated) -> None:
    member_status = await get_member_status(event.bot, config.CHANNEL_ID, event.from_user.id)
    if isinstance(member_status, (ChatMemberLeft, ChatMemberRestricted, ChatMemberBanned)):
        return

    if event.chat.type == "channel":
        return

    await event.answer("""
Привет, путник! Правил тут не много:
1. Оскорбления - бан
2. Вбросы 18+ контента - бан
3. Экстримизм - бан

Добро пожаловать🩵
    """.strip())

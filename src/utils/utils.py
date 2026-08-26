from aiogram import Bot
from aiogram.types import ResultChatMemberUnion


async def get_member_status(bot: Bot | None, chat_id: str | int, user_id: str | int) -> ResultChatMemberUnion:
    if bot is None:
        raise ValueError("Bot is None!")
    return await bot.get_chat_member(chat_id=chat_id, user_id=int(user_id))
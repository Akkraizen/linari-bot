from aiogram import Bot


async def get_member_status(bot: Bot, chat_id: str | int, user_id: str | int):
    return await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
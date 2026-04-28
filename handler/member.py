from aiogram import F
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER
from aiogram.types import ChatMemberUpdated

from bot import LinariBot

bot = LinariBot()

@bot.dp.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def new_member_handler(event: ChatMemberUpdated):
    # TODO: replace text
    await event.answer(f"<b>Hi, {event.new_chat_member.user.first_name}!</b>", parse_mode="HTML")
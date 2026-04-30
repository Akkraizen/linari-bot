from typing import Any

from aiogram import Router, F
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER
from aiogram.types import ChatMemberUpdated, \
    InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ChatPermissions, ChatMemberBanned, ChatMemberLeft
from loguru import logger

from config import Config
from utils import get_member_status

router = Router(name="member_router")
config = Config()


__WELCOME_TEXT = """
Привет, <a href="tg://user?id={user_id}">путник</a>! Правил тут не много:
1. Оскорбления - бан
2. Вбросы 18+ контента - бан
3. Экстремизм - бан

Прежде, чем начать общаться — прими правила.

Добро пожаловать🩵
"""


@router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def new_member_handler(event: ChatMemberUpdated) -> None:
    try:
        await event.bot.restrict_chat_member(
            event.chat.id,
            event.new_chat_member.user.id,
            permissions=ChatPermissions(
                can_send_messages=False,
                can_send_audios=False,
                can_send_documents=False,
                can_send_photos=False,
                can_send_videos=False,
                can_send_video_notes=False,
                can_send_voice_notes=False,
                can_send_polls=False,
                can_send_other_messages=False,
                can_add_web_page_previews=False,
                can_invite_users=False
            )
        )
        logger.info(f"Member {event.new_chat_member.user.id} was muted")
    except Exception as e:
        logger.exception(e)

    if event.chat.type == "channel":
        return

    user_id = event.new_chat_member.user.id
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Понятно", callback_data=f"accept_{user_id}")]
    ])

    await event.answer(__WELCOME_TEXT.format(**{"user_id": user_id}), reply_markup=kb, parse_mode="HTML")


@router.callback_query(F.data.startswith("accept_"))
async def accept_button_handler(callback: CallbackQuery) -> Any:
    _, user_id = callback.data.split("_")
    user_id = int(user_id)

    if user_id != callback.from_user.id:
        return await callback.answer("Это сообщение адресовано не вам!", show_alert=True)

    member_status = await get_member_status(callback.bot, config.CHANNEL_ID, user_id)
    logger.info(member_status)

    if isinstance(member_status, (ChatMemberLeft, ChatMemberBanned)):
        return await callback.answer("Подпишись на канал Лины! @linari_me", show_alert=True)

    try:
        await callback.bot.restrict_chat_member(
            callback.message.chat.id,
            user_id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_audios=True,
                can_send_documents=True,
                can_send_photos=True,
                can_send_videos=True,
                can_send_video_notes=True,
                can_send_voice_notes=True,
                can_send_polls=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True,
                can_invite_users=True
            )
        )
        logger.info(f"Member {user_id} was unmuted")
    except Exception as e:
        logger.exception(e)

    return await callback.message.delete()
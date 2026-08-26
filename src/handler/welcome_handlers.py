from aiogram import Router, F
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER
from aiogram.types import (
    ChatMemberUpdated,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
    ChatPermissions,
    ChatMemberBanned,
    ChatMemberLeft,
    Message
)
from loguru import logger

from config import Config, RESTRICTION_PERMISSIONS
from model.commands import Commands, Command
from utils.utils import get_member_status

router = Router(name="welcome_router")
config = Config()


__RULES = """
1. Оскорбления - бан
2. Вбросы 18+ контента - бан
3. Экстремизм - бан
"""

__WELCOME_TEXT = """
Привет, <a href="tg://user?id={user_id}">путник</a>! Правил тут не много:
{rules}

Прежде, чем начать общаться — прими правила.

Добро пожаловать🩵

Используй <code>/links</code> для просмотра остальных соцсетей🩵
"""


@router.message(Command(Commands.RULES))
async def links_command(message: Message) -> Message:
    return await message.answer(__RULES, disable_web_page_preview=True)


@router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def new_member_handler(event: ChatMemberUpdated) -> Message | None:
    if event.bot is None and event.chat is None:
        return await event.answer("Произошла ошибка!")

    try:
        # noinspection PyUnresolvedReferences
        await event.bot.restrict_chat_member(
            event.chat.id,
            event.new_chat_member.user.id,
            permissions=RESTRICTION_PERMISSIONS
        )
        logger.info(f"Member {event.new_chat_member.user.id} was muted")
    except Exception as e:
        logger.exception(e)

    if event.chat.type == "channel":
        return None

    user_id = event.new_chat_member.user.id
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Понятно", callback_data=f"accept_{user_id}")]
    ])

    return await event.answer(__WELCOME_TEXT.format(**{"user_id": user_id, "rules": __RULES}), reply_markup=kb, parse_mode="HTML")


@router.callback_query(F.data.startswith("accept_"))
async def accept_button_handler(callback: CallbackQuery):
    if callback.data is None:
        return await callback.answer("Произошла ошибка!")

    _, user_id = callback.data.split("_")
    user_id = int(user_id)

    if user_id != callback.from_user.id:
        return await callback.answer("Это сообщение адресовано не вам!", show_alert=True)

    member_status = await get_member_status(callback.bot, config.CHANNEL_ID, user_id)
    logger.info(member_status)

    if isinstance(member_status, (ChatMemberLeft, ChatMemberBanned)):
        return await callback.answer("Подпишись на канал Лины! @linari_me", show_alert=True)

    try:
        if not isinstance(callback.message, Message):
            return None

        # noinspection PyUnresolvedReferences
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
                can_edit_tag=True,
                can_change_info=True,
                can_invite_users=True,
                can_pin_messages=True,
                can_manage_topics=True
            )
        )
        logger.info(f"Member {user_id} was unmuted")
    except Exception as e:
        logger.exception(e)

    if isinstance(callback.message, Message):
        return await callback.message.delete()
    return None


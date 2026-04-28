from aiogram import Router, F
from aiogram.types import Message, ChatMemberLeft, ChatMemberRestricted, ChatMemberBanned
from loguru import logger

from config import Config
from utils import get_member_status

router = Router(name="message_router")
config = Config()

@router.message()
async def default_handler(message: Message) -> None:
    member_status = await get_member_status(message.bot, config.CHANNEL_ID, message.from_user.id)
    logger.info(member_status)
    if isinstance(member_status, (ChatMemberLeft, ChatMemberRestricted, ChatMemberBanned)):
        await message.delete()
        logger.info(f"Message from {message.from_user.full_name} was deleted")
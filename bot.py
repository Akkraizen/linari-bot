from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER
from aiogram.types import Message, ChatMemberLeft, ChatMemberBanned, ChatMemberRestricted, ChatMemberUpdated
from loguru import logger

from config import Config
from struture.singleton import Singleton


class LinariBot(Singleton):
    def __init__(self):
        if not self.created:
            self.config = Config()
            self.bot = Bot(token=self.config.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
            self.dp = Dispatcher()
            self.dp.message.register(self.default_handler)
            self.dp.chat_member.register(self.new_member_handler, ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
            logger.info("Bot instance was created")

    async def start(self):
        await self.dp.start_polling(self.bot)


    async def new_member_handler(self, event: ChatMemberUpdated):
        await event.answer("""
        Привет, путник! Правил тут не много:
        1. Оскорбления - бан
        2. Вбросы 18+ контента - бан
        3. Экстримизм - бан
        
        Добро пожаловать🩵
    """.strip())


    async def default_handler(self, message: Message) -> None:
        user_channel_status = await self.bot.get_chat_member(chat_id=self.config.CHANNEL_ID, user_id=message.from_user.id)
        logger.info(user_channel_status)
        if isinstance(user_channel_status, (ChatMemberLeft, ChatMemberRestricted, ChatMemberBanned)):
            await message.delete()
            logger.info(f"Message from {message.from_user.full_name} was deleted")
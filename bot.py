from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from loguru import logger
from handler.member_handlers import router as member_router
from handler.message_handlers import router as message_router

from config import Config
from struture.singleton import Singleton


class LinariBot(Singleton):
    def __init__(self):
        if not self.created:
            self.config = Config()
            self.bot = Bot(token=self.config.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
            self.dp = Dispatcher()
            logger.info("Bot instance was created")

    async def configure(self):
        self.dp.include_routers(member_router, message_router)
        logger.info("Bot was configured")

    async def start(self):
        await self.configure()
        await self.dp.start_polling(self.bot)

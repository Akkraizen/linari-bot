from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from loguru import logger
from handler.member_handlers import router as member_router

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
        self.dp.include_router(member_router)
        logger.info("Bot was configured")

    async def start(self):
        await self.configure()
        bot_name = await self.bot.get_my_name()
        logger.info(f"Bot {bot_name.name} was started")
        await self.dp.start_polling(self.bot)

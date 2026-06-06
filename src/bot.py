from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from loguru import logger
from handler.welcome_handlers import router as welcome_router
from handler.links_command import router as links_command
from handler.dev_commands import router as dev_commands

from config import Config
from middleware.throttling_middleware import UserThrottlingMiddleware, GlobalThrottlingMiddleware
from struture.singleton import Singleton


class LinariBot(Singleton):
    def __init__(self):
        if not self.created:
            self.config = Config()
            self.bot = Bot(token=self.config.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
            self.dp = Dispatcher()
            logger.info("Bot instance was created")

    async def configure(self):
        self.dp.include_router(welcome_router)
        self.dp.include_router(links_command)
        self.dp.include_router(dev_commands)

        self.dp.message.middleware(GlobalThrottlingMiddleware())
        self.dp.message.middleware(UserThrottlingMiddleware())
        logger.info("Bot was configured")

    async def start(self):
        await self.configure()
        bot_name = await self.bot.get_my_name()
        logger.info(f"Bot {bot_name.name} was started")
        await self.dp.start_polling(self.bot)

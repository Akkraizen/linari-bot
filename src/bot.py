from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from loguru import logger
from handler.dev_commands import router as dev_commands
from handler.links_command import router as links_command
from handler.pozdnyakov_handler import router as pozdnyakov_router
from handler.welcome_handlers import router as welcome_router

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
        self.dp.include_routers(
            dev_commands,
            links_command,
            pozdnyakov_router,
            welcome_router,
        )

        self.dp.message.middleware(GlobalThrottlingMiddleware())
        self.dp.message.middleware(UserThrottlingMiddleware())
        logger.info("Bot was configured")

    async def start(self):
        await self.configure()
        bot_name = await self.bot.get_my_name()
        logger.info(f"Bot {bot_name.name} was started")
        await self.dp.start_polling(self.bot)

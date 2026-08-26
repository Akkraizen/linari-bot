from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from loguru import logger

from config import Config
from database.db import init_db
from handler.dev_commands import router as dev_commands
from handler.links_command import router as links_command
from handler.moderation import router as moderation_router
from handler.celebrity_handler import router as celebrity_router
from handler.welcome_handlers import router as welcome_router
from middleware.throttling_middleware import UserThrottlingMiddleware, GlobalThrottlingMiddleware
from struture.singleton import Singleton
from utils.scheduler import setup_scheduler


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
            celebrity_router,
            welcome_router,
            moderation_router,
        )

        self.dp.message.middleware(GlobalThrottlingMiddleware())
        self.dp.message.middleware(UserThrottlingMiddleware())
        logger.info("Bot was configured")

    async def start(self):
        await init_db()
        await self.configure()
        
        scheduler = setup_scheduler()
        scheduler.start()
        logger.info("Scheduler started")

        bot_name = await self.bot.get_my_name()
        logger.info(f"Bot {bot_name.name} was started")
        await self.dp.start_polling(self.bot)

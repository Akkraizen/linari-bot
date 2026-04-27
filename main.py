import asyncio
import logging

from loguru import logger

from bot import LinariBot
from config import Config


def setup_logger():
    logging.disable(logging.CRITICAL)

    logger.add("../logs/log_{time}.log")
    logger.info("Logger was configured")


def setup():
    setup_logger()


async def main() -> None:
    config = Config()
    bot = LinariBot(config)
    await bot.start()


if __name__ == "__main__":
    asyncio.run(main())
import asyncio
import logging

from loguru import logger

from bot import LinariBot


def setup_logger():
    logging.disable(logging.CRITICAL)

    logger.add("../logs/log_{time}.log")
    logger.info("Logger was configured")


def setup():
    setup_logger()


async def main() -> None:
    setup()
    bot = LinariBot()
    await bot.start()


if __name__ == "__main__":
    asyncio.run(main())
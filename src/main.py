import asyncio
from contextlib import suppress

from loguru import logger

from bot import LinariBot


def setup_logger():
    logger.add("../logs/log_{time}.log")
    logger.info("Logger was configured")


def setup():
    setup_logger()


async def main() -> None:
    setup()
    bot = LinariBot()
    await bot.start()


if __name__ == "__main__":
    with suppress(KeyboardInterrupt):
        asyncio.run(main())
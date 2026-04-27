import asyncio
from os import getenv

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message, ChatMemberLeft

TOKEN = getenv("TOKEN")
CHANNEL_ID = getenv("CHANNEL_ID")

bot: Bot
dp = Dispatcher()


@dp.message()
async def bots_filter(message: Message) -> None:
    user_channel_status = bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)
    if user_channel_status != ChatMemberLeft:
        await message.delete()


async def main() -> None:
    global bot
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
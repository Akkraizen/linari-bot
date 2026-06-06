import time

from aiogram import Router
from aiogram.types import Message

from config import Config
from model.commands import Command, Commands

router = Router(name="dev_commands_router")
config = Config()

@router.message(Command(Commands.PING))
async def ping_command(message: Message) -> Message | bool:
    if message.from_user is not None and message.from_user.id not in config.OWNERS:
        return False

    start_time = time.time()
    message = await message.answer("🏓 Понг!")
    latency = int((time.time() - start_time) * 1000)
    return await message.edit_text(f"🏓 Понг!\n`{latency} мс`", parse_mode="Markdown")
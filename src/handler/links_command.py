from aiogram import Router
from aiogram.types import Message

from model.commands import Commands, Command

router = Router(name="links_command_router")

__LINKS_TEXT = """
tiktok -  https://www.tiktok.com/@linarime_
youtube - https://www.youtube.com/@linari_me
twtch - https://www.twitch.tv/linari_me

поддержать автора рублем - https://www.donationalerts.com/r/linari_me
"""

@router.message(Command(Commands.LINKS))
async def links_command(message: Message) -> Message:
    return await message.answer(__LINKS_TEXT, disable_web_page_preview=True)
from re import RegexFlag

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.utils.markdown import italic

router = Router(name="pozdnyakov_router")

@router.message(F.text.regexp(r"(поздняк|пиздняк|пиздяк)", search=True, flags=RegexFlag.IGNORECASE))
async def pozdnyakov_handler(message: Message) -> None:
    await message.reply(italic("*Поздняков признан ебланом на территории данного чата"), parse_mode=ParseMode.MARKDOWN_V2)
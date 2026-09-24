import re
from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.utils.markdown import italic

router = Router(name="celebrity_router")

CELEBRITIES = [
    {
        "pattern": re.compile(
            r"\b(?:поздняк(?:ов(?:а|у|ом|е|ы|ов|ам|ами|ах)?)?|пиздняк(?:ов(?:а|у|ом|е|ы|ов|ам|ами|ах)?)?|пиздяк(?:ов(?:а|у|ом|е|ы|ов|ам|ами|ах)?)?)\b",
            re.IGNORECASE,
        ),
        "text": "*Поздняков признан ебланом на территории данного чата",
    },
    {
        "pattern": re.compile(
            r"\bкац(?:а|у|ем|е|ы|ов|ам|ами|ах)?\b",
            re.IGNORECASE,
        ),
        "text": "*Кац признан ебателем собак на территории данного чата",
    },
    {
        "pattern": re.compile(
            r"\bнаки\b",
            re.IGNORECASE,
        ),
        "text": "*Майкл Наки признан сыном собаки на территории данного чата",
    },
    {
        "pattern": re.compile(
            r"\bварлам(?:ов(?:а|у|ом|е|ы|ов|ам|ами|ах)?)?\b",
            re.IGNORECASE,
        ),
        "text": "*Илья Варламов признан ебателем кошек на территории данного чата",
    },
]


@router.message()
async def celebrity_handler(message: Message) -> None:
    if not message.text:
        return

    for celeb in CELEBRITIES:
        if celeb["pattern"].search(message.text):
            await message.reply(italic(celeb["text"]), parse_mode=ParseMode.MARKDOWN_V2)
            break
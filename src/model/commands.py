from enum import Enum
from typing import Sequence

# noinspection PyProtectedMember
from aiogram import MagicFilter
from aiogram.filters import Command as AiogramCommand


class Command(AiogramCommand):
    def __init__(
            self,
            *values: Commands,
            commands: Sequence[Commands] | Commands | None = None,
            prefix: str = "/",
            ignore_case: bool = False,
            ignore_mention: bool = False,
            magic: MagicFilter | None = None,
    ):
        values = map(lambda c: c.value, values)
        commands = \
            (list(map(lambda c: c.value, commands))) \
            if isinstance(commands, Sequence) \
            else commands.value if commands is not None \
            else None
        super().__init__(
            *values,
            commands=commands,
            prefix=prefix,
            ignore_case=ignore_case,
            ignore_mention=ignore_mention,
            magic=magic
        )



class Commands(Enum):
    LINKS = "links"
    RULES = "rules"
    PING = "ping"
    WARN = "warn"
    BAN = "ban"
    MUTE = "mute"
    UNWARN = "unwarn"
    UNBAN = "unban"
    UNMUTE = "unmute"
    SETMOD = "setmod"
    DELMOD = "delmod"
    WARNS = "warns"

    @staticmethod
    def is_command(text: str | None) -> bool:
        if text is None:
            return False

        normalized = str(text or "").strip().lower()
        for command in Commands:
            if normalized.startswith("/" + command.value):
                return True
        return False

    @staticmethod
    def get_command(text: str | None) -> str | None:
        if text is None:
            return None

        normalized = str(text or "").strip().lower()
        for command in Commands:
            if normalized.startswith("/" + command.value):
                return command.value
        return None
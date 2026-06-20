from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message
from cachetools import TTLCache

from model.commands import Commands


class UserThrottlingMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.__cache = TTLCache(maxsize=10_000, ttl=1)

    async def __call__(self, handler: Callable[[Message, dict[str, Any]],Awaitable[Any]], event: Message, data: dict[str, Any]) -> Any:
        if event.from_user is None or not Commands.is_command(event.text):
            return await handler(event, data)

        user_id = event.from_user.id

        if user_id in self.__cache:
            return await event.answer("Подожди! Ты слишком часто используешь команды!")

        self.__cache[user_id] = True
        return await handler(event, data)


class GlobalThrottlingMiddleware(BaseMiddleware):
    def __init__(self):
        self.__cache = TTLCache(maxsize=10_000, ttl=5)

    async def __call__(self, handler: Callable[[Message, dict[str, Any]],Awaitable[Any]], event: Message, data: dict[str, Any]) -> Any:
        if event.from_user is None or event.text is None or not Commands.is_command(event.text):
            return await handler(event, data)

        command = event.text.removeprefix("/").split(" ")[0]

        if command not in self.__cache:
            self.__cache[command] = 0

        if self.__cache[command] >= 10:
            return await event.answer("Подожди! Эта команда используется слишком часто!")

        self.__cache[command] += 1
        return await handler(event, data)
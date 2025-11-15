from typing import Callable, Any, Dict, Awaitable

from maxapi.filters.middleware import BaseMiddleware
from maxapi.types import UpdateUnion, Message

from src.bot.ui import messages

class ErrorMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
            event: UpdateUnion,
            data: Dict[str, Any],
    ) -> Any:
        try:
            return await handler(event, data)
        except Exception as error:
            print(error)
            await event.message.answer(messages.unknown_error)

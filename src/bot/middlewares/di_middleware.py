from typing import Callable, Any, Dict, Awaitable

from maxapi.filters.middleware import BaseMiddleware
from maxapi.types import UpdateUnion

from src.models import Services

class DIMiddleware(BaseMiddleware):
    def __init__(self, services: Services):
        self._services = services

    async def __call__(
            self,
            handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
            event: UpdateUnion,
            data: Dict[str, Any],
    ) -> Any:
        data['services'] = self._services
        return await handler(event, data)

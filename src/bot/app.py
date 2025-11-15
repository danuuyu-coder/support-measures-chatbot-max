from maxapi import Bot, Dispatcher
from maxapi.enums.parse_mode import ParseMode
from maxapi.filters.middleware import BaseMiddleware

from src.bot.ui import create_commands
from src.bot.router import create_router

import asyncio, logging

class App:
    def __init__(self, token: str, *middlewares: BaseMiddleware):
        self._bot = Bot(token=token, parse_mode=ParseMode.HTML)
        self._dispatcher = Dispatcher()
        self._dispatcher.middlewares = middlewares
        self._dispatcher.include_routers(create_router())

    async def run(self):
        await self._bot.set_my_commands(*create_commands())
        try:
            await self._dispatcher.start_polling(self._bot)
        except asyncio.CancelledError:
            logging.info("Бот остановлен")
        finally:
            await self._bot.session.close()

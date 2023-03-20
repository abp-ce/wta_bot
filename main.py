import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.redis import RedisStorage

from app.config import settings
from app.handlers import router

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    dp = Dispatcher(storage=RedisStorage.from_url(url=settings.redis_host))
    dp.include_router(router)
    bot = Bot(token=settings.bot_token)
    commands = [
        types.BotCommand(command="menu", description="Выберите опцию"),
        types.BotCommand(command="cancel", description="Отменить действие"),
    ]
    await bot.set_my_commands(commands)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

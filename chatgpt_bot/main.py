from utils.initialization_bot import create_bot
from config.bot_config import config
import handlers.handle_message as handlers
from aiogram.filters import Command
from middlewares.album_middleware import AlbumMiddleware

from aiogram import F
import asyncio


async def main():
    bot, dp = await create_bot(config.TELEGRAM_TOKEN)

    dp.message.register(handlers.start_command, Command('start'))
    dp.message.register(handlers.handle_message, F.text & F.text.startswith('#'))
    dp.message.register(handlers.handle_photos, F.photo | F.text.startswith('#'))

    dp.message.middleware(AlbumMiddleware())

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())

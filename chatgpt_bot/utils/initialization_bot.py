__all__ = []

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage


async def create_bot(token: str):
    bot = Bot(token=token)
    dp = Dispatcher(storage=MemoryStorage())
    return bot, dp

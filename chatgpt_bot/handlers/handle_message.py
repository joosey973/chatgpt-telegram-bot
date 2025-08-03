from aiogram.types import Message


async def start_command(message: Message) -> Message:
    await message.reply('Привет! Я бот ChatGpt-4o специально для группы Проект X :)')


async def handle_message(message: Message) -> Message:
    pass


async def handle_photos(message: Message, album: list = None) -> Message:
    pass

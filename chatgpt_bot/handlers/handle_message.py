from aiogram.types import Message

from services.message_prompt import chatgpt_client


async def start_command(message: Message) -> Message:
    await message.reply('Привет! Я бот ChatGpt-4o специально для группы Проект X :)')


async def handle_message(message: Message) -> Message:
    prompt_text = message.text
    prompt_text = prompt_text[prompt_text.find('#') + 1:].strip()
    answer_from_chatgpt = await chatgpt_client.get_simple_message_answer(prompt_text)
    answer_from_chatgpt = answer_from_chatgpt.replace('###', '').replace('**', '')

    await message.reply(f'{answer_from_chatgpt}')


async def handle_photos(message: Message, album: list = None) -> Message:
    caption = message.caption if not album else album[0].caption
    if not caption:
        return

    if album:
        pass
    else:
        print(caption)
        print(message.photo[-1])

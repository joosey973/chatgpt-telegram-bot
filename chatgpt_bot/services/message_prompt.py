import httpx

from openai import AsyncOpenAI
from config.bot_config import config
import aiohttp
import base64


class ChatGptClient:
    def __init__(self):
        if not config.OPENAI_API_KEY:
            raise ValueError('Не рабочий токен ChatGpt')
        self.transport = httpx.AsyncHTTPTransport(proxy=config.PROXY_HTTP)
        self.http_client = httpx.AsyncClient(transport=self.transport, timeout=120.0)
        self.client = AsyncOpenAI(api_key=config.OPENAI_API_KEY, http_client=self.http_client)
        self.model = 'gpt-4o'
        self.timeout = aiohttp.ClientTimeout(total=30)

    async def _download_image(self, image_urls):
        list_of_bytes = []
        for image_url in image_urls:
            try:
                async with aiohttp.ClientSession(timeout=self.timeout) as session:
                    async with session.get(image_url) as response:
                        if response.status != 200:
                            return None

                        list_of_bytes.append(response.read())
            except Exception as e:
                return None

        return await list_of_bytes

    async def get_simple_message_answer(self, prompt_text):
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{
                'role': 'user',
                'content': [
                    {'type': 'text', 'text': prompt_text},
                ]
            }],
            temperature=0.1,
        )
        return response.choices[0].message.content

    async def get_answer_from_photos(self, image_urls, prompt):
        list_of_image_data = await self._download_image(image_urls)
        return await self.analyze_images(list_of_image_data, prompt)

    async def analyze_images(self, list_of_image_data, prompt):
        messages=[
            {
                'role': 'user',
                'content': [{
                    'type': 'text',
                    'text': prompt
                }]
            }
        ]
        for image_data in list_of_image_data:
            base64_image = base64.b64encode(image_data).decode('utf-8')
            messages.append({'type': 'image_url', 'image_url': {'url': f'data:image/jpeg;base64,{base64_image}'}})
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return response.choices[0].message.content


chatgpt_client = ChatGptClient()

import httpx

from openai import AsyncOpenAI
from config.bot_config import config


class ChatGptPrompt:
    def __init__(self):
        if not config.OPENAI_API_KEY:
            raise ValueError('Не рабочий токен ChatGpt')
        self.transport = httpx.AsyncHTTPTransport(proxy=HTTP_PROXY)
        self.http_client = httpx.AsyncClient(transport=self.transport, timeout=120.0)
        self.client = AsyncOpenAI(api_key=OPENAI_API_KEY, http_client=self.http_client)
        self.model = 'gpt-4o'

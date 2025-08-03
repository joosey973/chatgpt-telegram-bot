import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
    TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN', '')
    PROXY_HTTP = os.environ.get('PROXY_HTTP', '')


config = Config()

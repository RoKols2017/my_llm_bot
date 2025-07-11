import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
PROXYAPI_TOKEN = os.getenv("PROXYAPI_TOKEN")
GIGACHAT_TOKEN = os.getenv("GIGACHAT_TOKEN")
YANDEX_TOKEN = os.getenv("YANDEX_TOKEN")
LLM_DEFAULT = os.getenv("LLM_DEFAULT", "proxyapi")

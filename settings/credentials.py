import os
from dotenv import load_dotenv
from urllib.parse import quote

load_dotenv()

BOT_LOGIN = os.environ.get("BOT_LOGIN")
BOT_PASSWORD = os.environ.get("BOT_PASSWORD")

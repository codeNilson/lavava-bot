import os
from dotenv import load_dotenv

load_dotenv()

BOT_LOGIN = os.environ.get("BOT_LOGIN")
BOT_PASSWORD = os.environ.get("BOT_PASSWORD")

SITE_URL = os.environ.get("SITE_URL")
PLAYERS_API_URL = SITE_URL + os.environ.get("PLAYERS_API_URL")
TEAMS_API_URL = SITE_URL + os.environ.get("TEAMS_API_URL")
MATCHES_API_URL = SITE_URL + os.environ.get("MATCHES_API_URL")
AUTHENTICATION_API_URL = SITE_URL + os.environ.get("AUTHENTICATION_API_URL")

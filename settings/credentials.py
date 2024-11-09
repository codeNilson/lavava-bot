import os
from dotenv import load_dotenv

load_dotenv()

API_LOGIN = os.environ.get("API_LOGIN")
API_PASSWORD = os.environ.get("API_PASSWORD")

SITE_URL = os.environ.get("SITE_URL")
API_URL = SITE_URL + os.environ.get("API_URL")

from urllib.parse import urljoin
import os
from dotenv import load_dotenv

load_dotenv()

SITE_URL = os.environ.get("SITE_URL")
PLAYERS_API_URL = urljoin(SITE_URL, "players/api/v1/")
TEAMS_API_URL = urljoin(SITE_URL, "teams/api/v1/")
MAPS_API_URL = urljoin(SITE_URL, "maps/api/v1/")
MATCHES_API_URL = urljoin(SITE_URL, "matches/api/v1/")
AUTHENTICATION_API_URL = urljoin(SITE_URL, "api/v1/token/")

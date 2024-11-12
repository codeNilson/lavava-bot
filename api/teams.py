import aiohttp
import settings
from ..core.models.matches import Match


base_url = settings.TEAMS_API_URL
login = settings.BOT_LOGIN
password = settings.BOT_PASSWORD


async def create_team(team: list, match: Match) -> dict:

    async with aiohttp.ClientSession() as session:
        async with session.request("POST", base_url) as response:
            return await response.json()

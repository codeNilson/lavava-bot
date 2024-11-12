import aiohttp
import settings
from core.models.matches import Match


base_url = settings.MATCHES_API_URL
login = settings.BOT_LOGIN
password = settings.BOT_PASSWORD


async def create_match():

    # acrescentar tratamento de erro
    async with aiohttp.ClientSession() as session:
        async with session.request("POST", base_url) as response:
            match_data = await response.json()
            return Match(**match_data)

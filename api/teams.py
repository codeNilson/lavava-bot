import aiohttp
import settings


base_url = settings.TEAMS_API_URL
login = settings.API_LOGIN
password = settings.API_PASSWORD


async def create_team(team_a:list, team_b:list):

    async with aiohttp.ClientSession() as session:
        async with session.request("POST", base_url) as response:
            return await response.json()


async def get_player_by_user(uuid):
    url = f"{base_url}{uuid}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 404:
                return None
            data = await response.json()
            return data

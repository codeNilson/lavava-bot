import aiohttp
from core.models.player_model import PlayerModel
import settings


base_url = settings.PLAYERS_API_URL
login = settings.BOT_LOGIN
password = settings.BOT_PASSWORD


async def get_all_players() -> list[PlayerModel]:

    async with aiohttp.ClientSession() as session:
        async with session.request("GET", base_url) as response:
            player_data = await response.json()
            return list(map(lambda data: PlayerModel(**data), player_data))


async def get_player_by_user(uuid):
    url = f"{base_url}{uuid}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 404:
                return None
            data = await response.json()
            return PlayerModel(**data)

import aiohttp
import settings
from core.models.match_model import MatchModel


base_url = settings.TEAMS_API_URL
login = settings.BOT_LOGIN
password = settings.BOT_PASSWORD


async def create_team(team: list, match: MatchModel) -> dict:

    data = {
        "players_uuid": [],
        "match_uuid": match.uuid,
    }

    for player in team:
        data["players_uuid"].append(player.uuid)

    async with aiohttp.ClientSession() as session:
        async with session.request("POST", base_url, json=data) as response:
            team_data = await response.json()
            if response.status != 201:
                return {"error": team_data}
            return team_data

import aiohttp
import settings
from core import models


base_url = settings.TEAMS_API_URL
login = settings.BOT_LOGIN
password = settings.BOT_PASSWORD


async def create_team(team: models.TeamModel) -> dict:

    if not isinstance(team, models.TeamModel):
        raise ValueError("team must be an instance of TeamModel")

    data = {
        "players_uuid": team.players_uuids,
        "match_uuid": team.match.uuid,
    }

    async with aiohttp.ClientSession() as session:
        async with session.request("POST", base_url, json=data) as response:
            team_data = await response.json()
            if response.status != 201:
                return {"error": team_data}
            return team_data

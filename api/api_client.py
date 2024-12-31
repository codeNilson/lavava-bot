from contextlib import asynccontextmanager
import aiohttp
from api.token_manager import TokenManager
from api import models
import settings

CLIENT_CREDENTIALS = {
    "username": settings.BOT_LOGIN,
    "password": settings.BOT_PASSWORD,
}

API_ENDPOINTS = {
    "players": settings.PLAYERS_API_URL,
    "teams": settings.TEAMS_API_URL,
    "maps": settings.MAPS_API_URL,
    "matches": settings.MATCHES_API_URL,
}


class ApiClient:
    def __init__(self):

        self.token_manager = TokenManager(
            auth_endpoint=settings.AUTHENTICATION_API_URL,
            credentials=CLIENT_CREDENTIALS,
        )

    @asynccontextmanager
    async def _session_context(self):
        access_token = await self.token_manager.get_access_token()

        headers = {
            "Authorization": f"Bearer {access_token}",
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            yield session

    async def get_all_players(self) -> list[models.PlayerModel]:

        async with self._session_context() as session:
            async with session.get(API_ENDPOINTS.get("players")) as response:
                if response.status != 200:
                    return []
                players_data = await response.json()
                return [models.PlayerModel(**player) for player in players_data]

    async def get_player_by_user(self, username: str) -> models.PlayerModel:
        player_detail_endpoint = f"{API_ENDPOINTS.get('players')}{username}"
        async with self._session_context() as session:
            async with session.get(player_detail_endpoint) as response:
                if response.status == 404:
                    return None
                data = await response.json()
                return models.PlayerModel(**data)

    async def get_player_by_uid(self, uid: int) -> models.PlayerModel:
        player_detail_endpoint = f"{API_ENDPOINTS.get('players')}by-uid/{uid}"
        async with self._session_context() as session:
            async with session.get(player_detail_endpoint) as response:
                if response.status == 404:
                    return None
                data = await response.json()
                return models.PlayerModel(**data)

    async def create_match(self, data=None):
        async with self._session_context() as session:
            async with session.post(
                API_ENDPOINTS.get("matches"), json=data
            ) as response:
                match_data = await response.json()
                if response.status != 201:
                    return {"error": match_data}
                return models.MatchModel(**match_data)

    async def create_team(self, team: models.TeamModel) -> dict:

        if not isinstance(team, models.TeamModel):
            raise ValueError("team must be an instance of models.TeamModel")

        data = {
            "players_uuid": team.players_uuids,
            "match_uuid": team.match.uuid,
        }

        async with self._session_context() as session:
            async with session.post(API_ENDPOINTS.get("teams"), json=data) as response:
                team_data = await response.json()
                if response.status != 201:
                    return {"error": team_data}
                return team_data

    async def get_maps(self, map_name=None):
        async with self._session_context() as session:

            # if map_name is provided, return only the map with that name
            if map_name:
                async with session.get(
                    f"{API_ENDPOINTS.get('maps')}{map_name}"
                ) as response:
                    map_data = await response.json()
                    if response.status != 200:
                        return None
                    return models.MapModel(**map_data)

            # if map_name is not provided, return all maps
            async with session.get(API_ENDPOINTS.get("maps")) as response:
                maps_data = await response.json()
                return [models.MapModel(**mapa) for mapa in maps_data]


api_client = ApiClient()

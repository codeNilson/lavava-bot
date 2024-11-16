from pydantic import BaseModel
from core import models


class TeamModel(BaseModel):
    match: models.MatchModel | None = None
    players: list[models.PlayerModel]

    @property
    def players_uuids(self):
        return [player.uuid for player in self.players]

    @property
    def players_usernames(self):
        return f"{', '.join([player.username for player in self.players])}"

    def add_player(self, player: models.PlayerModel):
        if not isinstance(player, models.PlayerModel):
            raise ValueError("player must be an instance of PlayerModel")
        self.players.append(player)

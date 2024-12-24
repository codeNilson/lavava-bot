from pydantic import BaseModel
from api.models.player_model import PlayerModel
from api.models.match_model import MatchModel


class TeamModel(BaseModel):
    match: MatchModel | None = None
    players: list[PlayerModel]

    @property
    def players_uuids(self):
        return [player.uuid for player in self.players]

    @property
    def players_usernames(self):
        return f"{', '.join([player.username for player in self.players])}"

    def add_player(self, player: PlayerModel):
        if not isinstance(player, PlayerModel):
            raise ValueError("player must be an instance of PlayerModel")
        self.players.append(player)

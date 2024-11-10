from discord.ext import commands
from api.players import get_player_by_user
from core.models import PlayerModel


class Player(commands.Converter):
    async def convert(self, ctx, uuid):
        try:
            player_data = await get_player_by_user(uuid)
        except Exception as e:
            raise commands.BadArgument(str(e))
        return PlayerModel(**player_data)

from discord.ext import commands
from api.api_client import api_client


class Player(commands.Converter):
    async def convert(self, ctx, username):
        try:
            player_data = await api_client.get_player_by_user(username)
        except Exception as e:
            raise commands.BadArgument(str(e))
        return player_data

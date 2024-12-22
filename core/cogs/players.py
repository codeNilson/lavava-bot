import discord
from discord.ext import commands
from core.converters.player import Player


class Players(commands.Cog, name="PlayersCog"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="player", aliases=["jogador"])
    async def show_player(self, ctx, players: commands.Greedy[Player]):

        for player in players:
            await self._send_player_embed(ctx, player)

    async def _send_player_embed(self, ctx, player):
        discord_user = f"{str(player)}>"

        embed = discord.Embed(
            title=f"{player.username}",
            color=discord.Colour.random(),
            url=player.url,
        )

        embed.set_thumbnail(
            url=f"https://www.lavava.com.br/static/{player.main_agent['icon']}"
        )

        embed.add_field(
            name="Usuário",
            value=discord_user if player.discord_uid else "N/A",
        )
        embed.add_field(
            name="Agente Principal",
            value=player.main_agent["name"],
        )
        embed.add_field(name="Ranking", value=player.ranking)

        await ctx.send(embed=embed)

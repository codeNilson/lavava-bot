import discord
from discord import app_commands
from discord.ext import commands
from core.converters.player import Player


class Players(commands.Cog, name="PlayersCog"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="info", description="Mostra informações de um jogador.")
    @app_commands.describe(player="Nome de usuário (site) ou menção do jogador.")
    async def show_player(self, interaction: discord.Interaction, player: str = None):
        """
        Mostra informações de um ou mais jogadores. @mention ou username.
        """
        player = player or interaction.user.mention
        player = await Player().convert(interaction, player)

        await self._send_player_embed(interaction, player)

    async def _send_player_embed(
        self, interaction: discord.Interaction, player: Player
    ):

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
            value=player.mention,
        )
        embed.add_field(
            name="Agente Principal",
            value=player.main_agent["name"],
        )
        embed.add_field(name="Ranking", value=player.ranking)

        await interaction.response.send_message(embed=embed)

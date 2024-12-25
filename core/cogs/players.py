import discord
from discord import app_commands
from discord.ext import commands
from core.converters.player import Player
from core.ui.embeds import get_player_embed


class Players(commands.Cog, name="PlayersCog"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="info", description="Mostra informações de um jogador.")
    @app_commands.describe(member="@Jogador")
    async def show_player(
        self, interaction: discord.Interaction, member: discord.Member = None
    ):
        """
        Mostra informações de um ou mais jogadores. @mention ou username.
        """
        player = member or interaction.user
        player = await Player().convert(interaction, player)

        embed = get_player_embed(player)

        await interaction.response.send_message(embed=embed)

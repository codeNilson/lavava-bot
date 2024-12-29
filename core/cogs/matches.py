import asyncio
import random
import discord
from discord import app_commands
from discord.ext import commands
from api.api_client import api_client
from api import models
from core.ui.views import PlayersView
from core.ui.embeds import teams_embed
from core.ui.select import SelectMap
from utils import RoleID
import settings
from settings.errors import MissingPlayersException


class Matches(commands.Cog, name="MatchesCog"):

    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        self.channel = None
        self.players = []
        self.captain_blue = None
        self.captain_red = None
        self.team_blue = None
        self.team_red = None
        self.is_blue_captain_turn = True
        self.admin_cog: commands.Cog = self.bot.get_cog("AdminCog")

    @app_commands.command(name="sorteio", description="Inicia o sorteio dos capitães.")
    @app_commands.checks.has_role(RoleID.STAFF.value)
    async def draw_captains(self, interaction: discord.Interaction) -> None:
        """
        Begin the draft process by randomly selecting two players to be the captains.
        """

        # Load all players from the API
        await self._load_players()

        # Select only players that want to be drafted
        wants_to_be_drafted = [
            player
            for player in self.players
            if player.include_in_draft and player.discord_uid
        ]

        # If there's less than 2 players, return
        if len(wants_to_be_drafted) < 2:
            await interaction.response.send_message(
                f"Só é possível sortear com no mínimo 2 jogadores. Atualmente há {len(wants_to_be_drafted)} jogadores disponíveis."
            )
            return

        # Randomly select two players to be the captains
        self.captain_blue = random.choice(wants_to_be_drafted)
        wants_to_be_drafted.remove(
            self.captain_blue
        )  # Remove the captain from the list

        self.captain_red = random.choice(wants_to_be_drafted)
        wants_to_be_drafted.remove(self.captain_red)  # Remove the captain from the list

        # Remove the captains from the list of available players
        self.players.remove(self.captain_blue)
        self.players.remove(self.captain_red)

        self.channel = interaction.channel

        await interaction.response.send_message(
            f"Capitão 🔵: {self.captain_blue.mention}\nCapitão 🔴: {self.captain_red.mention}"
        )

        await asyncio.sleep(2)

        # Call make_teams function
        await self._choose_teams(interaction)

    async def _load_players(self) -> None:
        """Load all players from the api"""
        self.players = await api_client.get_all_players()

        # Check if there are enough players to start the draft
        if len(self.players) < 10:
            raise MissingPlayersException(
                "⚠️ Não há jogadores suficientes para o sorteio."
            )

    async def _choose_teams(self, interaction: discord.Interaction) -> None:

        self.team_blue = models.TeamModel(players=[self.captain_blue])
        self.team_red = models.TeamModel(players=[self.captain_red])

        blue_role = interaction.guild.get_role(RoleID.BLUE.value)
        red_role = interaction.guild.get_role(RoleID.RED.value)
        roles = [blue_role, red_role]

        # Clear team blue and team red roles
        for role in roles:
            await self.admin_cog.reset_role(role)

        # Reset self.is_blue_captain_turn
        self.is_blue_captain_turn = True

        await self.channel.send("Hora de escolher seus times!")

        await self.channel.send(
            f"🔵{self.captain_blue.mention} você começa!", delete_after=15
        )

        # Send the message with the buttons to choose the players
        update_view = await self._update_view()
        message = await self.channel.send(
            "Escolha um jogador disponível:", view=update_view
        )

        update_view.message = message

        # Wait until all players are chosen
        timed_out = await update_view.wait()

        # If the view timed out, end the function
        if timed_out:
            return

        view = discord.ui.View(timeout=180)
        view.add_item(SelectMap(cog=self))

        message_response = await interaction.followup.send(
            content="Capitães, escolham o mapa:", view=view, wait=True
        )

        new_timed_out = await view.wait()

        if new_timed_out:  # adicionar mensagem de feedback
            return

        embed_team = await teams_embed(self.team_blue, self.team_red, view.map_chosen)

        await message_response.edit(
            content=f"O mapa escolhido foi {view.map_chosen}.",
            embed=embed_team,
            view=None,
        )

        await self.create_match(teams=[self.team_blue, self.team_red])

    async def _update_view(self) -> PlayersView:

        view = PlayersView(cog=self, timeout=180)

        for player in self.players:
            await view.add_player_button(player=player)

        return view

    async def create_match(self, teams: list[models.TeamModel]):
        """Cria as equipes na API."""

        # Create a new match in the API
        match = await api_client.create_match()
        # Register the teams in the match
        for team in teams:
            team.match = match
            await api_client.create_team(team=team)
        settings.LOGGER.info("Equipes criadas com sucesso.")

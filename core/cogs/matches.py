import asyncio
import random
import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View
from api.api_client import api_client
from api import models
from core.ui.embeds import teams_embed
from core.ui.views import PlayersView
from utils import move_user_to_channel, RoleID, ChannelID
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

        team_blue = models.TeamModel(players=[self.captain_blue])
        team_red = models.TeamModel(players=[self.captain_red])

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
        view = await self._update_view(team_blue, team_red, blue_role, red_role)
        message = await self.channel.send("Escolha um jogador disponível:", view=view)

        view.message = message

        # Wait until all players are chosen
        timed_out = await view.wait()

        if timed_out:
            return
        await self.create_match(teams=[team_blue, team_red])

    async def _update_view(
        self,
        team_blue,
        team_red,
        blue_role: discord.Role,
        red_role: discord.Role,
    ) -> View:
        view = PlayersView(timeout=180)

        for player in self.players:

            button = Button(
                label=player.username,
                style=discord.ButtonStyle.secondary,
                custom_id=player.username,
            )

            async def button_callback(
                interaction: discord.Interaction, player: models.PlayerModel = player
            ):
                """Callback para cada botão."""

                current_captain = (
                    self.captain_blue if self.is_blue_captain_turn else self.captain_red
                )
                next_captain = (
                    self.captain_red if self.is_blue_captain_turn else self.captain_blue
                )

                blue_channel = interaction.guild.get_channel(ChannelID.BLUE.value)
                red_channel = interaction.guild.get_channel(ChannelID.RED.value)

                # if the player is not the current captain then return
                if interaction.user.id != current_captain.discord_uid:
                    await interaction.response.send_message(
                        "Não é sua vez de escolher!",
                        ephemeral=True,
                        delete_after=5,
                    )
                    return

                # add player to the team of the current captain
                team = team_blue if self.is_blue_captain_turn else team_red
                team.add_player(player)

                # remove player from the list of available players
                self.players.remove(player)

                # add role and move player to the channel
                member = await player.to_member(interaction)
                if member:
                    channel = blue_channel if self.is_blue_captain_turn else red_channel
                    await member.add_roles(
                        blue_role if self.is_blue_captain_turn else red_role
                    )
                    await move_user_to_channel(member, channel)

                # if the teams are full, show the teams and create the match
                if len(team_blue.players) == 5 and len(team_red.players) == 5:

                    embed_team = teams_embed(team_blue, team_red)

                    await interaction.response.edit_message(
                        content="Todos os jogadores foram escolhidos!",
                        view=None,
                        embed=embed_team,
                    )

                    view.stop()

                # if the team is not full change the current captain and start again the process
                else:
                    # this lets the captain of team red to choose two players in a row if there's only three remaining players
                    if len(team_red.players) != 4:
                        next_captain = (
                            self.captain_red
                            if self.is_blue_captain_turn
                            else self.captain_blue
                        )
                        self.is_blue_captain_turn = not self.is_blue_captain_turn
                        emoji = "🔵" if self.is_blue_captain_turn else "🔴"
                        message_content = f"Jogador {player.mention} foi escolhido! Agora é a vez de {emoji + next_captain.mention} escolher."
                    else:
                        message_content = f"Jogador {player.mention} foi escolhido! 🔴{current_captain.mention}, você tem o direito a mais uma escolha."

                    for button in view.children:
                        if button.custom_id == player.username:
                            button.disabled = True
                            button.style = (
                                discord.ButtonStyle.primary
                                if current_captain == self.captain_blue
                                else discord.ButtonStyle.danger
                            )

                    await interaction.response.edit_message(
                        content=message_content,
                        view=view,
                    )

            button.callback = button_callback
            view.add_item(button)
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

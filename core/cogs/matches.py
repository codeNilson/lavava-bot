import asyncio
import random
import discord
from discord.ext import commands
from discord.ui import Button
import settings
from api.api_client import api_client
from api import models
from settings.errors import MissingPlayersException
from utils.embeds import show_teams
from utils.admin import move_user_to_channel
from utils.enums import RoleID, ChannelID
from core.ui.view import PlayersView as View


class Matches(commands.Cog, name="MatchesCog"):

    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        self.players = []
        self.captain_blue = None
        self.captain_red = None
        self.blue_channel = self.bot.get_channel(ChannelID.BLUE.value)
        self.red_channel = self.bot.get_channel(ChannelID.RED.value)
        self.is_blue_captain_turn = True
        self.admin_cog = self.bot.get_cog("AdminCog")

    @commands.has_role(RoleID.STAFF.value)
    @commands.command(name="draw_captains", aliases=["sorteio"])
    async def draw_captains(self, ctx):
        """
        Begin the draft process by randomly selecting two players to be the captains.
        """

        # Select only players that wants to be drafted
        wants_to_be_drafted = [
            player
            for player in self.players
            if player.include_in_draft and player.discord_uid
        ]

        # If there's less than 2 players, return
        if len(wants_to_be_drafted) < 2:
            await ctx.send(
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

        await ctx.send(
            f"Capitão 🔵: {self.captain_blue.mention}\nCapitão 🔴: {self.captain_red.mention}"
        )

        await asyncio.sleep(2)

        # call make_teams function
        await self._choose_teams(ctx)

    @draw_captains.before_invoke
    async def _load_players(self, ctx) -> None:  # Pode ser mais rápido
        """Load all players from the api"""
        self.players = await api_client.get_all_players()

        # Check if there are enough players to start the draft
        if len(self.players) < 10:
            raise MissingPlayersException(
                "⚠️ Não há jogadores suficientes para o sorteio."
            )

    async def _choose_teams(self, ctx):

        team_blue = models.TeamModel(players=[self.captain_blue])
        team_red = models.TeamModel(players=[self.captain_red])

        blue_role = ctx.guild.get_role(RoleID.BLUE.value)
        red_role = ctx.guild.get_role(RoleID.RED.value)

        # Clear team blue and team red roles
        await self.admin_cog.remove_roles(roles=[blue_role, red_role])

        # Reset self.is_blue_captain_turn
        self.is_blue_captain_turn = True

        await ctx.send("Hora de escolher seus times!")

        await ctx.send(f"🔵{self.captain_blue.mention} você começa!")

        # Send the message with the buttons to choose the players
        view = await self._update_view(ctx, team_blue, team_red, blue_role, red_role)
        await ctx.send(
            "Escolha um jogador disponível:",
            view=view,
        )

        # Wait until all players are chosen
        await view.wait()

        if view.timed_out:
            await ctx.send(
                "⏳ Tempo esgotado! Nem todos os jogadores foram escolhidos."
            )
            return

        await self.create_match(teams=[team_blue, team_red])

    async def _update_view(self, ctx, team_blue, team_red, blue_role, red_role):
        view = View(ctx, timeout=10)

        for player in self.players:

            button = Button(
                label=player.username,
                style=discord.ButtonStyle.secondary,
                custom_id=player.username,
            )

            async def button_callback(interaction, player=player):
                """Callback para cada botão."""

                current_captain = (
                    self.captain_blue if self.is_blue_captain_turn else self.captain_red
                )
                next_captain = (
                    self.captain_red if self.is_blue_captain_turn else self.captain_blue
                )

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
                    channel = (
                        self.blue_channel
                        if self.is_blue_captain_turn
                        else self.red_channel
                    )
                    await member.add_roles(
                        blue_role if self.is_blue_captain_turn else red_role
                    )
                    await move_user_to_channel(member, channel)

                # if the teams is full, show the teams and create the match
                if len(team_blue.players) == 5 and len(team_red.players) == 5:
                    await interaction.response.edit_message(
                        content="Todos os jogadores foram escolhidos!",
                        view=None,
                    )
                    await view.stop()

                # if the team is not full change the current captain and start again the process
                else:
                    # this lets the captain of team b to choose two players in a row if there's only three remaining players
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

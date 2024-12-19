import asyncio
import random
import discord
from discord.ext import commands
from discord.ui import View, Button
import settings
from api.api_client import api_client
from core import models
from utils.embeds import show_teams
from utils.roles import clear_roles
from utils.admin import move_user_to_channel
from utils.enums import RoleID, ChannelID


class Matches(commands.Cog, name="MatchesCog"):

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.players = []
        self.all_chosen_event = None

    @commands.has_role(1309641234868080710)
    @commands.command(name="draw_captains", aliases=["sorteio"])
    async def draw_captains(self, ctx):
        """
        Begin the draft process by randomly selecting two players to be the captains.
        """

        # Select only players that wants to be drafted
        wants_to_be_drafted = [
            player for player in self.players if player.include_in_draft
        ]

        # If there's less than 2 players, return
        if len(wants_to_be_drafted) < 2:
            await ctx.send(
                f"Só é possível sortear com no mínimo 2 jogadores. Atualmente há {len(wants_to_be_drafted)} jogadores disponíveis."
            )
            return

        # Randomly select two players to be the captains
        captain_blue = random.choice(wants_to_be_drafted)
        wants_to_be_drafted.remove(captain_blue) # Remove the captain from the list
        captain_red = wants_to_be_drafted[0]

        # Remove the captains from the list of players
        self.players.remove(captain_blue)
        self.players.remove(captain_red)

        await ctx.send(
            f"Capitão A: <@{captain_blue.discord_uid}>\nCapitão B: <@{captain_red.discord_uid}>"
        )

        await asyncio.sleep(2)

        # call make_teams function
        await ctx.invoke(self.choose_teams, captain_blue=captain_blue, captain_red=captain_red)

    @draw_captains.before_invoke
    async def load_players(self, ctx) -> None:  # Pode ser mais rápido
        """Load all players from the api"""
        try:
            self.players = await api_client.get_all_players()
        except settings.LoginError:
            await ctx.send(
                "No momento não é possível carregar os jogadores. Por favor, tente mais tarde"
            )
            raise commands.CommandError("Erro ao carregar jogadores.")
        
        # Check if there are enough players to start the draft
        if len(self.players) < 10:
            await ctx.send("Não há jogadores suficientes para o sorteio.")
            raise commands.CommandError(
                f"É necessário ter pelo menos 10 jogadores para concluir o sorteio. Total de jogadores: {len(self.players)}"
            )

    async def choose_teams(self, ctx, captain_blue, captain_red):

        self.all_chosen_event = asyncio.Event()

        team_blue = models.TeamModel(players=[captain_blue])
        team_red = models.TeamModel(players=[captain_red])

        blue_role = ctx.guild.get_role(RoleID.BLUE)
        red_role = ctx.guild.get_role(RoleID.RED)

        blue_channel = ctx.guild.get_channel(ChannelID.BLUE)
        red_channel = ctx.guild.get_channel(ChannelID.RED)

        # Clear team blue and team red roles
        await ctx.invoke(self.bot.getcommand("clear_roles"), roles=[blue_role, red_role])

        choose_captain_blue = True

        await ctx.send("Hora de escolher seus times!")

        await clear_roles(roles=[blue_role, red_role])

        await ctx.send(f"<@{captain_blue.discord_uid}> você começa!")

        async def update_view():
            view = View(timeout=180)

            for player in self.players:

                button = Button(
                    label=player.username,
                    style=discord.ButtonStyle.secondary,
                    custom_id=player.username,
                )

                async def button_callback(interaction, player=player):
                    """Callback para cada botão."""
                    nonlocal choose_captain_blue

                    current_captain = captain_blue if choose_captain_blue else captain_red
                    next_captain = captain_red if choose_captain_blue else captain_blue

                    # if the player is not the current captain then return
                    if interaction.user.id != current_captain.discord_uid:
                        await interaction.response.send_message(
                            "Não é sua vez de escolher!",
                            ephemeral=True,
                            delete_after=5,
                        )
                        return

                    # add player to the team of the current captain
                    team = team_blue if choose_captain_blue else team_red
                    team.add_player(player)

                    # remove player from the list of available players
                    self.players.remove(player)

                    # add role and move player to the channel
                    member = await player.to_member(interaction)
                    if member:
                        channel = blue_channel if choose_captain_blue else red_channel
                        member.add_roles(blue_role if choose_captain_blue else red_role)
                        move_user_to_channel(member, channel)
                        
                    # if the teams is full, show the teams and create the match
                    if len(team_blue.players) == 5 and len(team_red.players) == 5:
                        self.all_chosen_event.set()
                        await interaction.response.edit_message(
                            content="Todos os jogadores foram escolhidos!",
                            view=None,
                        )

                    # if the team is not full, change the current captain and start again the process
                    else:
                        # this lets the captain of team b to choose two players in a row if there's only three remaining players
                        if len(team_red.players) != 4:
                            next_captain = captain_red if choose_captain_blue else captain_blue
                            choose_captain_blue = not choose_captain_blue
                            message_content = f"Jogador {player.username} foi escolhido! Agora é a vez de <@{next_captain.discord_uid}> escolher."
                        else:
                            message_content = f"Jogador {player.username} foi escolhido! Agora é a vez de <@{current_captain.discord_uid}> escolher."

                        await interaction.response.edit_message(
                            content=message_content,
                            view=await update_view(),
                        )

                button.callback = button_callback
                view.add_item(button)
            return view

        await ctx.send(
            "Escolha um jogador disponível:",
            view=await update_view(),
        )

        try:
            await asyncio.wait_for(self.all_chosen_event.wait(), timeout=180)
        except asyncio.TimeoutError:
            await ctx.send(
                "⏳ Tempo esgotado! Nem todos os jogadores foram escolhidos."
            )
            return

        await show_teams(ctx, team_blue, team_red)

        await self.create_match(teams=[team_blue, team_red])

    async def create_match(self, teams: list[models.TeamModel]):
        """Cria as equipes na API."""
        match = await api_client.create_match()
        for team in teams:
            team.match = match
            await api_client.create_team(team=team)
        settings.LOGGER.info("Equipes criadas com sucesso.")

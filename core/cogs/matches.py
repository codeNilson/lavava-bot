import asyncio
import discord
from discord.ext import commands
from discord.ui import View, Button
from api.api_client import api_client
from core import models


class Matches(commands.Cog, name="MatchesCog"):

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.players = []
        self.all_chosen_event = asyncio.Event()

    @commands.command(name="sortear")
    async def draw_captains(self, ctx):
        captain_a = next(
            player for player in self.players if player.username == "aro might"
        )
        captain_b = next(
            player for player in self.players if player.username == "taifuzinha"
        )

        self.players.remove(captain_a)
        self.players.remove(captain_b)

        await ctx.send(
            f"Capitão A: <@{captain_a.discord_uid}>\nCapitão B: <@{captain_b.discord_uid}>"
        )

        await asyncio.sleep(2)

        # call make_teams function
        await ctx.invoke(self.choose_teams, captain_a=captain_a, captain_b=captain_b)

    @draw_captains.before_invoke
    async def load_players(self, ctx) -> None:  # Pode ser mais rápido
        """Load all players from the api"""
        self.players = list(await api_client.get_all_players())

    async def choose_teams(self, ctx, captain_a, captain_b):

        team_a = models.TeamModel(players=[captain_a])
        team_b = models.TeamModel(players=[captain_b])

        choose_captain_a = True

        await ctx.send("Hora de escolher seus times!")

        async def update_view():
            view = View(timeout=120)

            for player in self.players:

                button = Button(
                    label=player.username,
                    style=discord.ButtonStyle.secondary,
                    custom_id=player.username,
                )

                async def button_callback(interaction, player=player):
                    """Callback para cada botão."""
                    nonlocal choose_captain_a

                    current_captain = captain_a if choose_captain_a else captain_b
                    next_captain = captain_b if choose_captain_a else captain_a

                    if interaction.user.id != current_captain.discord_uid:
                        await interaction.response.send_message(
                            f"É a vez de <@{current_captain.discord_uid}> escolher!",
                            ephemeral=True,
                            delete_after=5,
                        )
                        return

                    # Adiciona o jogador ao time do jogador que o escolheu
                    if choose_captain_a:
                        team_a.add_player(player)
                    else:
                        team_b.add_player(player)

                    # Remove o jogador da lista
                    self.players.remove(player)

                    if not self.players:
                        self.all_chosen_event.set()
                        await interaction.response.edit_message(
                            content="Todos os jogadores foram escolhidos!",
                            view=None,
                        )

                    else:

                        # Troca o capitão atual
                        choose_captain_a = not choose_captain_a

                        # Responde à interação

                        await interaction.response.edit_message(
                            content=f"Jogador {player.username} foi escolhido! Agora é a vez de <@{next_captain.discord_uid}> escolher.",
                            view=await update_view(),
                        )

                button.callback = button_callback
                view.add_item(button)
            return view

        await ctx.send(f"<@{captain_a.discord_uid}> você começa!")

        await ctx.send(
            "Escolha um jogador disponível:",
            view=await update_view(),
        )

        try:
            await asyncio.wait_for(self.all_chosen_event.wait(), timeout=120)
        except asyncio.TimeoutError:
            await ctx.send("Tempo esgotado! Nem todos os jogadores foram escolhidos.")

        await ctx.send(
            f"Time A: {team_a.players_usernames}\n"
            f"Time B: {team_b.players_usernames}"
        )

        await ctx.invoke(self.create_teams, teams=[team_a, team_b])

    async def create_teams(self, ctx, teams: list[models.TeamModel]):
        """Cria as equipes na API."""
        match = await api_client.create_match()
        for team in teams:
            team.match = match
            await api_client.create_team(team=team)

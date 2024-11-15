import asyncio
import random
import discord
from discord.ext import commands
from discord.ui import View, Button
from api.players import get_all_players
from api.teams import create_team
from api.matches import create_match


class Matches(commands.Cog, name="MatchesCog"):

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.players = []

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
        self.players = [player for player in await get_all_players()]

    async def choose_teams(self, ctx, captain_a, captain_b):

        captain_a_team = [captain_a]
        captain_b_team = [captain_b]
        choose_captain_a = True

        await ctx.send("Hora de escolher seus times!")

        async def update_view():
            view = View(timeout=120)
            colors = [
                discord.ButtonStyle.green,
                discord.ButtonStyle.red,
                discord.ButtonStyle.blurple,
            ]

            for player in self.players:

                button = Button(
                    label=player.username,
                    style=random.choice(colors),
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
                        )
                        return

                    # Adiciona o jogador ao time do jogador que o escolheu
                    if choose_captain_a:
                        captain_a_team.append(player)
                    else:
                        captain_b_team.append(player)

                    # Remove o jogador da lista
                    self.players.remove(player)

                    if not self.players:
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

        await asyncio.sleep(90)

        await ctx.send(
            f"Time A: {', '.join([p.username for p in captain_a_team])}\n"
            f"Time B: {', '.join([p.username for p in captain_b_team])}"
        )

        await ctx.invoke(self.create_teams, teams=[captain_a_team, captain_b_team])

    async def create_teams(self, ctx, teams: list):
        """Cria as equipes na API."""
        match = await create_match()
        team_a, team_b = teams
        await create_team(team=team_a, match=match)
        await create_team(team=team_b, match=match)

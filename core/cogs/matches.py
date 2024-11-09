import random
import discord
from discord.ext import commands
from api.players import get_all_players
from core.converters.models import PlayerModel


class Matches(commands.Cog, name="MatchesCog"):

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.players = []

    @commands.command(name="sortear")
    async def draw_captains(
        self, ctx
    ):  # adicionar opção para retirar jogadores da lista
        captain_a, captain_b = random.sample(self.players, 2)
        captain_a = PlayerModel(**captain_a)
        captain_b = PlayerModel(**captain_b)
        await ctx.send(
            f"Capitão A: <@{captain_a.username}>\nCapitão B: <@{captain_b.username}>"
        )
        await ctx.invoke(self.make_teams, captain_a=captain_a, captain_b=captain_b)

    @draw_captains.before_invoke
    async def load_players(self, ctx) -> None:  # could be more fast
        self.players = await get_all_players()

    async def make_teams(self, ctx, captain_a, captain_b):
        ctx.send("Hora de escolher seus times!")
        choose_captain_a = True
        await ctx.send(f"<@{captain_a.username}> você começa!")

        # def valide_player(self, mensagem):
        #     return (
        #         mensagem.author == captain_a
        #         if captain_a
        #         else captain_b
        #         and mensagem.content in [player["username"] for player in self.players]
        #     )

        while self.players:
            await ctx.send(
                "Digite o nick do jogador que deseja adicionar ao seu time. As opções são:"
            )
            for player in self.players:
                await ctx.send(
                    ", ".join([player["username"] for player in self.players])
                )
            break

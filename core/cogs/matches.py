import asyncio
import random
from discord.ext import commands
from api.players import get_all_players
from core.models import PlayerModel


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

        # Removing captains from players list
        self.players.remove(captain_a)
        self.players.remove(captain_b)

        # convertendo os capitães para PlayerModel
        captain_a = PlayerModel(**captain_a)
        captain_b = PlayerModel(**captain_b)

        await ctx.send(
            f"Capitão A: <@{captain_a.username}>\nCapitão B: <@{captain_b.username}>"
        )
        asyncio.sleep(2)

        # call make_teams function
        await ctx.invoke(self.choose_teams, captain_a=captain_a, captain_b=captain_b)

    @draw_captains.before_invoke
    async def load_players(self, ctx) -> None:  # could be more fast
        """Load all players from the api"""
        self.players = await get_all_players()

    async def choose_teams(self, ctx, captain_a, captain_b):

        captain_a_team = [captain_a.username]
        captain_b_team = [captain_b.username]

        await ctx.send("Hora de escolher seus times!")
        choose_captain_a = True
        await ctx.send(f"<@{captain_a.username}> você começa!")

        def valide_player(message):
            capitao_atual = captain_a if choose_captain_a else captain_b
            print(capitao_atual.get_discord_uid())
            print(message.author.id)
            print(message.author.id == capitao_atual.get_discord_uid())
            return (
                message.author.id == capitao_atual.get_discord_uid()
                and message.content in [player["username"] for player in self.players]
            )

        while self.players:  # what if the list has more than 10 players?
            await ctx.send(
                "Digite o nick do jogador que deseja adicionar ao seu time. As opções são:"
            )
            await ctx.send(", ".join([player["username"] for player in self.players]))

            choose = await self.bot.wait_for("message", check=valide_player)

            # Adicionando o jogador ao time do capitão
            if choose_captain_a:
                captain_a_team.append(choose.content)
            else:
                captain_b_team.append(choose.content)

            self.players = [
                player
                for player in self.players
                if player["username"] != choose.content
            ]

            choose_captain_a = not choose_captain_a
            proximo_capitao = captain_a if choose_captain_a else captain_b
            await ctx.send(f"Agora é a vez de <@{proximo_capitao.username}> escolher.")

        assert len(self.players) == 0
        assert len(captain_a_team) == 5
        assert len(captain_b_team) == 5

        await ctx.send(
            f"Times definidos!\nTime A: {', '.join(captain_a_team)}\nTime B: {', '.join(captain_b_team)}"
        )

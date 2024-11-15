import random
from time import sleep
from discord.ext import commands
from api.players import get_all_players
from api.teams import create_team
from api.matches import create_match


class Matches(commands.Cog, name="MatchesCog"):

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.players = []

    @commands.command(name="sortear")
    async def draw_captains(
        self, ctx
    ):  # adicionar opção para retirar jogadores da lista
        captain_a = next(
            player for player in self.players if player.username == "aro might"
        )
        captain_b = next(
            player for player in self.players if player.username == "neskauzz"
        )

        self.players.remove(captain_a)
        self.players.remove(captain_b)

        await ctx.send(
            f"Capitão A: <@{captain_a.username}>\nCapitão B: <@{captain_b.username}>"
        )
        sleep(2)

        # call make_teams function
        await ctx.invoke(self.choose_teams, captain_a=captain_a, captain_b=captain_b)

    @draw_captains.before_invoke
    async def load_players(self, ctx) -> None:  # could be more fast
        """Load all players from the api"""
        self.players = [
            player
            for player in await get_all_players()
            if player.username
            in [
                "aro might",
                "neskauzz",
                "denilson",
            ]
        ]

    async def choose_teams(self, ctx, captain_a, captain_b):

        captain_a_team = [captain_a]
        captain_b_team = [captain_b]

        await ctx.send("Hora de escolher seus times!")
        choose_captain_a = True

        await ctx.send(f"<@{captain_a.username}> você começa!")

        def valide_player(message):
            capitao_atual = captain_a if choose_captain_a else captain_b
            return (
                message.author.id == capitao_atual.get_discord_uid()
                and message.content in [player.username for player in self.players]
            )

        while self.players:  # what if the list has more than 10 players?
            await ctx.send(
                "Digite o nick do jogador que deseja adicionar ao seu time. As opções são:"
            )
            await ctx.send(", ".join([player.username for player in self.players]))

            choose = await self.bot.wait_for("message", check=valide_player)

            # Adicionando o jogador ao time do capitão
            chossen_player = next(
                player for player in self.players if player.username == choose.content
            )
            if choose_captain_a:
                captain_a_team.append(chossen_player)
            else:
                captain_b_team.append(chossen_player)

            # Removendo o jogador da lista de jogadores disponíveis
            self.players.remove(chossen_player)

            choose_captain_a = not choose_captain_a
            proximo_capitao = captain_a if choose_captain_a else captain_b
            if self.players:
                await ctx.send(
                    f"Agora é a vez de <@{proximo_capitao.username}> escolher."
                )
        await ctx.send(
            f"Times definidos!\nTime A: {', '.join([player.username for player in captain_a_team])}\nTime B: {', '.join([player.username for player in captain_b_team])}"
        )

        await ctx.invoke(self.create_teams, teams=[captain_a_team, captain_b_team])

    async def create_teams(self, ctx, teams: list):

        match = await create_match()

        team_a, team_b = teams
        await create_team(team=team_a, match=match)
        await create_team(team=team_b, match=match)

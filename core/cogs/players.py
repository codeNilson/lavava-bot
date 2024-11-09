import discord
from discord.ext import commands
from core.converters.player import Player


class Players(commands.Cog, name="PlayersCog"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def player(self, ctx, player: Player):

        discord_uid = player.get_discord_uid()
        discord_user = f"<@{discord_uid}>" if discord_uid else player.username

        embed = discord.Embed(
            title=f"{player.username}",
            color=discord.Colour.random(),
            url=player.url,
        )

        file = discord.File(
            "C:/Users/Denilson/Documents/GitHub/valorant-amateur-league/gamedata/static/gamedata/assets/agents/icons/omen_display_icon.webp",
            filename="omen_display_icon.webp",
        )
        embed.set_image(url="attachment://omen_display_icon.webp")

        embed.add_field(
            name="Usuário",
            value=discord_user,
        )
        embed.add_field(
            name="Agente Principal",
            value=player.main_agent["name"],
        )
        embed.add_field(name="Ranking", value=player.ranking)
        embed.add_field(name="Tier", value=player.tier.tier)

        await ctx.send(file=file, embed=embed)

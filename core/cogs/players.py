import discord
from discord.ext import commands
from core.converters.player import Player


class Players(commands.Cog, name="PlayersCog"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def player(self, ctx, player: Player):
        embed = discord.Embed(
            title=player.username, description=player.uuid, color=discord.Color.red()
        )
        embed.set_thumbnail(url="http://127.0.0.1:8000/static/" + player.tier.small_icon)

        url = "http://127.0.0.1:8000/static/" + player.tier.small_icon
        print(url)

        embed.add_field(name="Username", value=player.username)
        embed.add_field(name="Email", value=player.email)
        embed.add_field(name="Tier", value=player.tier.tier)
        embed.add_field(name="Division", value=player.tier.division)
        await ctx.send(embed=embed)

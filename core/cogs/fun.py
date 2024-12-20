from discord.ext import commands


class Fun(commands.Cog, name="FunCog"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if message.content.lower() == "ping":
            await message.reply("pong")
        if message.content.lower() in ("natan", "nathan"):
            await message.add_reaction("🐂")
        if message.content.lower() == "eric":
            await message.add_reaction("🃏")

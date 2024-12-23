from discord.ext import commands


class Fun(commands.Cog, name="FunCog"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def fun_reactions(self, message):
        if message.author == self.bot.user:
            return
        if message.content.lower() == "ping":
            await message.reply("pong")
        if message.content.lower() in ("natan", "nathan"):
            await message.add_reaction("🐂")
        if message.content.lower() == "eric":
            await message.add_reaction("💩")
        if message.content.lower() in ("leo", "leozin"):
            await message.add_reaction("🤏🏻")
        if message.content.lower() in ("catherine", "cath", "cat"):
            await message.add_reaction("👩🏻‍🦯‍➡️")

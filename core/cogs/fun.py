import discord
from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reactions = {
            "ping": "pong",
            "natan": "🐂",
            "nathan": "🐂",
            "eric": "💩",
            "leo": "🤏🏻",
            "leozin": "🤏🏻",
            "catherine": "👩🏻‍🦯",
            "cath": "👩🏻‍🦯",
            "cat": "👩🏻‍🦯",
        }

    @commands.Cog.listener("on_message")
    async def fun_reactions(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        content_lower = message.content.lower()
        if content_lower in self.reactions:
            reaction = self.reactions[content_lower]
            if reaction == "pong":
                await message.reply(reaction)
            else:
                await message.add_reaction(reaction)

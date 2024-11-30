from discord.ext import commands
import discord
from utils.cogs import add_cogs


class LavavaBot(commands.Bot):
    def __init__(self, command_prefix="!", intents=discord.Intents.default()):
        super().__init__(command_prefix=command_prefix, intents=intents)

    async def setup_hook(self):
        await add_cogs(self)

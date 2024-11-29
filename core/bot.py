from discord.ext import commands
import discord
from utils.cogs import add_cogs


class LavavaBot(commands.Bot):
    def __init__(self, command_prefix="!", intents=discord.Intents.default()):
        super().__init__(command_prefix=command_prefix, intents=intents)

    async def setup_hook(self):
        await add_cogs(self)

    # async def on_message(self, message: discord.Message) -> None:
    #     if not message.is_system() and message.channel.id == 1243897099398021182:
    #         channel = message.channel

    #         try:
    #             async for m in channel.history(limit=None):
    #                 if m != message:
    #                     await m.delete()
    #         except discord.HTTPException as e:
    #             print(f"Erro ao excluir mensagens: {e}")

    #         try:
    #             await message.pin()
    #         except discord.HTTPException as e:
    #             print(f"Erro ao fixar mensagem: {e}")

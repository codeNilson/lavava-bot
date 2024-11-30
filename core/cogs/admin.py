import discord
from discord.ext import commands
import logging


class AdminTasks(commands.Cog, name="AdminTasksCog"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if not message.is_system() and message.channel.id == 1243897099398021182:
            channel = message.channel

            try:
                async for m in channel.history(limit=None):
                    if m != message:
                        await m.delete()
            except discord.HTTPException as e:
                logging.warning(
                    f"Erro ao deletar mensagem após chamada do webhook: {e}"
                )

            try:
                await message.pin()
            except discord.HTTPException as e:
                logging.warning(f"Erro ao fixar mensagem após chamada do webhook: {e}")

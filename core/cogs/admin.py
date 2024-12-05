import discord
from discord.ext import commands
import settings


class AdminTasks(commands.Cog, name="AdminTasksCog"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.is_system() and message.channel.id != 1243897099398021182:
            return

        channel = message.channel

        if message.webhook_id:
            try:
                async for m in channel.history(limit=None):
                    if m != message:
                        await m.delete()
            except discord.HTTPException as e:
                settings.LOGGER.warning(
                    f"Erro ao deletar mensagem após chamada do webhook: {e}"
                )
            else:
                try:
                    await message.pin()
                except discord.HTTPException as e:
                    settings.LOGGER.warning(
                        f"Erro ao fixar mensagem após chamada do webhook: {e}"
                    )
        else:
            try:
                await message.delete()
            except discord.HTTPException as e:
                settings.LOGGER.warning(f"Erro ao deletar mensagem: {e}")
                await channel.send(
                    "⚠️ Não foi possível deletar uma mensagem devido a um erro."
                )

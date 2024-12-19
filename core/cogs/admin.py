from datetime import time as dt_time
import discord
from discord.ext import commands, tasks
import settings
from utils.roles import clear_roles


class AdminTasks(commands.Cog, name="AdminTasksCog"):
    def __init__(self, bot):
        self.bot = bot
        self.task_clear_message.start()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.is_system() or message.channel.id != 1243897099398021182:
            return

        channel = message.channel

        if message.webhook_id:
            try:
                async for m in channel.history(limit=None):
                    if m != message:
                        await m.delete()
            except discord.HTTPException as e:
                settings.LOGGER.warning(
                    "Erro ao deletar mensagem após chamada do webhook: %s", e
                )
            else:
                try:
                    await message.pin()
                except discord.HTTPException as e:
                    settings.LOGGER.warning(
                        "Erro ao fixar mensagem após chamada do webhook: %s", e
                    )
        else:
            try:
                await message.delete()
            except discord.HTTPException as e:
                settings.LOGGER.warning("Erro ao deletar mensagem: %s", e)
                await channel.send(
                    "⚠️ Não foi possível deletar uma mensagem devido a um erro."
                )

    @commands.command(name="clear", aliases=["limpar"])
    @commands.has_role(1309641234868080710)
    async def clear_messages(self, ctx, *, channel_name: str) -> None:
        """Clear messages from the channel"""
        channel = discord.utils.get(ctx.guild.channels, name=channel_name)

        if not channel or not isinstance(channel, discord.TextChannel):
            await ctx.send(
                f"⚠️ Canal {channel_name} não encontrado. Verifique o nome do canal e tente novamente."
            )
            return

        try:
            await channel.purge(limit=None)
            await ctx.send(f"Canal {channel_name} limpo com sucesso.")
        except discord.Forbidden:
            settings.LOGGER.warning("Permissão negada ao limpar canal %s", channel_name)
            await ctx.send(
                f"⚠️ Não foi possível limpar o canal {channel_name} devido a permissões insuficientes."
            )
        except discord.HTTPException as e:
            settings.LOGGER.warning("Erro ao limpar canal %s: %s", channel_name, e)
            await ctx.send(
                f"⚠️ Não foi possível limpar o canal {channel_name} devido a um erro."
            )

    async def cog_unload(self):
        self.task_clear_message.cancel()
        return super().cog_unload()

    time_to_run = dt_time(hour=3, minute=0)

    @tasks.loop(time=time_to_run)
    async def task_clear_message(self, *, channel_id: int = 1243610772735529054):
        channel_geral = self.bot.get_channel(channel_id)
        try:
            await channel_geral.purge(limit=None)
        except discord.Forbidden:
            settings.LOGGER.warning(
                "Permissão negada ao limpar canal %s", channel_geral
            )
        except discord.HTTPException as e:
            settings.LOGGER.warning("Erro ao limpar canal %s: %s", channel_geral, e)
        else:
            settings.LOGGER.info("Canal %s limpo com sucesso.", channel_geral)
            channel_audit = self.bot.get_channel(1318700402581176330)
            await channel_audit.send(f"✅ Canal {channel_geral} limpo automaticamente.")

    @tasks.loop(time=time_to_run)
    async def task_clear_teams_roles(self):
        guild = self.bot.get_guild(1243610772064698398)
        blue_role = guild.get_role(1319050096473542696)
        red_role = guild.get_role(1319050273603321916)

        await clear_roles(roles=[blue_role, red_role])
        settings.LOGGER.info("Papéis de times limpos com sucesso.")

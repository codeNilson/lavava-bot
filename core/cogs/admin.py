from datetime import time as dt_time
import discord
from discord.ext import commands, tasks
from utils.enums import RoleID, ChannelID
import settings


class Admin(commands.Cog, name="AdminCog"):

    time_to_run = dt_time(hour=3)

    def __init__(self, bot):
        self.bot = bot
        self.task_clear_message.start()
        self.task_clear_teams_roles.start()

    @commands.Cog.listener("on_message")
    async def clean_ranking_channel(self, message: discord.Message) -> None:
        if message.is_system() or message.channel.id != ChannelID.RANKING.value:
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
    @commands.has_role(RoleID.STAFF.value)
    async def clear_messages(
        self, ctx, channels: commands.Greedy[discord.TextChannel]
    ) -> None:
        """Clear messages from the channel"""

        if not channels:
            await ctx.send(
                "⚠️ Nenhum canal fornecido. Por favor, forneça um ou mais canais."
            )
            return

        for channel in channels:
            await channel.purge(limit=None)

    @commands.command(name="clear_roles", aliases=["limpar_cargos"])
    @commands.has_role(RoleID.STAFF.value)
    async def clear_roles(self, ctx, roles: commands.Greedy[discord.Role]) -> None:
        """Clear roles from members"""

        if not roles:
            await ctx.send(
                "⚠️ Nenhum cargo fornecido. Por favor, forneça um ou mais cargos."
            )
            return

        await self.remove_roles(roles)
        await ctx.send("Cargos removidos com sucesso.")

    async def remove_roles(self, roles: commands.Greedy[discord.Role]) -> None:

        for role in roles:
            for member in role.members:
                try:
                    await member.remove_roles(role)
                except discord.Forbidden:
                    settings.LOGGER.warning(
                        "Permissão negada ao remover cargo %s de %s", role, member
                    )
                except discord.HTTPException as e:
                    settings.LOGGER.warning(
                        "Erro ao remover cargo %s de %s: %s", role, member, e
                    )
        settings.LOGGER.info("Cargos removidos com sucesso.")

    @tasks.loop(time=time_to_run)
    async def task_clear_message(self, *, channel: discord.TextChannel = None):
        channel = channel or self.bot.get_channel(ChannelID.GERAL.value)

        await channel.purge(limit=None)

        settings.LOGGER.info("Canal %s limpo com sucesso.", channel)
        channel_audit = self.bot.get_channel(ChannelID.AUDIT.value)
        await channel_audit.send(f"✅ Canal {channel} limpo automaticamente.")

    @tasks.loop(time=time_to_run)
    async def task_clear_teams_roles(self):
        guild = self.bot.get_guild(1243610772064698398)  # WIP
        blue_role = guild.get_role(RoleID.BLUE.value)
        red_role = guild.get_role(RoleID.RED.value)

        try:
            await self.remove_roles(roles=[blue_role, red_role])
        except Exception as e:
            settings.LOGGER.warning("Erro ao limpar cargos de times: %s", e)
        else:
            settings.LOGGER.info("Papéis de times limpos com sucesso.")
            channel_audit = self.bot.get_channel(ChannelID.AUDIT.value)
            await channel_audit.send("✅ Cargos limpas automaticamente.")

    async def cog_unload(self):
        self.task_clear_message.cancel()
        self.task_clear_teams_roles.cancel()
        return super().cog_unload()

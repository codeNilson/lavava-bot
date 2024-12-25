from datetime import time as dt_time
import discord
from discord import app_commands
from discord.ext import commands, tasks
from utils.enums import RoleID, ChannelID
import settings


class Admin(commands.Cog, name="AdminCog"):

    time_to_run = dt_time(hour=3)

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.task_clear_message.start()
        self.task_clear_teams_roles.start()

    @commands.Cog.listener("on_message")
    async def clean_ranking_channel(self, message: discord.Message) -> None:
        if message.is_system() or message.channel.id != ChannelID.RANKING.value:
            return

        channel = message.channel

        if message.webhook_id == 1309823159540645950:
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

    group_clean = app_commands.Group(
        name="clean", description="Limpa mensagens ou cargos."
    )

    @group_clean.command(name="messages", description="Limpa mensagens de um canal.")
    @app_commands.checks.has_role(RoleID.STAFF.value)
    async def clean_messages(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ) -> None:
        """Clear messages from the channel"""

        if not channel:
            await interaction.response.send_message(
                "⚠️ Nenhum canal fornecido. Por favor, forneça um ou mais canais."
            )
            return
        # await interaction.response.defer(thinking=True)
        await channel.purge(limit=None)
        await interaction.response.send_message(
            "Mensagens removidas com sucesso.", ephemeral=True, delete_after=5
        )

    @group_clean.command(name="roles", description="Limpa os membros de um cargo.")
    @app_commands.checks.has_role(RoleID.STAFF.value)
    async def clean_roles(
        self, interaction: discord.Interaction, role: discord.Role
    ) -> None:
        """Clear roles from members"""
        if not role:
            await interaction.response.send_message(
                "⚠️ Nenhum cargo fornecido. Por favor, forneça um ou mais cargos."
            )
            return

        await self.reset_role(role)
        await interaction.response.send_message("Cargos removidos com sucesso.")

    async def reset_role(self, role: discord.Role) -> None:

        for member in role.members:
            await member.remove_roles(role)

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
        channel_audit = guild.get_channel(ChannelID.AUDIT.value)
        blue_role = guild.get_role(RoleID.BLUE.value)
        red_role = guild.get_role(RoleID.RED.value)
        roles = [blue_role, red_role]

        for role in roles:
            try:
                await self.reset_role(role=role)
            except Exception as e:
                settings.LOGGER.warning("Erro ao limpar cargos de times: %s", e)
            else:
                settings.LOGGER.info("Cargo %s limpo com sucesso.", role.name)
                await channel_audit.send(
                    f"✅ Cargo {role.name} limpos automaticamente."
                )

    async def cog_unload(self):
        self.task_clear_message.cancel()
        self.task_clear_teams_roles.cancel()
        return super().cog_unload()

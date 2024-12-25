from discord.ext import commands
import discord
from utils.cogs import add_cogs
from utils.enums import RoleID
import settings


class LavavaBot(commands.Bot):
    def __init__(
        self, command_prefix=commands.when_mentioned, intents=discord.Intents.default()
    ):
        self.timeout = 10
        super().__init__(command_prefix=command_prefix, intents=intents)
        super().tree.on_error = self.on_app_command_error

    async def handle_error(self, interaction_or_ctx, error):

        if isinstance(
            error,
            (
                discord.app_commands.MissingRole,
                commands.MissingRole,
                discord.app_commands.MissingPermissions,
            ),
        ):
            user = (
                interaction_or_ctx.user
                if isinstance(interaction_or_ctx, discord.Interaction)
                else interaction_or_ctx.author
            )
            settings.LOGGER.info(
                "User %s tried to use a command without permission", user
            )
            message = "⚠️ Você não tem permissão para usar esse comando, meu caro."

        elif isinstance(error, commands.MissingRequiredArgument):
            user = interaction_or_ctx.author
            settings.LOGGER.info(
                "User %s tried to use a command without necessary permissions or arguments",
                user,
            )
            message = "⚠️ Você não forneceu os argumentos necessários."

        elif isinstance(
            error, (discord.app_commands.CommandInvokeError, discord.HTTPException)
        ):
            settings.LOGGER.error(
                "An error occurred while invoking a command: %s", error
            )
            message = "❌ Ocorreu um erro ao executar esse comando. Tente novamente mais tarde."

        elif isinstance(error, discord.app_commands.CheckFailure):
            user = interaction_or_ctx.user
            settings.LOGGER.warning("User %s failed a check for a command", user)
            message = "⚠️ Você não tem permissão para usar esse comando."

        elif isinstance(error, commands.CommandNotFound):
            user = interaction_or_ctx.author
            settings.LOGGER.warning("User %s failed a check for a command", user)
            message = "⚠️ Esse Comando não existe."

        else:
            settings.LOGGER.error("Unhandled app command error: %s", error)
            message = "❌ Ocorreu um erro inesperado. Tente novamente mais tarde."

        if isinstance(interaction_or_ctx, discord.Interaction):
            await interaction_or_ctx.channel.send(
                message,
                delete_after=self.timeout,
            )
        else:
            await interaction_or_ctx.send(message)

    async def on_command_error(self, context, error):
        await self.handle_error(context, error)

    async def on_app_command_error(self, interaction, error):
        await self.handle_error(interaction, error)

    async def on_member_join(self, member):
        settings.LOGGER.info("User %s joined the server", member.name)
        cargo = member.guild.get_role(RoleID.PLAYER.value)
        if cargo:
            try:
                await member.add_roles(cargo)
            except Exception as e:
                settings.LOGGER.error("Error adding role: %s", e)

    async def setup_hook(self):
        await add_cogs(self)
        await self.tree.sync()

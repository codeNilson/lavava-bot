from discord.ext import commands
import discord
from utils.cogs import add_cogs
from utils.enums import RoleID
import settings


class LavavaBot(commands.Bot):
    def __init__(self, command_prefix="!", intents=discord.Intents.default()):
        super().__init__(command_prefix=command_prefix, intents=intents)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            settings.LOGGER.info(
                "User %s tried to use a command without permission", ctx.author
            )
            await ctx.send("Você não tem permissão para usar esse comando.")
        elif isinstance(error, commands.MissingRequiredArgument):
            settings.LOGGER.info(
                "User %s tried to use a command without required arguments", ctx.author
            )
            await ctx.send(
                "Você não forneceu todos os argumentos necessários. Use !help para mais informações."
            )
        elif isinstance(error, commands.CommandNotFound):
            settings.LOGGER.info(
                "User %s tried to use a command that doesn't exist", ctx.author
            )
            await ctx.send("Esse comando não existe.")
        elif isinstance(error, Exception):
            settings.LOGGER.error("An error occurred: %s", error)
            await ctx.send(f"Ocorreu um erro ao executar esse comando. {error}")

    async def on_member_join(self, member):
        settings.LOGGER.info("User %s joined the server", member.name)
        cargo = member.guild.get_role(RoleID.PLAYER.value)
        if cargo:
            await member.add_roles(cargo)
        else:
            settings.LOGGER.error("Falha ao adicionar cargo ao usuário %s", member.name)

    async def setup_hook(self):
        await add_cogs(self)

from discord.ext import commands
import discord
from utils.cogs import add_cogs
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

    async def on_member_join(self, member):
        CARGO_PLAYER = 1309639892791332905  # pylint: disable=invalid-name
        settings.LOGGER.info("User %s joined the server", member.name)
        cargo = member.guild.get_role(CARGO_PLAYER)
        if cargo:
            await member.add_roles(cargo)
        else:
            settings.LOGGER.error("Falha ao adicionar cargo ao usuário %s", member.name)

    async def setup_hook(self):
        await add_cogs(self)

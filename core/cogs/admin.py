import discord
from discord.ext import commands
import settings


class AdminTasks(commands.Cog, name="AdminTasksCog"):
    def __init__(self, bot):
        self.bot = bot

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

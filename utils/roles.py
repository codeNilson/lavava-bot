import discord
from discord.ext import commands
from api import models


async def add_roles(
    ctx: commands.Context,
    role: discord.Role,
    users: list[models.PlayerModel | discord.Member],
):
    for user in users:
        if isinstance(user, models.PlayerModel):
            user = await user.to_member(ctx)
        try:
            await user.add_roles(role)
        except Exception:
            pass

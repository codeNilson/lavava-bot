import discord
from discord import Role
from api.models.player_model import PlayerModel


async def add_roles(ctx, role: Role, users: list[PlayerModel | discord.Member]):
    for user in users:
        if isinstance(user, PlayerModel):
            user = await user.to_member(ctx)
        try:
            await user.add_roles(role)
        except Exception:
            pass

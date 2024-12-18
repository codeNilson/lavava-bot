from discord import Role


async def clear_roles(roles: list[Role]):
    for role in roles:
        for member in role.members:
            await member.remove_roles(role)

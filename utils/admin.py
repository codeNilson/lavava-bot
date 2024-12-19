import discord
import settings

async def move_user_to_channel(member, channel):
    try:
        await member.move_to(channel)
    except discord.HTTPException as e:
        settings.LOGGER.warning(
            "Não foi possível mover o jogador %s para o canal %s: %s",
            member.display_name,
            channel.name,
            e.text,
        )

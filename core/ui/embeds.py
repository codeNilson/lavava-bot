import discord
from discord.ext.commands import Context
from api.models.team_model import TeamModel


async def show_teams(
    ctx: Context, team_a: TeamModel, team_b: TeamModel
) -> discord.Embed:

    players_team_a = [f"⚔️ {player.mention}" for player in team_a.players]
    players_team_b = [f"🛡️ {player.mention}" for player in team_b.players]

    embed = discord.Embed(
        title="Times escolhidos!",
        color=discord.Colour.random(),
    )
    embed.add_field(name="Time 🔵", value="\n".join(players_team_a))
    embed.add_field(name="Time 🔴", value="\n".join(players_team_b))

    return embed

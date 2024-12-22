import discord


async def show_teams(ctx, team_a, team_b):

    players_team_a = [f"⚔️ <@{player.discord_uid or player.username}>" for player in team_a.players]
    players_team_b = [f"🛡️ <@{player.discord_uid or player.username}>" for player in team_b.players]

    embed = discord.Embed(
        title="Times escolhidos!",
        color=discord.Colour.random(),
    )
    embed.add_field(name="Time 🔵", value="\n".join(players_team_a))
    embed.add_field(name="Time 🔴", value="\n".join(players_team_b))

    await ctx.send(embed=embed)

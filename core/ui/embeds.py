import discord
from api import models
from utils.maps import get_map


async def teams_embed(
    team_a: models.TeamModel, team_b: models.TeamModel, map_name: str
) -> discord.Embed:

    players_team_a = [f"⚔️ {player.mention}" for player in team_a.players]
    players_team_b = [f"🛡️ {player.mention}" for player in team_b.players]
    map_model = await get_map(map_name)
    print(map_model.splash_art_url)

    embed = discord.Embed(
        title="Times escolhidos!",
        color=discord.Colour.random(),
    )
    embed.add_field(name="Time 🔵", value="\n".join(players_team_a))
    embed.add_field(name="Time 🔴", value="\n".join(players_team_b))
    embed.set_image(url=map_model.splash_art_url)

    return embed


def get_player_embed(player: models.PlayerModel):

    embed = discord.Embed(
        title=f"{player.username}",
        color=discord.Colour.random(),
        url=player.url,
    )

    embed.set_thumbnail(
        url=f"https://www.lavava.com.br/static/{player.main_agent['icon']}"
    )

    embed.add_field(
        name="Usuário",
        value=player.mention,
    )
    embed.add_field(
        name="Agente Principal",
        value=player.main_agent["name"],
    )
    embed.add_field(name="Ranking", value=player.ranking)

    return embed

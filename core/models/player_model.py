from urllib.parse import quote
from pydantic import BaseModel
import discord
from discord.ext.commands import Context
import settings


class PlayerModel(BaseModel):

    uuid: str
    username: str
    main_agent: dict | None
    tier: str | None
    ranking: int
    include_in_draft: bool
    social_accounts: list[dict]

    @property
    def url(self):
        return f"{settings.SITE_URL}players/profile/{quote(self.username)}"

    @property
    def discord_uid(self):
        if not self.social_accounts:
            return None

        for social_account in self.social_accounts:
            if social_account["provider"] == "discord":
                return int(social_account["uid"])
        return None

    async def to_member(self, ctx: Context) -> discord.Member | None:
        member_uid = self.discord_uid
        if member_uid:
            member = ctx.guild.get_member(member_uid)
            return member
        return None

    def __str__(self):
        return self.username or "Player Desconhecido"

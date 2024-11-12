from uuid import UUID
from urllib.parse import quote
from pydantic import BaseModel
import settings
from .tier import TierModel


class PlayerModel(BaseModel):

    uuid: UUID
    username: str
    main_agent: dict | None
    tier: TierModel | None
    ranking: int
    social_accounts: list[dict]

    @property
    def url(self):
        return f"{settings.SITE_URL}players/profile/{quote(self.username)}"

    def get_discord_uid(self):
        if not self.social_accounts:
            return None

        for social_account in self.social_accounts:
            if social_account["provider"] == "discord":
                return int(social_account["uid"])
        return None

    def __str__(self):
        return self.username

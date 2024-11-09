import settings
from .tier import TierModel


class PlayerModel:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key == "tier":
                try:
                    setattr(self, key, TierModel(**value))
                except Exception as e:
                    print(e)
            else:
                setattr(self, key, value)
        self.url = (
            settings.SITE_URL + f"players/profile/{self.username.replace(' ', '%20')}"
        )

    def get_discord_uid(self):
        for social_account in self.social_accounts:
            if social_account["provider"] == "discord":
                return social_account["uid"]
        return None

    def __str__(self):
        return self.username

from .tier import TierModel


class PlayerModel:
    def __init__(self, uuid, username, email, main_agent, tier, url):
        self.uuid = uuid
        self.username = username
        self.email = email
        self.main_agent = main_agent
        self.tier = TierModel(**tier)
        self.url = url

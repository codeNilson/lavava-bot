from .tier import TierModel


class PlayerModel:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key == "tier":
                setattr(self, key, TierModel(**value))
            else:
                setattr(self, key, value)

from pydantic import BaseModel

class TierModel(BaseModel):
    url: str
    tier: str
    division: str
    small_icon: str
    large_icon: str

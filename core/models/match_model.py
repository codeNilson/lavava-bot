from datetime import datetime
from pydantic import BaseModel


class MatchModel(BaseModel):
    uuid: str
    url: str
    winner: int | None  # modificar
    map: str | None
    youtube_url: str | None
    created_at: datetime

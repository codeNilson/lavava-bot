from datetime import datetime
from pydantic import BaseModel


class MatchModel(BaseModel):
    uuid: str
    map: str | None
    url: str
    winner: int | None  # modificar
    youtube_url: str | None
    created_at: datetime

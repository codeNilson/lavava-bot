from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class Match(BaseModel):
    uuid: UUID
    url: str
    winner: int | None  # modificar
    map: str | None
    youtube_url: str | None
    created_at: datetime

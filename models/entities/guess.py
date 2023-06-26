from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class GuessEnum(str, Enum):
    Up = "up"
    Down = "down"


class Guess(BaseModel):
    id: str
    guess: GuessEnum
    user_id: str
    game_id: str
    created_at: datetime

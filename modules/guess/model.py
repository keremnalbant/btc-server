from pydantic import BaseModel

from models.entities.guess import GuessEnum


class GuessInput(BaseModel):
    guess: GuessEnum
from pydantic import BaseModel


class Game(BaseModel):
    id: str
    value: float
    difference: float

from pydantic import BaseModel


class ActivePlayer(BaseModel):
    sid: str
    cookie: str
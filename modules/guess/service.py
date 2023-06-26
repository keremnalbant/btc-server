import datetime
from typing import List
from uuid import uuid4 as uuid

from fastapi import HTTPException

from models.entities.guess import Guess, GuessEnum
from repositories.guess_repository import GuessRepository


class GuessService:
    def __init__(self):
        self.repository = GuessRepository()

    async def guess(self, guess: GuessEnum, game_id: str, sid: str):
        is_guessed = await self.repository.find_one({'game_id': game_id, 'user_id': sid})
        if is_guessed:
            raise HTTPException(status_code=400, detail="You have already made a guess this game")

        await self.repository.create(
            Guess(id=str(uuid()), guess=guess, user_id=sid, game_id=game_id, created_at=datetime.datetime.now()))

    async def get_all_by_game_id(self, game_id: str) -> List[Guess]:
        return await self.repository.find({'game_id': game_id})

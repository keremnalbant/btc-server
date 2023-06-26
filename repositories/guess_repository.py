import os
from typing import List

from models.entities.guess import Guess
from mongo_helper import MongoHelper


class GuessRepository:
    def __init__(self):
        self.client = MongoHelper(os.getenv('DB_NAME'), os.getenv('DB_GUESS_COLLECTION'))

    async def create(self, data: Guess) -> str:
        await self.client.insert_one(data.dict())
        return str(data.id)

    async def find(self, query) -> List[Guess]:
        res = await self.client.find_many(query)
        items: List[Guess] = []
        for item in res:
            item.pop('_id')
            items.append(Guess(**item))
        return items

    async def find_one(self, query) -> Guess:
        res = await self.client.find_one(query)
        if res:
            res.pop('_id')
            return Guess(**res)

import os
from typing import List

from models.entities.user import User
from mongo_helper import MongoHelper


class UserRepository:
    def __init__(self):
        self.client = MongoHelper(os.getenv('DB_NAME'), os.getenv('DB_USER_COLLECTION'))

    async def create(self, data: User):
        await self.client.insert_one(data.dict())
        return str(data.id)

    async def find_one(self, query) -> User:
        res = await self.client.find_one(query)
        if res:
            res.pop('_id')
            return User(**res)

    async def find_all(self) -> List[User]:
        res = await self.client.find_all()
        items: List[User] = []
        for item in res:
            item.pop('_id')
            items.append(User(**item))
        return items

    async def update_one(self, query, update):
        await self.client.update_one(query, update)

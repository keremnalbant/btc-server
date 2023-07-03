from typing import List
from uuid import uuid4 as uuid
from models.entities.user import User
from repositories.user_repository import UserRepository


class UserService:
    def __init__(self):
        self.repository = UserRepository()

    async def get_user(self, sid: str) -> User or None:
        if sid:
            res = await self.repository.find_one({'id': sid})
            if not res:
                res = await self.create_user(sid)
            return res
        return None

    async def get_all_users(self) -> List[User]:
        return await self.repository.find_all()

    async def create_user(self, sid=None) -> User:
        if not sid:
            sid = str(uuid())
        await self.repository.create(User(score=0, id=sid))
        return await self.repository.find_one({'id': sid})

    async def update_score(self, sid: str, is_correct: bool) -> User:
        user = await self.get_user(sid)
        if user.score == 0 and not is_correct:
            return user
        else:
            user.score += 1 if is_correct else -1
            await self.repository.update_one({'id': sid}, {'$set': {'score': user.score}})
        return user

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from models.entities.user import User
from repositories.user_repository import UserRepository

security = HTTPBearer()

user_repository = UserRepository()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    token = credentials.credentials
    user = await user_repository.find_one({'id': token})
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user

from fastapi import APIRouter, status, Depends
from auth import get_current_user
from models.entities.user import User
from modules.user.service import UserService
from socket_handler import socket_handler

router = APIRouter()

user_service = UserService()


@router.get("/me", status_code=status.HTTP_200_OK, response_model=User)
async def get_me(current_user: User = Depends(get_current_user)) -> User:
    return current_user


@router.post("", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user() -> User:
    return await user_service.create_user()


@router.get("/active-users", status_code=status.HTTP_200_OK, response_model=int)
async def get_active_users(current_user: User = Depends(get_current_user)) -> int:
    return len(socket_handler.active_players)

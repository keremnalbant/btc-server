from fastapi import APIRouter, status, Depends
from auth import get_session_cookie_value
from models.entities.user import User
from modules.user.service import UserService
from socket_handler import socket_handler

router = APIRouter()

user_service = UserService()


@router.get("/me", status_code=status.HTTP_200_OK, response_model=User)
async def get_me(sid: str = Depends(get_session_cookie_value)) -> User:
    return await user_service.get_user(sid)


@router.get("/active-users", status_code=status.HTTP_200_OK, response_model=int)
async def get_active_users() -> int:
    return len(socket_handler.active_players)

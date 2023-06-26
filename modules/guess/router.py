from fastapi import APIRouter, status, Depends

from auth import get_current_user
from models.entities.guess import GuessEnum
from models.entities.user import User
from modules.guess.service import GuessService
from modules.game.game_manager import game_manager

router = APIRouter()

guess_service = GuessService()


@router.post("", status_code=status.HTTP_201_CREATED)
async def guess(guess: GuessEnum, current_user: User = Depends(get_current_user)):
    return await guess_service.guess(guess, game_manager.id, current_user)

from fastapi import APIRouter, status, Depends

from auth import get_current_user
from models.entities.user import User
from modules.guess.model import GuessInput
from modules.guess.service import GuessService
from modules.game.game_manager import game_manager

router = APIRouter()

guess_service = GuessService()


@router.post("", status_code=status.HTTP_201_CREATED)
async def guess(data: GuessInput, current_user: User = Depends(get_current_user)):
    return await guess_service.guess(data.guess, game_manager.id, current_user)


@router.get("", status_code=status.HTTP_200_OK)
async def guess(current_user: User = Depends(get_current_user)):
    return await guess_service.get_by_game_id(game_manager.id, current_user)

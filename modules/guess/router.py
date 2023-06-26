from fastapi import APIRouter, status, Depends

from auth import get_session_cookie_value
from models.entities.guess import GuessEnum
from modules.guess.service import GuessService
from modules.game.game_manager import game_manager

router = APIRouter()

guess_service = GuessService()


@router.post("", status_code=status.HTTP_201_CREATED)
async def guess(guess: GuessEnum, sid: str = Depends(get_session_cookie_value)):
    return await guess_service.guess(guess, game_manager.id, sid)

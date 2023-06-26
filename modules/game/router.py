from fastapi import APIRouter, status, Depends

from auth import get_current_user
from models.entities.game import Game
from models.entities.user import User
from modules.game.game_manager import game_manager

router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK, response_model=Game)
async def get_game(current_user: User = Depends(get_current_user)) -> Game:
    return Game(id=game_manager.id, value=game_manager.current_value,
                difference=game_manager.difference)

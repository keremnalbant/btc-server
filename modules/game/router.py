from fastapi import APIRouter, status

from models.entities.game import Game
from modules.game.game_manager import game_manager

router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK, response_model=Game)
async def get_game() -> Game:
    return Game(id=game_manager.id, value=game_manager.current_value,
                difference=game_manager.difference)

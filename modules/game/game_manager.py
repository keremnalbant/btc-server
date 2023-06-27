import asyncio
import time
from uuid import uuid4 as uuid

from btc_data import get_btc_usd_value
from models.entities.game import Game
from models.events.event import EventName
from models.entities.guess import GuessEnum
from modules.guess.service import GuessService
from modules.user.service import UserService
from socket_handler import socket_handler


class GameManager:
    def __init__(self):
        self.socket = socket_handler
        self.guess_service = GuessService()
        self.user_service = UserService()
        self.id = str(uuid())
        self.start_time = time.time()
        self.current_value = 0
        self.difference = 0.0
        self.round_length = 60
        asyncio.create_task(self.__init())

    @property
    def time_passed(self) -> float:
        return time.time() - self.start_time

    async def __init(self):
        self.current_value = await get_btc_usd_value()
        await self.__start_game()

    async def __start_game(self):
        while True:
            print("while", self.round_length - self.time_passed)
            if self.round_length - self.time_passed >= 0:
                print("emit_time", time.time())
                await self.socket.emit_with_retry(EventName.Time, self.round_length - self.time_passed)
                await asyncio.sleep(1)
            else:
                await self.__evaluate()

    async def __evaluate(self):
        try:
            new_value = await get_btc_usd_value()
        except Exception as e:
            print(e)
            self.id = str(uuid())
            self.start_time = time.time()
            return
        users = []
        # region evaluate guesses
        retries = 0
        while retries < 5:
            try:
                guesses = await self.guess_service.get_all_by_game_id(self.id)
                for guess in guesses:
                    is_correct = (new_value > self.current_value and guess.guess == GuessEnum.Up) or (
                            new_value < self.current_value and guess.guess == GuessEnum.Down)
                    user = await self.user_service.update_score(guess.user_id, is_correct)
                    users.append(user)
                break
            except Exception as e:
                print(e)
                retries += 1
                await asyncio.sleep(1)
        # endregion
        # region Emit New Game
        self.id = str(uuid())
        await self.__calculate_percentage_difference(
            float(self.current_value), float(new_value))
        await self.socket.emit_with_retry(EventName.Game,
                                          Game(value=new_value, id=self.id, difference=self.difference).dict())
        # endregion
        self.current_value = new_value
        # region Emit Socres
        tasks = [self.socket.emit_with_retry(EventName.Score, user.score, to=user.id) for user in users]
        await asyncio.gather(*tasks)

        # endregion
        # region Start New Game
        self.start_time = time.time()
        # endregion

    async def __calculate_percentage_difference(self, old_value, new_value):
        difference = new_value - old_value
        percentage_difference = (difference / old_value) * 100
        self.difference = percentage_difference


game_manager = GameManager()

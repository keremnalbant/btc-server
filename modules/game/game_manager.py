import asyncio
import time
from typing import Coroutine
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
        asyncio.create_task(self.__init())

    @property
    def time_passed(self) -> float:
        return time.time() - self.start_time

    async def __init(self):
        self.current_value = await get_btc_usd_value()
        await self.__create_scheduler()

    async def __create_scheduler(self):
        start_time = time.time()
        send_times = [start_time + i for i in range(0, 60)]
        for send_time in send_times:
            asyncio.ensure_future(self.__schedule_task(send_time, self.__emit_time()))
        await self.__schedule_task(start_time + 61, self.__evaluate())

    async def __schedule_task(self, run_time: float, task: Coroutine):
        delay = run_time - time.time()
        if delay > 0:
            await asyncio.sleep(delay)
        await task

    async def __emit_time(self):
        await self.socket.emit(EventName.Time, 60 - self.time_passed)

    async def __evaluate(self):
        new_value = await get_btc_usd_value()
        # region evaluate guesses
        guesses = await self.guess_service.get_all_by_game_id(self.id)
        users = []
        for guess in guesses:
            is_correct = (new_value > self.current_value and guess.guess == GuessEnum.Up) or (
                    new_value < self.current_value and guess.guess == GuessEnum.Down)
            user = await self.user_service.update_score(guess.user_id, is_correct)
            users.append(user)
        # endregion
        # region Emit New Game
        self.id = str(uuid())
        await self.__calculate_percentage_difference(
            float(self.current_value), float(new_value))
        await self.socket.emit(EventName.Game,
                               Game(value=new_value, id=self.id, difference=self.difference).dict())
        # endregion
        self.current_value = new_value
        # region Emit Socres
        tasks = [self.socket.emit(EventName.Score, user.score, to=user.id) for user in users]
        await asyncio.gather(*tasks)

        # endregion
        # region Start New Game
        self.start_time = time.time()
        await self.__create_scheduler()
        # endregion

    async def __calculate_percentage_difference(self, old_value, new_value):
        difference = new_value - old_value
        percentage_difference = (difference / old_value) * 100
        self.difference = percentage_difference


game_manager = GameManager()

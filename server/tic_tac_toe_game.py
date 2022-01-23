from typing import Callable

import ws_models
import inspect


class TicTacToeGame:
    """
    Represents the game

    Needs four callbacks:
        the board data callback
        the "waiting for player" callback
        the game ended callback
        the bad move callback
    """

    __board_data_cb: Callable[[ws_models.BoardData], None] = None
    __waiting_for_player_cb: Callable[
        [ws_models.CrossOrCircle], ws_models.MoveData
    ] = None
    __game_ended_cb: Callable[[ws_models.GameEndedReason], None] = None
    __bad_move_cb: Callable[[ws_models.GameEndedReason], None] = None

    def __init__(
        self,
        board_data_cb: Callable[[ws_models.BoardData], None],
        waiting_for_player_cb: Callable[[ws_models.CrossOrCircle], ws_models.MoveData],
        game_ended_cb: Callable[[ws_models.GameEndedReason], None],
        bad_move_cb: Callable[[ws_models.CrossOrCircle], None],
    ):
        self.__board_data_cb = board_data_cb
        self.__waiting_for_player_cb = waiting_for_player_cb
        self.__game_ended_cb = game_ended_cb
        self.__bad_move_cb = bad_move_cb

    __state: ws_models.BoardData = None  # TODO initial state

    async def __check_state_ends_game_and_end(self) -> bool:
        # TODO do what the method says it does
        return True

    async def __validate_move(
        self,
        player: ws_models.CrossOrCircle,
        move: ws_models.MoveData,
    ):
        # TODO actual move validation
        if False:
            await self.__bad_move_cb(player)
        return True

    async def start(self):
        try:
            while True:
                should_break = await self.__do_turn(ws_models.CrossOrCircle.CROSS)
                if should_break:
                    break
                should_break = await self.__do_turn(ws_models.CrossOrCircle.CIRCLE)
                if should_break:
                    break
            #  TODO Communicate reason for game end here
            await self.__game_ended_cb(ws_models.GameEndedReason.CIRCLE_WON)
        # pylint: disable=broad-except
        except Exception as e:
            print(e)
            await self.__game_ended_cb(ws_models.GameEndedReason.PLAYER_QUIT)

    async def __do_turn(self, player: ws_models.CrossOrCircle) -> bool:
        print("asd1")
        move = await self.__wait_for_player_move(player)
        print("asd2")
        # TODO calculate state based on move
        self.__state = self.__state
        await self.__board_data_cb(self.__state)
        print("asd3")
        return await self.__check_state_ends_game_and_end()

    async def __wait_for_player_move(
        self, player: ws_models.CrossOrCircle
    ) -> ws_models.MoveData:
        while True:
            move = await self.__waiting_for_player_cb(player)
            if await self.__validate_move(player, move):
                return move

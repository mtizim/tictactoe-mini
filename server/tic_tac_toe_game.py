from typing import Callable
import numpy as np

import ws_models


class SurrenderException(Exception):
    pass


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

    __state: ws_models.BoardData = [
        [[ws_models.BoardMark.NONE for _ in range(3)] for _ in range(3)]
        for _ in range(3)
    ]

    def ___check_2d_board_ends_game(self, board) -> bool:  # input - 2d np array
        # 3 horizontal checks,
        for i in range(3):
            vals = set(board[:, i].flatten())
            if len(vals) == 1 and vals.pop() != ws_models.BoardMark.NONE:
                return True
        # 3 vertical checks
        for i in range(3):
            vals = set(board[i, :].flatten())
            if len(vals) == 1 and vals.pop() != ws_models.BoardMark.NONE:
                return True
        # 2 cross checks
        vals = set(board[i, i] for i in range(3))
        if len(vals) == 1 and vals.pop() != ws_models.BoardMark.NONE:
            return True
        vals = set(board[i, 2 - i] for i in range(3))
        if len(vals) == 1 and vals.pop() != ws_models.BoardMark.NONE:
            return True
        return False

    def __check_state_ends_game(self) -> bool:
        board = np.array(self.__state, dtype=object)
        # 3x3 2d cases
        for case in (board, np.swapaxes(board, 0, 1), np.swapaxes(board, 0, 2)):
            for boardslice in (case[i, :, :] for i in range(3)):
                if self.___check_2d_board_ends_game(boardslice):
                    return True

        # 4 3d crosses
        vals = set(board[i, i, i] for i in range(3))
        if len(vals) == 1 and vals.pop() != ws_models.BoardMark.NONE:
            return True
        vals = set(board[i, 2 - i, i] for i in range(3))
        if len(vals) == 1 and vals.pop() != ws_models.BoardMark.NONE:
            return True
        vals = set(board[i, i, 2 - i] for i in range(3))
        if len(vals) == 1 and vals.pop() != ws_models.BoardMark.NONE:
            return True
        vals = set(board[2 - i, i, i] for i in range(3))
        if len(vals) == 1 and vals.pop() != ws_models.BoardMark.NONE:
            return True

        return False

    async def __validate_move(
        self,
        move: ws_models.MoveData,
    ):
        if any(not (0 <= e <= 2) for e in [move.row, move.board, move.column]):
            return False
        if self.__state[move.board][move.row][move.column] != ws_models.BoardMark.NONE:
            return False
        return True

    async def start(self):
        try:
            while True:
                try:
                    end_game = await self.__do_turn(ws_models.CrossOrCircle.CROSS)
                except SurrenderException:
                    await self.__game_ended_cb(
                        ws_models.GameEndedReason.CROSS_SURRENDER
                    )
                    break
                if end_game:
                    await self.__game_ended_cb(ws_models.GameEndedReason.CROSS_WON)
                    break

                try:
                    end_game = await self.__do_turn(ws_models.CrossOrCircle.CIRCLE)
                except SurrenderException:
                    await self.__game_ended_cb(
                        ws_models.GameEndedReason.CROSS_SURRENDER
                    )
                    break
                if end_game:
                    await self.__game_ended_cb(ws_models.GameEndedReason.CIRCLE_WON)
                    break
        # pylint: disable=broad-except
        except Exception:
            await self.__game_ended_cb(ws_models.GameEndedReason.PLAYER_QUIT)

    async def __do_turn(self, player: ws_models.CrossOrCircle) -> bool:
        move = await self.__wait_for_player_move(player)

        self.__state[move.board][move.row][move.column] = player
        await self.__board_data_cb(self.__state)
        return self.__check_state_ends_game()

    async def __wait_for_player_move(
        self, player: ws_models.CrossOrCircle
    ) -> ws_models.MoveData:
        while True:
            move = await self.__waiting_for_player_cb(player)
            if await self.__validate_move(move):
                return move
            else:
                await self.__bad_move_cb(player)

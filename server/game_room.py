from fastapi import WebSocket
from fastapi import WebSocketDisconnect
import rx
from rx.subject import Subject
import asyncio
import ws_models

import tic_tac_toe_game as game


class GameRoom:
    """
    Represents a game room and handles the game object
    Responsible for handling everything game related
    """

    creator_token: str = None

    __circle_token: str = None
    __cross_token: str = None

    __current_player_count: int = 0

    def __init__(self, creator_token: str):
        self.creator_token = creator_token

    __circle_player_ws: WebSocket = None
    __cross_player_ws: WebSocket = None

    __circle_player_subject = None
    __cross_player_subject = None

    # Connection handling

    async def register_token_for_circle(self, wbs: WebSocket):
        """
        Verifies or binds ws to a token
        """
        try:
            await wbs.accept()
            await wbs.send_json(
                ws_models.OutMessage(
                    message_type=ws_models.OutMessageType.WAITING_FOR_REGISTRATION,
                    payload=ws_models.CrossOrCircle.CIRCLE,
                ).dict()
            )

            received = await wbs.receive_json()

            try:
                parsed = ws_models.InMessage(**received)
            # pylint: disable=broad-except
            except Exception:
                return

            if parsed.message_type == ws_models.InMessageType.REGISTER:
                token = parsed.token
                self.__circle_token = token
                self.__circle_player_ws = wbs
                await self._send_circle_message(
                    ws_models.Reponse(failure_mode=ws_models.FailureMode.NONE)
                )
            else:
                await wbs.close()

            sub = Subject()

            async def __listener(msg: str):
                await self._handle_circle_message(ws_models.InMessage(**msg))

            sub.subscribe(lambda msg: asyncio.create_task(__listener(msg)))

            self.__circle_player_subject = sub

            self.__current_player_count += 1
            if self.__current_player_count == 2:
                asyncio.create_task(self._start_game())

            async for msg in wbs.iter_json():
                sub.on_next(msg)

        except WebSocketDisconnect:
            return

    async def register_token_for_cross(self, wbs: WebSocket):
        """
        Verifies or binds ws to a token
        """
        try:
            await wbs.accept()
            await wbs.send_json(
                ws_models.OutMessage(
                    message_type=ws_models.OutMessageType.WAITING_FOR_REGISTRATION,
                    payload=ws_models.CrossOrCircle.CIRCLE,
                ).dict()
            )

            received = await wbs.receive_json()

            try:
                parsed = ws_models.InMessage(**received)
            # pylint: disable=broad-except
            except Exception:
                return

            if parsed.message_type == ws_models.InMessageType.REGISTER:
                token = parsed.token
                self.__cross_token = token
                self.__cross_player_ws = wbs
                await self._send_cross_message(
                    ws_models.Reponse(failure_mode=ws_models.FailureMode.NONE)
                )
            else:
                await wbs.close()

            sub = Subject()

            async def __listener(msg: str):
                await self._handle_cross_message(ws_models.InMessage(**msg))

            sub.subscribe(lambda msg: asyncio.create_task(__listener(msg)))

            self.__cross_player_subject = sub

            self.__current_player_count += 1
            if self.__current_player_count == 2:
                asyncio.create_task(self._start_game())

            async for msg in wbs.iter_json():
                sub.on_next(msg)

        except WebSocketDisconnect:
            return

    async def register_token_for_second_player(self, wbs: WebSocket):
        """
        Redirects a websocket to a free one
        """
        if self.__cross_player_ws is not None and self.__circle_player_ws is not None:
            await wbs.close()
        elif self.__cross_player_ws is None:
            await self.register_token_for_cross(wbs)
        else:
            await self.register_token_for_circle(wbs)

    async def _send_circle_message(self, msg: ws_models.OutMessage):
        try:
            await self.__circle_player_ws.send_json(msg.dict())
        except WebSocketDisconnect:
            return

    async def _send_cross_message(self, msg: ws_models.OutMessage):
        try:
            await self.__cross_player_ws.send_json(msg.dict())
        except WebSocketDisconnect:
            return

    # TODO more handling here
    async def _handle_circle_message(self, msg: ws_models.InMessage):
        if msg.token != self.__circle_token:
            await self._send_circle_message(
                ws_models.Reponse(failure_mode=ws_models.FailureMode.BAD_TOKEN)
            )
        if msg.message_type == ws_models.InMessageType.SURRENDER:
            pass
        if msg.message_type == ws_models.InMessageType.MOVE:
            pass

    async def _handle_cross_message(self, msg: ws_models.InMessage):
        if msg.token != self.__cross_token:
            await self._send_cross_message(
                ws_models.Reponse(failure_mode=ws_models.FailureMode.BAD_TOKEN)
            )
        if msg.message_type == ws_models.InMessageType.SURRENDER:
            pass
        if msg.message_type == ws_models.InMessageType.MOVE:
            pass

    # Game related callbacks
    __game: game.TicTacToeGame = None

    async def _send_board_data(self, boardData: ws_models.BoardData):
        await self._send_circle_message(
            ws_models.OutMessage(
                message_type=ws_models.OutMessageType.BOARD_DATA,
                payload=boardData,
            )
        )
        await self._send_cross_message(
            ws_models.OutMessage(
                message_type=ws_models.OutMessageType.BOARD_DATA,
                payload=boardData,
            )
        )

    async def _notify_waiting_for_player(self, player: ws_models.CrossOrCircle):
        if player == ws_models.CrossOrCircle.CIRCLE:
            await self._send_circle_message(
                ws_models.OutMessage(
                    message_type=ws_models.OutMessageType.WAITING_FOR_MOVE,
                ),
            )
            await self._send_cross_message(
                ws_models.OutMessage(
                    message_type=ws_models.OutMessageType.WAITING_FOR_OTHER_MOVE,
                ),
            )
        else:
            await self._send_cross_message(
                ws_models.OutMessage(
                    message_type=ws_models.OutMessageType.WAITING_FOR_MOVE,
                ),
            )
            await self._send_circle_message(
                ws_models.OutMessage(
                    message_type=ws_models.OutMessageType.WAITING_FOR_OTHER_MOVE,
                ),
            )

    async def _notify_game_ended(self, reason: ws_models.GameEndedReason):
        await self._send_circle_message(
            ws_models.OutMessage(
                message_type=ws_models.OutMessageType.GAME_ENDED, payload=reason
            ),
        )
        await self._send_cross_message(
            ws_models.OutMessage(
                message_type=ws_models.OutMessageType.GAME_ENDED, payload=reason
            ),
        )

    async def _notify_bad_move(self, player: ws_models.CrossOrCircle):
        if player == ws_models.CrossOrCircle.CIRCLE:
            outwbs = self.__circle_player_ws
        else:
            outwbs = self.__cross_player_ws
        outwbs.send_json(ws_models.Reponse(failure_mode=ws_models.FailureMode.BAD_MOVE))

    async def _start_game(self):
        self.__game = game.TicTacToeGame(
            board_data_cb=lambda bData: self._send_board_data(bData),
            waiting_for_player_cb=lambda p: self._notify_waiting_for_player(p),
            game_ended_cb=lambda r: self._notify_game_ended(r),
            bad_move_cb=lambda p: self._notify_bad_move(p),
        )
        await self.__game.start()

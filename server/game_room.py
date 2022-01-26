import asyncio
from datetime import datetime
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
import rx.operators as ops
from rx.subject import Subject
import ws_models

import tic_tac_toe_game as game
import elo
import auth


class GameRoom:
    """
    Represents a game room and handles the game object
    Responsible for handling everything game related
    """

    def get_availability(
        self,
    ):  # None indicates not available, otherwise returns elo of circle or cross token
        if (
            self.__circle_token is not None and self.__cross_token is not None
        ) or self.__game is not None:
            return None

        token = self.__circle_token or self.__cross_token or self.creator_token
        return elo.get_elo_for_token(token)

    def on_try_delete(self) -> bool:  # returns True if game is deletable
        if self.__last_input_recv is None:
            return True
        if self.__game_ended:
            return True
        diff = (datetime.now() - self.__last_input_recv).total_seconds()

        if diff >= 60 * 10:
            return True

        return False

    creator_token: str = None

    __game_ended: bool = False
    __last_input_recv: datetime = None

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

            self.__circle_player_subject = sub

            self.__current_player_count += 1
            if self.__current_player_count == 2:
                asyncio.create_task(self._start_game())

            async for msg in wbs.iter_json():
                self.__last_input_recv = datetime.now()
                msg = ws_models.InMessage(**msg)
                if msg.token != self.__circle_token:
                    await self._send_circle_message(
                        ws_models.Reponse(failure_mode=ws_models.FailureMode.BAD_TOKEN)
                    )
                    continue
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
                    payload=ws_models.CrossOrCircle.CROSS,
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

            self.__cross_player_subject = sub

            self.__current_player_count += 1
            if self.__current_player_count == 2:
                asyncio.create_task(self._start_game())

            async for msg in wbs.iter_json():
                self.__last_input_recv = datetime.now()
                msg = ws_models.InMessage(**msg)
                if msg.token != self.__cross_token:
                    await self._send_cross_message(
                        ws_models.Reponse(failure_mode=ws_models.FailureMode.BAD_TOKEN)
                    )
                    continue
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

    # Game related callbacks
    __game: game.TicTacToeGame = None

    async def _send_board_data(self, board_data: ws_models.BoardData):
        await self._send_circle_message(
            ws_models.OutMessage(
                message_type=ws_models.OutMessageType.BOARD_DATA,
                payload=board_data,
            )
        )
        await self._send_cross_message(
            ws_models.OutMessage(
                message_type=ws_models.OutMessageType.BOARD_DATA,
                payload=board_data,
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
            completer = asyncio.Future()
            self.__circle_player_subject.pipe(
                ops.first(
                    lambda msg: msg.message_type == ws_models.InMessageType.MOVE
                    or msg.message_type == ws_models.InMessageType.SURRENDER
                )
            ).subscribe(lambda msg: completer.set_result(msg))
            result = await completer
            if result.message_type == ws_models.InMessageType.SURRENDER:
                raise game.SurrenderException()
            return ws_models.MoveData(**result.payload)
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
            completer = asyncio.Future()
            self.__cross_player_subject.pipe(
                ops.first(
                    lambda msg: msg.message_type == ws_models.InMessageType.MOVE
                    or msg.message_type == ws_models.InMessageType.SURRENDER
                )
            ).subscribe(lambda msg: completer.set_result(msg))

            result = await completer
            if result.message_type == ws_models.InMessageType.SURRENDER:
                raise game.SurrenderException()
            return ws_models.MoveData(**result.payload)

    async def _notify_game_ended(self, reason: ws_models.GameEndedReason):

        delta_circle, delta_cross = None, None
        if reason in (
            ws_models.GameEndedReason.CIRCLE_SURRENDER,
            ws_models.GameEndedReason.CROSS_WON,
        ):
            delta_cross, delta_circle = elo.update_elo(
                self.__cross_token, self.__circle_token
            )
        if reason in (
            ws_models.GameEndedReason.CROSS_SURRENDER,
            ws_models.GameEndedReason.CIRCLE_WON,
        ):
            delta_circle, delta_cross = elo.update_elo(
                self.__circle_token, self.__cross_token
            )

        await self._send_circle_message(
            ws_models.OutMessage(
                message_type=ws_models.OutMessageType.GAME_ENDED,
                payload=ws_models.GameEndedPayload(
                    reson=reason,
                    elo_delta=delta_circle,
                    opponent_elo_delta=delta_cross,
                ),
            ),
        )
        await self._send_cross_message(
            ws_models.OutMessage(
                message_type=ws_models.OutMessageType.GAME_ENDED,
                payload=ws_models.GameEndedPayload(
                    reson=reason,
                    elo_delta=delta_cross,
                    opponent_elo_delta=delta_circle,
                ),
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

        cross_name = auth.get_username_for_token(self.__cross_token)
        cross_elo = elo.get_elo_for_token(self.__cross_token)
        circle_name = auth.get_username_for_token(self.__circle_token)
        circle_elo = elo.get_elo_for_token(self.__circle_token)

        self._send_circle_message(
            ws_models.OutMessage(
                message_type=ws_models.OutMessageType.GAME_STARTED,
                payload=ws_models.GameStartedInformation(
                    opponent_name=cross_name,
                    opponent_elo=cross_elo,
                ),
            )
        )
        self._send_cross_message(
            ws_models.OutMessage(
                message_type=ws_models.OutMessageType.GAME_STARTED,
                payload=ws_models.GameStartedInformation(
                    opponent_name=circle_name,
                    opponent_elo=circle_elo,
                ),
            )
        )

        await self.__game.start()
        self.__game_ended = True

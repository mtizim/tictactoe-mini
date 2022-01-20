from fastapi import WebSocket
from fastapi import WebSocketDisconnect
import ws_models


class GameRoom:
    """
    Represents both a game room and a game object
    Responsible for handling everything game related
    """

    creator_token: str = None

    __circle_token: str = None
    __cross_token: str = None

    def __init__(self, creator_token: str):
        self.creator_token = creator_token

    __circle_player_ws: WebSocket = None
    __cross_player_ws: WebSocket = None

    async def _check_both_registered(self):
        if self.__circle_token is not None and self.__cross_token is not None:
            await self._start_game()

    async def register_token_for_circle(self, wbs: WebSocket):
        """
        Verifies or binds ws to a token
        """
        try:
            await wbs.accept()

            await wbs.send_json(
                ws_models.OutMessage(
                    message_type=ws_models.OutMessageType.WAITING_FOR_REGISTRATION
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
                print(token)
                self.__circle_token = token
                self.__circle_player_ws = wbs
                await self._send_circle_message(
                    ws_models.Reponse(failure_mode=ws_models.FailureMode.NONE)
                )

            async for msg in wbs.iter_json():
                await self._handle_circle_message(ws_models.InMessage(**msg))

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
                    message_type=ws_models.OutMessageType.WAITING_FOR_REGISTRATION
                )
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

            async for msg in wbs.iter_json():
                await self._handle_cross_message(ws_models.InMessage(**msg))

        except WebSocketDisconnect:
            return

    async def register_token_for_second_player(self, wbs: WebSocket):
        """
        Redirects a websocket to a free one
        """
        if self.__cross_player_ws is not None and self.__circle_player_ws is not None:
            await wbs.close()
        elif self.__cross_player_ws is None:
            self.register_token_for_cross(wbs)
        else:
            self.register_token_for_circle(wbs)

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

    async def _handle_cross_message(self, msg: ws_models.InMessage):
        if msg.token != self.__cross_token:
            await self._send_cross_message(
                ws_models.Reponse(failure_mode=ws_models.FailureMode.BAD_TOKEN)
            )

    async def _start_game(self):
        pass
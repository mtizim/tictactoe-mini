from fastapi import WebSocket
from fastapi import WebSocketDisconnect


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

    both_connected: bool = False

    __circle_player_ws: WebSocket = None
    __cross_player_ws: WebSocket = None

    async def __check_if_both_connected(self):
        if self.__circle_player_ws is not None and self.__cross_player_ws is not None:
            self.both_connected = True
            await self._start_game()

    async def verify_token_for_circle(self, wbs: WebSocket):
        """
        Verifies or binds ws to a token
        """
        try:
            if self.__circle_player_ws is not None:
                await wbs.close()

            await wbs.accept()

            token = await wbs.receive_text()

            if self.__circle_token is None:
                if token == self.__cross_token:
                    print(token, self.__cross_token)
                    await wbs.close()
                self.__circle_token = token
                self.__circle_player_ws = wbs

                # ! todo listen to messages in a separate thread, otherwise the sockets do get closed
                while True:
                    await self.__check_if_both_connected()
                    x = await self.__circle_player_ws.receive_text()
                    print(x)
                await future
                return

            # elif self.__circle_token == token:
            #     self.__circle_player_ws = wbs
            #     await self.__check_if_both_connected()

            else:
                await wbs.close()
        except WebSocketDisconnect:
            return

    async def verify_token_for_cross(self, wbs: WebSocket):
        """
        Verifies or binds ws to a token
        """
        try:
            if self.__cross_player_ws is not None:
                await wbs.close()

            await wbs.accept()

            token = await wbs.receive_text()

            if self.__cross_token is None:
                if token == self.__circle_token:
                    print(token, self.__circle_token)
                    await wbs.close()
                self.__cross_token = token
                self.__cross_player_ws = wbs
                while True:
                    await self.__check_if_both_connected()
                    x = await self.__cross_player_ws.receive_text()
                    print(x)
                return

            # elif self.__cross_token == token:
            #     self.__cross_player_ws = wbs
            #     await self.__check_if_both_connected()
            #     return

            else:
                await wbs.close()
        except WebSocketDisconnect:
            return

    async def _start_game(self):
        try:
            await self.__cross_player_ws.send_text("game_started")
        except BaseException as e:
            print(e)

        try:
            await self.__circle_player_ws.send_text("game_started2")
        except BaseException as e:
            print(e)

        print("sent???")
        print("received???")

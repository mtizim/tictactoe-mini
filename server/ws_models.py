from enum import Enum
from typing import Optional, Any, List
from pydantic import BaseModel

# Do serwera wysyłasz InMessage
# Serwer wysyła OutMessage i Response


class CrossOrCircle(str, Enum):
    CROSS = "cross"
    CIRCLE = "circle"


class InMessageType(str, Enum):
    REGISTER = "register"  #   command, registers this token to this websocket
    #                                   ALWAYS send after WAITING_FOR_REGISTRATION request
    #                                   responds with BAD_TOKEN or NONE

    MOVE = "move"  #           payload: MoveData
    #                                   responds with BAD_MOVE or BAD_TOKEN or NONE

    SURRENDER = "surrender"  # command, surrenders
    #                                   responds with BAD_TOKEN or NONE


class MoveData(BaseModel):
    row: int  #    from 0 to 2
    column: int  # from 0 to 2
    board: int  #  from 0 to 2


class InMessage(BaseModel):
    name = "InMessage"
    message_type: InMessageType
    token: str
    payload: Optional[Any]


class FailureMode(str, Enum):
    BAD_TOKEN = "bad_token"
    BAD_MOVE = "bad_move"
    UNEXPECTED = "unexpected"
    NONE = "none"


class Reponse(BaseModel):
    name = "Response"
    failure_mode: FailureMode


class BoardMark(str, Enum):
    CIRCLE = CrossOrCircle.CIRCLE
    CROSS = CrossOrCircle.CROSS
    NONE = "none"


class BoardData(BaseModel):
    data: List[List[List[BoardMark]]]


class OutMessageType(str, Enum):
    WAITING_FOR_REGISTRATION = "waiting_for_registration"  # payload: CrossOrCircle.
    #                             Use the payload to determine which player you are

    BOARD_DATA = "board_data"  #     payload: BoardData

    WAITING_FOR_MOVE = "waiting_for_move"  # no payload
    WAITING_FOR_OTHER_MOVE = "waiting_for_other_move"  # no payload

    GAME_ENDED = "game_ended"  # payload: GameEndedPayload
    GAME_STARTED = "game_started"  # payload: GameStartedInformation


class GameEndedReason(str, Enum):
    CIRCLE_WON = "circle_won"
    CROSS_WON = "cross_won"
    CIRCLE_SURRENDER = "circle_surrender"
    CROSS_SURRENDER = "cross_surrender"
    PLAYER_QUIT = "player_quit"


class GameStartedInformation(BaseModel):
    opponent_name: str
    opponent_elo: str


class GameEndedPayload(BaseModel):
    reason: GameEndedReason
    elo_delta: Optional[float]
    opponent_elo_delta: Optional[float]


class OutMessage(BaseModel):
    name = "OutMessage"
    message_type: OutMessageType
    payload: Optional[Any]

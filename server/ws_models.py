from enum import Enum
from typing import Optional, Any
from pydantic import BaseModel

# Do serwera wysyłasz InMessage
# Serwer wysyła OutMessage i Response


class InMessageType(str, Enum):
    REGISTER = "register"  #   command, registers this token to this websocket
    #                                   ALWAYS send after WAITING_FOR_REGISTRATION request
    #                                   responds with BAD_TOKEN or NONE

    VERIFY = "verify"  #       command, verifies that this token is correct
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
    NONE = "none"


class Reponse(BaseModel):
    name = "Response"
    failure_mode: FailureMode


# TODO -implement model - probly some kind of table
class BoardData(BaseModel):
    pass


class OutMessageType(str, Enum):
    WAITING_FOR_REGISTRATION = "waiting_for_registration"  # no payload

    BOARD_DATA = "board_data"  # payload: BoardData

    WAITING_FOR_MOVE = "waiting_for_move"

    WAITING_FOR_OTHER_MOVE = "waiting_for_other_move"


class OutMessage(BaseModel):
    name = "OutMessage"
    message_type: OutMessageType
    payload: Optional[Any]

from datetime import datetime
from typing import Optional
from enum import Enum
from pydantic import BaseModel


class LeaderboardData(BaseModel):
    wins: int  #  initial - 0
    games: int  # initial - 0
    elo: float  # initial - 1500


class PlayerPublic(BaseModel):
    username: str
    leaderboard_data: LeaderboardData
    disabled: Optional[datetime]


class PlayerInternal(BaseModel):
    username: str
    secret: str
    leaderboard_data: LeaderboardData
    disabled: Optional[datetime]


class AvailableRoomInfo(BaseModel):
    player_elo: int
    identifier: str


class RegistrationDTO(BaseModel):
    username: str
    password: str


class RegistrationError(str, Enum):
    ALREADY_TAKEN = "already_taken"
    INVALID_USERNAME = "invalid_username"
    INVALID_PASSWORD = "invalid_password"


class Token(BaseModel):
    access_token: str
    token_type = "Bearer"


class RegistrationResponse(BaseModel):
    success: bool
    errors: Optional[list[RegistrationError]]

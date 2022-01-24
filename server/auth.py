from typing import Optional, Tuple
from datetime import timedelta, datetime
import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from tinydb import Query
from models import PlayerInternal, RegistrationDTO, RegistrationError, LeaderboardData
import database as db
from server import ANON
from elo import DEFAULT_ELO


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.environ.get("SECRET_KEY") or ""
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1000


def _validate_username(username: str) -> bool:
    if len(username) < 3:
        return False
    return True


def _validate_password(password: str) -> bool:
    if len(password) < 6 or len(password) > 256:
        return False
    return True


def register(dto: RegistrationDTO) -> Tuple[bool, RegistrationError]:
    errors = []
    if dto.username == ANON or get_player(dto.username):
        errors.append(RegistrationError.ALREADY_TAKEN)

    if not _validate_username(dto.username):
        errors.append(RegistrationError.INVALID_USERNAME)
    if not _validate_password(dto.password):
        errors.append(RegistrationError.INVALID_PASSWORD)

    if len(errors) != 0:
        return (False, errors)

    secret = get_password_hash(dto.password)
    new_player = PlayerInternal(
        username=dto.username,
        secret=secret,
        leaderboard_data=LeaderboardData(
            wins=0,
            games=0,
            elo=DEFAULT_ELO,
        ),
    )
    db.players.insert(new_player.dict())
    return True, []


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_player(username: str) -> PlayerInternal:
    player = Query()
    results = db.players.search(player.username == username)
    if len(results) == 1:
        player_dict = results[0]
        return PlayerInternal(**player_dict)
    return None


def authenticate_player(username: str, password: str) -> Optional[PlayerInternal]:
    player = get_player(username)
    if not player:
        return None
    if not verify_password(password, player.secret):
        return None
    return player


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_player(token: str = Depends(oauth2_scheme)) -> PlayerInternal:

    player = get_player_for_token(token)
    if player is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return player


def get_player_for_token(token: str) -> PlayerInternal:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from err
    player = get_player(username)
    return player


async def get_current_active_player(
    current_player: PlayerInternal = Depends(get_current_player),
) -> PlayerInternal:
    if current_player.disabled:
        raise HTTPException(status_code=400, detail="Inactive player")

    return current_player

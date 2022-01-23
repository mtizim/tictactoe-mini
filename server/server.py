from datetime import timedelta
import time
from typing import Dict

from fastapi import FastAPI, Depends, HTTPException, status, WebSocket
from fastapi.security import OAuth2PasswordRequestForm

from fastapi.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()


ANON = "anon"
DEFAULT_ELO = 1500

# pylint: disable=wrong-import-position
import auth

# pylint: disable=wrong-import-position
import models

# pylint: disable=wrong-import-position
import database

# pylint: disable=wrong-import-position
import game_room


app = FastAPI(title="TicTacToe3D")


@app.get("/player", response_model=models.PlayerPublic)
async def get_current_player(
    current_player: models.PlayerInternal = Depends(auth.get_current_active_player),
):
    """
    Returns public player data, fails on inactive player or anonymous token
    """
    return current_player


@app.post("/token", response_model=models.Token, responses={401: {}})
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Returns an user specific token
    """
    user = auth.authenticate_player(form_data.username, form_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token}


@app.post("/token/anon", response_model=models.Token)
async def anon_token():
    """
    Returns a new anonymous token
    """
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": ANON},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token}


@app.post("/register", response_model=models.RegistrationResponse)
async def register(dto: models.RegistrationDTO):
    """
    Registers an user,
    Name cannot be "anon"
    """
    success, errors = auth.register(dto)
    return models.RegistrationResponse(
        success=success,
        errors=errors,
    )


# pylint: disable=invalid-name
leaderboards_cached = None
# pylint: disable=invalid-name
leaderboards_cache_time = None


@app.get("/leaderboards", response_model=list[models.PlayerPublic])
def leaderboards():
    """
    Get player data for the first 25 players sorted by elo
    """
    # pylint: disable=global-statement
    global leaderboards_cached
    # pylint: disable=global-statement
    global leaderboards_cache_time
    request_time = time.time()
    if leaderboards_cached and request_time - leaderboards_cache_time < 60:
        return leaderboards_cached

    # this scales awfully, but is okay enough
    players = database.players.all()
    leaderboards_cache_time = request_time
    leaderboards_cached = sorted(players, key=lambda e: -e["leaderboard_data"]["elo"])[
        :25
    ]
    return leaderboards_cached


active_rooms: Dict[str, game_room.GameRoom] = {}


@app.post("/room/{room_id}", status_code=201, responses={409: {}})
def create_room(
    room_id: str,
    token: str = Depends(auth.oauth2_scheme),
):
    """
    Creates a room if it does not exist
    Returns a HTTP 409 on full rooms
    A game room times out after 30 minutes of no use
    """
    # pylint: disable=global-statement
    if room_id in active_rooms:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"The room with id {room_id} already exists",
            headers={"WWW-Authenticate": "Bearer"},
        )
    active_rooms[room_id] = game_room.GameRoom(token)
    print(active_rooms[room_id])


@app.websocket("/room/{room_id}/circle")
async def circle_websocket(
    wbs: WebSocket,
    room_id: str,
):
    """
    The ws for the circle player. Use this after room creation, for the first player.
    The connection will be rejected on bad token or nonexistent room
    """
    if room_id not in active_rooms:
        await wbs.close()
        return
    room = active_rooms[room_id]
    await room.register_token_for_circle(wbs)


@app.websocket("/room/{room_id}/cross")
async def cross_websocket(
    wbs: WebSocket,
    room_id: str,
):
    """
    The ws for the cross player. Use this after room creation, for the first player.
    The connection will be rejected on bad token or nonexistent room
    """
    if room_id not in active_rooms:
        await wbs.close()
        return
    room = active_rooms[room_id]
    await room.register_token_for_cross(wbs)


@app.websocket("/room/{room_id}/other")
async def other_websocket(
    wbs: WebSocket,
    room_id: str,
):
    """
    The ws for the second player that joins the room. Use this to join an existing room.
    The connection will be rejected on bad token or nonexistent room
    """
    if room_id not in active_rooms:
        await wbs.close()
        return
    room = active_rooms[room_id]
    await room.register_token_for_second_player(wbs)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

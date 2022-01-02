from datetime import timedelta

from fastapi import FastAPI, Depends, HTTPException, status, WebSocket
from fastapi.security import OAuth2PasswordRequestForm

import auth
import models

app = FastAPI(title="TicTacToe3D")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/player", response_model=models.PlayerPublic)
async def get_current_player(
    current_player: models.PlayerInternal = Depends(auth.get_current_active_player),
):
    """
    Returns public player data, fails on inactive player
    """
    return current_player


@app.post("/token", response_model=models.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
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
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/register")
async def register(dto: models.RegistrationDTO):
    success, errors = auth.register(dto)
    return models.RegistrationResponse(
        success=success,
        errors=errors,
    )


@app.get("/leaderboards", response_model=list[models.PlayerPublic])
async def leaderboards():
    """
    Get player data sorted by elo
    """
    return models.PlayerPublic(
        elo=1600,
    )

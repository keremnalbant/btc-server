import os
from datetime import datetime, timedelta

import uvicorn
from uuid import uuid4 as uuid
from fastapi import FastAPI, Request, Response, Depends, status
from fastapi.middleware.cors import CORSMiddleware

from socket_handler import socket_handler
from modules.guess.router import router as guess_router
from modules.user.router import router as user_router
from modules.game.router import router as game_router
from router import router as utils_router

app = FastAPI()
app.include_router(guess_router, prefix="/api/v1/guess", tags=["Guess"])
app.include_router(user_router, prefix="/api/v1/user", tags=["User"])
app.include_router(game_router, prefix="/api/v1/game", tags=["Game"])
app.include_router(utils_router, prefix="/api/v1/utils", tags=["Utils"])

app.mount("/", app=socket_handler.app)
app.add_middleware(CORSMiddleware,
                   allow_origins=[os.getenv("CLIENT_URL")],
                   allow_methods=["*"],
                   allow_headers=["*"],
                   allow_credentials=True)


@app.middleware("http")
async def add_session_id(request: Request, call_next):
    session_id = has_session_id = request.cookies.get("btc-session")
    if session_id is None:
        session_id = str(uuid())
    request.cookies.setdefault("btc-session", session_id)
    response: Response = await call_next(request)
    if has_session_id is None:
        response.set_cookie(
            key="btc-session", value=session_id, path="/", expires=datetime.utcnow()+timedelta(days=365))
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)

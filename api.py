"""
api.py — token server, compatible with livekit-agents 0.12.x
"""
import os
import uuid
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from livekit.api import AccessToken, VideoGrants
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("token-server")

app = FastAPI(title="Dishant Twin - Token Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TokenResponse(BaseModel):
    token: str
    ws_url: str
    room_name: str


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/token", response_model=TokenResponse)
async def get_token():
    api_key    = os.getenv("LIVEKIT_API_KEY")
    api_secret = os.getenv("LIVEKIT_API_SECRET")
    ws_url     = os.getenv("LIVEKIT_URL")

    if not all([api_key, api_secret, ws_url]):
        raise HTTPException(status_code=500, detail="LiveKit credentials missing in .env")

    room_name        = f"twin-{uuid.uuid4().hex[:12]}"
    visitor_identity = f"visitor-{uuid.uuid4().hex[:8]}"

    token = (
        AccessToken(api_key, api_secret)
        .with_identity(visitor_identity)
        .with_name("Portfolio Visitor")
        .with_grants(VideoGrants(
            room_join=True,
            room=room_name,
            can_publish=True,
            can_subscribe=True,
        ))
        .to_jwt()
    )

    logger.info(f"Token issued for room: {room_name}")
    return TokenResponse(token=token, ws_url=ws_url, room_name=room_name)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)

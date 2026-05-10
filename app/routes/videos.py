from fastapi import APIRouter, Depends, HTTPException, status
from app.auth import get_current_user
from app.models import User
from app import config
import os
import time
import hashlib


router = APIRouter(
    prefix="/videos",
    tags=["videos"]
)

BUNNY_LIBRARY_ID = os.getenv("BUNNY_LIBRARY_ID")
BUNNY_STREAM_TOKEN = os.getenv("BUNNY_STREAM_TOKEN")

print("BUNNY_LIBRARY_ID:", BUNNY_LIBRARY_ID)
print("BUNNY_STREAM_TOKEN:", BUNNY_STREAM_TOKEN)


def generar_bunny_stream_token(video_id: str, expires: int) -> str:

    raw = f"{BUNNY_STREAM_TOKEN}{video_id}{expires}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


@router.get("/{video_id}/stream")
async def obtener_stream_video(
    video_id: str,
    current_user: User = Depends(get_current_user)
):
    expires = int(time.time()) + 300
    token = generar_bunny_stream_token(video_id, expires)

    embed_url = (
        f"https://iframe.mediadelivery.net/embed/"
        f"{BUNNY_LIBRARY_ID}/{video_id}"
        f"?token={token}&expires={expires}"
        f"&autoplay=true"
        f"&loop=true"
    )

    return {
        "embed_url": embed_url,
        "expires_in": 300
    }

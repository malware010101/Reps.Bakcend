from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
import httpx
import os
import uuid
from app.auth import get_current_user
from app.models import User

router = APIRouter(
    prefix="/upfiles",
    tags=["upfiles"]
)

BUNNY_STORAGE_ZONE = os.getenv("BUNNY_STORAGE_ZONE")
BUNNY_STORAGE_ACCESS_KEY = os.getenv("BUNNY_STORAGE_ACCESS_KEY")
BUNNY_STORAGE_REGION = os.getenv("BUNNY_STORAGE_REGION")


@router.post("/image")
async def upload_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):

    try:
        file_bytes = await file.read()

        # Nombre único
        unique_filename = f"{uuid.uuid4()}_{file.filename}"

        # Carpeta por usuario
        path = f"users/{current_user.id}/pesajes/{unique_filename}"

        upload_url = f"https://{BUNNY_STORAGE_REGION}/{BUNNY_STORAGE_ZONE}/{path}"

        headers = {
            "AccessKey": BUNNY_STORAGE_ACCESS_KEY,
            "Content-Type": file.content_type
        }

        async with httpx.AsyncClient() as client:
            response = await client.put(
                upload_url,
                content=file_bytes,
                headers=headers
            )

        if response.status_code != 201:
            raise HTTPException(
                status_code=400, detail="Error subiendo imagen a Bunny")

        # URL pública CDN
        public_url = f"https://{BUNNY_STORAGE_ZONE}.b-cdn.net/{path}"

        return {"url": public_url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

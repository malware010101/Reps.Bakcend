# app/services/bunny_storage.py

from fastapi import UploadFile, HTTPException
import httpx
import os
import uuid

BUNNY_STORAGE_ZONE = os.getenv("BUNNY_STORAGE_ZONE")
BUNNY_STORAGE_ACCESS_KEY = os.getenv("BUNNY_STORAGE_ACCESS_KEY")
BUNNY_STORAGE_REGION = os.getenv(
    "BUNNY_STORAGE_REGION", "storage.bunnycdn.com")


async def upload_img(file: UploadFile, path: str) -> str:
    if not BUNNY_STORAGE_ZONE or not BUNNY_STORAGE_ACCESS_KEY or not BUNNY_STORAGE_REGION:
        raise HTTPException(
            status_code=500, detail="Faltan variables de Bunny Storage")

    file_bytes = await file.read()

    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    full_path = f"{path.rstrip('/')}/{unique_filename}"

    upload_url = f"https://{BUNNY_STORAGE_REGION}/{BUNNY_STORAGE_ZONE}/{full_path}"

    headers = {
        "AccessKey": BUNNY_STORAGE_ACCESS_KEY,
        "Content-Type": file.content_type or "application/octet-stream",
    }

    async with httpx.AsyncClient() as client:
        response = await client.put(
            upload_url,
            content=file_bytes,
            headers=headers,
        )

    if response.status_code != 201:
        raise HTTPException(
            status_code=400,
            detail=f"Error subiendo imagen a Bunny: {response.text}"
        )

    public_url = f"https://{BUNNY_STORAGE_ZONE}.b-cdn.net/{full_path}"
    return public_url

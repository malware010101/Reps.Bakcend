from fastapi import APIRouter, UploadFile, File, Depends
from datetime import datetime
import asyncio

from app.auth import get_current_user
from app.models import User
from app.services.bunny_storage import upload_img

router = APIRouter(
    prefix="/upfiles",
    tags=["upfiles"]
)


@router.post("/pesajes")
async def upload_pesaje_images(
    foto_frontal: UploadFile | None = File(None),
    foto_izquierda: UploadFile | None = File(None),
    foto_derecha: UploadFile | None = File(None),
    foto_trasera: UploadFile | None = File(None),
    current_user: User = Depends(get_current_user),
):

    folder = datetime.now().strftime("%Y/%m/%d/%H-%M-%S")
    path = f"users/{current_user.id}/pesajes/{folder}"

    tasks = {}

    if foto_frontal:
        tasks["foto_frontal_url"] = upload_img(foto_frontal, path)

    if foto_izquierda:
        tasks["foto_izquierda_url"] = upload_img(foto_izquierda, path)

    if foto_derecha:
        tasks["foto_derecha_url"] = upload_img(foto_derecha, path)

    if foto_trasera:
        tasks["foto_trasera_url"] = upload_img(foto_trasera, path)

    results = await asyncio.gather(*tasks.values())

    response = {
        key: url
        for key, url in zip(tasks.keys(), results)
    }

    return response

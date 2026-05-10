
from fastapi import APIRouter, Depends
from app.models import User
from app.models import Anamnesis
from app.auth import get_current_user
from fastapi import HTTPException
from app.Schemas.anamnesis_schema import AnamnesisSchema


router = APIRouter(
    prefix="/anamnesis",
    tags=["anamnesis"]
)


@router.post("/")
async def guardar_anamnesis(
    data: AnamnesisSchema,
    current_user: User = Depends(get_current_user)
):
    anamnesis = await Anamnesis.get_or_none(usuario=current_user)

    if anamnesis:
        anamnesis.datos = data
        await anamnesis.save()
        return {"message": "Anamnesis actualizada"}

    nueva = await Anamnesis.create(
        usuario=current_user,
        datos=data.model_dump()
    )

    return {"message": "Anamnesis creada", "id": nueva.id}


@router.get("/{usuario_id}")
async def obtener_anamnesis(
    usuario_id: int,
    current_user: User = Depends(get_current_user)
):
    if current_user.rol not in ["admin", "coach"] and current_user.id != usuario_id:
        raise HTTPException(status_code=403, detail="No autorizado")

    anamnesis = await Anamnesis.get_or_none(usuario_id=usuario_id)
    if not anamnesis:
        return None

    return {
        "usuario_id": usuario_id,
        "datos": anamnesis.datos,
        "creada_en": anamnesis.creada_en
    }

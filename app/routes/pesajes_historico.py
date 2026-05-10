from fastapi import APIRouter, Depends, HTTPException, status
from tortoise.exceptions import DoesNotExist

from app.auth import get_current_user
from app.models import User, PesajeHistorico
from app.Schemas.pesajes_historico_schemas import (
    PesajeHistoricoInSchema,
    PesajeHistoricoOutSchema
)

router = APIRouter(
    prefix="/pesajes/historico",
    tags=["pesajes_historico"]
)


@router.post(
    "",
    response_model=PesajeHistoricoOutSchema,
    status_code=status.HTTP_201_CREATED
)
async def registrar_pesaje(
    data: PesajeHistoricoInSchema,
    current_user: User = Depends(get_current_user)
):
    pesaje = await PesajeHistorico.create(
        usuario=current_user,
        peso_kg=data.peso_kg,
        grasa_pct=data.grasa_pct,
        masa_muscular_kg=data.masa_muscular_kg,
        imc=data.imc,
        foto_frontal_url=data.foto_frontal_url,
        foto_izquierda_url=data.foto_izquierda_url,
        foto_derecha_url=data.foto_derecha_url,
        foto_trasera_url=data.foto_trasera_url
    )

    return PesajeHistoricoOutSchema(
        id=pesaje.id,
        peso_kg=pesaje.peso_kg,
        grasa_pct=pesaje.grasa_pct,
        masa_muscular_kg=pesaje.masa_muscular_kg,
        imc=pesaje.imc,
        foto_frontal_url=pesaje.foto_frontal_url,
        foto_izquierda_url=pesaje.foto_izquierda_url,
        foto_derecha_url=pesaje.foto_derecha_url,
        foto_trasera_url=pesaje.foto_trasera_url,
        registrado_en=pesaje.registrado_en.isoformat()
    )


@router.get("", response_model=list[PesajeHistoricoOutSchema])
async def obtener_mis_pesajes(
    current_user: User = Depends(get_current_user)
):
    registros = await PesajeHistorico.filter(
        usuario=current_user
    ).order_by("-registrado_en")

    return [
        PesajeHistoricoOutSchema(
            id=r.id,
            peso_kg=r.peso_kg,
            grasa_pct=r.grasa_pct,
            masa_muscular_kg=r.masa_muscular_kg,
            imc=r.imc,
            foto_frontal_url=r.foto_frontal_url,
            foto_izquierda_url=r.foto_izquierda_url,
            foto_derecha_url=r.foto_derecha_url,
            foto_trasera_url=r.foto_trasera_url,
            registrado_en=r.registrado_en.isoformat()
        )
        for r in registros
    ]


@router.get("/usuario/{usuario_id}", response_model=list[PesajeHistoricoOutSchema])
async def obtener_pesajes_por_usuario(
    usuario_id: int,
    current_user: User = Depends(get_current_user)
):
    if current_user.rol not in ["admin", "coach"]:
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso"
        )
    try:
        await User.get(id=usuario_id)
    except DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    registros = await PesajeHistorico.filter(
        usuario_id=usuario_id
    ).order_by("-registrado_en")

    return [
        PesajeHistoricoOutSchema(
            id=r.id,
            peso_kg=r.peso_kg,
            grasa_pct=r.grasa_pct,
            masa_muscular_kg=r.masa_muscular_kg,
            imc=r.imc,
            foto_frontal_url=r.foto_frontal_url,
            foto_izquierda_url=r.foto_izquierda_url,
            foto_derecha_url=r.foto_derecha_url,
            foto_trasera_url=r.foto_trasera_url,
            registrado_en=r.registrado_en.isoformat()
        )
        for r in registros
    ]

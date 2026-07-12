from fastapi import APIRouter, Depends, HTTPException, status
from tortoise.exceptions import DoesNotExist

from app.auth import get_current_user
from app.models import User, PesajeHistorico
from app.Schemas.pesajes_historico_schemas import (
    PesajeHistoricoInSchema,
    PesajeHistoricoOutSchema
)
from app.services.pesajes import normalizar_pesaje

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
    normalizado = normalizar_pesaje(
        peso_kg=data.peso_kg,
        grasa_valor=data.grasa_valor,
        grasa_tipo=data.grasa_tipo,
        musculo_valor=data.musculo_valor,
        musculo_tipo=data.musculo_tipo,
    )
    pesaje = await PesajeHistorico.create(
        usuario_id=current_user.id,
        peso_kg=data.peso_kg,

        grasa_pct=normalizado["grasa_pct"],
        grasa_kg=normalizado["grasa_kg"],

        masa_muscular_pct=normalizado["masa_muscular_pct"],
        masa_muscular_kg=normalizado["masa_muscular_kg"],

        imc=data.imc,

        foto_frontal_url=data.foto_frontal_url,
        foto_izquierda_url=data.foto_izquierda_url,
        foto_derecha_url=data.foto_derecha_url,
        foto_trasera_url=data.foto_trasera_url
    )

    return PesajeHistoricoOutSchema.model_validate(pesaje)


@router.get("", response_model=list[PesajeHistoricoOutSchema])
async def obtener_mis_pesajes(
    current_user: User = Depends(get_current_user)
):
    registros = await PesajeHistorico.filter(
        usuario=current_user
    ).order_by("-registrado_en")

    return [PesajeHistoricoOutSchema.model_validate(r) for r in registros]


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

    return [PesajeHistoricoOutSchema.model_validate(r) for r in registros]

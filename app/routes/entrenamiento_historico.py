from fastapi import APIRouter, Depends, HTTPException, status
from tortoise.exceptions import DoesNotExist

from app.auth import get_current_user
from app.models import User, EntrenamientoActivo, EntrenamientoHistorico
from app.Schemas.entrenamiento_schemas import EntrenamientoHistoricoInSchema, EntrenamientoHistoricoOutSchema

router = APIRouter(
    prefix="/entrenamiento/historico",
    tags=["entrenamiento_historico"]
)


@router.post(
    "",
    response_model=EntrenamientoHistoricoOutSchema,
    status_code=status.HTTP_201_CREATED
)
async def registrar_entrenamiento_historico(
    data: EntrenamientoHistoricoInSchema,
    current_user: User = Depends(get_current_user)
):
    # Validar entrenamiento activo
    try:
        entrenamiento = await EntrenamientoActivo.get(
            id=data.entrenamiento_id,
            usuario=current_user,
            activo=True
        ).prefetch_related("programa")
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entrenamiento activo no encontrado"
        )

    programa = entrenamiento.programa

    # Crear registro histórico
    historico = await EntrenamientoHistorico.create(
        usuario=current_user,
        entrenamiento_activo=entrenamiento,
        programa_id=programa.id,
        programa_nombre=programa.nombre,
        dia_realizado=data.dia_realizado
    )

    # Respuesta
    return EntrenamientoHistoricoOutSchema(
        id=historico.id,
        programa_nombre=historico.programa_nombre,
        dia_realizado=historico.dia_realizado,
        completado_en=historico.completado_en.isoformat()
    )


@router.get("", response_model=list[EntrenamientoHistoricoOutSchema])
async def obtener_historico(
    current_user: User = Depends(get_current_user)
):
    registros = await EntrenamientoHistorico.filter(
        usuario=current_user
    ).order_by("-completado_en")

    return [
        EntrenamientoHistoricoOutSchema(
            id=r.id,
            programa_nombre=r.programa_nombre,
            dia_realizado=r.dia_realizado,
            completado_en=r.completado_en.isoformat()
        )
        for r in registros
    ]

# enpoints para admin


@router.get("/usuario/{usuario_id}", response_model=list[EntrenamientoHistoricoOutSchema])
async def obtener_historico_por_usuario(
    usuario_id: int,
    current_user: User = Depends(get_current_user)
):
    # 🔐 Validación de rol
    if current_user.rol not in ["admin", "coach"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver el historial de otros usuarios"
        )

    # Validar que el usuario exista
    try:
        await User.get(id=usuario_id)
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    registros = await EntrenamientoHistorico.filter(
        usuario_id=usuario_id
    ).order_by("-completado_en")

    return [
        EntrenamientoHistoricoOutSchema(
            id=r.id,
            programa_nombre=r.programa_nombre,
            dia_realizado=r.dia_realizado,
            completado_en=r.completado_en.isoformat()
        )
        for r in registros
    ]

from fastapi import APIRouter, HTTPException, status, Depends
from app.Schemas.nutricion_schemas import DatosNutricion, PlanNutricionCreate
from app.services import nutricion as nutricion_service
from app.models import PlanNutricion, User
from app.services.menu_base import generar_menu_base
from app.services.resolver_menu import resolver_menu
from app.services.nutricion import generar_porcentajes
from app.auth import get_current_user
from tortoise.exceptions import DoesNotExist

import json
from datetime import datetime, timedelta, timezone

router = APIRouter()


@router.post("/nutricion/plan")
async def generar_plan(data: DatosNutricion):
    # Calcular la fokin TMB
    tmb = nutricion_service.calcular_tmb(
        peso=data.peso,
        altura=data.altura,
        edad=data.edad,
        genero=data.genero
    )

    # Calcular el fokin GET
    get = nutricion_service.calcular_get(
        tmb=tmb,
        nivel_actividad=data.nivelActividad
    )

    resultado = nutricion_service.distribuir_macros(
        get=get,
        objetivo=data.objetivo,
        peso=data.peso,
        enfermedades=data.enfermedades,
        nivel_actividad=data.nivelActividad,
        genero=data.genero
    )

    macros = resultado["macros"]
    calorias_finales = resultado["calorias_finales"]

    # Generar el fokin menu
    menus_base = generar_menu_base(objetivo=data.objetivo)
    distribucion = generar_porcentajes(data.comidas, data.enfermedades)
    menus_resueltos = resolver_menu(
        menus_base=menus_base,
        macros_diarios=macros,
        distribucion=distribucion
    )

    # los fokin resultados pa ponerte bien modo Dios griego/a
    return {
        "calorias_diarias": calorias_finales,
        "macronutrientes": macros,
        "opciones_menu": [
            {"opcion": 1, "menu": menus_resueltos["menu_1"]},
            {"opcion": 2, "menu": menus_resueltos["menu_2"]},
            {"opcion": 3, "menu": menus_resueltos["menu_3"]},
        ],
        "datos_recibidos": data.model_dump()
    }

# endpoint para guardar el plan


@router.post("/nutricion/plan/guardar")
async def guardar_plan(plan: PlanNutricionCreate):

    # Busca el plan activo del usuario
    await PlanNutricion.filter(
        usuario_id=plan.usuario_id,
        activo=True
    ).update(activo=False)

    # Fechas del nuevo plan
    ahora = datetime.now(timezone.utc)
    fecha_fin = ahora + timedelta(days=29)

    nuevo_plan = await PlanNutricion.create(
        usuario_id=plan.usuario_id,
        calorias_diarias=plan.calorias_diarias,
        macronutrientes=plan.macronutrientes,
        opciones_menu=plan.opciones_menu,
        datos_recibidos=plan.datos_recibidos,

        activo=True,
        estado="activo",
        fecha_inicio=ahora,
        fecha_fin=fecha_fin
    )

    return {
        "mensaje": "Plan nutricional guardado correctamente",
        "plan_id": nuevo_plan.id,
        "fecha_inicio": ahora.isoformat(),
        "fecha_fin": fecha_fin.isoformat(),
        "estado": "activo"
    }

# endpint para obtener el plan


@router.get("/nutricion/plan/activo/{usuario_id}")
async def obtener_plan_activo(
    usuario_id: int,
    current_user: User = Depends(get_current_user)
):
    # Solo puede ver
    # - Su propio plan
    # - Admin
    # - Coach

    if current_user.rol not in ["admin", "coach"] and current_user.id != usuario_id:
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso para ver este plan nutricional"
        )

    plan = await PlanNutricion.filter(
        usuario_id=usuario_id,
        activo=True
    ).first()

    if not plan:
        raise HTTPException(
            status_code=404,
            detail="No cuentas con un plan nutricional activo, solicita un plan."
        )

    ahora = datetime.now(timezone.utc)

    estado_calculado = plan.estado
    if plan.fecha_fin and ahora > plan.fecha_fin:
        estado_calculado = "vencido"

    creado_en = None
    if getattr(plan, "creado_en", None):
        try:
            creado_en = plan.creado_en.isoformat()
        except Exception:
            creado_en = str(plan.creado_en)

    return {
        "id": plan.id,
        "usuario_id": plan.usuario_id,
        "calorias_diarias": plan.calorias_diarias,
        "macronutrientes": plan.macronutrientes,
        "opciones_menu": plan.opciones_menu,
        "datos_recibidos": plan.datos_recibidos,
        "creado_en": creado_en,
        "fecha_inicio": plan.fecha_inicio.isoformat() if plan.fecha_inicio else None,
        "fecha_fin": plan.fecha_fin.isoformat() if plan.fecha_fin else None,
        "estado": estado_calculado,
        "activo": plan.activo
    }

from fastapi import APIRouter, HTTPException
from app.Schemas.nutricion_schemas import DatosNutricion, PlanNutricionCreate
from app.services import nutricion as nutricion_service
from app.models import PlanNutricion
import json

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

    # Distribuir los fokin MACROS
    macros = nutricion_service.distribuir_macros(
        get=get,
        objetivo=data.objetivo,
        peso=data.peso
    )

    # Generar el fokin menu
    menu1 = await nutricion_service.generar_menu(macros=macros, comidas=data.comidas, tipoDieta=data.tipoDieta)
    menu2 = await nutricion_service.generar_menu(macros=macros, comidas=data.comidas, tipoDieta=data.tipoDieta)
    menu3 = await nutricion_service.generar_menu(macros=macros, comidas=data.comidas, tipoDieta=data.tipoDieta)

    # los fokin resultados pa ponerte bien modo Dios griego/a
    return {
        "calorias_diarias": get,
        "macronutrientes": macros,
        "opciones_menu": [
            {"opcion": 1, "menu": menu1},
            {"opcion": 2, "menu": menu2},
            {"opcion": 3, "menu": menu3},
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

    nuevo_plan = await PlanNutricion.create(
        usuario_id=plan.usuario_id,
        calorias_diarias=plan.calorias_diarias,
        macronutrientes=plan.macronutrientes,
        opciones_menu=plan.opciones_menu,
        datos_recibidos=plan.datos_recibidos,
        activo=True
    )

    return {
        "mensaje": "Plan nutricional guardado correctamente",
        "plan_id": nuevo_plan.id
    }

# endpint para obtener el plan


@router.get("/nutricion/plan/activo/{usuario_id}")
async def obtener_plan_activo(usuario_id: int):
    # Busca el plan activo del usuario
    plan = await PlanNutricion.filter(usuario_id=usuario_id, activo=True).first()

    if not plan:
        raise HTTPException(
            status_code=404, detail="No cuentas con un plan nutricional activo, solicita un plan.")

    # Construir respuesta segura (convertir created datetime si existe)
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
        "activo": plan.activo
    }

from fastapi import APIRouter
from app.Schemas.nutricion_schemas import DatosNutricion
from app.services import nutricion as nutricion_service

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
    menu1 = await nutricion_service.generar_menu(macros=macros)
    menu2 = await nutricion_service.generar_menu(macros=macros)
    menu3 = await nutricion_service.generar_menu(macros=macros)
    
    # los fokin resultados pa ponerte bien modo Dios griego/a
    return {
        "calorias_diarias": get,
        "macronutrientes": macros,
        "opciones_menu" : [
            {"opcion": 1, "menu": menu1},
            {"opcion": 2, "menu": menu2},
            {"opcion": 3, "menu": menu3},
        ],
        "datos_recibidos": data.model_dump()
    }
    
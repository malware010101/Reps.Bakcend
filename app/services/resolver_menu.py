from typing import Dict
from app.services.resolver_receta import resolver_receta

MAPEO_COMIDAS = {
    "desayuno": "Desayuno",
    "colacion": "Colación1",
    "almuerzo": "Almuerzo",
    "comida": "Comida",
    "snack": "Snack",
    "cena": "Cena",
}


def resolver_menu(
    menus_base: Dict[str, dict],
    macros_diarios: Dict[str, float],
    distribucion: Dict[str, float]
) -> Dict[str, dict]:

    #  Normalización defensiva
    proteinas = macros_diarios.get("proteinas")
    carbohidratos = macros_diarios.get("carbohidratos")
    grasas = macros_diarios.get("grasas")

    if proteinas is None or carbohidratos is None or grasas is None:
        raise ValueError(f"Macros diarios incompletos: {macros_diarios}")

    menus_resueltos = {}

    for nombre_menu, menu in menus_base.items():

        menu_resuelto = {}

        for comida_key, receta in menu.items():

            nombre_distribucion = MAPEO_COMIDAS.get(comida_key)

            # Seguridad
            if not nombre_distribucion:
                continue

            porcentaje = distribucion.get(nombre_distribucion, 0)

            if porcentaje is None or porcentaje <= 0:
                continue

            # Macros objetivos por comida
            macros_comida = {
                "proteina": round(proteinas * porcentaje, 2),
                "carbohidrato": round(carbohidratos * porcentaje, 2),
                "grasa": round(grasas * porcentaje, 2),
            }

            receta_resuelta = resolver_receta(
                receta=receta,
                macros_objetivo=macros_comida
            )

            menu_resuelto[comida_key] = receta_resuelta

        menus_resueltos[nombre_menu] = menu_resuelto

    return menus_resueltos

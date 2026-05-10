# app/services/menu_base.py

import random
from typing import Dict, List
from app.services.recetas.desayunos import Desayunos
from app.services.recetas.almuerzos import Almuerzos
from app.services.recetas.comidas import Comidas
from app.services.recetas.colaciones import COLACIONES_POR_OBJETIVO
from app.services.recetas.snacks import SNACKS_POR_OBJETIVO
from app.services.recetas.cenas import CENAS_LIGERAS, CENAS_MODERADAS, CENAS_PESADAS
from app.utils.utils import normalizar_objetivo


def seleccionar_recetas_sin_repetir(
    recetas: List[dict],
    cantidad: int
) -> List[dict]:
    if len(recetas) < cantidad:
        raise ValueError("No hay suficientes recetas para evitar repetición")

    return random.sample(recetas, cantidad)


def seleccionar_cenas_por_objetivo(objetivo: str) -> List[dict]:
    """
    Define qué tipo de cenas usar en el PLAN BASE
    (sin considerar entrenamiento todavía).
    """

    objetivo = normalizar_objetivo(objetivo)

    if objetivo == "Perdida de Grasa":
        return CENAS_LIGERAS

    if objetivo in ("Mantenimiento", "Hipertrofia"):
        return CENAS_MODERADAS

    return CENAS_LIGERAS


def generar_menu_base(objetivo: str) -> Dict[str, dict]:
    """
    Genera 3 menús base diferentes (sin resolver macros).
    Cada menú tiene recetas distintas entre sí.
    """

    objetivo = normalizar_objetivo(objetivo)

    menus = {}

    # Recetas fijas (no dependen de objetivo)
    desayunos = seleccionar_recetas_sin_repetir(Desayunos, 3)
    almuerzos = seleccionar_recetas_sin_repetir(Almuerzos, 3)
    comidas = seleccionar_recetas_sin_repetir(Comidas, 3)

    # Recetas dependientes del objetivo
    colaciones_disponibles = COLACIONES_POR_OBJETIVO[objetivo]
    snacks_disponibles = SNACKS_POR_OBJETIVO[objetivo]
    cenas_disponibles = seleccionar_cenas_por_objetivo(objetivo)

    colaciones = seleccionar_recetas_sin_repetir(colaciones_disponibles, 3)
    snacks = seleccionar_recetas_sin_repetir(snacks_disponibles, 3)
    cenas = seleccionar_recetas_sin_repetir(cenas_disponibles, 3)

    for i in range(3):
        menus[f"menu_{i+1}"] = {
            "desayuno": desayunos[i],
            "colacion": colaciones[i],
            "almuerzo": almuerzos[i],
            "comida": comidas[i],
            "snack": snacks[i],
            "cena": cenas[i]
        }

    return menus

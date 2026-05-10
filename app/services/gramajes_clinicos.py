# app/services/gramajes_clinicos.py

from typing import Optional, Dict
from app.data.nutri_table import TABLA_NUTRIMENTAL


def calcular_gramos_base(
    ingrediente: str,
    macro_objetivo: float,
    diccionario_clinico: Dict
) -> Optional[float]:
    """
    Calcula gramos teóricos del alimento necesarios para alcanzar
    un objetivo de macronutriente, usando valores por 100 g.
    """

    if macro_objetivo <= 0:
        return None

    info = diccionario_clinico.get(ingrediente)
    tabla = TABLA_NUTRIMENTAL.get(ingrediente)

    if not info or not tabla:
        return None

    # Vegetales libres no escalan macros
    if info.get("tipo") == "libre":
        return None

    macro = info.get("macronutriente")

    # Seguridad clínica
    if macro not in tabla:
        return None

    aporte_por_100g = tabla[macro]

    if aporte_por_100g <= 0:
        return None

    # Fórmula clínica universal
    gramos_teoricos = (macro_objetivo / aporte_por_100g) * 100

    return gramos_teoricos

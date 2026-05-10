# app/services/porcion_clinica.py

from typing import Optional, Dict
from app.services.gramajes_clinicos import calcular_gramos_base
from app.services.redondeo_clinico import redondear_gramaje_clinico


def resolver_porcion_clinica(
    ingrediente: str,
    macro_objetivo: float,
    diccionario_clinico: Dict
) -> Optional[dict]:

    gramos_teoricos = calcular_gramos_base(
        ingrediente=ingrediente,
        macro_objetivo=macro_objetivo,
        diccionario_clinico=diccionario_clinico
    )

    if gramos_teoricos is None:
        return None

    return redondear_gramaje_clinico(
        ingrediente=ingrediente,
        gramos_teoricos=gramos_teoricos,
        diccionario_clinico=diccionario_clinico
    )

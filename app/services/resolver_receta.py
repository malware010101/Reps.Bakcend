# app/services/resolver_receta.py

from typing import Dict, List
from app.services.porcion_clinica import resolver_porcion_clinica
from app.services.diccionario_clinico import DICCIONARIO_CLINICO


def resolver_receta(
    receta: Dict,
    macros_objetivo: Dict[str, float]
) -> Dict:
    """
    Resuelve una receta completa en porciones clínicas humanas
    a partir de macros objetivo por comida.
    """

    ingredientes_resueltos = {}

    for categoria, ingredientes in receta["ingredientes"].items():

        # Vegetales libres no se calculan por macros
        if categoria == "vegetal":
            ingredientes_resueltos[categoria] = [
                {
                    "ingrediente": ing,
                    "cantidad": "libre",
                    "unidad": "al gusto",
                    "gramos_aprox": None
                }
                for ing in ingredientes
            ]
            continue

        macro_objetivo = macros_objetivo.get(categoria, 0)

        if not ingredientes or macro_objetivo <= 0:
            ingredientes_resueltos[categoria] = []
            continue

        macro_por_ingrediente = macro_objetivo / len(ingredientes)

        ingredientes_resueltos[categoria] = []

        for ingrediente in ingredientes:
            porcion = resolver_porcion_clinica(
                ingrediente=ingrediente,
                macro_objetivo=macro_por_ingrediente,
                diccionario_clinico=DICCIONARIO_CLINICO
            )

            if porcion:
                ingredientes_resueltos[categoria].append(porcion)

    return {
        "nombre": receta["nombre"],
        "descripcion": receta.get("descripcion", ""),
        "ingredientes": ingredientes_resueltos
    }

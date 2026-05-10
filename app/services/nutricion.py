from typing import Dict, List

from .catalogo import catalogo
import random

FACTORES_ACTIVIDAD = {
    "sedentary": 1.2,
    "light": 1.375,
    "moderate": 1.55,
    "intense": 1.725,
    "athlete": 1.9
}


def alimentos_por_categoria(categoria: str) -> List[Dict]:
    alimentos = []
    for alimento in catalogo:
        if alimento["categoria"] == categoria:
            alimentos.append(alimento)
    return alimentos


def calcular_tmb(peso: float, altura: float, edad: int, genero: str) -> float:

    if genero == "Masculino":
        tmb = (10 * peso) + (6.25 * altura) - (5 * edad) + 5
    elif genero == "Femenino":
        tmb = (10 * peso) + (6.25 * altura) - (5 * edad) - 161
    else:
        tmb = 0
    return round(tmb, 2)


def calcular_get(tmb: float, nivel_actividad: str) -> float:

    factor = FACTORES_ACTIVIDAD.get(nivel_actividad, 1.2)
    return round(tmb * factor, 2)


def distribuir_macros(
        get: float,
        objetivo: str,
        peso: float,
        enfermedades: List[str],
        nivel_actividad: str,
        genero: str
) -> Dict[str, float]:
    macros = {}

    es_diabetico = any(
        e in enfermedades
        for e in ["Diabetes tipo 2", "Resistencia a la insulina"]
    )
    # ajuste calorico para perdida de grasa
    if objetivo == "Perdida de Grasa":
        get = get * 0.80  # deficit del 20%

        # ajuste calorico para hipertrofia
    elif objetivo == "Hipertrofia":
        if nivel_actividad in ["sedentary", "light"]:
            superavit = 1.05  # superavit del 5%
        elif nivel_actividad == "moderate":
            superavit = 1.07  # superavit del 7%
        elif nivel_actividad == "intense":
            superavit = 1.10  # superavit del 10%
        elif nivel_actividad == "athlete":
            superavit = 1.12  # superavit del 12%
        else:  # fallback seguro
            superavit = 1.07
        # ajuste por genero (eficiencia energetica y evitar acumular mucha grasa en mujeres)
        if genero == "Femenino":
            superavit *= 0.85  # menos agresivo el superavit
        else:
            superavit *= 1.0

        get = round(get * superavit, 2)  # Masculino

    # Proteína
    if nivel_actividad in ["sedentary", "light"]:
        proteina_por_kg = 1.8
    elif nivel_actividad in ["moderate", "intense"]:
        proteina_por_kg = 2.0
    elif nivel_actividad == "athlete":
        proteina_por_kg = 2.2
    else:  # fallback seguro
        proteina_por_kg = 2.0
    gramos_proteina = peso * proteina_por_kg
    calorias_proteina = gramos_proteina * 4
    calorias_restantes = get - calorias_proteina

   # Tiene Diabetes o Resistencia a la insulina
    if es_diabetico:
        macros["carbohidratos"] = (calorias_restantes * 0.40) / 4
        macros["grasas"] = (calorias_restantes * 0.60) / 9

    # No patologicos
    elif objetivo == "Hipertrofia":
        macros["carbohidratos"] = (calorias_restantes * 0.60) / 4
        macros["grasas"] = (calorias_restantes * 0.40) / 9

    elif objetivo == "Perdida de Grasa":
        macros["carbohidratos"] = (calorias_restantes * 0.50) / 4
        macros["grasas"] = (calorias_restantes * 0.50) / 9

    else:  # Mantenimiento
        macros["carbohidratos"] = (calorias_restantes * 0.50) / 4
        macros["grasas"] = (calorias_restantes * 0.50) / 9

    macros["proteinas"] = gramos_proteina

    return {
        "calorias_finales": round(get, 2),
        "macros": {k: round(v, 2) for k, v in macros.items()}
    }


PORC_COMIDAS = {
    "Desayuno": 0.25,
    "Comida": 0.40,
    "Cena": 0.30,
    "Snack": 0.05
}


def generar_porcentajes(comidas: int, enfermedades: List[str]):

    es_diabetico = "Diabetes tipo 2" in enfermedades or "Resistencia a la insulina" in enfermedades
    if es_diabetico:
        distribuciones = {
            3: {
                "Desayuno": 0.30,
                "Comida": 0.45,
                "Cena": 0.25
            },
            4: {
                "Desayuno": 0.28,
                "Almuerzo": 0.22,
                "Comida": 0.30,
                "Cena": 0.20
            },
            5: {
                "Desayuno": 0.22,
                "Colación1": 0.10,
                "Almuerzo": 0.23,
                "Comida": 0.30,
                "Cena": 0.15
            },
            6: {
                "Desayuno": 0.20,
                "Colación1": 0.10,
                "Almuerzo": 0.20,
                "Comida": 0.25,
                "Snack": 0.10,
                "Cena": 0.15,
            }
        }
    else:
        distribuciones = {
            3: {
                "Desayuno": 0.30,
                "Comida": 0.45,
                "Cena": 0.25
            },
            4: {
                "Desayuno": 0.25,
                "Almuerzo": 0.25,
                "Comida": 0.30,
                "Cena": 0.20
            },
            5: {
                "Desayuno": 0.20,
                "Colación1": 0.10,
                "Almuerzo": 0.25,
                "Comida": 0.30,
                "Cena": 0.15
            },
            6: {
                "Desayuno": 0.18,
                "Colación1": 0.10,
                "Almuerzo": 0.22,
                "Comida": 0.25,
                "Snack": 0.10,
                "Cena": 0.15,
            }
        }
    return distribuciones.get(comidas)


def seleccionar_categoria_cena_base(objetivo: str) -> str:
    """
    Selecciona la categoría de cena BASE según el objetivo del usuario.
    No contempla entrenamiento (eso será una variante futura).
    """

    objetivo = objetivo.lower()

    if objetivo == "Perdida de Grasa":
        return "LIGERA"

    elif objetivo == "Mantenimiento":
        return "MODERADA"

    elif objetivo == "Hipertrofia":
        return "MODERADA"

    else:
        return "MODERADA"


def ajustar_carbohidratos_por_horario(distribucion, objetivo, horario):

    # HIPERTROFIA
    if objetivo != "Hipertrofia" or horario != "tarde":
        return distribucion

    if "Cena" in distribucion and "Comida" in distribucion:
        distribucion["Cena"] += 0.05
        distribucion["Comida"] -= 0.05

    return distribucion

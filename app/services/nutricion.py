from typing import Dict, List

from .catalogo import catalogo
import random
from .edamam_service import food_data

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


def distribuir_macros(get: float, objetivo: str, peso: float) -> Dict[str, float]:
    macros = {}

    proteina_por_kg = 2.0 if objetivo == "Hipertrofia" else 1.8
    gramos_proteina = peso * proteina_por_kg

    calorias_proteina = gramos_proteina * 4
    calorias_restantes = get - calorias_proteina

    if objetivo == "Hipertrofia":
        macros["carbohidratos"] = (calorias_restantes * 0.50) / 4
        macros["grasas"] = (calorias_restantes * 0.50) / 9
    elif objetivo == "Perdida de Grasa":
        macros["carbohidratos"] = (calorias_restantes * 0.40) / 4
        macros["grasas"] = (calorias_restantes * 0.60) / 9
    else:
        macros["carbohidratos"] = (calorias_restantes * 0.50) / 4
        macros["grasas"] = (calorias_restantes * 0.50) / 9

    macros["proteinas"] = gramos_proteina

    return {k: round(v, 2) for k, v in macros.items()}


PORC_COMIDAS = {
    "Desayuno": 0.25,
    "Comida": 0.40,
    "Cena": 0.30,
    "Snack": 0.05
}


def generar_porcentajes(comidas: int):

    # Distribuciones diseñadas .
    distribuciones = {
        3: {
            "Desayuno": 0.30,
            "Comida": 0.45,
            "Cena": 0.25
        },
        4: {
            "Desayuno": 0.25,
            "Comida": 0.40,
            "Cena": 0.25,
            "Snack": 0.10
        },
        5: {
            "Desayuno": 0.20,
            "Colación1": 0.10,
            "Comida": 0.40,
            "Colación2": 0.10,
            "Cena": 0.20
        },
        6: {
            "Desayuno": 0.20,
            "Colación1": 0.10,
            "Comida": 0.35,
            "Colación2": 0.10,
            "Cena": 0.20,
            "Snack": 0.05
        }
    }

    return distribuciones.get(comidas)


async def generar_menu(macros: Dict[str, float], comidas: int, tipoDieta: str) -> List[Dict]:
    menu = []

    distribucion = generar_porcentajes(comidas)

    for comida, porcentaje in distribucion.items():

        alimentos_comida = []

        macros_comida = {
            "proteinas": round(macros["proteinas"] * porcentaje, 2),
            "carbohidratos": round(macros["carbohidratos"] * porcentaje, 2),
            "grasas": round(macros["grasas"] * porcentaje, 2),
        }

        if comida in ["Snack", "Colación1", "Colación2"]:
            frutas = [a for a in catalogo["carbohidrato"]
                      if a["c"] > 8]  # frutas
            if frutas:
                alimento = random.choice(frutas)
                alimentos_comida.append({
                    "nombre": alimento["nombre"],
                    "gramos": 120  # Porción estándar de snack
                })
            menu.append({"comida": comida, "alimentos": alimentos_comida})
            continue

        def filtrar_por_dieta(lista):
            if tipoDieta == "vegano":
                return [a for a in lista if a.get("dieta") == "vegano"]
            if tipoDieta == "vegetariana":
                return [a for a in lista if a.get("dieta") in ["vegano", "vegetariano"]]
            if tipoDieta == 'normal':
                return [a for a in lista if a.get("dieta") == "normal"]

            return lista

        # SELECCIÓN POR CATEGORÍA
        categorias = {
            "proteina": filtrar_por_dieta(catalogo["proteina"]),
            "carbohidrato": catalogo["carbohidrato"],
            "grasa": catalogo["grasa"],
            "vegetal": catalogo["vegetal"],
        }

        for categoria, macro_key in [
            ("proteina", "proteinas"),
            ("carbohidrato", "carbohidratos"),
            ("grasa", "grasas"),
            ("vegetal", None),
        ]:

            lista = categorias[categoria]
            if not lista:
                continue

            alimento = random.choice(lista)

            if categoria == "vegetal":
                gramos = 120  # porción fija
            else:
                valor_macro = alimento["p" if categoria == "proteina" else
                                       "c" if categoria == "carbohidrato" else
                                       "g"]

                if valor_macro == 0:
                    continue

                gramos = (macros_comida[macro_key] / valor_macro) * 100

            alimentos_comida.append({
                "nombre": alimento["nombre"],
                "gramos": round(gramos)
            })

        menu.append({
            "comida": comida,
            "alimentos": alimentos_comida
        })

    return menu

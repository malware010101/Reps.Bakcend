from typing import Dict, List
from .alimentos import alimentos_sugeridos
import random
from .edamam_service import food_data

# Factores de actividad física para el cálculo del GET
FACTORES_ACTIVIDAD = {
    "sedentary": 1.2,
    "light": 1.375,
    "moderate": 1.55,
    "intense": 1.725,
    "athlete": 1.9
}

def calcular_tmb(peso: float, altura: float, edad: int, genero: str) -> float:
    """Calcula la Tasa Metabolica Basal usando la formula de Mifflin-St Jeor."""
    if genero == "Masculino":
        tmb = (10 * peso) + (6.25 * altura) - (5 * edad) + 5
    elif genero == "Femenino":
        tmb = (10 * peso) + (6.25 * altura) - (5 * edad) - 161
    else:
        tmb = 0
    return round(tmb, 2)

def calcular_get(tmb: float, nivel_actividad: str) -> float:
    """Calcula el Gasto Energético Total multiplicando la TMB por el factor de actividad."""
    factor = FACTORES_ACTIVIDAD.get(nivel_actividad, 1.2)
    get = tmb * factor
    return round(get, 2)

def distribuir_macros(get: float, objetivo: str, peso: float) -> Dict[str, float]:
    """
    Distribuye los macronutrientes de protes, carbs y grasas
    segun el objetivo y el peso del futuro asgardiano
    """
    macros = {}

    # GRAMOS DE PROTEINA
    proteina_por_kg = 2.0 if objetivo == "Hipertrofia" else 1.8
    gramos_proteina = peso * proteina_por_kg
    
    # CALORIAS RESTANTES para carbohidratos y grasas
    calorias_proteina = gramos_proteina * 4
    calorias_restantes = get - calorias_proteina
    
    # DISTRIBUCIÓN DE CARBOHIDRATOS Y GRASAS
    if objetivo == "Hipertrofia":
        # 50% de las calorías restantes para carbos, 50% para grasas
        macros["carbohidratos"] = (calorias_restantes * 0.50) / 4
        macros["grasas"] = (calorias_restantes * 0.50) / 9
    elif objetivo == "Perdida de Grasa":
        #  40% de las calorías restantes para carbos, 60% para grasas
        macros["carbohidratos"] = (calorias_restantes * 0.40) / 4
        macros["grasas"] = (calorias_restantes * 0.60) / 9
    else:  # Mantenimiento
        # 50% de las calorías restantes para carbos, 50% para grasas
        macros["carbohidratos"] = (calorias_restantes * 0.50) / 4
        macros["grasas"] = (calorias_restantes * 0.50) / 9
        
    macros["proteinas"] = gramos_proteina
    
    for key, value in macros.items():
        macros[key] = round(value, 2)
        
    return macros

PORCENTAJES_COMIDAS = {
    "Desayuno": 0.25,
    "Comida": 0.40,
    "Cena": 0.30,
    "Snack": 0.05
}

async def generar_menu(macros: Dict[str, float]) -> List[Dict]:
    menu = []
    
    macros_diarios = {
        "proteinas": macros["proteinas"],
        "carbohidratos": macros["carbohidratos"],
        "grasas": macros["grasas"]
    }
    comidas_del_dia = ["Desayuno", "Snack", "Comida", "Cena"]

    # Copias de las listas para poder eliminar elementos
    proteinas_disponibles = list(alimentos_sugeridos["proteina"])
    carbos_disponibles = list(alimentos_sugeridos["carbohidrato"])
    grasas_disponibles = list(alimentos_sugeridos["grasa"])
    vegetales_disponibles = list(alimentos_sugeridos["vegetales"])
    snacks_disponibles = list(alimentos_sugeridos["snack"])

    for comida in comidas_del_dia:
        porcentaje = PORCENTAJES_COMIDAS.get(comida, 0)
        macros_comida = {
            "proteinas": macros_diarios["proteinas"] * porcentaje,
            "carbohidratos": macros_diarios["carbohidratos"] * porcentaje,
            "grasas": macros_diarios["grasas"] * porcentaje,
        }
        alimentos_comida = []
        
        if comida == "Snack":
            if not snacks_disponibles:
                continue # No hay snacks disponibles, pasa a la siguiente comida
            alimento_snack_info = random.choice(snacks_disponibles)
            snacks_disponibles.remove(alimento_snack_info)
            alimento_data = await food_data(alimento_snack_info["query"])
            if alimento_data:
                alimentos_comida.append({
                    "nombre": alimento_snack_info["nombre"], # Usa el nombre de tu lista
                    "gramos": alimento_snack_info["porcion_sugerida"],
                })
        else:
            # Lógica para comidas principales
            if proteinas_disponibles:
                alimento_proteina_info = random.choice(proteinas_disponibles)
                proteinas_disponibles.remove(alimento_proteina_info)
                alimento_proteina_data = await food_data(alimento_proteina_info["query"])
                if alimento_proteina_data and macros_comida["proteinas"] > 0 and alimento_proteina_data["proteinas"] > 0:
                    gramos_proteina = (macros_comida["proteinas"] / alimento_proteina_data["proteinas"]) * 100
                    alimentos_comida.append({
                        "nombre": alimento_proteina_info["nombre"], # Usa el nombre de tu lista
                        "gramos": round(gramos_proteina)
                    })
            
            if carbos_disponibles:
                alimento_carbohidrato_info = random.choice(carbos_disponibles)
                carbos_disponibles.remove(alimento_carbohidrato_info)
                alimento_carbohidrato_data = await food_data(alimento_carbohidrato_info["query"])
                if alimento_carbohidrato_data and macros_comida["carbohidratos"] > 0 and alimento_carbohidrato_data["carbos"] > 0:
                    gramos_carbohidrato = (macros_comida["carbohidratos"] / alimento_carbohidrato_data["carbos"]) * 100
                    alimentos_comida.append({
                        "nombre": alimento_carbohidrato_info["nombre"], # Usa el nombre de tu lista
                        "gramos": round(gramos_carbohidrato)
                    })
            
            if grasas_disponibles:
                alimento_grasa_info = random.choice(grasas_disponibles)
                grasas_disponibles.remove(alimento_grasa_info)
                alimento_grasa_data = await food_data(alimento_grasa_info["query"])
                if alimento_grasa_data and macros_comida["grasas"] > 0 and alimento_grasa_data["grasas"] > 0:
                    gramos_grasa = (macros_comida["grasas"] / alimento_grasa_data["grasas"]) * 100
                    alimentos_comida.append({
                        "nombre": alimento_grasa_info["nombre"], # Usa el nombre de tu lista
                        "gramos": round(gramos_grasa)
                    })
            
            if vegetales_disponibles:
                alimento_vegetal_info = random.choice(vegetales_disponibles)
                vegetales_disponibles.remove(alimento_vegetal_info)
                alimento_vegetal_data = await food_data(alimento_vegetal_info["query"])
                if alimento_vegetal_data:
                    alimentos_comida.append({
                        "nombre": alimento_vegetal_info["nombre"], # Usa el nombre de tu lista
                        "gramos": 100
                    })

        menu.append({
            "comida": comida,
            "alimentos": alimentos_comida
        })
        
    return menu
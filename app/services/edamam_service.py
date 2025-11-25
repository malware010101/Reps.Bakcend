import httpx
import os
from .cache import cache_alimentos

EDAMAM_API_ID = os.getenv("EDAMAM_APP_ID", "de85471b")
EDAMAM_API_KEY = os.getenv(
    "EDAMAM_API_KEY", "366d757b7e7e2b154c48eadf2a258722")


async def food_data(query: str):
    api_url = "https://api.edamam.com/api/food-database/v2/parser"

    # Si ya existe en cache → devolverlo
    if query in cache_alimentos:
        return cache_alimentos[query]

    params = {
        "ingr": query,
        "app_id": EDAMAM_API_ID,
        "app_key": EDAMAM_API_KEY,
        "lang": "es"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, params=params)
            response.raise_for_status()
            data = response.json()

            if data and "parsed" in data and data["parsed"]:
                food_info = data["parsed"][0]["food"]

                alimento = {
                    "nombre": food_info.get("label"),
                    "calorias": food_info["nutrients"].get("ENERC_KCAL", 0),
                    "proteinas": food_info["nutrients"].get("PROCNT", 0),
                    "carbos": food_info["nutrients"].get("CHOCDF", 0),
                    "grasas": food_info["nutrients"].get("FAT", 0)
                }

                # Guardar en caché
                cache_alimentos[query] = alimento
                return alimento

            return None

    except Exception as e:
        print("Error en food_data:", e)
        return None

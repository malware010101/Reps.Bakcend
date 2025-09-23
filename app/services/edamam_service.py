import httpx
import os

EDAMAM_API_ID = os.getenv("EDAMAM_APP_ID", "de85471b")
EDAMAM_API_KEY = os.getenv("EDAMAM_API_KEY", "366d757b7e7e2b154c48eadf2a258722")

async def food_data(query: str):
    # La URL de la API de Edamam para búsqueda de alimentos
    api_url = "https://api.edamam.com/api/food-database/v2/parser" 

    params = {
        "ingr": query,
        "app_id": EDAMAM_API_ID,
        "app_key": EDAMAM_API_KEY,
        "lang": "es"
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, params=params)
            response.raise_for_status()  # Lanza una excepción si la respuesta no es 2xx
            data = response.json()

            if data and 'parsed' in data and data['parsed']:
                # Devuelve el primer resultado
                food_info = data['parsed'][0]['food']
                return {
                    "nombre": food_info.get("label"),
                    "calorias": food_info.get("nutrients", {}).get("ENERC_KCAL", 0),
                    "proteinas": food_info.get("nutrients", {}).get("PROCNT", 0),
                    "carbos": food_info.get("nutrients", {}).get("CHOCDF", 0),
                    "grasas": food_info.get("nutrients", {}).get("FAT", 0)
                }
            return None

    except httpx.HTTPStatusError as exc:
        print(f"Error de HTTP al consultar Edamam: {exc.response.status_code}")
        return None
    except Exception as exc:
        print(f"Ocurrió un error al procesar la petición: {exc}")
        return None
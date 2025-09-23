# app/init_db.py
import asyncio
from tortoise import Tortoise

async def init():
    await Tortoise.init(
        db_url="sqlite://nutri_and_entrena.sqlite",
        modules={"models": ["app.models"]}
    )
    await Tortoise.generate_schemas()
    print("Base de datos inicializada correctamente")
    await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(init())
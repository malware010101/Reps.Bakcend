import asyncio
from tortoise import Tortoise


async def init():
    await Tortoise.init(
        db_url="postgres://reps_user:admin123@localhost:5432/reps_db",
        modules={"models": ["app.models"]},
    )
    await Tortoise.generate_schemas()
    print("Base de datos PostgreSQL inicializada correctamente")
    await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(init())

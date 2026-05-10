from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "planes_nutricion" ADD "fecha_fin" TIMESTAMPTZ;
        ALTER TABLE "planes_nutricion" ADD "estado" VARCHAR(20) NOT NULL DEFAULT 'activo';
        ALTER TABLE "planes_nutricion" ADD "fecha_inicio" TIMESTAMPTZ;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "planes_nutricion" DROP COLUMN "fecha_fin";
        ALTER TABLE "planes_nutricion" DROP COLUMN "estado";
        ALTER TABLE "planes_nutricion" DROP COLUMN "fecha_inicio";"""


MODELS_STATE = (
    "eJztmltz2jgUx78Kw1N2JttJaGg7+waEbNkm0EnIbqedjkfYB6PGlqgk5zIdvvtKvl9kF+"
    "8GYqZ+Sjg6f1v6STrSOfCj61ILHP7qo4PI1BMMm5iS7h+dH12CXJD/6B2OO120XifNyiDQ"
    "wvEVa+kK3CAZ7wUXDJlCti+Rw0GaLOAmw2sRvJB4jqOM1JSOmNiJySP4uweGoDaIFTDZ8O"
    "WrNGNiwSPw6OP6zlhicKxM37Gl3u3bDfG09m0TIi58R/W2hWFSx3NJ4rx+EitKYm9MhLLa"
    "QIAhAerxgnmq+6p34YijEQU9TVyCLqY0FiyR54jUcLdkYFKi+MnecH+AtnrL773Ts7dn71"
    "6/OXsnXfyexJa3m2B4ydgDoU9gOu9u/HYkUODhY0y4edxDDFOjFr+s6OccI2pVICNDw0km"
    "5EzkUIYRNyyM1N8a/HTSXVFM9mAzMbrIZNQPIEAEaCj+dTOb6jFqpDmKt0SO7ouFTXHccT"
    "AXX5vJtAKYGr3qtMv5d0cZpn8PrkfvB9dHV4NPv6kWKoNtEI2no8vZ0KdAubCZ/xT/AcMc"
    "c7pWwVoGbheIV4d4Qdjy3oa3jL6UGwxMvMAWrbXGNdKW+TbM5Q0E39Mi6iGlDiCip52Icp"
    "AXUrUrrvE599xch7PZZYbrcDLP0by9Go6vj059yNIJCyg57BggixpAikDPJQ6BXSg56tLC"
    "HFQrVL6K/tmCcAirGQt3Prka38wHVx8zlM8H87Fq6fnWp5z16E1uRccP6fwzmb/vqI+dz7"
    "PpOL/IY7/5567qE/IENQh9MJCVHnZkjkyZaVyCuUIGJuqyXncm89p2MhsxmUtce09mhO00"
    "vvA0AhcyQhbncLRCTD9/iSI3eRLRrg6p1NH4XxMHFz0aDhBbrOTH3knFHEbHf+8kf/qHLT"
    "2/abNR5YDlXSqxVYYFMu8eELOMQgvt0TLfYpPbc/MWRJDt81EjVP2PKiaM2gy5aEwEAzmv"
    "Kh+hXV1pRet4XFliCSVcnqF5UVtpecaYsutKC6HugkGdfZ4o9rfP/yfDzB4/Pdlmk0uv0l"
    "3ut+Vy18U30N/sy0GmNYeJsr8NyX45yH6BoylHa6sqVB2QGVFLMtzY+B6cGjEx9v9VS36W"
    "J7nKPhgc1JFap3Kqk+4P41mDGGLdjWBbilrx/ji+bhjHb5xqkqg5PFbxi0SHEgarcqbxp3"
    "l1AS5OmS5n0z8j93xVLksWcyOAoImNlUW4rLAtxGkKcaze93VZ0a907BQSxALJIsYLygDb"
    "5AM8+TQnslOImLp7eJjV3XJo9p5PrMkqZ+ghTu5yC0SOUI4LgiU4GtyMBufj7uZlUmufrS"
    "aTjpiXJ86e9OBtmtymyc3blntIk+X1GGsO3oqiYiR4Hog7X4a7R7hGnD9QGcBWiK/qoCwI"
    "23UZQ2W01qoM3Q8T4N5r3Km1G1eNg6Ndk2MPw0dcfLgGBwmszWZ+Vrdu3hSUXXk2u7ylDI"
    "Bhc6W7p4QtlTcVlPi0V5UDuqrcywsm1lUOyuNZSnKgMa3f3yao9fvlUU215X6rI7dGDYih"
    "+2EC3MmpKt8oINiD2/6wLCVpf1CW/14/+kHZi36/vPkXjWFFQQ=="
)

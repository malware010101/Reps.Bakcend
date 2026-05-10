from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "pesajes_historico" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "peso_kg" DOUBLE PRECISION NOT NULL,
    "grasa_pct" DOUBLE PRECISION,
    "masa_muscular_kg" DOUBLE PRECISION,
    "imc" DOUBLE PRECISION,
    "foto_frontal_url" TEXT,
    "foto_izquierda_url" TEXT,
    "foto_derecha_url" TEXT,
    "foto_trasera_url" TEXT,
    "registrado_en" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "usuario_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "pesajes_historico";"""


MODELS_STATE = (
    "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"
)

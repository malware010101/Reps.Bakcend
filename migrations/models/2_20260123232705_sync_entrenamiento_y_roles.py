from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "entrenamientos_activos" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "tipo" VARCHAR(20) NOT NULL,
    "fecha_inicio" TIMESTAMPTZ,
    "fecha_fin" TIMESTAMPTZ,
    "fecha_asignacion" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "activo" BOOL NOT NULL DEFAULT True,
    "programa_id" INT NOT NULL REFERENCES "programas_entrenamiento" ("id") ON DELETE CASCADE,
    "usuario_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
        CREATE TABLE IF NOT EXISTS "entrenamientos_historico" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "programa_id" INT NOT NULL,
    "programa_nombre" VARCHAR(100) NOT NULL,
    "dia_realizado" VARCHAR(30) NOT NULL,
    "completado_en" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "entrenamiento_activo_id" INT NOT NULL REFERENCES "entrenamientos_activos" ("id") ON DELETE CASCADE,
    "usuario_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
        ALTER TABLE "programas_entrenamiento" ADD "tipo" VARCHAR(20) NOT NULL DEFAULT 'base';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "programas_entrenamiento" DROP COLUMN "tipo";
        DROP TABLE IF EXISTS "entrenamientos_historico";
        DROP TABLE IF EXISTS "entrenamientos_activos";"""


MODELS_STATE = (
    "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"
    "gTGQzewVV3waZU9O5XSUGx+/VFN8M8/Q8RAq+/"
)

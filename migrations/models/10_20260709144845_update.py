from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "entrenamientos_activos" ALTER COLUMN "tipo" TYPE VARCHAR(50) USING "tipo"::VARCHAR(50);
        ALTER TABLE "programas_entrenamiento" ALTER COLUMN "tipo" TYPE VARCHAR(50) USING "tipo"::VARCHAR(50);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "entrenamientos_activos" ALTER COLUMN "tipo" TYPE VARCHAR(20) USING "tipo"::VARCHAR(20);
        ALTER TABLE "programas_entrenamiento" ALTER COLUMN "tipo" TYPE VARCHAR(20) USING "tipo"::VARCHAR(20);"""


MODELS_STATE = (
    "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"
    "IuYWVtYKj29h7fRQ9uP/qnYOfg=="
)

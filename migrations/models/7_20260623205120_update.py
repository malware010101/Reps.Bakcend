from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "pesajes_historico" ADD "masa_muscular_pct" DOUBLE PRECISION;
        ALTER TABLE "pesajes_historico" ADD "grasa_kg" DOUBLE PRECISION;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "pesajes_historico" DROP COLUMN "masa_muscular_pct";
        ALTER TABLE "pesajes_historico" DROP COLUMN "grasa_kg";"""


MODELS_STATE = (
    "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"
    "Q="
)

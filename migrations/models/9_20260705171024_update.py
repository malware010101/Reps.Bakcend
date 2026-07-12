from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" ALTER COLUMN "membresia_plan" DROP DEFAULT;
        ALTER TABLE "users" ALTER COLUMN "membresia_plan" DROP NOT NULL;
        ALTER TABLE "users" ALTER COLUMN "membresia_estado" DROP DEFAULT;
        ALTER TABLE "users" ALTER COLUMN "membresia_estado" DROP NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" ALTER COLUMN "membresia_plan" SET NOT NULL;
        ALTER TABLE "users" ALTER COLUMN "membresia_plan" SET DEFAULT 'standard';
        ALTER TABLE "users" ALTER COLUMN "membresia_estado" SET NOT NULL;
        ALTER TABLE "users" ALTER COLUMN "membresia_estado" SET DEFAULT 'activa';"""


MODELS_STATE = (
    "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"
    "/g8lxw5s"
)

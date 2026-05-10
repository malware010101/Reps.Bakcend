from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "chats" DROP CONSTRAINT IF EXISTS "fk_chats_users_2f0ecfe7";
        ALTER TABLE "chats" DROP COLUMN "staff_id";
        CREATE UNIQUE INDEX IF NOT EXISTS "uid_chats_usuario_550a51" ON "chats" ("usuario_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS "uid_chats_usuario_550a51";
        ALTER TABLE "chats" ADD "staff_id" INT NOT NULL;
        ALTER TABLE "chats" ADD CONSTRAINT "fk_chats_users_2f0ecfe7" FOREIGN KEY ("staff_id") REFERENCES "users" ("id") ON DELETE CASCADE;"""


MODELS_STATE = (
    "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"
)

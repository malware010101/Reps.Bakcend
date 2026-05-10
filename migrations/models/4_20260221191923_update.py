from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "chats" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "creado_en" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "activo" BOOL NOT NULL DEFAULT True,
    "staff_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    "usuario_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
        CREATE TABLE IF NOT EXISTS "mensajes" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "contenido" TEXT NOT NULL,
    "leido" BOOL NOT NULL DEFAULT False,
    "enviado_en" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "chat_id" INT NOT NULL REFERENCES "chats" ("id") ON DELETE CASCADE,
    "remitente_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "chats";
        DROP TABLE IF EXISTS "mensajes";"""


MODELS_STATE = (
    "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"
    "vdw/+5cFqg"
)

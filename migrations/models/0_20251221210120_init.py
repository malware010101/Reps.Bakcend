from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "planes_nutricion" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "usuario_id" INT NOT NULL,
    "calorias_diarias" INT NOT NULL,
    "macronutrientes" JSONB NOT NULL,
    "opciones_menu" JSONB NOT NULL,
    "datos_recibidos" JSONB NOT NULL,
    "activo" BOOL NOT NULL DEFAULT True,
    "creado_en" TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS "idx_planes_nutr_usuario_0c8788" ON "planes_nutricion" ("usuario_id");
CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "nombre" VARCHAR(100) NOT NULL,
    "email" VARCHAR(100) NOT NULL UNIQUE,
    "password_hash" VARCHAR(100) NOT NULL,
    "rol" VARCHAR(20) NOT NULL
);
CREATE TABLE IF NOT EXISTS "programas_entrenamiento" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "nombre" VARCHAR(100) NOT NULL,
    "objetivo" VARCHAR(50) NOT NULL,
    "categoria" VARCHAR(50) NOT NULL,
    "nivel" INT NOT NULL,
    "duracion_semanas" INT NOT NULL DEFAULT 4,
    "dias_entrenamiento" INT NOT NULL DEFAULT 3,
    "dias_json" TEXT NOT NULL,
    "is_general" BOOL NOT NULL DEFAULT True,
    "creador_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztmm1v2kgQgP8K4lNOylUNDW1134CQK9cEqsS5q1pV1mJPzDb2Lt1d50UV//121+/2mm"
    "KppEb1J2B2xp59mJ0Xw/d+QF3w+YsPPiLzUDDsYEr6f/W+9wkKQL4xKxz3+mi9zpaVQKCl"
    "ry3WUhW4TQraSy4YcoRcv0U+BylygTsMr0V0QxL6vhJSRypi4mWikOBvIdiCeiBWwOTC5y"
    "9SjIkLj8CTj+s7+xaD7xZ8x666t5bb4mmtZTMizrWiutvSdqgfBiRTXj+JFSWpNiZCST0g"
    "wJAAdXnBQuW+8i7ecbKjyNNMJXIxZ+PCLQp9kdvujgwcShQ/6Q3XG/TUXf4cnJy+OX376v"
    "XpW6miPUklbzbR9rK9R4aawNzqb/Q6EijS0BgzbiEPEcPUbsSvaPRjjgm1bSATQctJZuQc"
    "5FOGEbddjNRrA34m031RzM5gOzEGyGFUJxAgAgwU/7lezM0YDaYlijdE7u6zix1x3PMxF1"
    "/ayXQLMLV75XTA+TdfCeb/jq4m70ZXR5ejj3+oFSqTbZSN55OLxVhToFx4TF9FX2BcYk7X"
    "KlnLxB0ACZsQrxh2vHfhLbMv5TYDBy+xSxvFuMG0Y74Lc9mB4HtaRT2m1AdEzLQzoxLkpb"
    "TaF9e0zv1sruPF4qLAdTyzSjRvLsfTq6MTDVkqYQE1xY4BcqkNpAr0TOIQOICaUpc3LEF1"
    "Y8sXyZsdCMew2hG41uxyem2NLj8UKJ+NrKlaGWjpU0l69LoU0elFev/NrHc99bH3aTGflo"
    "M81bM+9ZVPKBTUJvTBRm5+24k4EW1Uy3x7l2v+lGCJnLsHxFy7skIHtE63uhQMgrIEEeTp"
    "70HRVH4mUwWjHkMBmhLBQIaVqtm0bxo/jIrHW8eQ2ITLOCsbddNI65q/+mmE0GDJoMpusk"
    "LMDC+zKAGUbrezEMoj8mj7QDyxkh9PXr7cQiypg1KrXAfjpUG0Vurvll/BXP3qQeZtDhPl"
    "cBeSw3qQwwpHR+7WU5NaE5AFo45kfLDxPfgNcmKq/7uOxW4ouUofbA6qpDZ5umAyfT6Mpy"
    "1iiE0dwa4UjcbPx/FVyzh+5dTQ/FvwuI1fYnQoaXBbrz/9aG0fUtNW/2Ix/ztRL0+uRbKY"
    "2xEEQ27cOqgWDbth1TCssmbPtItGv1PZqQyIFZJVjOeUAfbIe3jSNGfSKUQcUx8eT3U3HN"
    "p95jNpFuUMPaTDXSlA5A7lviAKwcnoejI6m/Y3v2a01mwNk3TCvH5wDqUG78bkbkxu37F8"
    "hjFZtsfYUHjrKaYGPwfi3sNw/wjXiPMHKhPYCvFVE5QVwy4uU6iMNorKWP0wAQ524Teoxz"
    "fQ9Bo8487FbvrUOCrthhl7HF/i/P0V+Ehg4zTzo+fW7fsK6lqezT67lBEw7KxMfUq8srVT"
    "QZlO16ocUKtyLxtMbHpyUJ/PciYHmtOGw12S2nBYn9XUWun3bHk0GkCM1Q8T4F6qqryjgO"
    "gM7vrni5xJ96eLuj9d/NLflzf/A9L6uQI="
)

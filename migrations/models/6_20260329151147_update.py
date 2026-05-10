from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "anamnesis" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "datos" JSONB NOT NULL,
    "creada_en" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "usuario_id" INT NOT NULL UNIQUE REFERENCES "users" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "anamnesis";"""


MODELS_STATE = (
    "eJztnVtz0zgUgP9KJ0/sTJaBXoDZt6QNS5e26bTpLgPDeBRbSURtKVh2S2H631eSr7JlN0"
    "5zkYleoJF0HOvT7Zwj6eRXxyMOdOnLHgYehhTRzl97vzrsA2R/lDO7ex0wn2dZPCEAY1eU"
    "BlKxMQ18YAcsYwJcClmSA6nto3mACGapOHRdnkhsVhDhaZYUYvQ9hFZApjCYQZ9lfPnKkh"
    "F24A9Ik4/zW2uCoOtIL4wc/t0i3Qoe5iLtFAfvRUH+bWPLJm7o4azw/CGYEZyWRjjgqVOI"
    "oQ8CyB8f+CF/ff52cVWTGkVvmhWJXjEn48AJCN0gV90FGdgEc37sbaIWmfJv+XP/9eHbw3"
    "cHbw7fsSLiTdKUt49R9bK6R4KCwMWo8yjyQQCiEgJjxo1lEFpG98/18ELNLhUo4LvBrGZf"
    "HGQH3T0X0eBrEWaCro5mkpDhzLrQanjWwOJ15i/tUfrd5QkX//aujj/0rl6c9z79wXMI69"
    "dRj784Phv2BQVCg6kvniIe0Be8M762D4EDLIjLjE8YmAB5UM1ZEiywdmLJl8kferLu8CoM"
    "sfsQD4sa9qPT88H1qHd+KTXASW804Dn7IvWhkPriTaFR0ofs/Xc6+rDHP+59Hl4Miu2Ulh"
    "t97vB3AmFALEzuLeDkRnCSmoCRmjWkIfARsRpNO7LQ09PPIq3YhvmHT9qT29z0wxPGwL69"
    "B75jlXLIPlFOVTG+MvAhhiPC/hHUT9nrA2xDBeJ4UbuhbGnREPVj0l+S1OwrfHCfrnmFbs"
    "Tqx2oFA1HD4971ce9k0HmUCMtAeZa37xVT2Bo+FbXiL8dfJaZ1PAOBSjUQ6bVagc1KrEEj"
    "+JJ2hK9GOVivciDWILLs4kXM4qXn4sWGIrpTzKN9QlwIsLpJM6FCe46Z1LqaMB0vq9b1+s"
    "PhmdRa/dNRQcO7Oe8Prl68Fs3ECqFohk0GjYaqwAbGxDqUgQUW+PfEh2iKP8KHNS/xG7M/"
    "Vr/IVzD1IKbgG1SYeP1Y8v3HK+gCUY9KnufRU9qF9LGsTK5OLRrgwIcMMoI4IL1oblRoSa"
    "pitUoTzAtQK5p1jV+ldapTgOaKiYwpzb4aXVK+AI+9sp6Djo2MH5YL8TSYcWivamAlXpT9"
    "V0UnSpyzL7LkVXUCmflgIYxs1YJQr30WZVeggMa9Tw9HlU76ZlLtWoUzapAJamxHSIKmGb"
    "VoRkCZKgbsWF9o3pqyvDEOjXH4GxuHc59MfeCBZtZhQWqXzENjWRvLevuWtWoIrwDeZfwo"
    "ySpsN83CVLW8o2KGaEB8BNzneSoktB+iZ9otY7w5x0UG6CnfhYRyYffFTJIyDgzNVoxujQ"
    "PDaC7P0FxSDJh4Yx82cQQpRNvpE3r9ahGnECtV6RUSeTJYBwGL2V4u+gmcRv61kmA7oR4s"
    "wvSgGulBiahNvDlbsJfc5y0KG3NeM3NeWpDj7YRmU3rNE3Z1ejeGqTFMt2+YqgbmCkBWbF"
    "m2l2vNBNbUXF2nYZbssSsssdz2e7Xpld/pN6aWbnNgt8bUYl8XQIxUCu0I/qjgJwm1RZmt"
    "U6wGn0aSTlU6fZ/qVWfDi7+T4sUj+fJC7UIl1dq9jFRmg1sZTQfpVvYyIL5Dy5kJsqSxET"
    "SzEfhB7Wa6bE5ilxTZPDQfemyksDm4Gbmi2C7hq7ED7Pg2wTN11+RSgn78FlVWcyPraQsg"
    "7UzGflIMLZ2U+0vIdfPa7ZZikW6dsj8Xhc0GS4u1flaaWLdTxdB1CajaXslkCgwnXEjr8a"
    "uidDK86Z8N9i6vBsen16fx9dtUNRKZslZ6NeidFRbiqQ8osOa2av2oJilJLclSq9OEq0Dp"
    "cSZeSO3QBX7TvqkSNmDjOdKzG7GMyxt88cFTwqyXiU9wAFwr9BVHRKr9JCrZpdwlWlFdi7"
    "dEoEI/v4cI+g5YCnRJ2qCuRu1AX5yIXgZ0QdZgrsbMvp/ZNsthLsgazErMPpwi/v1LOQdL"
    "wsY/qJl/0Gx3m+3u7Wx3b8lZ4wJ8EbJa2lHVy64aqUC31lHDikJqYam08dNoNmS7NX4ajW"
    "c/LUnmnPrA5Sf6qeUgwP9vssGkEN2lNUT2ytjMfOUTCHduNwrWpxA1YfuKGpIqbB+Z88ma"
    "TdwexGET4iVBw3sR3iKqpMVMWjRGzhIBKWVRw3wR5uam7ypPx2gTK00vd4NGpm5S7QViHJ"
    "i4I79RY5q4Iy1vRkiDhre9MonNnYzNLY0axVQqOaO25FJR3nxXuVaqrsjXuFhiEWrBkpDx"
    "tKxwTlm3p6X5ZVlzR1ZxR5aMv0G1Zl8NMi/TTpRHi5A8qgZ5VL4Zy2o75V6oJiAlIUMyHt"
    "joDir2XivnxLT8rrr8nNAXEdIsCvmS2sRzqhLdHMZDjRgilUawKEWl8OY4HujDUf9IpkxH"
    "pVAzvbvUE79RVcDE6uMnklBbFpJNHzxB1IogqKJG1bkxZUHjylS4Mv2GV8IkoV1auOuuNU"
    "VQyhh38LyH3EGWDxRXjJAuwskq94yWjhvXxqgHaw0aJ3qfwluT9Mpq50zISpiQBMYVo+FI"
    "2oArhplgSKGa1DiuE4HVQFx7N1w/wjmg9J6wCWwG6KwJypKg6ZfZgW3SqFfGxdsJcOP7KP"
    "Kt9mfqJe270V6IGVL1cza7rKrlCaVxj2V30yoZtTUMsnQIMo5uZcWxZHbyB63U/SaOBfA8"
    "IIroAy0Fk20HRxbnc8G0P2Z7M9Mwd0Aw/7PuaoLJT+8+zVH6KXldj8uo0TUwlHuQjZ5ZR2"
    "EqxzndOmMZZGWMtbxKhXDN1vId9Kny95CqVeqcSEvV6qOjRfTqo6NqxZrnFY4ks6HRAGJc"
    "vJ0A12LYRVEhFaFQqs/P50TMuXlBQXFufqvH6B7/BxX9LOc="
)

from datetime import datetime, UTC


async def actualizar_estado_si_vencio(user):

    # Admin y coach no manejan membresías
    if user.rol in ("admin", "coach"):
        return user

    if (
        user.membresia_estado == "activa"
        and user.membresia_fin
        and datetime.now(UTC) >= user.membresia_fin
    ):
        user.membresia_estado = "vencida"
        await user.save()

    return user

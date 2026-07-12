from datetime import datetime, UTC

from app.models import User


async def actualizar_membresias():

    usuarios = await User.filter(membresia_estado="activa")

    for usuario in usuarios:

        if (
            usuario.membresia_fin
            and usuario.membresia_fin <= datetime.now(UTC)
        ):

            usuario.membresia_estado = "vencida"
            await usuario.save()

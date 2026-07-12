from datetime import datetime, timedelta, UTC

from app.services.memberships.plans import PLANES


def asignar_membresia(plan: str):

    if plan not in PLANES:
        raise ValueError("Plan de membresía inválido")

    fecha_inicio = datetime.now(UTC)

    dias = PLANES[plan]["dias"]

    fecha_fin = fecha_inicio + timedelta(days=dias)

    return {
        "membresia_plan": plan,
        "membresia_inicio": fecha_inicio,
        "membresia_fin": fecha_fin,
        "membresia_estado": "activa",
    }


def dias_restantes(fecha_fin):
    if not fecha_fin:
        return 0

    return max(
        (fecha_fin - datetime.now(UTC)).days,
        0
    )


def obtener_datos_membresia(rol: str, plan: str):

    if rol in ("admin", "coach"):
        return {
            "membresia_plan": None,
            "membresia_inicio": None,
            "membresia_fin": None,
            "membresia_estado": None,
        }

    return asignar_membresia(plan)


def duracion_plan(plan: str | None) -> int:

    if not plan:
        return 0

    return PLANES.get(plan, {}).get("dias", 0)

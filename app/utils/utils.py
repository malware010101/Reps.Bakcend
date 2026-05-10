def normalizar_objetivo(objetivo: str) -> str:
    objetivo = objetivo.strip().lower()

    if objetivo in ("hipertrofia",):
        return "Hipertrofia"

    if objetivo in ("mantenimiento",):
        return "Mantenimiento"

    if objetivo in ("perdida de grasa", "perdida_grasa"):
        return "Perdida de Grasa"

    raise ValueError(f"Objetivo no soportado: {objetivo}")

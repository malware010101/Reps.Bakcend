from typing import Dict, Optional, Literal
from app.services.pesajes_reglas import (
    validar_peso,
    validar_grasa_pct,
    validar_masa_muscular,
    validar_composicion
)


def normalizar_pesaje(
    peso_kg: float,

    grasa_valor: Optional[float],
    grasa_tipo: Optional[Literal["%", "kg"]],

    musculo_valor: Optional[float],
    musculo_tipo: Optional[Literal["%", "kg"]],
):
    """
    Convierte grasa y músculo a formato completo:
    - % y kg siempre disponibles
    """

    resultado = {}

    validar_peso(peso_kg)

    # =========================
    # GRASA CORPORAL
    # =========================
    grasa_pct = None
    grasa_kg = None

    if grasa_valor is not None and grasa_tipo is not None:
        if grasa_tipo == "%":
            grasa_pct = grasa_valor
            grasa_kg = round((peso_kg * grasa_pct) / 100, 2)

        elif grasa_tipo == "kg":
            grasa_kg = grasa_valor
            grasa_pct = round((grasa_kg / peso_kg) * 100, 2)

    # VALIDACIÓN GRASA
    if grasa_pct is not None:
        validar_grasa_pct(grasa_pct)

    # =========================
    # MASA MUSCULAR
    # =========================
    musculo_pct = None
    musculo_kg = None

    if musculo_valor is not None and musculo_tipo is not None:
        if musculo_tipo == "%":
            musculo_pct = musculo_valor
            musculo_kg = round((peso_kg * musculo_pct) / 100, 2)

        elif musculo_tipo == "kg":
            musculo_kg = musculo_valor
            musculo_pct = round((musculo_kg / peso_kg) * 100, 2)

    # VALIDACIÓN MUSCULO
    if musculo_kg is not None:
        validar_masa_muscular(peso_kg, musculo_kg)

    # VALIDACIÓN COMPOSICIÓN
    if grasa_kg is not None and musculo_kg is not None:
        validar_composicion(grasa_kg, musculo_kg, peso_kg)

    # =========================
    # OUTPUT NORMALIZADO
    # =========================
    resultado = {
        "grasa_pct": grasa_pct,
        "grasa_kg": grasa_kg,
        "masa_muscular_pct": musculo_pct,
        "masa_muscular_kg": musculo_kg,
    }

    return resultado

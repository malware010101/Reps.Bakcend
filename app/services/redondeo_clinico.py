# app/services/redondeo_clinico.py

from typing import Optional, Dict
import math

FRACCIONES_HUMANAS = {
    0.25: "1/4",
    0.5: "1/2",
    0.75: "3/4",
    1: "1"
}


def redondear_gramaje_clinico(
    ingrediente: str,
    gramos_teoricos: float,
    diccionario_clinico: Dict
) -> Optional[dict]:
    """
    Convierte gramos teóricos en una presentación clínica humana.
    NO recalcula macros.
    SOLO transforma visualmente.
    """

    if gramos_teoricos <= 0:
        return None

    info = diccionario_clinico.get(ingrediente)
    if not info:
        return None

    tipo = info.get("tipo")
    unidad = info.get("unidad_visible", "g")

    # ─────────────────────────────
    # VEGETALES LIBRES
    # ─────────────────────────────
    if tipo == "libre":
        return {
            "ingrediente": ingrediente,
            "cantidad": "libre",
            "unidad": "al gusto",
            "gramos_aprox": None
        }

    # ─────────────────────────────
    # DISCRETOS (PIEZAS)
    # ─────────────────────────────
    if tipo == "discreto":
        peso_pieza = info.get("peso_por_pieza_g")
        regla = info.get("regla_redondeo")

        if not peso_pieza:
            return None

        piezas_teoricas = gramos_teoricos / peso_pieza

        #  SOLO ENTEROS (huevo, pan, tortillas)
        if regla == "entero_mas_cercano":
            piezas_final = max(1, round(piezas_teoricas))
            cantidad_mostrar = piezas_final

        #  FRACCIONES
        elif regla == "fraccion_mas_cercana":
            fracciones = info.get("fracciones_permitidas", [1])

            piezas_final = min(
                fracciones,
                key=lambda x: abs(x - piezas_teoricas)
            )

            cantidad_mostrar = FRACCIONES_HUMANAS.get(
                piezas_final,
                str(piezas_final)
            )

        else:
            piezas_final = round(piezas_teoricas)
            cantidad_mostrar = piezas_final

        return {
            "ingrediente": ingrediente,
            "cantidad": cantidad_mostrar,
            "unidad": unidad,
            "gramos_aprox": round(piezas_final * peso_pieza)
        }

    # ─────────────────────────────
    # CONTINUOS (GRAMOS / TAZAS / CUCHARADAS)
    # ─────────────────────────────
    if tipo == "continuo":

        # CASO SCOOP (proteína en polvo)
        if unidad == "scoop":
            peso_scoop = info.get("peso_por_scoop_g")

            if not peso_scoop:
                return None

            scoops_teoricos = gramos_teoricos / peso_scoop
            scoops_final = max(1, round(scoops_teoricos))

            return {
                "ingrediente": ingrediente,
                "cantidad": scoops_final,
                "unidad": "scoop",
                "gramos_aprox": scoops_final * peso_scoop
            }

        # CASO TAZA
        if unidad == "taza":
            peso_taza = info.get("peso_por_taza_g")
            if not peso_taza:
                return None

            tazas_teoricas = gramos_teoricos / peso_taza
            regla = info.get("regla_redondeo", "normal")

            # 🟢 TAZAS ENTERAS (ej. maíz palomero)
            if regla == "entero_mas_cercano":
                tazas_final = max(1, round(tazas_teoricas))

            # 🟡 TAZAS CON FRACCIONES (ej. avena en taza)
            else:
                fracciones = info.get("fracciones_permitidas", [0.25, 0.5, 1])
                tazas_final = min(
                    fracciones,
                    key=lambda f: abs(f - tazas_teoricas)
                )

            return {
                "ingrediente": ingrediente,
                "cantidad": tazas_final,
                "unidad": "taza",
                "gramos_aprox": round(tazas_final * peso_taza)
            }

        # CASO CUCHARADA
        if unidad == "cucharada":
            peso_cda = info.get("peso_por_cucharada_g")
            if not peso_cda:
                return None

            cucharadas_teoricas = gramos_teoricos / peso_cda
            cucharadas_red = max(1, math.ceil(cucharadas_teoricas))

            return {
                "ingrediente": ingrediente,
                "cantidad": cucharadas_red,
                "unidad": "cucharada",
                "gramos_aprox": round(cucharadas_red * peso_cda)
            }

        # CASO GRAMOS
        gramos_red = round(gramos_teoricos / 5) * 5

        return {
            "ingrediente": ingrediente,
            "cantidad": gramos_red,
            "unidad": "g",
            "gramos_aprox": gramos_red
        }

    return None

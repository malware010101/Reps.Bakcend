def validar_peso(peso_kg: float):
    if peso_kg is None or peso_kg <= 0:
        raise ValueError("El peso debe ser mayor a 0 kg")

    if peso_kg > 400:
        raise ValueError("Peso fuera de rango lógico")


def validar_grasa_pct(grasa_pct: float):
    if grasa_pct is None:
        return

    if grasa_pct < 0 or grasa_pct > 100:
        raise ValueError("La grasa corporal debe estar entre 0 y 100%")


def validar_masa_muscular(peso_kg: float, masa_kg: float):
    if masa_kg is None:
        return

    if masa_kg < 0:
        raise ValueError("La masa muscular no puede ser negativa")

    if masa_kg > peso_kg:
        raise ValueError("La masa muscular no puede ser mayor al peso total")


def validar_composicion(grasa_kg: float, masa_kg: float, peso_kg: float):
    if grasa_kg and masa_kg is not None:
        if grasa_kg + masa_kg > peso_kg:
            raise ValueError("Grasa + músculo no puede exceder el peso total")


def validar_imc(imc: float):
    if imc is None:
        return

    if imc < 10 or imc > 60:
        raise ValueError("IMC fuera de rango lógico")

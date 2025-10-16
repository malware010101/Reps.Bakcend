from pydantic import BaseModel
from typing import List, Optional


class DatosNutricion(BaseModel):
    usuarioIdAsignado: int
    peso: float
    altura: float
    edad: int
    genero: str
    nivelActividad: str
    objetivo: str
    enfermedades: List[str]
    tipoDieta: str
    alergias: Optional[List[str]] = None

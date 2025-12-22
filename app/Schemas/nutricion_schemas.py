from pydantic import BaseModel
from typing import List, Optional, Dict, Any


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
    comidas: int


class PlanNutricionCreate(BaseModel):
    usuario_id: int
    calorias_diarias: float
    macronutrientes: Dict[str, Any]
    opciones_menu: List[Dict[str, Any]]
    datos_recibidos: Dict[str, Any]

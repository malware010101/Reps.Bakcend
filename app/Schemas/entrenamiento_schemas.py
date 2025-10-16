from pydantic import BaseModel, Field
from typing import List, Dict, Optional

# --- Esquemas de Sub-componentes (Estructura anidada) ---


class ExerciseSchema(BaseModel):
    id: str
    nombre: str
    descripcion: str
    series: int
    repeticiones: str
    descanso: int
    videoUrl: Optional[str] = None


class MethodSchema(BaseModel):
    id: str
    nombre: str
    descripcion: str


class DiaEntrenamientoSchema(BaseModel):
    dia: str
    ejercicios: List[ExerciseSchema]
    metodos: List[MethodSchema]


class ProgramaInSchema(BaseModel):
    nombre: str
    objetivo: str
    categoria: str
    nivel: int
    duracion_semanas: int
    dias_entrenamiento: int
    dias: List[DiaEntrenamientoSchema]
    # Recibimos el ID que el frontend toma del usuario autenticado
    creador_id: int = Field(..., description="ID del usuario creador.")
    is_general: bool = True

# --- Esquema de Salida (ProgramaOutSchema) ---


class ProgramaOutSchema(BaseModel):
    id: int
    nombre: str
    objetivo: str
    categoria: str
    nivel: str
    duracion_semanas: int
    dias_entrenamiento: int
    # Este campo recibirá la versión deserializada del JSON
    dias: List[Dict] = Field(...,
                             description="Lista deserializada de días, ejercicios y métodos.")
    creador_id: int

    class Config:
        orm_mode = True  # Permite mapear los campos del modelo de Tortoise a Pydantic

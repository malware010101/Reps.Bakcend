from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from pydantic import ConfigDict
from datetime import datetime, timezone, timedelta

# --- Esquemas de Sub-componentes (Estructura anidada) ---


class DiaItemSchema(BaseModel):
    id: int
    type: str  # "exercise" | "method"
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    series: Optional[int] = None
    repeticiones: Optional[str] = None
    descanso: Optional[int] = None
    videoUrl: Optional[str] = None


class DiaEntrenamientoSchema(BaseModel):
    dia: str
    items: List[DiaItemSchema]


class ProgramaInSchema(BaseModel):
    nombre: str
    objetivo: str
    categoria: str
    nivel: int
    duracion_semanas: int
    dias_entrenamiento: int
    dias: List[DiaEntrenamientoSchema]
    tipo: str = "base"
    # Recibimos el ID que el frontend toma del usuario autenticado
    creador_id: int = Field(..., description="ID del usuario creador.")
    is_general: Optional[bool] = True

# --- Esquema de Salida (ProgramaOutSchema) ---


class ProgramaOutSchema(BaseModel):
    id: int
    nombre: str
    objetivo: str
    categoria: str
    nivel: int
    duracion_semanas: int
    dias_entrenamiento: int
    tipo: str
    # Este campo recibirá la versión deserializada del JSON
    dias: List[DiaEntrenamientoSchema]
    creador_id: int

    # Permite mapear los campos del modelo de Tortoise a Pydantic
    model_config = ConfigDict(from_attributes=True)


class AsignarProgramaSchema(BaseModel):
    programa_id: int
    usuario_id: Optional[int] = None


class ProgramaActivoOutSchema(BaseModel):
    entrenamiento_id: int
    tipo: str | None = None
    fecha_inicio: datetime | None = None
    fecha_fin: datetime | None = None
    programa: ProgramaOutSchema


class EntrenamientoHistoricoInSchema(BaseModel):
    entrenamiento_id: int
    dia_realizado: str


class EntrenamientoHistoricoOutSchema(BaseModel):
    id: int
    programa_nombre: str
    dia_realizado: str
    completado_en: str

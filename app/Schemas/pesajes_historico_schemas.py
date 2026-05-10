from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PesajeHistoricoInSchema(BaseModel):
    peso_kg: float
    grasa_pct: Optional[float] = None
    masa_muscular_kg: Optional[float] = None
    imc: Optional[float] = None

    foto_frontal_url: Optional[str] = None
    foto_izquierda_url: Optional[str] = None
    foto_derecha_url: Optional[str] = None
    foto_trasera_url: Optional[str] = None


class PesajeHistoricoOutSchema(BaseModel):
    id: int
    peso_kg: float
    grasa_pct: Optional[float]
    masa_muscular_kg: Optional[float]
    imc: Optional[float]

    foto_frontal_url: Optional[str]
    foto_izquierda_url: Optional[str]
    foto_derecha_url: Optional[str]
    foto_trasera_url: Optional[str]

    registrado_en: datetime

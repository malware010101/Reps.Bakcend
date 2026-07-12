from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal
from datetime import datetime


class PesajeHistoricoInSchema(BaseModel):
    peso_kg: float

    grasa_valor: Optional[float] = None
    grasa_tipo: Optional[Literal["%", "kg"]] = None

    musculo_valor: Optional[float] = None
    musculo_tipo: Optional[Literal["%", "kg"]] = None

    imc: Optional[float] = None

    foto_frontal_url: Optional[str] = None
    foto_izquierda_url: Optional[str] = None
    foto_derecha_url: Optional[str] = None
    foto_trasera_url: Optional[str] = None


class PesajeHistoricoOutSchema(BaseModel):
    id: int
    peso_kg: float

    grasa_pct: Optional[float]
    grasa_kg: Optional[float]

    masa_muscular_pct: Optional[float]
    masa_muscular_kg: Optional[float]

    imc: Optional[float]

    foto_frontal_url: Optional[str]
    foto_izquierda_url: Optional[str]
    foto_derecha_url: Optional[str]
    foto_trasera_url: Optional[str]

    registrado_en: datetime
    model_config = ConfigDict(from_attributes=True)

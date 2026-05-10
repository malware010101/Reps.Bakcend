from pydantic import BaseModel, Field, model_validator
from typing import Optional, Literal


class AnamnesisSchema(BaseModel):
    edad: int = Field(..., ge=12, le=90)
    genero: Literal["masculino", "femenino"]
    objetivo: Literal["aumentar masa muscular", "perdida grasa", "salud"]
    experiencia: Literal["principiante", "intermedio", "avanzado"]
    frecuencia: int = Field(..., ge=3, le=6)

    tieneEnfermedad: Literal["si", "no"]
    enfermedad: Optional[str] = None

    tieneLesion: Literal["si", "no"]
    lesion: Optional[str] = None

    comentarios: str

    @model_validator(mode="after")
    def validar_condicionales(self):
        if self.tieneEnfermedad == "si" and not self.enfermedad:
            raise ValueError("Debes especificar la enfermedad")

        if self.tieneLesion == "si" and not self.lesion:
            raise ValueError("Debes especificar la lesión")

        return self

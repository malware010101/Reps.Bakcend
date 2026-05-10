from pydantic import BaseModel
from typing import List
from datetime import datetime
from pydantic import ConfigDict


# ============================
# MENSAJES
# ============================

class MensajeCreateSchema(BaseModel):
    contenido: str


class MensajeOutSchema(BaseModel):
    id: int
    chat_id: int
    remitente_id: int
    contenido: str
    leido: bool
    enviado_en: datetime

    model_config = ConfigDict(from_attributes=True)


# ============================
# CHAT
# ============================

class ChatOutSchema(BaseModel):
    id: int
    usuario_id: int
    creado_en: datetime
    activo: bool

    model_config = ConfigDict(from_attributes=True)


class ChatConMensajesSchema(BaseModel):
    id: int
    usuario_id: int
    creado_en: datetime
    activo: bool
    mensajes: List[MensajeOutSchema]

    model_config = ConfigDict(from_attributes=True)

# ============================
# CHAT LISTA PRO (SIDEBAR)
# ============================


class ChatListItemSchema(BaseModel):
    chat_id: int
    usuario_id: int
    usuario_nombre: str
    ultimo_mensaje: str | None
    ultimo_mensaje_fecha: datetime | None
    no_leidos: int

    model_config = ConfigDict(from_attributes=True)


class TotalNoLeidosSchema(BaseModel):
    total_no_leidos: int

    model_config = ConfigDict(from_attributes=True)

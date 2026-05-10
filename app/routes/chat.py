from fastapi import APIRouter, Depends, HTTPException, status
from tortoise.exceptions import DoesNotExist

from datetime import datetime

from app.auth import get_current_user, SECRET_KEY, ALGORITHM
from app.models import User, Chat, Mensaje
from app.Schemas.chat_schemas import MensajeCreateSchema, MensajeOutSchema, ChatOutSchema, ChatConMensajesSchema, ChatListItemSchema, TotalNoLeidosSchema

from fastapi import WebSocket, WebSocketDisconnect
from app.websocket.websocket_manager import manager
from jose import jwt, JWTError

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)

# ============================
# ENVIAR MENSAJE
# ============================


# ENVIAR MENSAJE
@router.post("/mensaje", response_model=MensajeOutSchema)
async def enviar_mensaje(
    data: MensajeCreateSchema,
    chat_id: int | None = None,
    current_user: User = Depends(get_current_user)
):
    if current_user.rol in ["usuario", "pro"]:
        chat = await Chat.filter(usuario_id=current_user.id).first()
        if not chat:
            chat = await Chat.create(usuario=current_user)
    elif current_user.rol in ["admin", "coach"]:
        if not chat_id:
            raise HTTPException(
                status_code=400, detail="Admin debe especificar chat_id")
        chat = await Chat.get_or_none(id=chat_id)
        if not chat:
            raise HTTPException(status_code=404, detail="Chat no encontrado")
    else:
        raise HTTPException(status_code=403)

    mensaje = await Mensaje.create(chat=chat, remitente=current_user, contenido=data.contenido)

    # ⚡ Broadcast a todos los WS conectados en ese chat y admins
    await manager.broadcast_chat(chat.id, {
        "type": "nuevo_mensaje",
        "mensaje": {
            "id": mensaje.id,
            "chat_id": mensaje.chat_id,
            "remitente_id": mensaje.remitente_id,
            "contenido": mensaje.contenido,
            "leido": mensaje.leido,
            "enviado_en": mensaje.enviado_en.isoformat()
        }
    })

    # ⚡ Broadcast global de totales por chat para badges
    await manager.broadcast_total_no_leidos()

    return mensaje

# ============================
# LISTAR CHATS PRO (ADMIN / COACH)
# ============================


@router.get("/lista", response_model=list[ChatListItemSchema])
async def listar_chats_pro(
    current_user: User = Depends(get_current_user)
):
    if current_user.rol not in ["admin", "coach"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver los chats"
        )

    chats = await Chat.all().prefetch_related("usuario")

    resultado = []

    for chat in chats:
        # Último mensaje
        ultimo_mensaje = await Mensaje.filter(
            chat_id=chat.id
        ).order_by("-enviado_en").first()

        # Conteo de no leídos (solo los que NO envió el staff)
        no_leidos = await Mensaje.filter(
            chat_id=chat.id,
            leido=False
        ).exclude(remitente_id=current_user.id).count()

        resultado.append(
            ChatListItemSchema(
                chat_id=chat.id,
                usuario_id=chat.usuario_id,
                usuario_nombre=chat.usuario.nombre,
                ultimo_mensaje=ultimo_mensaje.contenido if ultimo_mensaje else None,
                ultimo_mensaje_fecha=ultimo_mensaje.enviado_en if ultimo_mensaje else None,
                no_leidos=no_leidos
            )
        )

    # Ordenar estilo WhatsApp:
    # Chats con no leídos arriba
    # Luego por fecha del último mensaje DESC
    resultado.sort(
        key=lambda x: (
            x.no_leidos > 0,
            x.ultimo_mensaje_fecha or datetime.min
        ),
        reverse=True
    )

    return resultado

# ============================
# OBTENER MI CHAT (USUARIO)
# ============================


@router.get("/mi-chat", response_model=ChatOutSchema)
async def obtener_mi_chat(
    current_user: User = Depends(get_current_user)
):
    if current_user.rol not in ["usuario", "pro"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo usuarios pueden usar este endpoint"
        )

    chat = await Chat.filter(usuario_id=current_user.id).first()

    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No tienes chat asignado"
        )

    return ChatOutSchema(
        id=chat.id,
        usuario_id=chat.usuario_id,
        creado_en=chat.creado_en,
        activo=chat.activo
    )

# ============================
# TOTAL NO LEÍDOS (GLOBAL)
# ============================


@router.get("/no-leidos-total", response_model=TotalNoLeidosSchema)
async def total_no_leidos(
    current_user: User = Depends(get_current_user)
):
    # 👤 Usuario / Pro
    if current_user.rol in ["usuario", "pro"]:
        chat = await Chat.filter(usuario_id=current_user.id).first()

        if not chat:
            return {"total_no_leidos": 0}

        total = await Mensaje.filter(
            chat_id=chat.id,
            leido=False
        ).exclude(remitente_id=current_user.id).count()

        return {"total_no_leidos": total}

    # Admin / Coach
    elif current_user.rol in ["admin", "coach"]:
        total = await Mensaje.filter(
            leido=False
        ).exclude(remitente_id=current_user.id).count()

        return {"total_no_leidos": total}

    else:
        raise HTTPException(status_code=403)

# ============================
# OBTENER CHAT CON MENSAJES
# ============================


@router.get("/{chat_id}", response_model=ChatConMensajesSchema)
async def obtener_chat(
    chat_id: int,
    current_user: User = Depends(get_current_user)
):
    try:
        chat = await Chat.get(id=chat_id).prefetch_related("mensajes")
        mensajes = await Mensaje.filter(
            chat_id=chat_id
        ).order_by("enviado_en")

    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat no encontrado"
        )

    # 🔐 Permisos
    if current_user.id != chat.usuario_id and current_user.rol not in ["admin", "coach"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver este chat"
        )

    mensajes_out = [
        MensajeOutSchema(
            id=m.id,
            chat_id=m.chat_id,
            remitente_id=m.remitente_id,
            contenido=m.contenido,
            leido=m.leido,
            enviado_en=m.enviado_en
        )
        for m in mensajes
    ]

    return ChatConMensajesSchema(
        id=chat.id,
        usuario_id=chat.usuario_id,
        creado_en=chat.creado_en,
        activo=chat.activo,
        mensajes=mensajes_out
    )


# ============================
# MARCAR MENSAJES COMO LEÍDOS
# ============================

@router.post("/{chat_id}/marcar-leido")
async def marcar_como_leido(chat_id: int, current_user: User = Depends(get_current_user)):
    await Mensaje.filter(chat_id=chat_id, leido=False).exclude(remitente_id=current_user.id).update(leido=True)
    await manager.broadcast_total_no_leidos()
    return {"mensaje": "Mensajes marcados como leídos"}


@router.websocket("/ws/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, chat_id: int, token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except JWTError:
        await websocket.close(code=1008)
        return

    user = await User.get(id=user_id)
    is_admin = user.rol in ["admin", "coach"]

    await manager.connect(chat_id, websocket, user_id=user.id, is_admin=is_admin)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(chat_id, websocket, is_admin=is_admin)

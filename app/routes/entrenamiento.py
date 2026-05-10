from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from ..Schemas.entrenamiento_schemas import ProgramaInSchema, ProgramaOutSchema
from app.models import ProgramaEntrenamiento, User, EntrenamientoActivo
from tortoise.exceptions import DoesNotExist
from app.auth import get_current_user
from app.Schemas.entrenamiento_schemas import AsignarProgramaSchema, ProgramaActivoOutSchema
from datetime import datetime, timedelta, timezone


router = APIRouter(
    prefix="/programas",
    tags=["programas"]
)


@router.post("/", response_model=ProgramaOutSchema, status_code=status.HTTP_201_CREATED)
async def crear_programa(
    programa_data: ProgramaInSchema,

    current_user: User = Depends(get_current_user)
):
    if current_user.rol not in ["admin", "coach"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Solo administradores y coaches pueden crear programas.")

    try:
        # ver datos recibidos y borrar antes del deploy
        print("DIAS RECIBIDOS (Pydantic):", programa_data.dias)
        print(
            "DIAS COMO DICT (JSON listo):",
            [d.dict() for d in programa_data.dias]
        )
        # El modelo se encarga de serializar 'dias' a 'dias_json'
        programa_obj = await ProgramaEntrenamiento.create(
            nombre=programa_data.nombre,
            objetivo=programa_data.objetivo,
            categoria=programa_data.categoria,
            nivel=programa_data.nivel,
            duracion_semanas=programa_data.duracion_semanas,
            tipo=programa_data.tipo,
            dias_entrenamiento=programa_data.dias_entrenamiento,
            dias=[dia.dict() for dia in programa_data.dias],
            # Se serializa en el método create del modelo
            creador_id=current_user.id,  # Usamos el ID del usuario autenticado y validado
            is_general=programa_data.is_general
        )

        # Prepara la respuesta: deserializa los días para el frontend
        programa_out = ProgramaOutSchema(
            id=programa_obj.id,
            nombre=programa_obj.nombre,
            objetivo=programa_obj.objetivo,
            categoria=programa_obj.categoria,
            nivel=programa_obj.nivel,
            duracion_semanas=programa_obj.duracion_semanas,
            tipo=programa_obj.tipo,
            dias_entrenamiento=programa_obj.dias_entrenamiento,
            dias=programa_obj.get_dias(),
            creador_id=programa_obj.creador_id
        )

        return programa_out

    except Exception as e:
        print(f"Error al crear programa: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error interno al guardar el programa.")


@router.get("/general", response_model=List[ProgramaOutSchema])
async def obtener_programas_generales():

    programas = await ProgramaEntrenamiento.filter(is_general=True).all()

    programas_out = []
    for p in programas:
        programa_out = ProgramaOutSchema(
            id=p.id,
            nombre=p.nombre,
            objetivo=p.objetivo,
            categoria=p.categoria,
            nivel=p.nivel,
            duracion_semanas=p.duracion_semanas,
            tipo=p.tipo,
            dias_entrenamiento=p.dias_entrenamiento,
            dias=p.get_dias(),  # 👈 CLAVE
            creador_id=p.creador_id
        )
        programas_out.append(programa_out)

    return programas_out

# Endpoint 3: ELIMINAR un programa (DELETE)


@router.delete("/{programa_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_programa(
    programa_id: int,
    current_user: User = Depends(get_current_user)
):
    # Validación de rol: solo 'admin' o 'coach' pueden eliminar
    if current_user.rol not in ["admin", "coach"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Solo admins y coaches pueden eliminar programas.")

    try:
        programa = await ProgramaEntrenamiento.get(id=programa_id)

        # Opcional pero recomendado: solo el creador o un admin puede eliminar
        if programa.creador_id != current_user.id and current_user.rol != "admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="No tienes permiso para eliminar este programa.")

        await programa.delete()
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Programa no encontrado")


@router.post("/asignar", status_code=status.HTTP_201_CREATED)
async def asignar_programa(
    data: AsignarProgramaSchema,
    current_user: User = Depends(get_current_user)
):
    # Determinar usuario destino
    if current_user.rol in ["admin", "coach"]:
        if not data.usuario_id:
            raise HTTPException(
                status_code=400,
                detail="usuario_id es requerido para admin o coach"
            )
        usuario_id = data.usuario_id
    else:
        # Usuario normal se asigna a sí mismo
        usuario_id = current_user.id

    # Validar usuario
    # Validar usuario
    try:
        usuario = await User.get(id=usuario_id)
    except DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    # Validar programa
    try:
        programa = await ProgramaEntrenamiento.get(id=data.programa_id)
    except DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Programa no encontrado"
        )

# Evitar duplicados activos
    existe = await EntrenamientoActivo.filter(
        usuario=usuario,
        programa=programa,
        activo=True
    ).exists()

    if existe:
        raise HTTPException(
            status_code=400,
            detail="El usuario ya tiene este programa activo"
        )

    def familia(tipo: str) -> str:
        if tipo in ["base", "personalizado_base"]:
            return "base"
        if tipo in ["complemento", "personalizado_complemento"]:
            return "complemento"
        return "otro"

    entrenamientos_activos = await EntrenamientoActivo.filter(
        usuario=usuario,
        activo=True
    ).prefetch_related("programa")

    nueva_familia = familia(programa.tipo)
    ahora = datetime.now(timezone.utc)

    for e in entrenamientos_activos:
        if familia(e.programa.tipo) == nueva_familia:
            e.activo = False
            e.fecha_fin = ahora
            await e.save()

    if programa.duracion_semanas <= 0:
        raise HTTPException(
            status_code=400,
            detail="El programa no tiene una duración válida"
        )

    duracion_dias = programa.duracion_semanas * 7
    fecha_fin = ahora + timedelta(days=duracion_dias)

    # Crear entrenamiento activo (FORMA CORRECTA)
    entrenamiento = await EntrenamientoActivo.create(
        usuario=usuario,
        programa=programa,
        tipo=programa.tipo,
        activo=True,
        fecha_inicio=ahora,
        fecha_fin=fecha_fin

    )

    return {
        "message": "Programa asignado correctamente",
        "entrenamiento_id": entrenamiento.id,
        "fecha_inicio": ahora.isoformat(),
        "fecha_fin": fecha_fin.isoformat(),
        "duracion_dias": duracion_dias
    }

# get para ver mis programas asigandos a mi seccion Mientrenamiento


@router.get("/mis-programas", response_model=List[ProgramaActivoOutSchema])
async def obtener_mis_programas(
    current_user: User = Depends(get_current_user)
):
    entrenamientos = await EntrenamientoActivo.filter(
        usuario=current_user,
        activo=True
    ).prefetch_related("programa")

    if not entrenamientos:
        return []

    programas = []

    for e in entrenamientos:
        p = e.programa

        programas.append(
            ProgramaActivoOutSchema(
                entrenamiento_id=e.id,
                tipo=e.tipo,
                fecha_inicio=e.fecha_inicio,
                fecha_fin=e.fecha_fin,
                programa=ProgramaOutSchema(
                    id=p.id,
                    nombre=p.nombre,
                    objetivo=p.objetivo,
                    categoria=p.categoria,
                    nivel=p.nivel,
                    duracion_semanas=p.duracion_semanas,
                    tipo=p.tipo,
                    dias_entrenamiento=p.dias_entrenamiento,
                    dias=p.get_dias(),
                    creador_id=p.creador_id,

                )
            )
        )

    return programas

# enpoint para ver los programas activos de un usuario


@router.get("/usuario/{usuario_id}", response_model=List[ProgramaActivoOutSchema])
async def obtener_programas_por_usuario(
    usuario_id: int,
    current_user: User = Depends(get_current_user)
):
    # 🔐 Validación de rol
    if current_user.rol not in ["admin", "coach"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver programas de otros usuarios"
        )

    # Validar usuario
    try:
        usuario = await User.get(id=usuario_id)
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    entrenamientos = await EntrenamientoActivo.filter(
        usuario=usuario,
        activo=True
    ).prefetch_related("programa")

    programas = []

    for e in entrenamientos:
        p = e.programa

        programas.append(
            ProgramaActivoOutSchema(
                entrenamiento_id=e.id,
                tipo=e.tipo,
                fecha_inicio=e.fecha_inicio,
                fecha_fin=e.fecha_fin,
                programa=ProgramaOutSchema(
                    id=p.id,
                    nombre=p.nombre,
                    objetivo=p.objetivo,
                    categoria=p.categoria,
                    nivel=p.nivel,
                    duracion_semanas=p.duracion_semanas,
                    tipo=p.tipo,
                    dias_entrenamiento=p.dias_entrenamiento,
                    dias=p.get_dias(),
                    creador_id=p.creador_id
                )
            )
        )

    return programas

# get para traerme la ruitna del entranmieto-usuario asiganda


@router.get("/activo/{entrenamiento_id}", response_model=ProgramaActivoOutSchema)
async def obtener_entrenamiento_activo(
    entrenamiento_id: int,
    current_user: User = Depends(get_current_user)
):
    try:
        entrenamiento = await EntrenamientoActivo.get(
            id=entrenamiento_id,
            usuario=current_user,
            activo=True
        ).prefetch_related("programa")

    except DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Entrenamiento activo no encontrado"
        )

    p = entrenamiento.programa

    return ProgramaActivoOutSchema(
        entrenamiento_id=entrenamiento.id,
        tipo=entrenamiento.tipo,
        fecha_inicio=entrenamiento.fecha_inicio,
        fecha_fin=entrenamiento.fecha_fin,
        programa=ProgramaOutSchema(
            id=p.id,
            nombre=p.nombre,
            objetivo=p.objetivo,
            categoria=p.categoria,
            nivel=p.nivel,
            duracion_semanas=p.duracion_semanas,
            tipo=p.tipo,
            dias_entrenamiento=p.dias_entrenamiento,
            dias=p.get_dias(),
            creador_id=p.creador_id
        )
    )

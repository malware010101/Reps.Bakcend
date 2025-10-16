from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from ..Schemas.entrenamiento_schemas import ProgramaInSchema, ProgramaOutSchema
from ..models import ProgramaEntrenamiento, User
from tortoise.exceptions import DoesNotExist
from app.auth import get_current_user

router = APIRouter(
    prefix="/programas",
    tags=["programas"]
)


@router.post("/", response_model=ProgramaOutSchema, status_code=status.HTTP_201_CREATED)
async def crear_programa(
    programa_data: ProgramaInSchema,

    current_user: User = Depends(get_current_user)
):
    # Validación de rol: solo 'admin' o 'coach' pueden crear
    if current_user.rol not in ["admin", "coach"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Solo administradores y coaches pueden crear programas.")

    try:
        # El modelo se encarga de serializar 'dias' a 'dias_json'
        programa_obj = await ProgramaEntrenamiento.create(
            nombre=programa_data.nombre,
            objetivo=programa_data.objetivo,
            categoria=programa_data.categoria,
            nivel=programa_data.nivel,
            duracion_semanas=programa_data.duracion_semanas,
            dias_entrenamiento=programa_data.dias_entrenamiento,
            dias=programa_data.dias,  # Se serializa en el método create del modelo
            creador_id=current_user.id,  # Usamos el ID del usuario autenticado y validado
            is_general=programa_data.is_general
        )

        # Prepara la respuesta: deserializa los días para el frontend
        programa_out = ProgramaOutSchema.from_orm(programa_obj)
        programa_out.dias = programa_obj.get_dias()
        return programa_out

    except Exception as e:
        print(f"Error al crear programa: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error interno al guardar el programa.")

# Endpoint 2: OBTENER todos los programas generales (GET)


@router.get("/general", response_model=List[ProgramaOutSchema])
async def obtener_programas_generales():

    programas = await ProgramaEntrenamiento.filter(is_general=True).all()

    programas_out = []
    for p in programas:
        p_out = ProgramaOutSchema.from_orm(p)
        p_out.dias = p.get_dias()  # Deserializa el JSON antes de enviarlo
        programas_out.append(p_out)

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

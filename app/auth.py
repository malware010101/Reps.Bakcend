from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr
from app.models import User
from tortoise.exceptions import DoesNotExist
import bcrypt
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional, List
from app.models import Anamnesis
from app.services.memberships.service import dias_restantes, obtener_datos_membresia, duracion_plan
from app.services.memberships.validator import actualizar_estado_si_vencio
from app.services.memberships.service import asignar_membresia
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY no encontrada en variables de entorno")

ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1440)
)

# Esquema para obtener el token del encabezado "Authorization: Bearer <token>"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


router = APIRouter()


class UserInSchema(BaseModel):
    nombre: str
    email: EmailStr
    password: str
    rol: str = "usuario"
    membresia_plan: str = "standard"


class UpdateUserRoleSchema(BaseModel):
    user_id: int
    rol: str


class userSchemaOut(BaseModel):
    id: int
    nombre: str
    rol: str

    membresia_plan: str | None
    membresia_estado: str | None
    membresia_inicio: datetime | None
    membresia_fin: datetime | None

    duracion_plan: int
    dias_restantes: int


class RenovarMembresiaSchema(BaseModel):
    user_id: int
    membresia_plan: str


@router.get("/users", response_model=List[userSchemaOut])
async def get_all_users():

    users = await User.all()

    response = []

    for user in users:
        await actualizar_estado_si_vencio(user)

        response.append({
            "id": user.id,
            "nombre": user.nombre,
            "rol": user.rol,
            "membresia_plan": user.membresia_plan,
            "membresia_estado": user.membresia_estado,
            "membresia_inicio": user.membresia_inicio,
            "membresia_fin": user.membresia_fin,

            "duracion_plan": duracion_plan(user.membresia_plan),
            "dias_restantes": dias_restantes(user.membresia_fin)
        })
    return response


@router.get("/users/{user_id}", response_model=userSchemaOut)
async def get_user_by_id(user_id: int):

    try:
        user = await User.get(id=user_id)

        await actualizar_estado_si_vencio(user)

        return {
            "id": user.id,
            "nombre": user.nombre,
            "rol": user.rol,
            "membresia_plan": user.membresia_plan,
            "membresia_estado": user.membresia_estado,
            "membresia_inicio": user.membresia_inicio,
            "membresia_fin": user.membresia_fin,

            "duracion_plan": duracion_plan(user.membresia_plan),
            "dias_restantes": dias_restantes(user.membresia_fin)
        }

    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )


def hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserInSchema):

    hashed_password = hash_password(user_data.password)
    datos_membresia = obtener_datos_membresia(
        rol=user_data.rol,
        plan=user_data.membresia_plan
    )

    # Crea el usuario en la db
    new_user = await register_user_in_db(
        nombre=user_data.nombre,
        email=user_data.email,
        password_hash=hashed_password,
        rol=user_data.rol,
        **datos_membresia
    )

    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al registrar el usuario en la base de datos"
        )

    return {"message": "Usuario registrado exitosamente", "user_id": new_user.id}


async def register_user_in_db(nombre: str, email: str, password_hash: str, rol: str, membresia_plan: str | None, membresia_inicio: datetime | None, membresia_fin: datetime | None, membresia_estado: str | None):

    try:
        new_user = await User.create(
            nombre=nombre,
            email=email,
            password_hash=password_hash,
            rol=rol,
            membresia_plan=membresia_plan,
            membresia_inicio=membresia_inicio,
            membresia_fin=membresia_fin,
            membresia_estado=membresia_estado
        )
        return new_user
    except Exception as e:
        print(f"Error al registrar usuario en DB: {e}")
        return None


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


@router.post("/login")
async def login_user(login_data: LoginSchema):
    try:
        user = await User.get(email=login_data.email)
        await actualizar_estado_si_vencio(user)
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )

    # Verificar la contraseña
    if not bcrypt.checkpw(login_data.password.encode('utf-8'), user.password_hash.encode('utf-8')):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )

    tiene_anamnesis = await Anamnesis.get_or_none(usuario=user) is not None

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "rol": user.rol},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "nombre": user.nombre,
        "rol": user.rol,
        "membresia_plan": user.membresia_plan,
        "membresia_inicio": user.membresia_inicio,
        "membresia_fin": user.membresia_fin,
        "membresia_estado": user.membresia_estado,

        "duracion_plan": duracion_plan(user.membresia_plan),
        "dias_restantes": dias_restantes(user.membresia_fin),

        "tiene_anamnesis": tiene_anamnesis
    }


@router.put("/update-role", status_code=status.HTTP_200_OK)
async def update_user_role(update_data: UpdateUserRoleSchema):
    try:
        user = await User.get(id=update_data.user_id)
        user.rol = update_data.rol
        await user.save()
        return {"message": "Rol de usuario actualizado exitosamente"}
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# obtwngo el usuario autenticado atravez del token


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decodificar el token usando tu clave secreta
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    try:
        # Buscar el usuario en la base de datos usando el ID del token
        user = await User.get(id=int(user_id))
    except DoesNotExist:
        raise credentials_exception

    return user


@router.get("/me")
async def obtener_usuario_actual(
    current_user: User = Depends(get_current_user)
):
    tiene_anamnesis = await Anamnesis.get_or_none(usuario=current_user) is not None
    await actualizar_estado_si_vencio(current_user)

    return {
        "id": current_user.id,
        "nombre": current_user.nombre,
        "rol": current_user.rol,
        "membresia_plan": current_user.membresia_plan,
        "membresia_inicio": current_user.membresia_inicio,
        "membresia_fin": current_user.membresia_fin,
        "membresia_estado": current_user.membresia_estado,

        "duracion_plan": duracion_plan(current_user.membresia_plan),
        "dias_restantes": dias_restantes(current_user.membresia_fin),

        "tiene_anamnesis": tiene_anamnesis
    }


@router.put("/renovar-membresia", status_code=status.HTTP_200_OK)
async def renovar_membresia(data: RenovarMembresiaSchema, current_user: User = Depends(get_current_user)):

    if current_user.rol not in ("admin", "coach"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para renovar membresías."
        )
    user = await User.get_or_none(id=data.user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    if user.rol in ("admin", "coach"):
        raise HTTPException(
            status_code=400,
            detail="Este usuario no maneja membresías"
        )

    try:
        datos = asignar_membresia(data.membresia_plan)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    user.membresia_plan = datos["membresia_plan"]
    user.membresia_inicio = datos["membresia_inicio"]
    user.membresia_fin = datos["membresia_fin"]
    user.membresia_estado = datos["membresia_estado"]

    await user.save()

    return {
        "message": "Membresía renovada correctamente"
    }

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr
from .models import User
from tortoise.exceptions import DoesNotExist
import bcrypt
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional

SECRET_KEY = "tu_clave_secreta_super_segura_y_larga"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # El token expira en 60 minutos

# Esquema para obtener el token del encabezado "Authorization: Bearer <token>"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
# Asegúrate que tokenUrl coincida con el prefijo de tu router de autenticación


router = APIRouter()


class UserInSchema(BaseModel):
    nombre: str
    email: EmailStr
    password: str
    rol: str = "usuario"

    # modelo para la actualización de rol


class UpdateUserRoleSchema(BaseModel):
    user_id: int
    rol: str


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserInSchema):
    # Encriptar la contraseña
    # Esto devuelve un objeto de tipo bytes
    hashed_password = bcrypt.hashpw(
        user_data.password.encode('utf-8'), bcrypt.gensalt())

    # Crear el usuario en la base de datos
    new_user = await User.create(
        nombre=user_data.nombre,
        email=user_data.email,
        # Aquí decodificamos el objeto de bytes a una cadena de texto antes de guardarlo
        password_hash=hashed_password.decode('utf-8'),
        rol=user_data.rol
    )

    return {"message": "Usuario registrado exitosamente", "user_id": new_user.id}


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


@router.post("/login")
async def login_user(login_data: LoginSchema):
    try:
        user = await User.get(email=login_data.email)
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
        "rol": user.rol
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
# FUNCIÓN AUXILIAR PARA CREAR EL TOKEN


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# FUNCIÓN PARA OBTENER EL USUARIO AUTENTICADO A PARTIR DEL TOKEN


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

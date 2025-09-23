# app/auth.py

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from .models import User
from tortoise.exceptions import DoesNotExist
import bcrypt

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
    hashed_password = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt())

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
    
    # Autenticación exitosa
    return {"message": "Inicio de sesión exitoso", 
            "user_id": user.id,
             "nombre": user.nombre,
             "rol": user.rol}


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
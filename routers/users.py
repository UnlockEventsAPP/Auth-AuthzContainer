import os

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import BackgroundTasks
from sqlalchemy.orm import Session

from mail import send_registration_email
from models import Usuario
from schemas import UsuarioCreate, Usuario as UserSchema, LoginRequest
from database import get_db
from .auth import create_access_token, verify_password, get_password_hash, ACCESS_TOKEN_EXPIRE_MINUTES, decode_access_token
from datetime import timedelta

router = APIRouter()

# Crear un usuario
@router.post("/usuarios/", response_model=UserSchema)
def create_user(
    user: UsuarioCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    hashed_password = get_password_hash(user.password)
    db_user = Usuario(
        nombre=user.nombre,
        email=user.email,
        telefono=user.telefono,
        estado=user.estado,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Asegurarse de que los parámetros coincidan con la definición de la función
    background_tasks.add_task(send_registration_email, user.email, user.nombre, os.getenv('FRONTEND_URL_USER'))

    return db_user

# Endpoint para login y obtener un token JWT
@router.post("/login/")
def login_for_access_token(login_data: LoginRequest, db: Session = Depends(get_db)):
    db_user = db.query(Usuario).filter(Usuario.email == login_data.email).first()
    if not db_user or not verify_password(login_data.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Proteger un endpoint usando el token JWT
@router.get("/usuarios/me/", response_model=UserSchema)
def read_users_me(db: Session = Depends(get_db), token: dict = Depends(decode_access_token)):
    email = token.get("sub")
    if email is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    db_user = db.query(Usuario).filter(Usuario.email == email).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user

# Endpoint para listar todos los usuarios
@router.get("/getall-usuarios/", response_model=list[UserSchema])
def list_users(db: Session = Depends(get_db)):
    """
    Obtener todos los usuarios registrados en el sistema.
    """
    users = db.query(Usuario).all()
    return users


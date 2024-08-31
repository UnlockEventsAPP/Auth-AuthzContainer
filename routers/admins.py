from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import Administrador
from schemas import AdministradorCreate, Administrador as AdminSchema, AdminLogin
from database import get_db
from .auth import create_access_token, verify_password, get_password_hash, ACCESS_TOKEN_EXPIRE_MINUTES, decode_access_token

from datetime import timedelta

router = APIRouter()


# Crear un administrador
@router.post("/administradores/", response_model=AdminSchema)
def create_admin(admin: AdministradorCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(admin.password)
    db_admin = Administrador(
        nombre=admin.nombre,
        email=admin.email,
        telefono=admin.telefono,
        hashed_password=hashed_password
    )
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin


# Endpoint para login y obtener un token JWT
@router.post("/admin-login/")
def login_for_access_token(admin: AdminLogin, db: Session = Depends(get_db)):
    db_admin = db.query(Administrador).filter(Administrador.email == admin.email).first()
    if not db_admin or not verify_password(admin.password, db_admin.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_admin.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Proteger un endpoint usando el token JWT
@router.get("/administradores/me/", response_model=AdminSchema)
def read_admin_me(db: Session = Depends(get_db), token: str = Depends(decode_access_token)):
    email = token.get("sub")
    if email is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    db_admin = db.query(Administrador).filter(Administrador.email == email).first()
    if db_admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")

    return db_admin

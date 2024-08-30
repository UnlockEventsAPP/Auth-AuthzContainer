from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from models import Usuario
from schemas import UsuarioCreate, Usuario as UserSchema
from database import get_db

router = APIRouter()

# Configuración de PassLib para hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


# Crear un usuario
@router.post("/usuarios/", response_model=UserSchema)
def create_user(user: UsuarioCreate, db: Session = Depends(get_db)):
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
    return db_user


# Obtener un usuario por ID
@router.get("/usuarios/{user_id}", response_model=UserSchema)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# Actualizar un usuario
@router.put("/usuarios/{user_id}", response_model=UserSchema)
def update_user(user_id: int, user: UsuarioCreate, db: Session = Depends(get_db)):
    db_user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.nombre = user.nombre
    db_user.email = user.email
    db_user.telefono = user.telefono
    db_user.estado = user.estado
    db_user.hashed_password = get_password_hash(user.password)

    db.commit()
    db.refresh(db_user)
    return db_user


# Eliminar un usuario
@router.delete("/usuarios/{user_id}", response_model=UserSchema)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return db_user

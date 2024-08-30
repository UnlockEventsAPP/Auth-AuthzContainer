from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Usuario
from schemas import UsuarioCreate, Usuario as UserSchema
from database import get_db

router = APIRouter()


@router.post("/usuarios/", response_model=UserSchema)
def create_user(user: UsuarioCreate, db: Session = Depends(get_db)):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = Usuario(nombre=user.nombre, email=user.email, telefono=user.telefono, estado=user.estado,
                      hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/usuarios/{user_id}", response_model=UserSchema)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/usuarios/{user_id}", response_model=UserSchema)
def update_user(user_id: int, user: UsuarioCreate, db: Session = Depends(get_db)):
    db_user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.nombre = user.nombre
    db_user.email = user.email
    db_user.telefono = user.telefono
    db_user.estado = user.estado
    db_user.hashed_password = user.password + "notreallyhashed"

    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/usuarios/{user_id}", response_model=UserSchema)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return db_user

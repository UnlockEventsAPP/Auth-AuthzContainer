from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Administrador
from schemas import AdministradorCreate, Administrador as AdminSchema
from database import get_db

router = APIRouter()


@router.post("/administradores/", response_model=AdminSchema)
def create_admin(admin: AdministradorCreate, db: Session = Depends(get_db)):
    db_admin = Administrador(nombre=admin.nombre, email=admin.email, telefono=admin.telefono)
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin


@router.get("/administradores/{admin_id}", response_model=AdminSchema)
def read_admin(admin_id: int, db: Session = Depends(get_db)):
    db_admin = db.query(Administrador).filter(Administrador.id == admin_id).first()
    if db_admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    return db_admin


@router.put("/administradores/{admin_id}", response_model=AdminSchema)
def update_admin(admin_id: int, admin: AdministradorCreate, db: Session = Depends(get_db)):
    db_admin = db.query(Administrador).filter(Administrador.id == admin_id).first()
    if db_admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")

    db_admin.nombre = admin.nombre
    db_admin.email = admin.email
    db_admin.telefono = admin.telefono

    db.commit()
    db.refresh(db_admin)
    return db_admin


@router.delete("/administradores/{admin_id}", response_model=AdminSchema)
def delete_admin(admin_id: int, db: Session = Depends(get_db)):
    db_admin = db.query(Administrador).filter(Administrador.id == admin_id).first()
    if db_admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")

    db.delete(db_admin)
    db.commit()
    return db_admin
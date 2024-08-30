from sqlalchemy import Column, Integer, String
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), index=True)
    email = Column(String(255), unique=True, index=True)
    telefono = Column(String(20), index=True)
    estado = Column(String(50))
    hashed_password = Column(String(255))

class Administrador(Base):
    __tablename__ = "administradores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), index=True)
    email = Column(String(255), unique=True, index=True)
    telefono = Column(String(20), index=True)
    hashed_password = Column(String(255))



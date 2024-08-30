from sqlalchemy import Column, Integer, String
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), index=True)  # Especificar longitud
    email = Column(String(255), unique=True, index=True)  # Especificar longitud
    telefono = Column(String(20), index=True)  # Especificar longitud
    estado = Column(String(50))  # Especificar longitud
    hashed_password = Column(String(255))  # Especificar longitud

class Administrador(Base):
    __tablename__ = "administradores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), index=True)  # Especificar longitud
    email = Column(String(255), unique=True, index=True)  # Especificar longitud
    telefono = Column(String(20), index=True)  # Especificar longitud


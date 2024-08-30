from pydantic import BaseModel

class UsuarioBase(BaseModel):
    nombre: str
    email: str
    telefono: str
    estado: str

class UsuarioCreate(UsuarioBase):
    password: str

class Usuario(UsuarioBase):
    id: int

    class Config:
        from_attributes = True

class AdministradorBase(BaseModel):
    nombre: str
    email: str
    telefono: str

class AdministradorCreate(AdministradorBase):
    password: str

class Administrador(AdministradorBase):
    id: int

    class Config:
        from_attributes = True

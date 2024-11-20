from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers import users, admins, auth

app = FastAPI()

origins = [
    "https://front-unlock-patrones.vercel.app",  # Dominio del frontend en producción
    "http://localhost:4200",  # Dominio local para pruebas
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permitir solicitudes desde estos orígenes
    allow_credentials=True,  # Permitir envío de credenciales (cookies, headers de autenticación, etc.)
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los encabezados
)


app.include_router(users.router, prefix="/auth", tags=["usuarios"])
app.include_router(admins.router, prefix="/auth", tags=["administradores"])

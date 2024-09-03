from fastapi import FastAPI
from routers import users, admins, auth

app = FastAPI()

app.include_router(users.router, prefix="/auth", tags=["usuarios"])
app.include_router(admins.router, prefix="/auth", tags=["administradores"])

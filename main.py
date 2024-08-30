from database import engine, Base, get_db
from routers import users, admins
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router, prefix="/api/auth", tags=["usuarios"])
app.include_router(admins.router, prefix="/api/auth", tags=["administradores"])

@app.get("/test-db-connection/")
def test_db_connection(db: Session = Depends(get_db)):
    try:
        result = db.execute("SELECT 1").scalar()
        return {"status": "success", "result": result}
    except SQLAlchemyError as e:
        return {"status": "failure", "error": str(e)}

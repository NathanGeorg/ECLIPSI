from fastapi import FastAPI

from app.database.connection import Base, engine
from app.routers.auth import router as auth_router
from app.routers.professionals import router as professionals_router
from app.seed import seed_database

Base.metadata.create_all(bind=engine)
seed_database()

app = FastAPI(
    title="EcliPsi API",
    description="API inicial do EcliPsi - P.I. 1",
    version="1.0.0",
)

app.include_router(auth_router)
app.include_router(professionals_router)


@app.get("/", tags=["Geral"])
def root():
    return {"message": "EcliPsi API funcionando", "docs": "/docs"}

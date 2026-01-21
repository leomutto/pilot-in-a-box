from fastapi import FastAPI

from backend.api.routes.auth import router as auth_router
from backend.api.routes.mass import router as mass_router

app = FastAPI(
    title="MASS Simple",
    version="1.0.0"
)

# Registrar routers del MVP
app.include_router(auth_router)
app.include_router(mass_router)
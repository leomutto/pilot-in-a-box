from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.auth import router as auth_router
from api.routes.mass import router as mass_router

from db.session import engine
from db.base import Base


app = FastAPI(
    title="MASS Simple",
    version="1.0.0"
)


# ---------------------------------------------------------
# CORS (necesario para frontend)
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en producción, reemplazar por dominios reales
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# Crear tablas al iniciar FastAPI
# ---------------------------------------------------------
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


# ---------------------------------------------------------
# Healthcheck (útil para Docker/Kubernetes)
# ---------------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# ---------------------------------------------------------
# Registrar rutas
# ---------------------------------------------------------
app.include_router(auth_router)
app.include_router(mass_router)

# En MASS Enterprise, aquí se agregarán más routers:
# app.include_router(admin_router)
# app.include_router(analytics_router)
# app.include_router(ai_router)
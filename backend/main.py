from fastapi import FastAPI
from core.config import settings
from routers.health import router as health_router
from routers.items import router as items_router
from routers.auth import router as auth_router

# Importar configuración de OpenTelemetry
from app.otel_config import setup_otel

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION
)

# Inicializar OpenTelemetry
setup_otel(app)

# Registrar routers
app.include_router(health_router)
app.include_router(items_router)
app.include_router(auth_router)
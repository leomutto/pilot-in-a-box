from fastapi import FastAPI
from app.ingestion.routers import router as ingestion_router

app = FastAPI()

# Registrar router de ingestion
app.include_router(ingestion_router)
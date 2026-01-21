from fastapi import FastAPI
from backend.api.routes import mass

app = FastAPI()

# Registrar router MASS simple
app.include_router(mass.router)
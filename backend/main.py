# Contenido para: backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Importamos TODOS nuestros routers
from backend.routers import config_router, kpi_router, forecast_router

# Inicialización de la Aplicación
app = FastAPI(
    title="Retail Forecasting API",
    description="API para obtener pronósticos de ventas (SARIMA y XGBoost) filtrado por categoría y región.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint Raíz
@app.get("/")
def read_root():
    return {"message": "Welcome to the Retail Forecasting API. Access /docs for documentation."}

# --- Incluimos los routers ---
# Esto conecta todos los endpoints
app.include_router(config_router.router)
app.include_router(kpi_router.router)
app.include_router(forecast_router.router) # <-- Esta línea es la clave
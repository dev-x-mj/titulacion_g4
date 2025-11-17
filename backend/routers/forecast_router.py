# Contenido para: backend/routers/forecast_router.py

from fastapi import APIRouter, Query, HTTPException
from typing import Dict
import pandas as pd

# Importamos los datos crudos y la función de chequeo
from backend.config import DF_RAW, check_data_loaded
# Importamos los servicios que orquestan la lógica
from backend.services.forecast_service import process_forecast_request, process_evaluation_request

router = APIRouter(
    prefix="/sales",
    tags=["Sales Forecasting"]
)

@router.get("/forecast", response_model=Dict)
def sales_forecast_endpoint(
    model_type: str = Query("sarima", description="El modelo a usar: 'sarima' o 'xgboost'"),
    category: str = Query("All Categories", description="Categoría del producto."),
    region: str = Query("All Regions", description="Región geográfica."),
    steps: int = Query(12, description="Número de períodos a pronosticar."),
    frequency: str = Query("M", description="Frecuencia (M, Q, A)")
):
    """
    Endpoint dinámico que genera un pronóstico futuro usando el modelo seleccionado.
    """
    check_data_loaded()
    
    # 1. Llamamos al servicio para procesar la petición
    result = process_forecast_request(DF_RAW, model_type, category, region, steps, frequency)
    
    # 2. Manejamos la respuesta del servicio
    if result["status"] != "success":
        raise HTTPException(status_code=400, detail=result["message"])
        
    # 3. Formateamos la respuesta a JSON
    history_ts = result["history"]
    forecast_df = result["forecast_df"]
    
    history_json = {
        "index": [i.strftime("%Y-%m-%d") for i in history_ts.index],
        "data": history_ts.values.tolist()
    }
    forecast_df['Date'] = forecast_df.index.strftime('%Y-%m-%d')
    forecast_json = forecast_df.reset_index(drop=True).to_dict(orient='records')

    return {
        "status": "success",
        "model_used": result["model_used"],
        "history": history_json,
        "forecast": forecast_json
    }

@router.get("/evaluation", response_model=Dict)
def sales_evaluation_endpoint(
    model_type: str = Query("sarima", description="El modelo a evaluar: 'sarima' o 'xgboost'"),
    category: str = Query("All Categories", description="Categoría del producto."),
    region: str = Query("All Regions", description="Región geográfica."),
    frequency: str = Query("M", description="Frecuencia (M, Q, A)")
):
    """
    Realiza un backtest del modelo seleccionado y devuelve las métricas de error.
    """
    check_data_loaded()
    
    # 1. Llamamos al servicio
    metrics = process_evaluation_request(DF_RAW, model_type, category, region, frequency)
    
    # 2. Manejamos la respuesta
    if metrics.get("status") != "Success":
        raise HTTPException(status_code=400, detail=metrics.get("message", "Error desconocido en evaluación"))
        
    metrics["model_used"] = model_type
    return metrics


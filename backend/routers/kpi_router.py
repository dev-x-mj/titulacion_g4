from fastapi import APIRouter, HTTPException
from typing import Dict
# Importamos los datos crudos y el chequeo
from backend.config import DF_RAW, check_data_loaded
#  Importamos las funciones de servicio
from backend.services.kpi_service import calculate_global_kpis, get_regional_analysis

router = APIRouter(
    prefix="/global",
    tags=["KPIs"]
)

@router.get("/kpis", response_model=Dict)
def global_kpis_endpoint():
    """
    Devuelve métricas clave de rendimiento (KPIs) a nivel global.
    """
    check_data_loaded()
    
    
    # 1. Calculamos los KPIs
    kpis = calculate_global_kpis(DF_RAW)
    # 2. Calculamos el análisis regional
    regional_data = get_regional_analysis(DF_RAW)
    
    # 3. Los devolvemos en la respuesta
    return {
        "status": "success",
        "kpis": kpis, # <-- La llave que faltaba
        "regional_analysis": regional_data # <-- Esta también
    }
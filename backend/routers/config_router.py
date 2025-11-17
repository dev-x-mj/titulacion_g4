from fastapi import APIRouter, HTTPException
# Importamos las variables globales y la función de chequeo desde config.py
from backend.config import CATEGORIES, REGIONS, FREQUENCIES, check_data_loaded

router = APIRouter(
    prefix="/config",
    tags=["Configuration"]
)

@router.get("/filters") 
def get_filters(): 
    """
    Devuelve las listas de filtros para poblar los selectores del frontend.
    """ 
    check_data_loaded() # Verifica si DF_RAW es None
    
    return { 
        "categories": CATEGORIES, 
        "regions": REGIONS, 
        "frequencies": FREQUENCIES 
    }
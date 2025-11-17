# Contenido para: backend/routers/config_router.py

from fastapi import APIRouter, HTTPException
# Importamos las variables globales y la función de chequeo desde config.py
from backend.config import CATEGORIES, REGIONS, FREQUENCIES, check_data_loaded

router = APIRouter(
    prefix="/config",
    tags=["Configuration"]
)

@router.get("/filters") # [fuente: 695]
def get_filters(): # [fuente: 696]
    """
    Devuelve las listas de filtros para poblar los selectores del frontend.
    """ # [fuente: 697]
    check_data_loaded() # Verifica si DF_RAW es None
    
    return { # [fuente: 701]
        "categories": CATEGORIES, # [fuente: 702]
        "regions": REGIONS, # [fuente: 703]
        "frequencies": FREQUENCIES # [fuente: 704]
    }
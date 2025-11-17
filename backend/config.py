# Contenido para: backend/config.py

from fastapi import HTTPException
# Importamos la función de carga desde su nueva ubicación
from backend.data_processing import load_data 

# 2. Carga de Datos (Lógica de api_service.py) 
DF_RAW, STATUS = load_data() 

if DF_RAW is None:
    print(f"FATAL ERROR: Datos no cargados. Razón: {STATUS}") # 
    # En un escenario real, podrías querer que la app falle si no carga datos.
    # Por ahora, dejamos que las variables se inicialicen como None o vacías.
    CATEGORIES = ['All Categories']
    REGIONS = ['All Regions']
    FREQUENCIES = {"Mensual (M)": "M"}
else:
    print("Datos cargados y preprocesados exitosamente.") 
    CATEGORIES = ['All Categories'] + sorted(DF_RAW['Category'].unique().tolist()) 
    REGIONS = ['All Regions'] + sorted(DF_RAW['Region'].unique().tolist()) 
    # Definimos las frecuencias que soporta nuestro API 
    FREQUENCIES = { 
        "Mensual (ME)": "ME", 
        "Trimestral (QE)": "QE", 
        "Anual (AE)": "AE" 
    }

# Función helper para verificar el estado de los datos en los routers
def check_data_loaded():
    if DF_RAW is None:
        raise HTTPException(status_code=500, detail=f"Datos no cargados. Razón: {STATUS}") # [fuente: 698, 699, 700]
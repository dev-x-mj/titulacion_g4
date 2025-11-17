import streamlit as st
import requests

# URL del Backend (FastAPI)
API_BASE_URL = "http://127.0.0.1:8000"

# --- Funciones de Comunicación de Configuración ---

@st.cache_data(ttl=600)
def fetch_config():
    """
    Obtiene las opciones de filtros (Categorías, Regiones, Frecuencias) desde el API.
    """
    try:
        response = requests.get(f"{API_BASE_URL}/config/filters")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error(f"⚠️ Error de Conexión: Asegúrate de que el backend (FastAPI) esté corriendo en {API_BASE_URL}")
        st.stop() # Detiene la app si no puede cargar la configuración
    except Exception as e:
        st.error(f"Ocurrió un error al cargar la configuración: {e}")
        st.stop()
        
# --- NUEVO (Paso 4) ---
@st.cache_data(ttl=3600) # Cachear por 1 hora
def fetch_global_kpis():
    """
    Obtiene las métricas KPIs globales desde el nuevo endpoint.
    """
    try:
        response = requests.get(f"{API_BASE_URL}/global/kpis")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Error de Conexión: No se pudo conectar al API para obtener los KPIs.")
        return None
    except Exception as e:
        st.error(f"Error al cargar los KPIs globales: {e}")
        return None

# --- MODIFICADO (Paso 4) ---
def fetch_forecast(category, region, model_type, steps, frequency_code):
    """
    Obtiene el pronóstico y la evaluación para los filtros seleccionados.
    Ahora envía los parámetros de 'steps' y 'frequency_code'.
    """
    try:
        # 1. Llamamos al endpoint de evaluación
        eval_response = requests.get(f"{API_BASE_URL}/sales/evaluation", params={
            "model_type": model_type.lower(), 
            "category": category, 
            "region": region,
            "frequency": frequency_code # <-- NUEVO
        })
        eval_response.raise_for_status()
        metrics = eval_response.json()
        
        # 2. Llamamos al endpoint de pronóstico
        forecast_response = requests.get(f"{API_BASE_URL}/sales/forecast", params={
            "model_type": model_type.lower(), 
            "category": category, 
            "region": region,
            "steps": steps,            # <-- MODIFICADO
            "frequency": frequency_code # <-- NUEVO
        })
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()
        
        # 3. Combinamos la respuesta
        forecast_data['metrics'] = metrics
        forecast_data['model_used'] = model_type.upper() # Guardar como 'SARIMA' o 'XGBOOST'
        
        return forecast_data
        
    except requests.exceptions.HTTPError as e:
        # Muestra el error específico del backend (ej. "Datos insuficientes...")
        error_detail = "Error desconocido en el API"
        try:
            # Intentamos leer el JSON que envía FastAPI
            error_detail = e.response.json().get('detail', error_detail)
        except requests.exceptions.JSONDecodeError:
            # Si falla (respuesta vacía), usamos el texto plano
            error_detail = e.response.text if e.response.text else f"Error {e.response.status_code} sin mensaje"
        
        st.error(f"Error del API: {error_detail}")
        return None
        
    except requests.exceptions.ConnectionError:
        st.error("Error de Conexión con el API. Asegúrate de que Uvicorn esté corriendo.")
        return None
    except Exception as e:
        st.error(f"Error inesperado durante la comunicación: {e}")
        return None
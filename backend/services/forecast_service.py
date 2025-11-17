# Contenido para: backend/services/forecast_service.py

# 1. Importaciones de nuestros módulos
from backend.data_processing import aggregate_sales
from backend.models.sarima_model import get_sarima_forecast, run_backtest_sarima 
from backend.models.xgboost_model import get_xgboost_forecast, run_backtest_xgboost 

def process_forecast_request(df_raw, model_type, category, region, steps, frequency):
    """
    Orquesta la lógica para generar un pronóstico.
    1. Agrega los datos.
    2. Llama al modelo solicitado.
    3. Devuelve los resultados (historia y pronóstico).
    """
    
    # 1. Agregamos los datos históricos según los filtros
    # (Esta lógica estaba en el endpoint /sales/forecast 
    ts_history, data_available = aggregate_sales( 
        df=df_raw, 
        category=category, 
        region=region, 
        frequency=frequency 
    )
    
    if not data_available: 
        return {"status": "error", "message": f"No data found for {category}/{region}."} 

    # 2. Enrutador de modelo
    if model_type == "sarima": 
        forecast_df, status = get_sarima_forecast(ts_history, steps, frequency) 
    elif model_type == "xgboost": 
        forecast_df, status = get_xgboost_forecast(ts_history, steps, frequency) 
    else:
        return {"status": "error", "message": "model_type debe ser 'sarima' o 'xgboost'"} 
    
    if status != "Success" or forecast_df is None:
        # 'status' aquí contiene el mensaje de error del modelo (ej. "Datos insuficientes...")
        return {"status": "error", "message": status} 
    
    # 3. Devolvemos los datos crudos (Series y DataFrame)
    # El router se encargará de formatearlos a JSON
    return {
        "status": "success",
        "model_used": model_type, 
        "history": ts_history, 
        "forecast_df": forecast_df 
    }

def process_evaluation_request(df_raw, model_type, category, region, frequency):
    """
    Orquesta la lógica para generar una evaluación (backtest).
    1. Agrega los datos.
    2. Llama al modelo de backtest solicitado.
    3. Devuelve las métricas.
    """
    
    # 1. Agregamos los datos históricos
    # (Esta lógica estaba en el endpoint /sales/evaluation 
    ts_history, data_available = aggregate_sales( 
        df=df_raw, 
        category=category, 
        region=region, 
        frequency=frequency 
    )
    
    if not data_available: 
        return {"status": "error", "message": f"No data found for {category}/{region}."} 

    # 2. Enrutador de modelo
    if model_type == "sarima": 
        metrics = run_backtest_sarima(ts_history, frequency) 
    elif model_type == "xgboost": 
        metrics = run_backtest_xgboost(ts_history, frequency) 
    else:
        return {"status": "error", "message": "model_type debe ser 'sarima' o 'xgboost'"} 

    # 3. Devolvemos el diccionario de métricas
    # El diccionario ya incluye un "status" y "message" en caso de error
    return metrics 
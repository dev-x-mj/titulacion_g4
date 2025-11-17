# Contenido para: backend/services/forecast_service.py

# 1. Importaciones de nuestros módulos
from backend.data_processing import aggregate_sales # [cite: 652]
from backend.models.sarima_model import get_sarima_forecast, run_backtest_sarima # [cite: 660]
from backend.models.xgboost_model import get_xgboost_forecast, run_backtest_xgboost # [cite: 660]

def process_forecast_request(df_raw, model_type, category, region, steps, frequency):
    """
    Orquesta la lógica para generar un pronóstico.
    1. Agrega los datos.
    2. Llama al modelo solicitado.
    3. Devuelve los resultados (historia y pronóstico).
    """
    
    # 1. Agregamos los datos históricos según los filtros
    # (Esta lógica estaba en el endpoint /sales/forecast [cite: 737])
    ts_history, data_available = aggregate_sales( # [cite: 737]
        df=df_raw, # [cite: 738]
        category=category, # [cite: 739]
        region=region, # [cite: 740]
        frequency=frequency # [cite: 741]
    )
    
    if not data_available: # [cite: 743]
        return {"status": "error", "message": f"No data found for {category}/{region}."} # [cite: 744]

    # 2. Enrutador de modelo
    if model_type == "sarima": # [cite: 747]
        forecast_df, status = get_sarima_forecast(ts_history, steps, frequency) # [cite: 748, 749]
    elif model_type == "xgboost": # [cite: 750]
        forecast_df, status = get_xgboost_forecast(ts_history, steps, frequency) # [cite: 751, 752]
    else:
        return {"status": "error", "message": "model_type debe ser 'sarima' o 'xgboost'"} # [cite: 753, 754]
    
    if status != "Success" or forecast_df is None: # [cite: 755]
        # 'status' aquí contiene el mensaje de error del modelo (ej. "Datos insuficientes...")
        return {"status": "error", "message": status} # [cite: 756]
    
    # 3. Devolvemos los datos crudos (Series y DataFrame)
    # El router se encargará de formatearlos a JSON
    return {
        "status": "success", # [cite: 765]
        "model_used": model_type, # [cite: 766]
        "history": ts_history, # [cite: 767]
        "forecast_df": forecast_df # [cite: 768] (Nombrado para claridad)
    }

def process_evaluation_request(df_raw, model_type, category, region, frequency):
    """
    Orquesta la lógica para generar una evaluación (backtest).
    1. Agrega los datos.
    2. Llama al modelo de backtest solicitado.
    3. Devuelve las métricas.
    """
    
    # 1. Agregamos los datos históricos
    # (Esta lógica estaba en el endpoint /sales/evaluation [cite: 784])
    ts_history, data_available = aggregate_sales( # [cite: 784]
        df=df_raw, # [cite: 786]
        category=category, # [cite: 787]
        region=region, # [cite: 788]
        frequency=frequency # [cite: 789]
    )
    
    if not data_available: # [cite: 790]
        return {"status": "error", "message": f"No data found for {category}/{region}."} # [cite: 791]

    # 2. Enrutador de modelo
    if model_type == "sarima": # [cite: 794]
        metrics = run_backtest_sarima(ts_history, frequency) # [cite: 795]
    elif model_type == "xgboost": # [cite: 796]
        metrics = run_backtest_xgboost(ts_history, frequency) # [cite: 797]
    else:
        return {"status": "error", "message": "model_type debe ser 'sarima' o 'xgboost'"} # [cite: 799]

    # 3. Devolvemos el diccionario de métricas
    # El diccionario ya incluye un "status" y "message" en caso de error
    return metrics # [cite: 804]
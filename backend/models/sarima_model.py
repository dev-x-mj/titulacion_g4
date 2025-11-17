# Contenido para: backend/models/sarima_model.py

import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.statespace.sarimax import SARIMAX


def get_sarima_forecast(ts_history, steps=12, frequency_code="ME"):
    """
    Entrena el modelo SARIMA y genera el pronóstico de 'steps' períodos futuros.
    La estacionalidad (S=12, S=4) se adapta a la frecuencia.
    """
    
    # 1. Lógica de Estacionalidad Dinámica 
    if frequency_code == "ME":
        seasonal_period = 12 
        min_periods = 24 # 2 años de datos
    elif frequency_code == "QE":
        seasonal_period = 4 # 4 trimestres
        min_periods = 8 # 2 años de datos
    else: # Anual (AE)
        seasonal_period = 1 # Sin estacionalidad
        min_periods = 3 # 3 años de datos

    try:
        # 2. Validación Dinámica
        if len(ts_history) < min_periods:
            return None, f"Datos insuficientes para SARIMA (se requieren > {min_periods} períodos para la frecuencia {frequency_code})."
        
        # Parámetros SARIMA
        order = (0, 1, 1)
        # 3. seasonal_order ahora es dinámico
        seasonal_order = (0, 1, 1, seasonal_period)
        
        # Entrenar el modelo
        model = SARIMAX(
            ts_history,
            order=order,
            seasonal_order=seasonal_order,
            enforce_stationarity=False,
            enforce_invertibility=False
        )
        results = model.fit(disp=False)

        # Generar el pronóstico
        forecast = results.get_forecast(steps=steps)
        forecast_df = forecast.summary_frame(alpha=0.05) # 95% CI
        
        # Limpiar el DataFrame de salida
        forecast_df.rename(columns={
            'mean': 'Sales Forecast',
            'mean_ci_lower': 'Lower Bound',
            'mean_ci_upper': 'Upper Bound'
        }, inplace=True)
        
        if 'lower 95%' in forecast_df.columns:
            forecast_df.rename(columns={
                'lower 95%': 'Lower Bound',
                'upper 95%': 'Upper Bound'
            }, inplace=True)
            
        final_cols = ['Sales Forecast', 'Lower Bound', 'Upper Bound']
        forecast_df = forecast_df[final_cols].astype(float).round(2)
        forecast_df['Sales Forecast'] = forecast_df['Sales Forecast'].clip(lower=0)
        
        return forecast_df, "Success"
    
    except Exception as e:
        return None, f"Error en el entrenamiento SARIMA: {e}"


def run_backtest_sarima(ts_history, frequency_code="ME"):
    """
    Realiza un backtest del modelo SARIMA.
    El período de prueba se adapta a la frecuencia (1 año de datos).
    """
    
    # 1. Lógica de Períodos Dinámica 
    if frequency_code == "ME":
        seasonal_period = 12
        min_periods = 24
        test_periods = 12 # Probar con 12 meses
    elif frequency_code == "QE":
        seasonal_period = 4
        min_periods = 8
        test_periods = 4 # Probar con 4 trimestres
    else: # Anual (AE)
        seasonal_period = 1
        min_periods = 3
        test_periods = 1 # Probar con 1 año

    # 2. Validación Dinámica
    if len(ts_history) < (min_periods + test_periods):
        return {
            "status": "Error",
            "message": f"Datos insuficientes para backtest SARIMA. Se necesitan > {(min_periods + test_periods)} períodos."
        }
        
    # Dividir en Entrenamiento y Prueba
    train_data = ts_history[:-test_periods]
    test_data = ts_history[-test_periods:]
    
    try:
        # Parametros
        order = (0, 1, 1)
        # 3. seasonal order ahora es dinámico
        seasonal_order = (0, 1, 1, seasonal_period)
        
        model = SARIMAX(
            train_data,
            order=order,
            seasonal_order=seasonal_order,
            enforce_stationarity=False,
            enforce_invertibility=False
        )
        results = model.fit(disp=False)
        
        forecast = results.get_forecast(steps=test_periods)
        predictions = forecast.predicted_mean
        
        # Calcular Métricas
        rmse = np.sqrt(np.mean((test_data.values - predictions.values)**2))
        mask = test_data.values != 0
        mape = np.mean(
            np.abs((test_data.values[mask] - predictions.values[mask]) / test_data.values[mask])
        ) * 100
        
        return {
            "status": "Success",
            "test_period_months": test_periods,
            "mape": mape,
            "rmse": rmse
        }
    except Exception as e:
        return {"status": "Error", "message": f"Error en backtesting SARIMA: {e}"}
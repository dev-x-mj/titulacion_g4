import numpy as np
import pandas as pd
from xgboost import XGBRegressor
from backend.data_processing import create_features_for_ml


def get_xgboost_forecast(ts_history, steps=12, frequency_code="ME"):
    """
    Entrena el modelo XGBoost y genera el pronóstico de 'steps' períodos futuros.
    """
    
    # 1. Lógica de Períodos Dinámica
    if frequency_code == "ME":
        min_periods = 24
    elif frequency_code == "QE":
        min_periods = 8
    else: # Anual (AE)
        min_periods = 3

    try:
        # 2. Validación Dinámica
        if len(ts_history) < min_periods:
            return None, f"Datos insuficientes para XGBoost (se requieren > {min_periods} períodos para la frecuencia {frequency_code})."
        
        # 1. Crear features para todo el historial
        X, y = create_features_for_ml(ts_history, frequency_code)
        
        # 2. Entrenar el modelo
        model = XGBRegressor(objective='reg:squarederror', n_estimators=100)
        model.fit(X, y)
        
        # 3. Generar pronóstico futuro
        last_date = ts_history.index[-1]
        
        # 4. Usamos el 'frequency_code' para el rango de fechas
        future_dates = pd.date_range(start=last_date, periods=steps + 1, freq=f'{frequency_code}') [1:]
        future_df = pd.DataFrame(index=future_dates)
        future_df['Sales'] = np.nan
        
        full_ts = pd.concat([ts_history, future_df['Sales']])
        
        # Creamos features para el set completo
        full_features_X, _ = create_features_for_ml(full_ts, frequency_code)
        
        X_future = full_features_X.iloc[-steps:]
        
        # Predecir
        predictions = model.predict(X_future)
        predictions = predictions.clip(min=0)
        
        forecast_df = pd.DataFrame({
            'Sales Forecast': predictions,
            'Lower Bound': np.nan,
            'Upper Bound': np.nan
        }, index=future_dates)
        
        return forecast_df, "Success"
    
    except Exception as e:
        return None, f"Error en el entrenamiento XGBoost: {e}"


def run_backtest_xgboost(ts_history, frequency_code="ME"):
    """
    Realiza un backtest del modelo XGBoost.
    El período de prueba se adapta a la frecuencia (1 año de datos).
    """
    
    # 1. Lógica de Períodos Dinámica 
    if frequency_code == "ME":
        min_periods = 24
        test_periods = 12 # Probar con 12 meses
    elif frequency_code == "QE":
        min_periods = 8
        test_periods = 4 # Probar con 4 trimestres
    else: # Anual (AE)
        min_periods = 3
        test_periods = 1 # Probar con 1 año

    # 2. Validación Dinámica
    if len(ts_history) < (min_periods + test_periods):
        return {
            "status": "Error",
            "message": f"Datos insuficientes para backtest XGBoost. Se necesitan > {(min_periods + test_periods)} períodos."
        }
        
    # 1. Crear features para todos los datos
    X, y = create_features_for_ml(ts_history, frequency_code)
    
    # 2. Dividir en Entrenamiento y Prueba
    X_train, X_test = X.iloc[:-test_periods], X.iloc[-test_periods:]
    y_train, y_test = y.iloc[:-test_periods], y.iloc[-test_periods:]
    
    try:
        # 3. Entrenar el modelo
        model = XGBRegressor(objective='reg:squarederror', n_estimators=100)
        model.fit(X_train, y_train)
        
        # 4. Predecir en el set de prueba
        predictions = model.predict(X_test)
        
        # 5. Calcular Métricas
        rmse = np.sqrt(np.mean((y_test.values - predictions)**2))
        mask = y_test.values != 0
        mape = np.mean(
            np.abs((y_test.values[mask] - predictions[mask]) / y_test.values[mask])
        ) * 100
        
        return {
            "status": "Success",
            "test_period_months": test_periods,
            "mape": mape,
            "rmse": rmse
        }
    except Exception as e:
        return {"status": "Error", "message": f"Error en backtesting XGBoost: {e}"}
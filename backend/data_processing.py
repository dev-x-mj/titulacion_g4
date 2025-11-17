import pandas as pd
import numpy as np
import os

# --- Constante de Ruta Absoluta ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..'))
FILE_NAME = os.path.join(PROJECT_ROOT, 'data', 'US Superstore data.xls')

# --- Funciones de Carga y Preprocesamiento ---
def load_data():
    """
    Carga el dataset de Excel, lo limpia y retorna el DataFrame.
    Retorna (DataFrame, status_message).
    """
    try:
        df = pd.read_excel(FILE_NAME)
        
        # Limpieza de columnas
        df.columns = df.columns.str.replace(' ', '_').str.replace('-', '_').str.lower()
        
        # Aseguramos que las columnas clave existan antes de renombrar
        if 'order_date' in df.columns:
             df['Order_Date'] = pd.to_datetime(df['order_date'])
        if 'ship_date' in df.columns:
            df['Ship_Date'] = pd.to_datetime(df['ship_date'])

        # Estandarizar nombres de columnas principales que usaremos
        df = df.rename(columns={
            'category': 'Category',
            'region': 'Region',
            'sales': 'Sales',
            'profit': 'Profit',
            'discount': 'Discount',
            'state': 'State',
            'product_name': 'Product_Name',
            'segment': 'Segment',
            'sub_category': 'Sub_Category'
        })

        return df, "Success"
    except FileNotFoundError:
        return None, f"Error: Archivo no encontrado en la ruta esperada: {FILE_NAME}"
    except Exception as e:
        return None, f"Error al cargar o preprocesar los datos: {e}"

# --- Agregación de ventas ---
def aggregate_sales(df, category="All Categories", region="All Regions", frequency="M"):
    """
    Filtra el DataFrame y agrega las ventas a un nivel de frecuencia (M, Q, etc.).
    """
    if df is None:
        return pd.Series(dtype='float64'), False
    
    df_filtered = df.copy()
    if category != "All Categories":
        df_filtered = df_filtered[df_filtered['Category'] == category]
    if region != "All Regions":
        df_filtered = df_filtered[df_filtered['Region'] == region]
    
    if df_filtered.empty:
        return pd.Series(dtype='float64'), False
    
    df_filtered = df_filtered.set_index('Order_Date')
    ts_aggregated = df_filtered['Sales'].resample(f'{frequency}').sum()
    ts_aggregated = ts_aggregated[ts_aggregated.index.min():]
    
    return ts_aggregated, True

# --- Creación de features para ML ---
def create_features_for_ml(ts_data, frequency_code="M"):
    """
    Crea características de ML (lags, mes, año) a partir de una serie de tiempo.
    """
    df = pd.DataFrame(ts_data.copy())
    df.columns = ['Sales']
    df['month'] = df.index.month
    df['year'] = df.index.year
    df['quarter'] = df.index.quarter
    
    # Lags dinámicos según frecuencia
    if frequency_code == "ME":
        lag_period = 12
    elif frequency_code == "QE":
        lag_period = 4
    else: # 'A' o cualquier otro
        lag_period = 1
        
    df[f'lag_{lag_period}'] = df['Sales'].shift(lag_period)
    df = df.bfill()
    
    X = df.drop('Sales', axis=1)
    y = df['Sales']
    
    return X, y
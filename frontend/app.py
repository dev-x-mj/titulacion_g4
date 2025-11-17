# Contenido para: frontend/app.py

import streamlit as st

from api_client import fetch_config
from tabs.forecast_tab import render_forecast_tab
from tabs.kpi_tab import render_kpi_tab
from tabs.detailed_tab import render_detailed_tab

# 2. Configuración de la Página
st.set_page_config(
    page_title="Dashboard de Pronóstico de Ventas",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 3. Función Principal
def main():
    # Inicializar el estado de sesión
    if 'forecast_data' not in st.session_state:
        st.session_state['forecast_data'] = None
    
    # Cargar la configuración (filtros) desde el API
    config = fetch_config()
    
    if config:
        # Crear las pestañas
        tab1, tab2, tab3 = st.tabs([
            "📊 Pronóstico de Ventas",
            "🌍 KPIs Globales",
            "📈 Análisis Detallado"
        ])

        # Renderizar cada pestaña
        with tab1:
            render_forecast_tab(config)
        
        with tab2:
            render_kpi_tab()
            
        with tab3:
            render_detailed_tab()

# 4. Punto de entrada
if __name__ == "__main__":
    main()
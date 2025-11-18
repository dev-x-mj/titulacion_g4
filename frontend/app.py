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
#Ocultar alementos por defecto de la plantilla
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            
            /* ---  Ocultar la barra de herramientas de las tablas (el botón pequeño de descarga) --- */
            [data-testid="stElementToolbar"] {
                display: none;
            }
            
            /* --- REGLAS SOLO PARA IMPRESIÓN --- */
            @media print {
                [data-testid="stSidebar"] { display: none; }
                .stDeployButton { display: none; }
                .block-container {
                    max-width: 100% !important;
                    padding: 1rem !important;
                }
                .stPlotlyChart { break-inside: avoid; }
            }
            </style>
            """
            
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

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
            "Pronóstico de Ventas",
            "KPIs Globales",
            "Análisis Detallado"
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